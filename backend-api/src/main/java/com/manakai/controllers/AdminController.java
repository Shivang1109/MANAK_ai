package com.manakai.controllers;

import com.manakai.models.User;
import com.manakai.repositories.FeedbackRepository;
import com.manakai.repositories.QueryLogRepository;
import com.manakai.repositories.UserRepository;
import com.manakai.repositories.ConversationRepository;
import com.manakai.services.AuthService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.*;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/admin")
@CrossOrigin(originPatterns = "${manakai.cors.allowed-origins}")
public class AdminController {

    private static final Logger logger = LoggerFactory.getLogger(AdminController.class);

    @Value("${manakai.rag-service.url}")
    private String ragServiceUrl;

    @Autowired private AuthService authService;
    @Autowired private QueryLogRepository queryLogRepository;
    @Autowired private FeedbackRepository feedbackRepository;
    @Autowired private UserRepository userRepository;
    @Autowired private ConversationRepository conversationRepository;
    @Autowired private RestTemplate restTemplate;

    /**
     * GET /api/admin/stats — full dashboard data
     * Open to all authenticated users for demo purposes
     */
    @GetMapping("/stats")
    public ResponseEntity<?> getStats(Authentication authentication) {
        try {
            authService.getUserByUsername(authentication.getName()); // verify auth

            Map<String, Object> stats = new LinkedHashMap<>();

            // ── Core counts ──────────────────────────────────────────
            long totalQueries   = queryLogRepository.count();
            long totalUsers     = userRepository.count();
            long totalConversations = conversationRepository.count();
            long totalFeedback  = feedbackRepository.count();

            stats.put("totalQueries",       totalQueries);
            stats.put("totalUsers",         totalUsers);
            stats.put("totalConversations", totalConversations);
            stats.put("totalFeedback",      totalFeedback);

            // ── Feedback breakdown ───────────────────────────────────
            long positiveFeedback = feedbackRepository.findAll().stream()
                    .filter(f -> f.getRating() >= 1).count();
            long negativeFeedback = feedbackRepository.findAll().stream()
                    .filter(f -> f.getRating() == 0).count();
            double positiveRate = totalFeedback > 0
                    ? Math.round((positiveFeedback * 100.0 / totalFeedback) * 10) / 10.0
                    : 0.0;

            stats.put("positiveFeedback", positiveFeedback);
            stats.put("negativeFeedback", negativeFeedback);
            stats.put("positiveRate",     positiveRate);

            // ── Latency + confidence averages ────────────────────────
            List<Object[]> rawLogs = queryLogRepository.findAll().stream()
                    .filter(q -> q.getLatencyMs() != null && q.getConfidenceScore() != null)
                    .map(q -> new Object[]{q.getLatencyMs(), q.getConfidenceScore()})
                    .collect(Collectors.toList());

            double avgLatency    = rawLogs.stream().mapToInt(r -> (Integer) r[0]).average().orElse(0);
            double avgConfidence = rawLogs.stream().mapToDouble(r -> (Double)  r[1]).average().orElse(0);

            stats.put("avgLatencyMs",    Math.round(avgLatency));
            stats.put("avgConfidence",   Math.round(avgConfidence * 100.0) / 100.0);

            // ── Low-confidence recent queries ────────────────────────
            List<Map<String, Object>> lowConf = queryLogRepository
                    .findByConfidenceScoreLessThanOrderByCreatedAtDesc(0.6, PageRequest.of(0, 5))
                    .stream()
                    .map(q -> {
                        Map<String, Object> m = new LinkedHashMap<>();
                        m.put("query",           q.getQuery());
                        m.put("confidenceScore", q.getConfidenceScore());
                        m.put("createdAt",       q.getCreatedAt() != null ? q.getCreatedAt().toString() : "");
                        return m;
                    }).collect(Collectors.toList());
            stats.put("lowConfidenceQueries", lowConf);

            // ── Recent queries (last 5) ──────────────────────────────
            List<Map<String, Object>> recentQueries = queryLogRepository
                    .findAll(PageRequest.of(0, 5,
                            org.springframework.data.domain.Sort.by("createdAt").descending()))
                    .stream()
                    .map(q -> {
                        Map<String, Object> m = new LinkedHashMap<>();
                        m.put("query",           q.getQuery());
                        m.put("confidenceScore", q.getConfidenceScore());
                        m.put("latencyMs",       q.getLatencyMs());
                        m.put("sourcesCount",    q.getSourcesCount());
                        m.put("createdAt",       q.getCreatedAt() != null ? q.getCreatedAt().toString() : "");
                        return m;
                    }).collect(Collectors.toList());
            stats.put("recentQueries", recentQueries);

            // ── RAG / ChromaDB stats (proxy to RAG service) ──────────
            try {
                @SuppressWarnings("unchecked")
                Map<String, Object> ragStats = restTemplate.getForObject(
                        ragServiceUrl + "/stats", Map.class);
                if (ragStats != null) {
                    stats.put("totalChunks",      ragStats.get("total_chunks"));
                    stats.put("uniqueStandards",  ragStats.get("unique_standards"));
                    stats.put("industries",        ragStats.get("industries"));
                    stats.put("sampleStandards",   ragStats.get("sample_standards"));
                }
            } catch (Exception e) {
                logger.warn("Could not fetch RAG stats: {}", e.getMessage());
                stats.put("totalChunks",     "N/A");
                stats.put("uniqueStandards", "N/A");
                stats.put("industries",      List.of());
            }

            return ResponseEntity.ok(stats);

        } catch (Exception e) {
            logger.error("Error fetching admin stats", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(Map.of("error", "Failed to fetch stats: " + e.getMessage()));
        }
    }

    /** GET /api/admin/health */
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        return ResponseEntity.ok(Map.of("status", "healthy", "service", "admin"));
    }
}
