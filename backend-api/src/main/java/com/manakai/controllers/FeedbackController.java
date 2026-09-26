package com.manakai.controllers;

import com.manakai.dto.FeedbackRequest;
import com.manakai.models.Feedback;
import com.manakai.models.User;
import com.manakai.services.AuthService;
import com.manakai.services.FeedbackService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.Authentication;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/feedback")
@CrossOrigin(originPatterns = "${manakai.cors.allowed-origins}")
public class FeedbackController {

    private static final Logger logger = LoggerFactory.getLogger(FeedbackController.class);

    @Autowired
    private FeedbackService feedbackService;

    @Autowired
    private AuthService authService;

    /**
     * Submit feedback for a message
     * POST /api/feedback
     */
    @PostMapping
    public ResponseEntity<?> submitFeedback(
            @Valid @RequestBody FeedbackRequest request,
            Authentication authentication) {
        try {
            String username = authentication.getName();
            User user = authService.getUserByUsername(username);

            logger.info("Submitting feedback from user: {}, messageId: {}, rating: {}",
                    username, request.getMessageId(), request.getRating());

            Feedback feedback = feedbackService.submitFeedback(request, user);

            Map<String, Object> response = new HashMap<>();
            response.put("message", "Feedback submitted successfully");
            response.put("feedbackId", feedback.getId().toString());
            response.put("rating", feedback.getRating());

            return ResponseEntity.status(HttpStatus.CREATED).body(response);

        } catch (IllegalArgumentException e) {
            logger.warn("Submit feedback failed: {}", e.getMessage());
            return ResponseEntity.status(HttpStatus.BAD_REQUEST)
                    .body(createErrorResponse(e.getMessage()));
        } catch (Exception e) {
            logger.error("Submit feedback error", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(createErrorResponse("Failed to submit feedback: " + e.getMessage()));
        }
    }

    /**
     * Get user's feedback history
     * GET /api/feedback/my
     */
    @GetMapping("/my")
    public ResponseEntity<?> getMyFeedback(Authentication authentication) {
        try {
            String username = authentication.getName();
            User user = authService.getUserByUsername(username);

            logger.info("Fetching feedback for user: {}", username);

            List<Feedback> feedbackList = feedbackService.getUserFeedback(user);

            return ResponseEntity.ok(feedbackList);

        } catch (Exception e) {
            logger.error("Get feedback error", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(createErrorResponse("Failed to get feedback: " + e.getMessage()));
        }
    }

    /**
     * Get feedback statistics (admin endpoint)
     * GET /api/feedback/stats
     */
    @GetMapping("/stats")
    public ResponseEntity<?> getFeedbackStats(Authentication authentication) {
        try {
            String username = authentication.getName();
            User user = authService.getUserByUsername(username);

            // Simple check - in production, use @PreAuthorize or role check
            if (!"ADMIN".equals(user.getRole())) {
                return ResponseEntity.status(HttpStatus.FORBIDDEN)
                        .body(createErrorResponse("Admin access required"));
            }

            logger.info("Fetching feedback stats for admin: {}", username);

            FeedbackService.FeedbackStats stats = feedbackService.getFeedbackStats();

            return ResponseEntity.ok(stats);

        } catch (Exception e) {
            logger.error("Get feedback stats error", e);
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
                    .body(createErrorResponse("Failed to get stats: " + e.getMessage()));
        }
    }

    /**
     * Health check endpoint
     * GET /api/feedback/health
     */
    @GetMapping("/health")
    public ResponseEntity<Map<String, String>> health() {
        Map<String, String> response = new HashMap<>();
        response.put("status", "healthy");
        response.put("service", "feedback");
        return ResponseEntity.ok(response);
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
