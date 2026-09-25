package com.manakai.dto;

import java.util.UUID;

public class AuthResponse {
    private String token;
    private String type = "Bearer";
    private UUID userId;
    private String username;
    private String email;
    private String role;
    
    // Default constructor
    public AuthResponse() {
    }
    
    // Constructor
    public AuthResponse(String token, UUID userId, String username, String email, String role) {
        this.token = token;
        this.type = "Bearer";
        this.userId = userId;
        this.username = username;
        this.email = email;
        this.role = role;
    }
    
    // Getters and setters
    public String getToken() { 
        return token; 
    }
    
    public void setToken(String token) { 
        this.token = token; 
    }
    
    public String getType() { 
        return type; 
    }
    
    public void setType(String type) { 
        this.type = type; 
    }
    
    public UUID getUserId() { 
        return userId; 
    }
    
    public void setUserId(UUID userId) { 
        this.userId = userId; 
    }
    
    public String getUsername() { 
        return username; 
    }
    
    public void setUsername(String username) { 
        this.username = username; 
    }
    
    public String getEmail() { 
        return email; 
    }
    
    public void setEmail(String email) { 
        this.email = email; 
    }
    
    public String getRole() { 
        return role; 
    }
    
    public void setRole(String role) { 
        this.role = role; 
    }
}
