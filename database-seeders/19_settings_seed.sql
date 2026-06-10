-- DanangTrip Settings Seeder
-- FILE: 19_settings_seed.sql
-- Purpose:
--   SQL mirror of danangtrip-api/database/seeders/SettingSeeder.php.
--   Use this when seeding from the standalone database-seeders folder.

INSERT INTO settings (key, value, value_type, is_public, created_at, updated_at) VALUES
('general.hotline', '1900 1800', 'string', true, NOW(), NOW()),
('general.email', 'info@danangtrip.com', 'string', true, NOW(), NOW()),
('general.address', '123 Bach Dang, Hai Chau, Da Nang', 'string', true, NOW(), NOW()),
('general.support_hours', '08:00 - 22:00', 'string', true, NOW(), NOW()),
('brand.website_name', 'DaNangTrip', 'string', true, NOW(), NOW()),
('brand.logo', 'https://res.cloudinary.com/dmukxquza/image/upload/v1781012077/danangtrip/branding/logo/danangtrip-logo.png', 'string', true, NOW(), NOW()),
('brand.favicon', 'https://res.cloudinary.com/dmukxquza/image/upload/v1781012079/danangtrip/branding/favicon/danangtrip-favicon.png', 'string', true, NOW(), NOW()),
('social.facebook', 'https://facebook.com/danangtrip', 'string', true, NOW(), NOW()),
('social.instagram', 'https://instagram.com/danangtrip', 'string', true, NOW(), NOW()),
('social.youtube', 'https://youtube.com/danangtrip', 'string', true, NOW(), NOW()),
('social.tiktok', 'https://tiktok.com/@danangtrip', 'string', true, NOW(), NOW()),
('social.zalo', 'https://zalo.me/danangtrip', 'string', true, NOW(), NOW()),
('payment.sepay', 'true', 'boolean', true, NOW(), NOW()),
('payment.cod', 'true', 'boolean', true, NOW(), NOW()),
('payment.vnpay', 'false', 'boolean', true, NOW(), NOW()),
('payment.momo', 'false', 'boolean', true, NOW(), NOW()),
('payment.zalopay', 'false', 'boolean', true, NOW(), NOW()),
('policy.terms', 'https://danangtrip.com/terms', 'string', true, NOW(), NOW()),
('policy.privacy', 'https://danangtrip.com/privacy', 'string', true, NOW(), NOW()),
('policy.data_protection', 'https://danangtrip.com/data-protection', 'string', true, NOW(), NOW()),
('seo.meta_title', 'DaNangTrip - Du lịch Đà Nẵng trọn vẹn', 'string', true, NOW(), NOW()),
('seo.meta_description', 'Đặt tour du lịch Đà Nẵng giá rẻ, khám phá các địa danh nổi tiếng Bà Nà Hills, Hội An, Ngũ Hành Sơn cùng DaNangTrip.', 'string', true, NOW(), NOW()),
('seo.og_image', 'https://res.cloudinary.com/dmukxquza/image/upload/v1781012083/danangtrip/branding/og/danangtrip-og-image.jpg', 'string', true, NOW(), NOW())
ON CONFLICT (key) DO UPDATE SET
    value = EXCLUDED.value,
    value_type = EXCLUDED.value_type,
    is_public = EXCLUDED.is_public,
    updated_at = NOW();
