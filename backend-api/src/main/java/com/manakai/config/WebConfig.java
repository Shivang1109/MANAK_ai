package com.manakai.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.servlet.config.annotation.CorsRegistry;
import org.springframework.web.servlet.config.annotation.WebMvcConfigurer;

@Configuration
public class WebConfig implements WebMvcConfigurer {
    
    @Value("${manakai.cors.allowed-origins}")
    private String allowedOrigins;
    
    @Value("${manakai.cors.allowed-methods}")
    private String allowedMethods;
    
    @Value("${manakai.cors.allowed-headers}")
    private String allowedHeaders;
    
    @Value("${manakai.cors.allow-credentials}")
    private boolean allowCredentials;
    
    @Value("${manakai.cors.max-age}")
    private long maxAge;
    
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/**")
                .allowedOrigins(allowedOrigins.split(","))
                .allowedMethods(allowedMethods.split(","))
                .allowedHeaders(allowedHeaders.split(","))
                .allowCredentials(allowCredentials)
                .maxAge(maxAge);
    }
}
