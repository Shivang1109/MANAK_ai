package com.manakai.repositories;

import com.manakai.models.Feedback;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;
import java.util.UUID;

@Repository
public interface FeedbackRepository extends JpaRepository<Feedback, UUID> {
    Page<Feedback> findByOrderByCreatedAtDesc(Pageable pageable);
    
    Page<Feedback> findByUserIdOrderByCreatedAtDesc(UUID userId, Pageable pageable);
    
    List<Feedback> findByRatingLessThanOrderByCreatedAtDesc(Integer rating, Pageable pageable);
    
    @Query("SELECT AVG(f.rating) FROM Feedback f")
    Double getAverageRating();
    
    @Query("SELECT f.rating, COUNT(f) FROM Feedback f GROUP BY f.rating ORDER BY f.rating DESC")
    List<Object[]> getRatingDistribution();
}
