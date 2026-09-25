package com.manakai.models;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.type.SqlTypes;

import java.time.LocalDateTime;
import java.util.UUID;

@Entity
@Table(name = "query_logs")
@Data
@NoArgsConstructor
@AllArgsConstructor
public class QueryLog {
    
    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "conversation_id")
    private Conversation conversation;
    
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_id")
    private User user;
    
    @Column(columnDefinition = "TEXT", nullable = false)
    private String query;
    
    @Column(columnDefinition = "TEXT")
    private String response;
    
    @Column(name = "confidence_score")
    private Double confidenceScore;
    
    @Column(name = "latency_ms")
    private Integer latencyMs;
    
    @Column(name = "retrieval_score")
    private Double retrievalScore;
    
    @Column(name = "sources_count")
    private Integer sourcesCount;
    
    @Column(length = 100)
    private String intent;
    
    @JdbcTypeCode(SqlTypes.JSON)
    @Column(columnDefinition = "JSONB")
    private String metadata;
    
    @CreationTimestamp
    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;
    
    // Manual getters/setters for compatibility
    public UUID getId() { return id; }
    public void setId(UUID id) { this.id = id; }
    
    public Conversation getConversation() { return conversation; }
    public void setConversation(Conversation conversation) { this.conversation = conversation; }
    
    public User getUser() { return user; }
    public void setUser(User user) { this.user = user; }
    
    public String getQuery() { return query; }
    public void setQuery(String query) { this.query = query; }
    
    public String getResponse() { return response; }
    public void setResponse(String response) { this.response = response; }
    
    public Double getConfidenceScore() { return confidenceScore; }
    public void setConfidenceScore(Double confidenceScore) { this.confidenceScore = confidenceScore; }
    
    public Integer getLatencyMs() { return latencyMs; }
    public void setLatencyMs(Integer latencyMs) { this.latencyMs = latencyMs; }
    
    public Double getRetrievalScore() { return retrievalScore; }
    public void setRetrievalScore(Double retrievalScore) { this.retrievalScore = retrievalScore; }
    
    public Integer getSourcesCount() { return sourcesCount; }
    public void setSourcesCount(Integer sourcesCount) { this.sourcesCount = sourcesCount; }
    
    public String getIntent() { return intent; }
    public void setIntent(String intent) { this.intent = intent; }
    
    public String getMetadata() { return metadata; }
    public void setMetadata(String metadata) { this.metadata = metadata; }
    
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
