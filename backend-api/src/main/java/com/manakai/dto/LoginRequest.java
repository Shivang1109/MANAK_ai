package com.manakai.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class LoginRequest {
    @NotBlank(message = "Username is required")
    private String username;
    
    @NotBlank(message = "Password is required")
    private String password;
    
    // Manual getters for compatibility
    public String getUsername() {
        return username;
    }
    
    public String getPassword() {
        return password;
    }
}
