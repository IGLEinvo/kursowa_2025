-- Add many articles with different authors
-- This script creates multiple authors and adds diverse articles

USE news_newspaper;

-- Create multiple authors (editors) 
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active) VALUES
('sarah_johnson', 'sarah.johnson@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'Sarah', 'Johnson', 'editor', TRUE),
('michael_chen', 'michael.chen@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'Michael', 'Chen', 'editor', TRUE),
('emma_williams', 'emma.williams@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'Emma', 'Williams', 'editor', TRUE),
('david_brown', 'david.brown@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'David', 'Brown', 'editor', TRUE),
('lisa_anderson', 'lisa.anderson@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'Lisa', 'Anderson', 'editor', TRUE),
('james_taylor', 'james.taylor@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'James', 'Taylor', 'editor', TRUE),
('olivia_martinez', 'olivia.martinez@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'Olivia', 'Martinez', 'editor', TRUE),
('robert_wilson', 'robert.wilson@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'Robert', 'Wilson', 'editor', TRUE),
('sophia_thomas', 'sophia.thomas@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'Sophia', 'Thomas', 'editor', TRUE),
('william_davis', 'william.davis@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'William', 'Davis', 'editor', TRUE),
('jennifer_lee', 'jennifer.lee@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'Jennifer', 'Lee', 'editor', TRUE),
('christopher_garcia', 'christopher.garcia@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'Christopher', 'Garcia', 'editor', TRUE)
ON DUPLICATE KEY UPDATE
    first_name = VALUES(first_name),
    last_name = VALUES(last_name),
    role = VALUES(role),
    is_active = VALUES(is_active);

-- Update existing "editor" user to have a real name
UPDATE users 
SET first_name = 'Editor', last_name = 'Team', username = 'editor_team'
WHERE username = 'editor' AND email = 'editor@example.com';

-- Now add many articles - using a Python script approach would be better, but here's SQL version
-- Let's add articles in batches

-- Get author and category IDs  
SET @authors = (SELECT GROUP_CONCAT(id) FROM users WHERE role = 'editor');
SET @politics_cat = (SELECT id FROM categories WHERE slug = 'politics' LIMIT 1);
SET @economy_cat = (SELECT id FROM categories WHERE slug = 'economy' LIMIT 1);
SET @culture_cat = (SELECT id FROM categories WHERE slug = 'culture' LIMIT 1);
SET @sports_cat = (SELECT id FROM categories WHERE slug = 'sports' LIMIT 1);
SET @tech_cat = (SELECT id FROM categories WHERE slug = 'technology' LIMIT 1);
SET @science_cat = (SELECT id FROM categories WHERE slug = 'science' LIMIT 1);
SET @health_cat = (SELECT id FROM categories WHERE slug = 'health' LIMIT 1);
SET @world_cat = (SELECT id FROM categories WHERE slug = 'world' LIMIT 1);

-- Note: Due to SQL limitations, I'll create a Python script to add many articles efficiently
-- This SQL file creates the authors, and a Python script will add the articles

SELECT 'Authors created successfully. Run the Python script to add articles.' as status;

