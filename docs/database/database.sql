-- ============================================================
-- DATABASE SCHEMA - WEBSITE DU LỊCH ĐÀ NẴNG "ĐÀ NẴNG TRIP"
-- Stack: Laravel 11.x + MySQL 8.0
-- Encoding: utf8mb4_unicode_ci
-- Tổng: 24 bảng | Dịch vụ tour (không có point)
-- ============================================================

CREATE DATABASE IF NOT EXISTS danang_trip
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE danang_trip;

-- ============================================================
-- BẢNG 1: users
-- ============================================================
CREATE TABLE users (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  username          VARCHAR(50)  NOT NULL UNIQUE,
  email             VARCHAR(100) NOT NULL UNIQUE,
  password          VARCHAR(255) NOT NULL,
  full_name         VARCHAR(100),
  avatar            VARCHAR(255),
  phone             VARCHAR(20),
  birthdate         DATE,
  gender            VARCHAR(20),
  city              VARCHAR(100),
  role              VARCHAR(20)  NOT NULL DEFAULT 'user' COMMENT 'user | admin | staff',
  status            VARCHAR(20)  NOT NULL DEFAULT 'active' COMMENT 'active | banned',
  email_verified_at TIMESTAMP    NULL,
  last_login_at     TIMESTAMP    NULL,
  remember_token    VARCHAR(100),
  created_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_email  (email),
  INDEX idx_status (status),
  INDEX idx_role   (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 2: categories
-- ============================================================
CREATE TABLE categories (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(50)  NOT NULL,
  slug        VARCHAR(60)  NOT NULL UNIQUE,
  icon        VARCHAR(50),
  description TEXT,
  image       VARCHAR(255),
  sort_order  INT          DEFAULT 0,
  status      VARCHAR(20)  NOT NULL DEFAULT 'active' COMMENT 'active | inactive',
  created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 3: subcategories
-- ============================================================
CREATE TABLE subcategories (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  category_id BIGINT UNSIGNED NOT NULL,
  name        VARCHAR(50)  NOT NULL,
  slug        VARCHAR(60)  NOT NULL UNIQUE,
  description TEXT,
  sort_order  INT          DEFAULT 0,
  status      VARCHAR(20)  NOT NULL DEFAULT 'active' COMMENT 'active | inactive',
  created_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_category_id (category_id),
  INDEX idx_status      (status),
  FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 4: locations
-- ============================================================
CREATE TABLE locations (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name              VARCHAR(200) NOT NULL,
  slug              VARCHAR(220) NOT NULL UNIQUE,
  category_id       BIGINT UNSIGNED NOT NULL,
  subcategory_id    BIGINT UNSIGNED NULL,
  description       TEXT         NOT NULL,
  short_description VARCHAR(500) NOT NULL,
  address           VARCHAR(255) NOT NULL,
  district          VARCHAR(50)  NOT NULL COMMENT 'Hải Châu | Sơn Trà | Ngũ Hành Sơn | Cẩm Lệ | Thanh Khê | Liên Chiểu',
  ward              VARCHAR(50),
  latitude          DECIMAL(10,8) NOT NULL,
  longitude         DECIMAL(11,8) NOT NULL,
  phone             VARCHAR(20),
  email             VARCHAR(100),
  website           VARCHAR(255),
  opening_hours     TEXT COMMENT 'JSON: {"mon":"08:00-22:00","sun":"closed"}',
  price_min         DECIMAL(12,0),
  price_max         DECIMAL(12,0),
  price_level       TINYINT COMMENT '1=Rẻ | 2=Trung bình | 3=Cao | 4=Sang trọng',
  avg_rating        DECIMAL(3,2) DEFAULT 0.00,
  review_count      INT          DEFAULT 0,
  view_count        INT          DEFAULT 0,
  favorite_count    INT          DEFAULT 0,
  thumbnail         VARCHAR(255),
  images            TEXT COMMENT 'JSON array URL ảnh',
  video_url         VARCHAR(255),
  status            VARCHAR(20)  NOT NULL DEFAULT 'active' COMMENT 'active | inactive',
  is_featured       BOOLEAN      NOT NULL DEFAULT FALSE,
  created_by        BIGINT UNSIGNED NOT NULL,
  created_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at        TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_category_id    (category_id),
  INDEX idx_subcategory_id (subcategory_id),
  INDEX idx_district       (district),
  INDEX idx_status         (status),
  INDEX idx_is_featured    (is_featured),
  INDEX idx_avg_rating     (avg_rating),
  INDEX idx_view_count     (view_count),
  FOREIGN KEY (category_id)    REFERENCES categories(id),
  FOREIGN KEY (subcategory_id) REFERENCES subcategories(id) ON DELETE SET NULL,
  FOREIGN KEY (created_by)     REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 5: tags
-- ============================================================
CREATE TABLE tags (
  id         BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name       VARCHAR(50) NOT NULL UNIQUE,
  slug       VARCHAR(60) NOT NULL UNIQUE,
  type       VARCHAR(30) COMMENT 'cuisine | service | feature | atmosphere',
  created_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 6: location_tags
-- ============================================================
CREATE TABLE location_tags (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  location_id BIGINT UNSIGNED NOT NULL,
  tag_id      BIGINT UNSIGNED NOT NULL,
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_location_tag (location_id, tag_id),
  FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
  FOREIGN KEY (tag_id)      REFERENCES tags(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 7: amenities
-- ============================================================
CREATE TABLE amenities (
  id         BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name       VARCHAR(50) NOT NULL UNIQUE,
  icon       VARCHAR(50),
  category   VARCHAR(30) COMMENT 'connectivity | parking | comfort | payment',
  created_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 8: location_amenities
-- ============================================================
CREATE TABLE location_amenities (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  location_id BIGINT UNSIGNED NOT NULL,
  amenity_id  BIGINT UNSIGNED NOT NULL,
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_location_amenity (location_id, amenity_id),
  FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
  FOREIGN KEY (amenity_id)  REFERENCES amenities(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 9: tour_categories
-- ============================================================
CREATE TABLE tour_categories (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(50) NOT NULL UNIQUE,
  slug        VARCHAR(60) NOT NULL UNIQUE,
  description TEXT,
  icon        VARCHAR(50),
  sort_order  INT         DEFAULT 0,
  status      VARCHAR(20) NOT NULL DEFAULT 'active' COMMENT 'active | inactive',
  created_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 10: tours
-- ============================================================
CREATE TABLE tours (
  id               BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name             VARCHAR(200) NOT NULL,
  slug             VARCHAR(220) NOT NULL UNIQUE,
  tour_category_id BIGINT UNSIGNED NOT NULL,
  description      TEXT,
  short_desc       VARCHAR(500),
  itinerary        TEXT COMMENT 'Lịch trình chi tiết (JSON hoặc HTML)',
  inclusions       TEXT COMMENT 'Bao gồm (JSON array)',
  exclusions       TEXT COMMENT 'Không bao gồm (JSON array)',
  price_adult      DECIMAL(12,0) NOT NULL,
  price_child      DECIMAL(12,0),
  price_infant     DECIMAL(12,0),
  discount_percent INT           DEFAULT 0 COMMENT '0-100',
  duration         VARCHAR(50)   COMMENT 'Ví dụ: 1 ngày, 2 ngày 1 đêm',
  start_time       VARCHAR(50),
  meeting_point    VARCHAR(255),
  max_people       INT           DEFAULT 0 COMMENT '0 = không giới hạn',
  min_people       INT           DEFAULT 1,
  available_from   DATE,
  available_to     DATE,
  thumbnail        VARCHAR(255),
  images           TEXT COMMENT 'JSON array URL ảnh',
  video_url        VARCHAR(255),
  location_ids     TEXT COMMENT 'JSON array ID các địa điểm trong tour',
  status           VARCHAR(20)   NOT NULL DEFAULT 'active' COMMENT 'active | inactive | sold_out',
  is_featured      BOOLEAN       NOT NULL DEFAULT FALSE,
  is_hot           BOOLEAN       NOT NULL DEFAULT FALSE,
  view_count       INT           DEFAULT 0,
  booking_count    INT           DEFAULT 0,
  created_by       BIGINT UNSIGNED NOT NULL,
  created_at       TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_tour_category_id (tour_category_id),
  INDEX idx_status           (status),
  INDEX idx_is_featured      (is_featured),
  INDEX idx_is_hot           (is_hot),
  INDEX idx_price_adult      (price_adult),
  INDEX idx_available_from   (available_from),
  INDEX idx_available_to     (available_to),
  FOREIGN KEY (tour_category_id) REFERENCES tour_categories(id),
  FOREIGN KEY (created_by)       REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 11: tour_schedules
-- ============================================================
CREATE TABLE tour_schedules (
  id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  tour_id       BIGINT UNSIGNED NOT NULL,
  start_date    DATE            NOT NULL,
  end_date      DATE            NOT NULL,
  max_people    INT             NOT NULL DEFAULT 0,
  booked_people INT             NOT NULL DEFAULT 0,
  price_adult   DECIMAL(12,0)   NULL COMMENT 'Override giá tour cho ngày này',
  price_child   DECIMAL(12,0)   NULL,
  price_infant  DECIMAL(12,0)   NULL,
  status        VARCHAR(20)     NOT NULL DEFAULT 'available' COMMENT 'available | full | cancelled',
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_tour_id    (tour_id),
  INDEX idx_start_date (start_date),
  INDEX idx_status     (status),
  UNIQUE KEY uq_tour_schedule (tour_id, start_date),
  FOREIGN KEY (tour_id) REFERENCES tours(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 12: bookings
-- ============================================================
CREATE TABLE bookings (
  id                  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  booking_code        VARCHAR(20)   NOT NULL UNIQUE COMMENT 'DANANG-YYYYMMDD-XXXX',
  user_id             BIGINT UNSIGNED NULL,
  customer_name       VARCHAR(100)  NOT NULL,
  customer_email      VARCHAR(100)  NOT NULL,
  customer_phone      VARCHAR(20)   NOT NULL,
  customer_address    TEXT,
  customer_note       TEXT,
  total_amount        DECIMAL(12,0) NOT NULL,
  discount_amount     DECIMAL(12,0) NOT NULL DEFAULT 0,
  final_amount        DECIMAL(12,0) NOT NULL,
  deposit_amount      DECIMAL(12,0) DEFAULT 0,
  payment_method      VARCHAR(30)   COMMENT 'momo | vnpay | bank | cash',
  payment_status      VARCHAR(30)   NOT NULL DEFAULT 'unpaid' COMMENT 'unpaid | paid | failed | refunded',
  booking_status      VARCHAR(30)   NOT NULL DEFAULT 'pending' COMMENT 'pending | confirmed | cancelled | completed',
  cancellation_reason TEXT,
  booked_at           TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  confirmed_at        TIMESTAMP     NULL,
  cancelled_at        TIMESTAMP     NULL,
  completed_at        TIMESTAMP     NULL,
  created_at          TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at          TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_booking_code    (booking_code),
  INDEX idx_user_id         (user_id),
  INDEX idx_customer_email  (customer_email),
  INDEX idx_customer_phone  (customer_phone),
  INDEX idx_booking_status  (booking_status),
  INDEX idx_payment_status  (payment_status),
  INDEX idx_booked_at       (booked_at),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 13: booking_items
-- ============================================================
CREATE TABLE booking_items (
  id                BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  booking_id        BIGINT UNSIGNED NOT NULL,
  tour_id           BIGINT UNSIGNED NOT NULL,
  tour_schedule_id  BIGINT UNSIGNED NOT NULL,
  item_type         VARCHAR(30)   NOT NULL DEFAULT 'tour' COMMENT 'tour | hotel | transport | extra',
  item_name         VARCHAR(200)  NOT NULL,
  travel_date       DATE          NOT NULL,
  quantity_adult    INT           NOT NULL DEFAULT 0,
  quantity_child    INT           NOT NULL DEFAULT 0,
  quantity_infant   INT           NOT NULL DEFAULT 0,
  unit_price_adult  DECIMAL(12,0) NOT NULL DEFAULT 0,
  unit_price_child  DECIMAL(12,0) NOT NULL DEFAULT 0,
  unit_price_infant DECIMAL(12,0) NOT NULL DEFAULT 0,
  subtotal          DECIMAL(12,0) NOT NULL,
  status            VARCHAR(30)   NOT NULL DEFAULT 'pending' COMMENT 'pending | confirmed | cancelled | completed',
  created_at        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at        TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_booking_id       (booking_id),
  INDEX idx_tour_id          (tour_id),
  INDEX idx_tour_schedule_id (tour_schedule_id),
  INDEX idx_travel_date      (travel_date),
  FOREIGN KEY (booking_id)       REFERENCES bookings(id) ON DELETE CASCADE,
  FOREIGN KEY (tour_id)          REFERENCES tours(id),
  FOREIGN KEY (tour_schedule_id) REFERENCES tour_schedules(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 14: payments
-- ============================================================
CREATE TABLE payments (
  id               BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  booking_id       BIGINT UNSIGNED NOT NULL,
  transaction_code VARCHAR(100)  NOT NULL UNIQUE,
  amount           DECIMAL(12,0) NOT NULL,
  payment_method   VARCHAR(30),
  payment_status   VARCHAR(30)   NOT NULL DEFAULT 'pending' COMMENT 'pending | success | failed | refunded',
  payment_gateway  VARCHAR(50)   COMMENT 'momo | vnpay | zalopay',
  gateway_response TEXT          COMMENT 'JSON response từ cổng thanh toán',
  paid_at          TIMESTAMP     NULL,
  refunded_at      TIMESTAMP     NULL,
  refund_reason    TEXT,
  created_at       TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at       TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_booking_id      (booking_id),
  INDEX idx_transaction_code (transaction_code),
  INDEX idx_payment_status  (payment_status),
  FOREIGN KEY (booking_id) REFERENCES bookings(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 15: ratings
-- ============================================================
CREATE TABLE ratings (
  id              BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id         BIGINT UNSIGNED NOT NULL,
  location_id     BIGINT UNSIGNED NULL,
  tour_id         BIGINT UNSIGNED NULL,
  booking_id      BIGINT UNSIGNED NULL,
  score           TINYINT         NOT NULL COMMENT '1-5 sao',
  comment         TEXT,
  image_urls      TEXT            COMMENT 'JSON array, tối đa 5 ảnh',
  status          VARCHAR(20)     NOT NULL DEFAULT 'pending' COMMENT 'pending | approved | rejected',
  rejected_reason VARCHAR(255),
  approved_by     BIGINT UNSIGNED NULL,
  approved_at     TIMESTAMP       NULL,
  helpful_count   INT             DEFAULT 0,
  created_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_user_id     (user_id),
  INDEX idx_location_id (location_id),
  INDEX idx_tour_id     (tour_id),
  INDEX idx_booking_id  (booking_id),
  INDEX idx_status      (status),
  INDEX idx_score       (score),
  INDEX idx_created_at  (created_at),
  UNIQUE KEY uq_user_location_rating (user_id, location_id),
  UNIQUE KEY uq_user_tour_rating     (user_id, tour_id),
  FOREIGN KEY (user_id)     REFERENCES users(id),
  FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
  FOREIGN KEY (tour_id)     REFERENCES tours(id) ON DELETE CASCADE,
  FOREIGN KEY (booking_id)  REFERENCES bookings(id) ON DELETE SET NULL,
  FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 16: rating_images
-- ============================================================
CREATE TABLE rating_images (
  id         BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  rating_id  BIGINT UNSIGNED NOT NULL,
  image_url  VARCHAR(255)    NOT NULL,
  sort_order TINYINT         DEFAULT 0,
  created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_rating_id (rating_id),
  FOREIGN KEY (rating_id) REFERENCES ratings(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 17: favorites
-- ============================================================
CREATE TABLE favorites (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id     BIGINT UNSIGNED NOT NULL,
  location_id BIGINT UNSIGNED NOT NULL,
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_user_location_fav (user_id, location_id),
  INDEX idx_location_id (location_id),
  FOREIGN KEY (user_id)     REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 18: blog_categories
-- ============================================================
CREATE TABLE blog_categories (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(50) NOT NULL UNIQUE,
  slug        VARCHAR(60) NOT NULL UNIQUE,
  description TEXT,
  created_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP   NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 19: blog_posts
-- ============================================================
CREATE TABLE blog_posts (
  id             BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  title          VARCHAR(255) NOT NULL,
  slug           VARCHAR(280) NOT NULL UNIQUE,
  excerpt        VARCHAR(500),
  content        LONGTEXT,
  featured_image VARCHAR(255),
  author_id      BIGINT UNSIGNED NOT NULL,
  view_count     INT          DEFAULT 0,
  status         VARCHAR(20)  NOT NULL DEFAULT 'draft' COMMENT 'draft | published | archived',
  published_at   TIMESTAMP    NULL,
  created_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_author_id    (author_id),
  INDEX idx_status       (status),
  INDEX idx_published_at (published_at),
  FOREIGN KEY (author_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 20: blog_post_categories
-- ============================================================
CREATE TABLE blog_post_categories (
  id               BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  post_id          BIGINT UNSIGNED NOT NULL,
  blog_category_id BIGINT UNSIGNED NOT NULL,
  UNIQUE KEY uq_post_blog_category (post_id, blog_category_id),
  FOREIGN KEY (post_id)          REFERENCES blog_posts(id) ON DELETE CASCADE,
  FOREIGN KEY (blog_category_id) REFERENCES blog_categories(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 21: views
-- ============================================================
CREATE TABLE views (
  id          BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id     BIGINT UNSIGNED NULL,
  location_id BIGINT UNSIGNED NOT NULL,
  session_id  VARCHAR(100),
  time_spent  INT             DEFAULT 0 COMMENT 'Thời gian xem (giây)',
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_user_id     (user_id),
  INDEX idx_location_id (location_id),
  INDEX idx_created_at  (created_at),
  INDEX idx_session_id  (session_id),
  FOREIGN KEY (user_id)     REFERENCES users(id) ON DELETE SET NULL,
  FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 22: search_logs
-- ============================================================
CREATE TABLE search_logs (
  id            BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id       BIGINT UNSIGNED NULL,
  session_id    VARCHAR(100),
  query         VARCHAR(255)    NOT NULL,
  results_count INT             DEFAULT 0,
  filters       TEXT            COMMENT 'JSON filters đã áp dụng',
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_user_id    (user_id),
  INDEX idx_query      (query),
  INDEX idx_created_at (created_at),
  INDEX idx_session_id (session_id),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 23: notifications
-- ============================================================
CREATE TABLE notifications (
  id         BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  user_id    BIGINT UNSIGNED NOT NULL,
  type       VARCHAR(30)     NOT NULL COMMENT 'booking_confirmed | booking_cancelled | payment_success | rating_approved',
  title      VARCHAR(255)    NOT NULL,
  content    TEXT,
  data       TEXT            COMMENT 'JSON data bổ sung',
  is_read    BOOLEAN         NOT NULL DEFAULT FALSE,
  read_at    TIMESTAMP       NULL,
  created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_user_is_read (user_id, is_read),
  INDEX idx_created_at   (created_at),
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================
-- BẢNG 24: contacts
-- ============================================================
CREATE TABLE contacts (
  id         BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name       VARCHAR(100) NOT NULL,
  email      VARCHAR(100) NOT NULL,
  phone      VARCHAR(20),
  subject    VARCHAR(200),
  message    TEXT         NOT NULL,
  status     VARCHAR(20)  NOT NULL DEFAULT 'new' COMMENT 'new | read | replied',
  replied_by BIGINT UNSIGNED NULL,
  replied_at TIMESTAMP    NULL,
  reply      TEXT,
  created_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_status     (status),
  INDEX idx_created_at (created_at),
  FOREIGN KEY (replied_by) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
