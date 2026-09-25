package com.manakai.services;

import com.manakai.dto.FeedbackRequest;
import com.manakai.models.Feedback;
import com.manakai.models.Message;
import com.manakai.models.User;
import com.manakai.repositories.FeedbackRepository;
import com.manakai.repositories.MessageRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Service
public class FeedbackService {

    private static final Logger logger = LoggerFactory.getLogger(FeedbackService.class);

    @Autowired
    private FeedbackRepository feedbackRepository;

    @Autowired
    private MessageRepository messageRepository;

    /**
     * Submit user feedback for a message
     */
    @Transactional
    public Feedback submitFeedback(FeedbackRequest request, User user) {
        // Get the message
        UUID messageId = request.getMessageId();
        Message message = messageRepository.findById(messageId)
                .orElseThrow(() -> new IllegalArgumentException("Message not found"));

        // Verify user owns the conversation
        if (!message.getConversation().getUser().getId().equals(user.getId())) {
            throw new IllegalArgumentException("Unauthorized access to message");
        }

        // Create feedback
        Feedback feedback = new Feedback();
        feedback.setUser(user);
        feedback.setMessage(message);
        feedback.setRating(request.getRating());
        feedback.setComment(request.getComment());
        feedback.setFeedbackType(request.getFeedbackType());

        feedback = feedbackRepository.save(feedback);

        logger.info("Feedback submitted: messageId={}, rating={}, type={}",
                messageId, request.getRating(), request.getFeedbackType());

        return feedback;
    }

    /**
     * Get all feedback for a user
     */
    public List<Feedback> getUserFeedback(User user) {
        return feedbackRepository.findByUserIdOrderByCreatedAtDesc(user.getId(), org.springframework.data.domain.Pageable.unpaged()).getContent();
    }

    /**
     * Get feedback statistics (for admin)
     */
    public FeedbackStats getFeedbackStats() {
        List<Feedback> allFeedback = feedbackRepository.findAll();
        
        long totalCount = allFeedback.size();
        double averageRating = allFeedback.stream()
                .mapToInt(Feedback::getRating)
                .average()
                .orElse(0.0);
        
        long positiveCount = allFeedback.stream()
                .filter(f -> f.getRating() >= 4)
                .count();
        
        long negativeCount = allFeedback.stream()
                .filter(f -> f.getRating() <= 2)
                .count();

        return new FeedbackStats(totalCount, averageRating, positiveCount, negativeCount);
    }

    /**
     * Feedback statistics data class
     */
    public static class FeedbackStats {
        private long totalCount;
        private double averageRating;
        private long positiveCount;
        private long negativeCount;

        public FeedbackStats(long totalCount, double averageRating, long positiveCount, long negativeCount) {
            this.totalCount = totalCount;
            this.averageRating = averageRating;
            this.positiveCount = positiveCount;
            this.negativeCount = negativeCount;
        }

        // Getters
        public long getTotalCount() { return totalCount; }
        public double getAverageRating() { return averageRating; }
        public long getPositiveCount() { return positiveCount; }
        public long getNegativeCount() { return negativeCount; }
    }
}
