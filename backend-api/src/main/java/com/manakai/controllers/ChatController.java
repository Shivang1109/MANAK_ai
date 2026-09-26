package com.manakai.controllers;

import com.manakai.dto.ChatRequest;
import com.manakai.dto.ChatResponse;
import com.manakai.models.Conversation;
import com.manakai.models.Message;
import com.manakai.models.User;
import com.manakai.services.AuthService;
import com.manakai.services.ChatService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.util.UriComponentsBuilder;

import jakarta.validation.Valid;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/chat")
@CrossOrigin(originPatterns = "${manakai.cors.allowed-origins}")
public class ChatController {

    private static final Logger logger = LoggerFactory.getLogger(ChatController.class);

    @Value("${manakai.rag-service.url}")
    private String ragServiceUrl;

    @Autowired
    private RestTemplate restTemplate;

    @Autowired
    private ChatService chatService;

    @Autowired
    private AuthService authService;

    /**
     * Send chat message and get AI response
     * POST /api/chat
     */
    @PostMapping
    public ResponseEntity<?> sendMessage(
            @Valid @RequestBody ChatRequest request,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            User user = authService.getUserByUsername(username);

            logger.info("Processing chat message from user: {}", username);

            ChatResponse response = chatService.processMessage(request, user);

            return ResponseEntity.ok(response);

        } catch (IllegalArgumentException e) {
            logger.warn("Chat request failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(createErrorResponse(e.getMessage()));
        } catch (Exception e) {
            logger.error("Chat processing error", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(createErrorResponse("Failed to process message: " + e.getMessage()));
        }
    }

    /**
     * Get conversation history
     * GET /api/chat/history/{conversationId}
     */
    @GetMapping("/history/{conversationId}")
    public ResponseEntity<?> getConversationHistory(
            @PathVariable String conversationId,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            User user = authService.getUserByUsername(username);

            logger.info("Fetching conversation history: conversationId={}, user={}",
                    conversationId, username);

            List<Message> messages = chatService.getConversationHistory(conversationId, user);

            return ResponseEntity.ok(messages);

        } catch (IllegalArgumentException e) {
            logger.warn("Get history failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(createErrorResponse(e.getMessage()));
        } catch (Exception e) {
            logger.error("Get history error", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(createErrorResponse("Failed to get history: " + e.getMessage()));
        }
    }

    /**
     * Get all conversations for logged-in user
     * GET /api/chat/conversations
     */
    @GetMapping("/conversations")
    public ResponseEntity<?> getUserConversations(Authentication authentication) {
        try {
            String username = authentication.getName();
            User user = authService.getUserByUsername(username);

            logger.info("Fetching conversations for user: {}", username);

            List<Conversation> conversations = chatService.getUserConversations(user);

            return ResponseEntity.ok(conversations);

        } catch (Exception e) {
            logger.error("Get conversations error", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(createErrorResponse("Failed to get conversations: " + e.getMessage()));
        }
    }

    /**
     * Delete conversation
     * DELETE /api/chat/conversations/{conversationId}
     */
    @DeleteMapping("/conversations/{conversationId}")
    public ResponseEntity<?> deleteConversation(
            @PathVariable String conversationId,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            User user = authService.getUserByUsername(username);

            logger.info("Deleting conversation: conversationId={}, user={}",
                    conversationId, username);

            chatService.deleteConversation(conversationId, user);

            Map<String, String> response = new HashMap<>();
            response.put("message", "Conversation deleted successfully");
            response.put("conversationId", conversationId);

            return ResponseEntity.ok(response);

        } catch (IllegalArgumentException e) {
            logger.warn("Delete conversation failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(createErrorResponse(e.getMessage()));
        } catch (Exception e) {
            logger.error("Delete conversation error", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(createErrorResponse("Failed to delete conversation: " + e.getMessage()));
        }
    }

    /**
     * Health check endpoint
     * GET /api/chat/health
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "healthy");
        response.put("service", "chat");
        return ResponseEntity.ok(response);
    }

    /**
     * Standard Finder proxy — FinderView calls this.
     * GET /api/rag/standards?product=LED+bulb&industry=electronics
     *
     * Proxies to the RAG service GET /search/standards
     */
    @GetMapping("/rag/standards")
    public ResponseEntity<?> searchStandards(
            @RequestParam String product,
            @RequestParam(required = false) String industry,
            Authentication authentication) {
        try {
            if (authentication != null && authentication.getName() != null) {
                try {
                    authService.getUserByUsername(authentication.getName());
                } catch (Exception ignored) {
                    // Ignore user lookup if optional
                }
            }

            String url = UriComponentsBuilder
                    .fromHttpUrl(ragServiceUrl + "/search/standards")
                    .queryParam("product", product)
                    .queryParamIfPresent("industry",
                            java.util.Optional.ofNullable(industry)
                                    .filter(s -> !s.isBlank()))
                    .toUriString();

            logger.info("Standard search proxy: product={}, industry={}", product, industry);

            Object result = restTemplate.getForObject(url, Object.class);
            return ResponseEntity.ok(result);

        } catch (Exception e) {
            logger.error("Standard search proxy failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_GATEWAY)
                    .body(createErrorResponse("RAG service unavailable: " + e.getMessage()));
        }
    }

    /**
     * RAG stats proxy — AdminView calls this.
     * GET /api/rag/stats  →  proxies to RAG service GET /stats
     */
    @GetMapping("/rag/stats")
    public ResponseEntity<?> getRagStats(Authentication authentication) {
        try {
            if (authentication != null && authentication.getName() != null) {
                try {
                    authService.getUserByUsername(authentication.getName());
                } catch (Exception ignored) {}
            }
            Object result = restTemplate.getForObject(ragServiceUrl + "/stats", Object.class);
            return ResponseEntity.ok(result);
        } catch (Exception e) {
            logger.warn("RAG stats proxy failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_GATEWAY)
                    .body(createErrorResponse("RAG service unavailable"));
        }
    }

    /**
     * Create error response
     */
    private Map<String, String> createErrorResponse(String message) {
        Map<String, String> error = new HashMap<>();
        error.put("error", message);
        error.put("timestamp", java.time.LocalDateTime.now().toString());
        return error;
    }
}
