BEGIN;
INSERT INTO "settings" ("id", "key", "value", "value_type", "is_public", "created_at", "updated_at") VALUES
(1, 'general.hotline', '1900 1800', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(2, 'general.email', 'info@danangtrip.com', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(3, 'general.address', '123 Bach Dang, Hai Chau, Da Nang', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(4, 'general.support_hours', '08:00 - 22:00', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(5, 'brand.website_name', 'DaNangTrip', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(6, 'brand.logo', 'https://res.cloudinary.com/dmukxquza/image/upload/v1781012077/danangtrip/branding/logo/danangtrip-logo.png', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(7, 'brand.favicon', 'https://res.cloudinary.com/dmukxquza/image/upload/v1781012079/danangtrip/branding/favicon/danangtrip-favicon.png', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(8, 'social.facebook', 'https://facebook.com/danangtrip', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(9, 'social.instagram', 'https://instagram.com/danangtrip', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(10, 'social.youtube', 'https://youtube.com/danangtrip', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(11, 'social.tiktok', 'https://tiktok.com/@danangtrip', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(12, 'social.zalo', 'https://zalo.me/danangtrip', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(13, 'payment.sepay', 'true', 'boolean', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(14, 'payment.cod', 'true', 'boolean', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(15, 'payment.vnpay', 'false', 'boolean', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(16, 'payment.momo', 'false', 'boolean', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(17, 'payment.zalopay', 'false', 'boolean', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(18, 'policy.terms', 'https://danangtrip.com/terms', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(19, 'policy.privacy', 'https://danangtrip.com/privacy', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(20, 'policy.data_protection', 'https://danangtrip.com/data-protection', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(21, 'seo.meta_title', 'DaNangTrip - Du lịch Đà Nẵng trọn vẹn', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(22, 'seo.meta_description', 'Đặt tour du lịch Đà Nẵng giá rẻ, khám phá các địa danh nổi tiếng Bà Nà Hills, Hội An, Ngũ Hành Sơn cùng DaNangTrip.', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(23, 'seo.og_image', 'https://res.cloudinary.com/dmukxquza/image/upload/v1781012083/danangtrip/branding/og/danangtrip-og-image.jpg', 'string', true, '2026-06-13 10:19:57', '2026-06-13 10:19:57'),
(24, 'data.ratings_admin_read_state_initialized_v1', '2026-06-13 10:21:18.161656+00', 'string', false, '2026-06-13 10:21:18', '2026-06-13 10:21:18'),
(25, 'chatbot.enabled', 'true', 'boolean', false, '2026-06-14 11:22:48', '2026-06-14 11:22:48'),
(26, 'chatbot.clarification_attempt_limit', '2', 'number', false, '2026-06-14 11:22:52', '2026-06-14 11:22:52'),
(27, 'chatbot.cache_ttl_seconds', '86400', 'number', false, '2026-06-14 11:22:57', '2026-06-14 11:22:57'),
(28, 'chatbot.cache', '{\threshold_transactional\:0.97,\threshold_faq\:0.92}', 'json', false, '2026-06-14 11:23:35', '2026-06-14 11:23:35')
ON CONFLICT (id) DO NOTHING;

COMMIT;
