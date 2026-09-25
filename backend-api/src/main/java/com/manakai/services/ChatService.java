package com.manakai.services;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.manakai.dto.ChatRequest;
import com.manakai.dto.ChatResponse;
import com.manakai.models.Conversation;
import com.manakai.models.Message;
import com.manakai.models.QueryLog;
import com.manakai.models.User;
import com.manakai.repositories.ConversationRepository;
import com.manakai.repositories.MessageRepository;
import com.manakai.repositories.QueryLogRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

@Service
public class ChatService {

    private static final Logger logger = LoggerFactory.getLogger(ChatService.class);

    @Value("${manakai.rag-service.url}")
    private String ragServiceUrl;

    @Autowired
    private ConversationRepository conversationRepository;

    @Autowired
    private MessageRepository messageRepository;

    @Autowired
    private QueryLogRepository queryLogRepository;

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private ObjectMapper objectMapper;

    /**
     * Process chat message and get response from RAG service
     */
    @Transactional
    public ChatResponse processMessage(ChatRequest request, User user) {
        try {
            // Get or create conversation
            Conversation conversation = getOrCreateConversation(
                    request.getConversationId() != null ? request.getConversationId().toString() : null, 
                    user
            );

            // Save user message
            Message userMessage = new Message();
            userMessage.setConversation(conversation);
            userMessage.setRole("user");
            userMessage.setContent(request.getQuery());
            messageRepository.save(userMessage);

            // Get conversation history for context
            List<Message> history = messageRepository.findByConversationIdOrderByCreatedAtAsc(conversation.getId());
            List<Map<String, String>> conversationHistory = history.stream()
                    .limit(10) // Last 10 messages for context
                    .map(msg -> {
                        Map<String, String> historyMsg = new HashMap<>();
                        historyMsg.put("role", msg.getRole());
                        historyMsg.put("content", msg.getContent());
                        return historyMsg;
                    })
                    .collect(Collectors.toList());

            // Call RAG service
            long startTime = System.currentTimeMillis();
            JsonNode ragResponse = callRagService(request.getQuery(), conversation.getId().toString(), conversationHistory);
            long processingTime = System.currentTimeMillis() - startTime;

            // Parse RAG response
            String answer = ragResponse.get("answer").asText();
            String confidence = ragResponse.get("confidence").asText();
            double confidenceScore = ragResponse.get("confidence_score").asDouble();
            
            List<ChatResponse.Source> sources = new ArrayList<>();
            JsonNode sourcesNode = ragResponse.get("sources");
            if (sourcesNode != null && sourcesNode.isArray()) {
                for (JsonNode sourceNode : sourcesNode) {
                    ChatResponse.Source source = new ChatResponse.Source();
                    source.setStandardNumber(sourceNode.path("standard_number").asText(null));
                    source.setTitle(sourceNode.path("title").asText(null));
                    source.setClause(sourceNode.path("clause").asText(null));
                    source.setPage(sourceNode.path("page").asInt(0));
                    source.setDocumentType(sourceNode.path("document_type").asText(null));
                    source.setSourceUrl(sourceNode.path("source_url").asText(null));
                    source.setContentPreview(sourceNode.path("content_preview").asText(null));
                    sources.add(source);
                }
            }

            // Save assistant message
            Message assistantMessage = new Message();
            assistantMessage.setConversation(conversation);
            assistantMessage.setRole("assistant");
            assistantMessage.setContent(answer);
            messageRepository.save(assistantMessage);

            // Update conversation
            conversation.setLastMessageAt(LocalDateTime.now());
            conversationRepository.save(conversation);

            // Log query
            QueryLog queryLog = new QueryLog();
            queryLog.setUser(user);
            queryLog.setConversation(conversation);
            queryLog.setQuery(request.getQuery());
            queryLog.setResponse(answer);
            queryLog.setConfidenceScore(confidenceScore);
            queryLog.setLatencyMs((int) processingTime);
            queryLog.setSourcesCount(sources.size());
            queryLogRepository.save(queryLog);

            // Build response
            ChatResponse response = new ChatResponse();
            response.setConversationId(conversation.getId().toString());
            response.setAnswer(answer);
            response.setSources(sources);
            response.setConfidence(confidence);
            response.setConfidenceScore(confidenceScore);
            response.setProcessingTimeMs(processingTime);
            response.setTimestamp(LocalDateTime.now());

            logger.info("Chat message processed: conversationId={}, confidence={}, processingTime={}ms",
                    conversation.getId(), confidence, processingTime);

            return response;

        } catch (Exception e) {
            logger.error("Error processing chat message", e);
            throw new RuntimeException("Failed to process chat message: " + e.getMessage());
        }
    }

    /**
     * Get conversation history
     */
    public List<Message> getConversationHistory(String conversationId, User user) {
        UUID uuid = UUID.fromString(conversationId);
        Conversation conversation = conversationRepository.findById(uuid)
                .orElseThrow(() -> new IllegalArgumentException("Conversation not found"));

        // Verify user owns this conversation
        if (!conversation.getUser().getId().equals(user.getId())) {
            throw new IllegalArgumentException("Unauthorized access to conversation");
        }

        return messageRepository.findByConversationIdOrderByCreatedAtAsc(uuid);
    }

    /**
     * Get all conversations for a user
     */
    public List<Conversation> getUserConversations(User user) {
        return conversationRepository.findByUserIdOrderByLastMessageAtDesc(user.getId());
    }

    /**
     * Delete conversation
     */
    @Transactional
    public void deleteConversation(String conversationId, User user) {
        UUID uuid = UUID.fromString(conversationId);
        Conversation conversation = conversationRepository.findById(uuid)
                .orElseThrow(() -> new IllegalArgumentException("Conversation not found"));

        // Verify user owns this conversation
        if (!conversation.getUser().getId().equals(user.getId())) {
            throw new IllegalArgumentException("Unauthorized access to conversation");
        }

        conversationRepository.delete(conversation);
    }

    /**
     * Get or create conversation
     */
    private Conversation getOrCreateConversation(String conversationId, User user) {
        if (conversationId != null && !conversationId.isEmpty()) {
            UUID uuid = UUID.fromString(conversationId);
            return conversationRepository.findById(uuid)
                    .orElseThrow(() -> new IllegalArgumentException("Conversation not found"));
        }

        // Create new conversation
        Conversation conversation = new Conversation();
        conversation.setUser(user);
        conversation.setTitle("New Chat");
        conversation.setLastMessageAt(LocalDateTime.now());
        return conversationRepository.save(conversation);
    }

    /**
     * Call RAG service
     */
    private JsonNode callRagService(String query, String sessionId, List<Map<String, String>> conversationHistory) {
        try {
            String url = ragServiceUrl + "/internal/rag/query";

            // Build request
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("query", query);
            requestBody.put("session_id", sessionId);
            if (conversationHistory != null && !conversationHistory.isEmpty()) {
                requestBody.put("conversation_history", conversationHistory);
            }

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, Object>> request = new HttpEntity<>(requestBody, headers);

            // Call RAG service
            logger.info("Calling RAG service: {}", url);
            ResponseEntity<String> response = restTemplate.postForEntity(url, request, String.class);

            if (!response.getStatusCode().is2xxSuccessful()) {
                throw new RuntimeException("RAG service returned error: " + response.getStatusCode());
            }

            return objectMapper.readTree(response.getBody());

        } catch (Exception e) {
            logger.error("Failed to call RAG service", e);
            throw new RuntimeException("Failed to call RAG service: " + e.getMessage());
        }
    }
}
