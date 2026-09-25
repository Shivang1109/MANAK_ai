package com.manakai.dto;

import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import lombok.Data;

import java.util.UUID;

@Data
public class FeedbackRequest {
    @NotNull(message = "Message ID is required")
    private UUID messageId;
    
    @NotNull(message = "Rating is required")
    @Min(value = 1, message = "Rating must be between 1 and 5")
    @Max(value = 5, message = "Rating must be between 1 and 5")
    private Integer rating;
    
    private String comment;
    
    private String feedbackType;
    
    // Manual getters for compatibility
    public UUID getMessageId() {
        return messageId;
    }
    
    public Integer getRating() {
        return rating;
    }
    
    public String getComment() {
        return comment;
    }
    
    public String getFeedbackType() {
        return feedbackType;
    }
}
