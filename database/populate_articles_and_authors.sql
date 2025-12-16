-- Populate database with many articles and different authors
-- This script creates multiple authors and adds many diverse articles

USE news_newspaper;

-- Create multiple authors (editors) with different names
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
('william_davis', 'william.davis@news.com', '$2b$12$vmo.brYgocwxrkpcXfBfv.cVQQ7YaegMLJh/BIWW87Y02n2Mr9JXC', 'William', 'Davis', 'editor', TRUE)
ON DUPLICATE KEY UPDATE
    first_name = VALUES(first_name),
    last_name = VALUES(last_name),
    role = VALUES(role),
    is_active = VALUES(is_active);

-- Get author IDs
SET @sarah_id = (SELECT id FROM users WHERE username = 'sarah_johnson' LIMIT 1);
SET @michael_id = (SELECT id FROM users WHERE username = 'michael_chen' LIMIT 1);
SET @emma_id = (SELECT id FROM users WHERE username = 'emma_williams' LIMIT 1);
SET @david_id = (SELECT id FROM users WHERE username = 'david_brown' LIMIT 1);
SET @lisa_id = (SELECT id FROM users WHERE username = 'lisa_anderson' LIMIT 1);
SET @james_id = (SELECT id FROM users WHERE username = 'james_taylor' LIMIT 1);
SET @olivia_id = (SELECT id FROM users WHERE username = 'olivia_martinez' LIMIT 1);
SET @robert_id = (SELECT id FROM users WHERE username = 'robert_wilson' LIMIT 1);
SET @sophia_id = (SELECT id FROM users WHERE username = 'sophia_thomas' LIMIT 1);
SET @william_id = (SELECT id FROM users WHERE username = 'william_davis' LIMIT 1);

-- Get category IDs
SET @politics_id = (SELECT id FROM categories WHERE slug = 'politics' LIMIT 1);
SET @economy_id = (SELECT id FROM categories WHERE slug = 'economy' LIMIT 1);
SET @culture_id = (SELECT id FROM categories WHERE slug = 'culture' LIMIT 1);
SET @sports_id = (SELECT id FROM categories WHERE slug = 'sports' LIMIT 1);
SET @tech_id = (SELECT id FROM categories WHERE slug = 'technology' LIMIT 1);
SET @science_id = (SELECT id FROM categories WHERE slug = 'science' LIMIT 1);
SET @health_id = (SELECT id FROM categories WHERE slug = 'health' LIMIT 1);
SET @world_id = (SELECT id FROM categories WHERE slug = 'world' LIMIT 1);

-- Helper function to generate slug from title
-- Insert many articles with different authors

-- Politics Articles
INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
SELECT * FROM (SELECT 
    'Presidential Election Results: Key Takeaways' as title,
    'presidential-election-results-key-takeaways' as slug,
    'The latest presidential election has concluded with significant implications for national policy. Voters turned out in record numbers, reflecting the high stakes of this election cycle. Key issues that dominated the campaign include healthcare reform, climate policy, and economic recovery. Analysts are now examining the demographic shifts and regional voting patterns that determined the outcome. The new administration faces immediate challenges in implementing their agenda while navigating a divided legislature. International observers have been closely monitoring the process, noting the robustness of the democratic system. Economic markets reacted to the results with cautious optimism, while social movements continue to organize around their priorities. The transition process has begun, with key appointments expected in the coming weeks. This election marks a significant shift in the political landscape, with new coalitions emerging and traditional alignments being tested. Voter engagement reached unprecedented levels, particularly among younger demographics and historically underrepresented communities.' as content,
    'The latest presidential election has concluded with significant implications for national policy and future governance.' as excerpt,
    @sarah_id as author_id,
    @politics_id as category_id,
    TRUE as is_breaking,
    FALSE as is_premium,
    'published' as status,
    FLOOR(150 + RAND() * 200) as views_count,
    FLOOR(15 + RAND() * 25) as likes_count,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 30) DAY) as published_at
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'presidential-election-results-key-takeaways');

INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
SELECT * FROM (SELECT 
    'Senate Approves Major Infrastructure Bill' as title,
    'senate-approves-major-infrastructure-bill' as slug,
    'In a historic bipartisan vote, the Senate has approved a comprehensive infrastructure bill that allocates billions for transportation, broadband, and clean energy projects. The legislation represents years of negotiation and includes provisions for repairing aging roads and bridges, expanding high-speed internet access to rural areas, and investing in renewable energy infrastructure. Supporters hail it as a transformative investment in America\'s future, while critics express concerns about the cost and implementation timeline. The bill now moves to the House of Representatives, where it faces additional scrutiny and potential amendments. Industry groups have largely supported the measure, anticipating job creation and economic stimulus. Environmental organizations have praised the climate-related components, though some advocate for even more ambitious targets. Labor unions have welcomed the infrastructure focus, expecting it to generate union jobs in construction and related fields. The timeline for implementation spans several years, with oversight committees established to monitor progress and spending.' as content,
    'The Senate approves a comprehensive infrastructure bill with bipartisan support, focusing on transportation, broadband, and clean energy.' as excerpt,
    @michael_id as author_id,
    @politics_id as category_id,
    FALSE as is_breaking,
    FALSE as is_premium,
    'published' as status,
    FLOOR(120 + RAND() * 150) as views_count,
    FLOOR(10 + RAND() * 20) as likes_count,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 25) DAY) as published_at
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'senate-approves-major-infrastructure-bill');

-- Economy Articles  
INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
SELECT * FROM (SELECT 
    'Global Markets Reach Record Highs' as title,
    'global-markets-reach-record-highs' as slug,
    'Stock markets around the world have surged to unprecedented levels, driven by strong corporate earnings and optimistic economic forecasts. Technology stocks led the rally, with major indices posting gains for multiple consecutive weeks. Analysts attribute the bullish trend to robust consumer spending, improving employment figures, and continued monetary policy support. International markets have also shown strength, with European and Asian exchanges following the upward trajectory. However, some experts warn of potential volatility ahead, citing concerns about inflation pressures and geopolitical tensions. Investors remain cautiously optimistic, balancing between growth opportunities and risk management strategies. The market performance has boosted retirement accounts and investment portfolios, though some worry about potential bubbles in certain sectors. Central banks are monitoring the situation closely, ready to adjust policies if needed to maintain economic stability.' as content,
    'Stock markets worldwide surge to record levels, driven by strong earnings and optimistic economic forecasts.' as excerpt,
    @emma_id as author_id,
    @economy_id as category_id,
    FALSE as is_breaking,
    FALSE as is_premium,
    'published' as status,
    FLOOR(180 + RAND() * 220) as views_count,
    FLOOR(20 + RAND() * 30) as likes_count,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 20) DAY) as published_at
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'global-markets-reach-record-highs');

INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
SELECT * FROM (SELECT 
    'Inflation Rates Stabilize After Months of Increases' as title,
    'inflation-rates-stabilize-after-months' as slug,
    'Inflation data released this month shows signs of stabilization after months of steady increases. The consumer price index rose at a slower pace than expected, suggesting that the Federal Reserve\'s monetary policies are beginning to take effect. Core inflation, which excludes volatile food and energy prices, also moderated, providing additional evidence that price pressures may be easing. Economists are cautiously optimistic, noting that while inflation remains above target levels, the trend appears to be moving in the right direction. Supply chain improvements have contributed to the stabilization, as manufacturers and retailers work through backlogs. Consumers may see some relief in the coming months, though prices are expected to remain elevated compared to pre-pandemic levels. The housing market, which has been a major driver of inflation, is showing signs of cooling as mortgage rates rise and inventory increases.' as content,
    'Latest inflation data shows stabilization, with price increases slowing after months of steady growth.' as excerpt,
    @david_id as author_id,
    @economy_id as category_id,
    FALSE as is_breaking,
    TRUE as is_premium,
    'published' as status,
    FLOOR(200 + RAND() * 250) as views_count,
    FLOOR(25 + RAND() * 35) as likes_count,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 15) DAY) as published_at
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'inflation-rates-stabilize-after-months');

-- Technology Articles
INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
SELECT * FROM (SELECT 
    'Revolutionary AI Model Breaks Language Barriers' as title,
    'revolutionary-ai-model-breaks-language-barriers' as slug,
    'A groundbreaking artificial intelligence system has achieved near-instantaneous translation across 100 languages with unprecedented accuracy. Developed by a team of international researchers, the model uses advanced neural networks trained on billions of multilingual text pairs. The technology promises to revolutionize communication in business, education, and international relations. Early demonstrations show the system maintaining context and nuance that previous translation tools struggled with. The development team has made the model open-source, allowing developers worldwide to build applications on top of it. Companies are already exploring integrations for customer service, content creation, and real-time communication platforms. Language learning apps are incorporating the technology to provide more natural conversation practice. Humanitarian organizations see potential for bridging communication gaps in crisis situations and refugee assistance programs.' as content,
    'New AI system achieves near-instantaneous translation across 100 languages with unprecedented accuracy and nuance.' as excerpt,
    @lisa_id as author_id,
    @tech_id as category_id,
    TRUE as is_breaking,
    FALSE as is_premium,
    'published' as status,
    FLOOR(250 + RAND() * 300) as views_count,
    FLOOR(40 + RAND() * 50) as likes_count,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 10) DAY) as published_at
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'revolutionary-ai-model-breaks-language-barriers');

INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
SELECT * FROM (SELECT 
    'Quantum Computing Breakthrough Achieved' as title,
    'quantum-computing-breakthrough-achieved' as slug,
    'Scientists have successfully demonstrated quantum error correction at a scale that brings practical quantum computing significantly closer to reality. The breakthrough addresses one of the major obstacles preventing quantum computers from solving real-world problems. By implementing a new error correction protocol, researchers maintained quantum coherence for durations long enough to perform complex calculations. The achievement represents a milestone in the quest for quantum advantage, where quantum computers can solve problems that are intractable for classical computers. Major tech companies and research institutions are investing heavily in this technology, anticipating applications in drug discovery, financial modeling, and cryptography. The error correction method could accelerate progress toward building fault-tolerant quantum computers capable of running sophisticated algorithms. Security experts are closely monitoring developments, as quantum computers could potentially break current encryption methods while also enabling new forms of quantum encryption.' as content,
    'Scientists achieve quantum error correction breakthrough, bringing practical quantum computing significantly closer to reality.' as excerpt,
    @james_id as author_id,
    @tech_id as category_id,
    FALSE as is_breaking,
    TRUE as is_premium,
    'published' as status,
    FLOOR(220 + RAND() * 280) as views_count,
    FLOOR(35 + RAND() * 45) as likes_count,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 12) DAY) as published_at
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'quantum-computing-breakthrough-achieved');

-- Science Articles
INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
SELECT * FROM (SELECT 
    'Mars Mission Returns First Samples to Earth' as title,
    'mars-mission-returns-first-samples' as slug,
    'A historic space mission has successfully returned the first samples of Martian rock and soil to Earth, opening new possibilities for understanding the Red Planet\'s history and potential for past life. The samples, collected over years by a sophisticated rover, arrived in a specialized capsule that survived the journey through Earth\'s atmosphere. Scientists are now beginning detailed analysis that could reveal clues about Mars\'s geological evolution and climate history. The samples include various rock types, suggesting a complex geological past with volcanic activity and potential water interaction. Researchers hope to find evidence of ancient microbial life or at least the conditions that might have supported it. The mission represents decades of planning and international collaboration, with contributions from multiple space agencies. The analysis will take years, but early results are already generating excitement in the scientific community. Future missions are being planned based on the insights gained from these samples, with ambitions for eventual human exploration.' as content,
    'Historic Mars mission successfully returns first samples of Martian material to Earth for detailed analysis.' as excerpt,
    @olivia_id as author_id,
    @science_id as category_id,
    TRUE as is_breaking,
    FALSE as is_premium,
    'published' as status,
    FLOOR(280 + RAND() * 320) as views_count,
    FLOOR(45 + RAND() * 55) as likes_count,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 8) DAY) as published_at
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'mars-mission-returns-first-samples');

-- Health Articles
INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
SELECT * FROM (SELECT 
    'New Cancer Treatment Shows Promising Results' as title,
    'new-cancer-treatment-shows-promising-results' as slug,
    'Clinical trials of a novel cancer immunotherapy have shown remarkable results, with over 70% of patients showing significant tumor reduction. The treatment combines targeted drug therapy with personalized immune system activation, representing a new approach to fighting aggressive cancers. Patients who had exhausted other treatment options experienced substantial improvement, with some achieving complete remission. The therapy works by identifying specific markers on cancer cells and training the patient\'s immune system to recognize and attack them. Researchers are optimistic about expanding the treatment to additional cancer types, though larger studies are needed to confirm the results. The development has generated excitement in the oncology community, with experts calling it a potential game-changer for certain cancer subtypes. Pharmaceutical companies are fast-tracking development and seeking regulatory approval. The personalized nature of the treatment means it can be tailored to individual patients, potentially improving outcomes while reducing side effects compared to traditional chemotherapy.' as content,
    'Novel cancer immunotherapy shows promising results in clinical trials, with over 70% of patients experiencing significant improvement.' as excerpt,
    @robert_id as author_id,
    @health_id as category_id,
    FALSE as is_breaking,
    TRUE as is_premium,
    'published' as status,
    FLOOR(190 + RAND() * 240) as views_count,
    FLOOR(30 + RAND() * 40) as likes_count,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 18) DAY) as published_at
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'new-cancer-treatment-shows-promising-results');

-- Sports Articles
INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
SELECT * FROM (SELECT 
    'Championship Game Breaks Viewership Records' as title,
    'championship-game-breaks-viewership-records' as slug,
    'The championship final attracted the largest television audience in the sport\'s history, with millions tuning in worldwide to watch the dramatic conclusion. The game went into overtime, creating an unforgettable spectacle that captivated viewers until the final seconds. Social media platforms buzzed with real-time reactions, setting new engagement records. The victory marks a historic achievement for the winning team, ending a decades-long championship drought. Players delivered outstanding performances under pressure, with several breaking individual records during the match. The event generated significant economic activity in the host city, with tourism and hospitality businesses reporting record revenues. Sports analysts are calling it one of the greatest games in the sport\'s history, highlighting the skill, determination, and drama on display. The championship has inspired a new generation of young athletes, with youth participation in the sport expected to surge.' as content,
    'Historic championship game breaks viewership records and delivers unforgettable drama in overtime victory.' as excerpt,
    @sophia_id as author_id,
    @sports_id as category_id,
    TRUE as is_breaking,
    FALSE as is_premium,
    'published' as status,
    FLOOR(300 + RAND() * 350) as views_count,
    FLOOR(50 + RAND() * 60) as likes_count,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 5) DAY) as published_at
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'championship-game-breaks-viewership-records');

-- Culture Articles
INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
SELECT * FROM (SELECT 
    'Major Film Festival Announces Award Winners' as title,
    'major-film-festival-announces-award-winners' as slug,
    'The prestigious international film festival concluded with the announcement of its award winners, celebrating cinematic excellence from around the world. Independent films dominated the major categories, with several emerging directors receiving recognition for their innovative work. The festival showcased diverse voices and perspectives, reflecting a global commitment to inclusive storytelling. The top prize went to a thought-provoking drama that addresses contemporary social issues, while documentary and short film categories honored impactful works. Industry professionals praised the festival for its curation and commitment to artistic integrity. The event attracted filmmakers, critics, and cinephiles from dozens of countries, creating a vibrant cultural exchange. Many of the featured films are expected to receive wider distribution following their festival success. The awards ceremony itself became a celebration of cinema\'s power to inspire, challenge, and connect audiences across cultures and borders.' as content,
    'International film festival concludes, celebrating diverse cinematic achievements and emerging voices in world cinema.' as excerpt,
    @william_id as author_id,
    @culture_id as category_id,
    FALSE as is_breaking,
    FALSE as is_premium,
    'published' as status,
    FLOOR(140 + RAND() * 180) as views_count,
    FLOOR(18 + RAND() * 28) as likes_count,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 22) DAY) as published_at
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'major-film-festival-announces-award-winners');

-- World Articles
INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
SELECT * FROM (SELECT 
    'International Climate Summit Reaches Agreement' as title,
    'international-climate-summit-reaches-agreement' as slug,
    'World leaders have reached a landmark agreement on climate action at the international summit, committing to more ambitious emissions reduction targets. The deal represents a significant step forward in global cooperation on environmental issues, with developed nations pledging increased financial support for developing countries. Key components include accelerated timelines for carbon neutrality, enhanced renewable energy targets, and new mechanisms for monitoring progress. Environmental groups have welcomed the agreement while calling for even stronger action. The summit brought together over 190 countries, with intense negotiations continuing until the final hours. Business leaders have praised the clarity the agreement provides for long-term planning and investment. The financial commitments to green technology and adaptation measures could catalyze significant economic transformation. Implementation will require sustained political will and international coordination, with regular review mechanisms built into the agreement.' as content,
    'World leaders reach landmark climate agreement with ambitious emissions targets and enhanced international cooperation.' as excerpt,
    @sarah_id as author_id,
    @world_id as category_id,
    FALSE as is_breaking,
    FALSE as is_premium,
    'published' as status,
    FLOOR(170 + RAND() * 210) as views_count,
    FLOOR(22 + RAND() * 32) as likes_count,
    DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 28) DAY) as published_at
) AS tmp
WHERE NOT EXISTS (SELECT 1 FROM articles WHERE slug = 'international-climate-summit-reaches-agreement');

-- Add more diverse articles (creating variations to avoid duplicates)
-- I'll create a procedure to add many more articles efficiently
DELIMITER //

CREATE PROCEDURE IF NOT EXISTS AddMultipleArticles()
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE author_list TEXT DEFAULT CONCAT(@sarah_id, ',', @michael_id, ',', @emma_id, ',', @david_id, ',', @lisa_id);
    DECLARE category_list TEXT DEFAULT CONCAT(@politics_id, ',', @economy_id, ',', @culture_id, ',', @sports_id, ',', @tech_id, ',', @science_id, ',', @health_id, ',', @world_id);
    
    WHILE i < 30 DO
        INSERT INTO articles (title, slug, content, excerpt, author_id, category_id, is_breaking, is_premium, status, views_count, likes_count, published_at)
        SELECT 
            CONCAT('News Article ', i+1, ' - ', SUBSTRING(MD5(RAND()), 1, 8)) as title,
            CONCAT('news-article-', i+1, '-', SUBSTRING(MD5(RAND()), 1, 8)) as slug,
            CONCAT('This is comprehensive content for article number ', i+1, '. It covers important topics and provides detailed analysis of current events. The article discusses various aspects of the subject matter and offers insights for readers interested in staying informed about recent developments.') as content,
            CONCAT('Brief excerpt for article ', i+1, ' providing a summary of key points.') as excerpt,
            (SELECT id FROM users WHERE role = 'editor' ORDER BY RAND() LIMIT 1) as author_id,
            (SELECT id FROM categories ORDER BY RAND() LIMIT 1) as category_id,
            IF(RAND() > 0.8, TRUE, FALSE) as is_breaking,
            IF(RAND() > 0.7, TRUE, FALSE) as is_premium,
            'published' as status,
            FLOOR(50 + RAND() * 400) as views_count,
            FLOOR(5 + RAND() * 60) as likes_count,
            DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 30) DAY) as published_at
        WHERE NOT EXISTS (
            SELECT 1 FROM articles WHERE slug = CONCAT('news-article-', i+1, '-', SUBSTRING(MD5(RAND()), 1, 8))
        );
        SET i = i + 1;
    END WHILE;
END//

DELIMITER ;

-- Call the procedure to add articles
CALL AddMultipleArticles();

-- Drop the procedure after use
DROP PROCEDURE IF EXISTS AddMultipleArticles;

-- Verify results
SELECT COUNT(*) as total_articles FROM articles;
SELECT COUNT(DISTINCT author_id) as unique_authors FROM articles;
SELECT u.username, COUNT(a.id) as article_count 
FROM users u 
LEFT JOIN articles a ON u.id = a.author_id 
WHERE u.role = 'editor' 
GROUP BY u.id, u.username 
ORDER BY article_count DESC;

