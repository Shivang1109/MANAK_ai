package com.manakai.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

import java.util.UUID;

@Data
public class ChatRequest {
    @NotBlank(message = "Query cannot be empty")
    private String query;
    
    private UUID conversationId;
    
    // Manual getters for compatibility
    public String getQuery() {
        return query;
    }
    
    public UUID getConversationId() {
        return conversationId;
    }
}
