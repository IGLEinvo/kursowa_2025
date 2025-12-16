-- Populate Categories with Complete Data
-- This script ensures all categories have proper data

USE news_newspaper;

-- Clear existing categories (optional - comment out if you want to keep existing)
-- TRUNCATE TABLE categories;

-- Insert/Update categories with complete data
INSERT INTO categories (name, slug, description) VALUES
('Politics', 'politics', 'Political news, government policies, elections, and political analysis from around the world') 
ON DUPLICATE KEY UPDATE description = 'Political news, government policies, elections, and political analysis from around the world';

INSERT INTO categories (name, slug, description) VALUES
('Economy', 'economy', 'Economic news, financial markets, business updates, and economic analysis')
ON DUPLICATE KEY UPDATE description = 'Economic news, financial markets, business updates, and economic analysis';

INSERT INTO categories (name, slug, description) VALUES
('Culture', 'culture', 'Cultural events, entertainment, arts, music, movies, books, and lifestyle news')
ON DUPLICATE KEY UPDATE description = 'Cultural events, entertainment, arts, music, movies, books, and lifestyle news';

INSERT INTO categories (name, slug, description) VALUES
('Sports', 'sports', 'Sports news, match results, athlete updates, and sports analysis from all major leagues')
ON DUPLICATE KEY UPDATE description = 'Sports news, match results, athlete updates, and sports analysis from all major leagues';

INSERT INTO categories (name, slug, description) VALUES
('Technology', 'technology', 'Technology news, innovations, gadgets, software updates, and tech industry analysis')
ON DUPLICATE KEY UPDATE description = 'Technology news, innovations, gadgets, software updates, and tech industry analysis';

INSERT INTO categories (name, slug, description) VALUES
('Science', 'science', 'Scientific discoveries, research findings, space exploration, and scientific breakthroughs')
ON DUPLICATE KEY UPDATE description = 'Scientific discoveries, research findings, space exploration, and scientific breakthroughs';

INSERT INTO categories (name, slug, description) VALUES
('Health', 'health', 'Health news, medical research, wellness tips, and healthcare updates')
ON DUPLICATE KEY UPDATE description = 'Health news, medical research, wellness tips, and healthcare updates';

INSERT INTO categories (name, slug, description) VALUES
('World', 'world', 'International news, global events, world affairs, and international relations')
ON DUPLICATE KEY UPDATE description = 'International news, global events, world affairs, and international relations';

-- Verify the data
SELECT id, name, slug, description FROM categories ORDER BY id;

