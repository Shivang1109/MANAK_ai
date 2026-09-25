package com.manakai.dto;

import java.time.LocalDateTime;
import java.util.List;

public class ChatResponse {
    private String conversationId;
    private String answer;
    private List<Source> sources;
    private String confidence;
    private Double confidenceScore;
    private Long processingTimeMs;
    private LocalDateTime timestamp;
    
    public ChatResponse() {
    }
    
    public ChatResponse(String conversationId, String answer, List<Source> sources, 
                       String confidence, Double confidenceScore, Long processingTimeMs, 
                       LocalDateTime timestamp) {
        this.conversationId = conversationId;
        this.answer = answer;
        this.sources = sources;
        this.confidence = confidence;
        this.confidenceScore = confidenceScore;
        this.processingTimeMs = processingTimeMs;
        this.timestamp = timestamp;
    }
    
    public String getConversationId() { return conversationId; }
    public void setConversationId(String conversationId) { this.conversationId = conversationId; }
    
    public String getAnswer() { return answer; }
    public void setAnswer(String answer) { this.answer = answer; }
    
    public List<Source> getSources() { return sources; }
    public void setSources(List<Source> sources) { this.sources = sources; }
    
    public String getConfidence() { return confidence; }
    public void setConfidence(String confidence) { this.confidence = confidence; }
    
    public Double getConfidenceScore() { return confidenceScore; }
    public void setConfidenceScore(Double confidenceScore) { this.confidenceScore = confidenceScore; }
    
    public Long getProcessingTimeMs() { return processingTimeMs; }
    public void setProcessingTimeMs(Long processingTimeMs) { this.processingTimeMs = processingTimeMs; }
    
    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
    
    public static class Source {
        private String standardNumber;
        private String title;
        private String clause;
        private Integer page;
        private String documentType;
        private String sourceUrl;
        private String contentPreview;
        
        public Source() {
        }
        
        public Source(String standardNumber, String title, String clause, Integer page,
                     String documentType, String sourceUrl, String contentPreview) {
            this.standardNumber = standardNumber;
            this.title = title;
            this.clause = clause;
            this.page = page;
            this.documentType = documentType;
            this.sourceUrl = sourceUrl;
            this.contentPreview = contentPreview;
        }
        
        public String getStandardNumber() { return standardNumber; }
        public void setStandardNumber(String standardNumber) { this.standardNumber = standardNumber; }
        
        public String getTitle() { return title; }
        public void setTitle(String title) { this.title = title; }
        
        public String getClause() { return clause; }
        public void setClause(String clause) { this.clause = clause; }
        
        public Integer getPage() { return page; }
        public void setPage(Integer page) { this.page = page; }
        
        public String getDocumentType() { return documentType; }
        public void setDocumentType(String documentType) { this.documentType = documentType; }
        
        public String getSourceUrl() { return sourceUrl; }
        public void setSourceUrl(String sourceUrl) { this.sourceUrl = sourceUrl; }
        
        public String getContentPreview() { return contentPreview; }
        public void setContentPreview(String contentPreview) { this.contentPreview = contentPreview; }
    }
}
