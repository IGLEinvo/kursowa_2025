-- Script to add premium user with premium subscription
-- Run this script to add user: premium1, email: premium1@gmail.com, password: premium123
-- Usage: /usr/local/mysql/bin/mysql -u root -poko200505@ news_newspaper < database/add_premium_user.sql

USE news_newspaper;

-- Check if user already exists and create if not
INSERT INTO users (username, email, password_hash, first_name, last_name, role, is_active)
SELECT 
    'premium1',
    'premium1@gmail.com',
    '$2b$12$oAh1V8beeCZ5l0U0TlYWiOQaJw0qU8GPVE8f2n0UIpP6tK6eWzzn.', -- bcrypt hash for 'premium123'
    'Premium',
    'User',
    'user',
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM users WHERE email = 'premium1@gmail.com' OR username = 'premium1'
);

-- Get user ID
SET @user_id = (SELECT id FROM users WHERE email = 'premium1@gmail.com' LIMIT 1);

-- Get Premium tier ID (type='paid')
SET @tier_id = (SELECT id FROM subscription_tiers WHERE type = 'paid' LIMIT 1);

-- Check if user already has active premium subscription and create if not (1 year)
INSERT INTO user_subscriptions (user_id, tier_id, start_date, end_date, is_active)
SELECT 
    @user_id,
    @tier_id,
    NOW(),
    DATE_ADD(NOW(), INTERVAL 365 DAY),
    TRUE
WHERE NOT EXISTS (
    SELECT 1 FROM user_subscriptions 
    WHERE user_id = @user_id 
    AND tier_id = @tier_id 
    AND is_active = TRUE 
    AND end_date > NOW()
);

-- Display results
SELECT 
    u.id as user_id,
    u.username,
    u.email,
    st.name as subscription_tier,
    st.type as tier_type,
    us.start_date,
    us.end_date,
    us.is_active,
    CASE 
        WHEN us.end_date > NOW() THEN 'Active'
        ELSE 'Expired'
    END as status
FROM users u
LEFT JOIN user_subscriptions us ON u.id = us.user_id AND us.is_active = TRUE
LEFT JOIN subscription_tiers st ON us.tier_id = st.id
WHERE u.email = 'premium1@gmail.com';

