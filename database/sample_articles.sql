-- Sample data for categories and articles
USE news_newspaper;

-- Create sample admin/editor user if not exists
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active)
VALUES ('editor', 'editor@example.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC',
        'News', 'Editor', 'editor', TRUE)
ON DUPLICATE KEY UPDATE
    first_name = VALUES(first_name),
    last_name = VALUES(last_name),
    role = VALUES(role),
    is_active = VALUES(is_active);

SET @editor_id = (SELECT id FROM users WHERE email = 'editor@example.com' LIMIT 1);

-- Helper to insert articles if they do not already exist
INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium,
                      status, views_count, likes_count, published_at)
SELECT 'Global Politics Update 2025',
       'global-politics-update-2025',
       'In-depth analysis of current geopolitical events and their impact on global stability...',
       'In-depth analysis of current geopolitical events...',
       @editor_id, (SELECT id FROM categories WHERE slug = 'politics'), TRUE, FALSE,
       'published', 120, 15, NOW()
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'global-politics-update-2025');

INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium,
                      status, views_count, likes_count, published_at)
SELECT 'Economic Outlook for Q1 2026',
       'economic-outlook-q1-2026',
       'Economists from leading institutions share insights on market trends...',
       'Economists share insights on market trends...',
       @editor_id, (SELECT id FROM categories WHERE slug = 'economy'), FALSE, FALSE,
       'published', 95, 8, NOW()
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'economic-outlook-q1-2026');

INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium,
                      status, views_count, likes_count, published_at)
SELECT 'Cultural Festivals Around the World',
       'cultural-festivals-around-the-world',
       'A journey through vibrant cultural festivals happening this season...',
       'A journey through vibrant cultural festivals...',
       @editor_id, (SELECT id FROM categories WHERE slug = 'culture'), FALSE, FALSE,
       'published', 60, 6, NOW()
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'cultural-festivals-around-the-world');

INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium,
                      status, views_count, likes_count, published_at)
SELECT 'Championship Highlights and Analysis',
       'championship-highlights-analysis',
       'Highlights from the latest championship games with expert analysis...',
       'Highlights from the latest championship games...',
       @editor_id, (SELECT id FROM categories WHERE slug = 'sports'), FALSE, FALSE,
       'published', 150, 28, NOW()
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'championship-highlights-analysis');

INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium,
                      status, views_count, likes_count, published_at)
SELECT 'Breakthroughs in AI Technology',
       'breakthroughs-in-ai-technology',
       'Tech companies unveil groundbreaking AI tools set to transform industries...',
       'Tech companies unveil groundbreaking AI tools...',
       @editor_id, (SELECT id FROM categories WHERE slug = 'technology'), TRUE, TRUE,
       'published', 200, 45, NOW()
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'breakthroughs-in-ai-technology');

INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium,
                      status, views_count, likes_count, published_at)
SELECT 'Exploring the Latest Space Missions',
       'exploring-latest-space-missions',
       'Scientists prepare for new space missions aiming to reach distant planets...',
       'Scientists prepare for new space missions...',
       @editor_id, (SELECT id FROM categories WHERE slug = 'science'), FALSE, FALSE,
       'published', 110, 12, NOW()
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'exploring-latest-space-missions');

INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium,
                      status, views_count, likes_count, published_at)
SELECT 'Health Innovations Improving Lives',
       'health-innovations-improving-lives',
       'Medical researchers introduce innovative treatments improving patient outcomes...',
       'Medical researchers introduce innovative treatments...',
       @editor_id, (SELECT id FROM categories WHERE slug = 'health'), FALSE, FALSE,
       'published', 80, 9, NOW()
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'health-innovations-improving-lives');

INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium,
                      status, views_count, likes_count, published_at)
SELECT 'Global Affairs: Weekly Brief',
       'global-affairs-weekly-brief',
       'Key international updates including diplomatic talks and humanitarian efforts...',
       'Key international updates including diplomatic talks...',
       @editor_id, (SELECT id FROM categories WHERE slug = 'world'), FALSE, FALSE,
       'published', 70, 7, NOW()
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'global-affairs-weekly-brief');

SELECT id, title, category_id FROM articles ORDER BY id DESC LIMIT 10;

