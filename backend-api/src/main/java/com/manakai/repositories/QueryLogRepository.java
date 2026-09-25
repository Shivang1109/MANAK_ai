package com.manakai.repositories;

import com.manakai.models.QueryLog;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.UUID;

@Repository
public interface QueryLogRepository extends JpaRepository<QueryLog, UUID> {
    Page<QueryLog> findByUserIdOrderByCreatedAtDesc(UUID userId, Pageable pageable);
    
    List<QueryLog> findByConfidenceScoreLessThanOrderByCreatedAtDesc(Double threshold, Pageable pageable);
    
    @Query("SELECT ql FROM QueryLog ql WHERE ql.createdAt BETWEEN :startDate AND :endDate")
    List<QueryLog> findByDateRange(LocalDateTime startDate, LocalDateTime endDate);
    
    @Query("SELECT ql.intent, COUNT(ql) as count FROM QueryLog ql GROUP BY ql.intent ORDER BY count DESC")
    List<Object[]> getIntentDistribution();
}
