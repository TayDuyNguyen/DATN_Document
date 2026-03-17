-- ============================================================
-- DATABASE SCHEMA - WEBSITE DU LỊCH ĐÀ NẴNG "ĐÀ NẴNG TRIP"
-- Stack: Laravel 10.x + MySQL 8.0
-- Encoding: utf8mb4_unicode_ci
-- Tổng: 18 bảng
-- ============================================================

CREATE DATABASE IF NOT EXISTS danang_trip
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE danang_trip;

SET FOREIGN_KEY_CHECKS = 0;

-- ============================================================
-- BẢNG: users
-- Mục đích: Lưu thông tin tài khoản người dùng (User + Admin)
-- ============================================================
CREATE TABLE users (
  id                BIGINT UNSIGNED   NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  username          VARCHAR(50)       NOT NULL                COMMENT 'Tên đăng nhập, duy nhất trong hệ thống',
  email             VARCHAR(100)      NOT NULL                COMMENT 'Email đăng nhập, duy nhất',
  password          VARCHAR(255)      NOT NULL                COMMENT 'Mật khẩu đã hash bằng bcrypt',
  full_name         VARCHAR(100)      NULL                    COMMENT 'Họ tên đầy đủ hiển thị trên profile',
  avatar            VARCHAR(255)      NULL                    COMMENT 'URL ảnh đại diện lưu trên Cloudinary',
  phone             VARCHAR(20)       NULL                    COMMENT 'Số điện thoại liên hệ (không bắt buộc)',
  birthdate         DATE              NULL                    COMMENT 'Ngày sinh (không bắt buộc)',
  gender            VARCHAR(20)       NULL                    COMMENT 'Giới tính: male | female | other',
  city              VARCHAR(100)      NULL                    COMMENT 'Thành phố hiện tại của người dùng',
  point_balance     INT               NOT NULL DEFAULT 0      COMMENT 'Số dư point hiện tại, mặc định 0, có thể âm',
  role              VARCHAR(20)       NOT NULL DEFAULT 'user' COMMENT 'Vai trò: user | admin',
  status            VARCHAR(20)       NOT NULL DEFAULT 'active' COMMENT 'Trạng thái tài khoản: active | banned',
  email_verified_at TIMESTAMP         NULL                    COMMENT 'Thời điểm xác thực email, NULL nếu chưa xác thực',
  last_login_at     TIMESTAMP         NULL                    COMMENT 'Lần đăng nhập gần nhất',
  created_at        TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm tạo tài khoản',
  updated_at        TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Thời điểm cập nhật gần nhất',

  PRIMARY KEY (id),
  UNIQUE KEY uq_users_username (username),
  UNIQUE KEY uq_users_email (email),
  INDEX idx_users_status (status),
  INDEX idx_users_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Tài khoản người dùng và admin';


-- ============================================================
-- BẢNG: categories
-- Mục đích: Danh mục chính (Ăn uống | Khách sạn | Du lịch)
-- ============================================================
CREATE TABLE categories (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  name        VARCHAR(50)     NOT NULL                COMMENT 'Tên danh mục, ví dụ: Ăn uống, Khách sạn, Du lịch',
  slug        VARCHAR(60)     NOT NULL                COMMENT 'URL thân thiện, ví dụ: an-uong, khach-san',
  icon        VARCHAR(50)     NULL                    COMMENT 'Tên icon FontAwesome, ví dụ: fa-utensils',
  description TEXT            NULL                    COMMENT 'Mô tả ngắn về danh mục',
  image       VARCHAR(255)    NULL                    COMMENT 'URL ảnh đại diện danh mục',
  sort_order  INT             NOT NULL DEFAULT 0      COMMENT 'Thứ tự hiển thị trên trang chủ, số nhỏ hiển thị trước',
  status      VARCHAR(20)     NOT NULL DEFAULT 'active' COMMENT 'Trạng thái: active | inactive',
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm tạo',
  updated_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Thời điểm cập nhật',

  PRIMARY KEY (id),
  UNIQUE KEY uq_categories_slug (slug),
  INDEX idx_categories_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Danh mục chính của địa điểm';


-- ============================================================
-- BẢNG: subcategories
-- Mục đích: Danh mục con (Hải sản, Resort, Bãi biển...)
-- ============================================================
CREATE TABLE subcategories (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  category_id BIGINT UNSIGNED NOT NULL                COMMENT 'FK → categories.id, danh mục cha',
  name        VARCHAR(50)     NOT NULL                COMMENT 'Tên danh mục con, ví dụ: Hải sản, Resort',
  slug        VARCHAR(60)     NOT NULL                COMMENT 'URL thân thiện của danh mục con',
  description TEXT            NULL                    COMMENT 'Mô tả danh mục con',
  sort_order  INT             NOT NULL DEFAULT 0      COMMENT 'Thứ tự hiển thị trong danh mục cha',
  status      VARCHAR(20)     NOT NULL DEFAULT 'active' COMMENT 'Trạng thái: active | inactive',
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm tạo',
  updated_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Thời điểm cập nhật',

  PRIMARY KEY (id),
  UNIQUE KEY uq_subcategories_slug (slug),
  INDEX idx_subcategories_category (category_id),
  INDEX idx_subcategories_status (status),
  CONSTRAINT fk_subcategories_category FOREIGN KEY (category_id)
    REFERENCES categories (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Danh mục con của địa điểm';


-- ============================================================
-- BẢNG: locations (BẢNG TRUNG TÂM)
-- Mục đích: Địa điểm du lịch, ăn uống, khách sạn tại Đà Nẵng
-- Lưu ý: avg_rating và review_count tự cập nhật khi duyệt rating
-- ============================================================
CREATE TABLE locations (
  id                BIGINT UNSIGNED   NOT NULL AUTO_INCREMENT  COMMENT 'Khóa chính, tự tăng',
  name              VARCHAR(200)      NOT NULL                  COMMENT 'Tên địa điểm, ví dụ: Nhà hàng Bé Mặn',
  slug              VARCHAR(220)      NOT NULL                  COMMENT 'URL thân thiện, tự sinh từ name',
  category_id       BIGINT UNSIGNED   NOT NULL                  COMMENT 'FK → categories.id, danh mục chính (bắt buộc)',
  subcategory_id    BIGINT UNSIGNED   NULL                      COMMENT 'FK → subcategories.id, danh mục con (tùy chọn)',
  description       TEXT              NULL                      COMMENT 'Mô tả chi tiết về địa điểm',
  short_description VARCHAR(500)      NULL                      COMMENT 'Mô tả ngắn hiển thị trên card danh sách',
  address           VARCHAR(255)      NOT NULL                  COMMENT 'Địa chỉ đầy đủ, ví dụ: 123 Trần Phú',
  district          VARCHAR(50)       NOT NULL                  COMMENT 'Quận: Hải Châu | Sơn Trà | Ngũ Hành Sơn | Cẩm Lệ | Thanh Khê | Liên Chiểu',
  ward              VARCHAR(50)       NULL                      COMMENT 'Phường/Xã (tùy chọn)',
  latitude          DECIMAL(10,8)     NULL                      COMMENT 'Vĩ độ GPS, dùng cho Google Maps và tìm kiếm gần nhất',
  longitude         DECIMAL(11,8)     NULL                      COMMENT 'Kinh độ GPS, dùng cho Google Maps và tìm kiếm gần nhất',
  phone             VARCHAR(20)       NULL                      COMMENT 'Số điện thoại liên hệ của địa điểm',
  email             VARCHAR(100)      NULL                      COMMENT 'Email liên hệ của địa điểm',
  website           VARCHAR(255)      NULL                      COMMENT 'Website chính thức của địa điểm',
  opening_hours     JSON              NULL                      COMMENT 'Giờ mở cửa dạng JSON, ví dụ: {"mon":"08:00-22:00","sun":"closed"}',
  price_min         DECIMAL(12,0)     NULL                      COMMENT 'Giá thấp nhất (VNĐ), dùng để lọc theo khoảng giá',
  price_max         DECIMAL(12,0)     NULL                      COMMENT 'Giá cao nhất (VNĐ), dùng để lọc theo khoảng giá',
  price_level       TINYINT UNSIGNED  NULL                      COMMENT 'Mức giá tổng quát: 1=Rẻ, 2=Trung bình, 3=Cao, 4=Sang trọng',
  avg_rating        DECIMAL(3,2)      NOT NULL DEFAULT 0.00     COMMENT 'Điểm đánh giá trung bình (0.00-5.00), tự cập nhật khi duyệt rating',
  review_count      INT               NOT NULL DEFAULT 0        COMMENT 'Tổng số bài đánh giá đã được duyệt (approved)',
  view_count        INT               NOT NULL DEFAULT 0        COMMENT 'Tổng lượt xem trang chi tiết địa điểm',
  favorite_count    INT               NOT NULL DEFAULT 0        COMMENT 'Tổng số user đã thêm vào yêu thích',
  thumbnail         VARCHAR(255)      NULL                      COMMENT 'URL ảnh đại diện chính hiển thị trên card',
  images            JSON              NULL                      COMMENT 'Danh sách URL ảnh bổ sung dạng JSON array',
  video_url         VARCHAR(255)      NULL                      COMMENT 'URL video YouTube giới thiệu địa điểm',
  status            VARCHAR(20)       NOT NULL DEFAULT 'active' COMMENT 'Trạng thái: active | inactive (ẩn khỏi kết quả tìm kiếm)',
  is_featured       TINYINT(1)        NOT NULL DEFAULT 0        COMMENT '1 = địa điểm nổi bật, hiển thị trên trang chủ',
  created_by        BIGINT UNSIGNED   NULL                      COMMENT 'FK → users.id, admin đã tạo địa điểm này',
  created_at        TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm tạo',
  updated_at        TIMESTAMP         NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Thời điểm cập nhật',

  PRIMARY KEY (id),
  UNIQUE KEY uq_locations_slug (slug),
  INDEX idx_locations_category (category_id),
  INDEX idx_locations_subcategory (subcategory_id),
  INDEX idx_locations_district (district),
  INDEX idx_locations_status (status),
  INDEX idx_locations_featured (is_featured),
  INDEX idx_locations_avg_rating (avg_rating),
  INDEX idx_locations_view_count (view_count),
  CONSTRAINT fk_locations_category    FOREIGN KEY (category_id)    REFERENCES categories    (id) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT fk_locations_subcategory FOREIGN KEY (subcategory_id) REFERENCES subcategories (id) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT fk_locations_created_by  FOREIGN KEY (created_by)     REFERENCES users         (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Địa điểm du lịch, ăn uống, khách sạn tại Đà Nẵng';


-- ============================================================
-- BẢNG: tags
-- Mục đích: Nhãn mô tả đặc điểm địa điểm (view đẹp, giá rẻ...)
-- ============================================================
CREATE TABLE tags (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  name       VARCHAR(50)     NOT NULL                COMMENT 'Tên tag, ví dụ: View đẹp, Giá rẻ',
  slug       VARCHAR(60)     NOT NULL                COMMENT 'URL thân thiện của tag',
  type       VARCHAR(30)     NULL                    COMMENT 'Phân loại tag: cuisine | service | feature | atmosphere',
  created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm tạo',
  updated_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Thời điểm cập nhật',

  PRIMARY KEY (id),
  UNIQUE KEY uq_tags_name (name),
  UNIQUE KEY uq_tags_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Nhãn mô tả đặc điểm địa điểm';


-- ============================================================
-- BẢNG: location_tags (TRUNG GIAN)
-- Mục đích: Liên kết nhiều-nhiều giữa locations và tags
-- ============================================================
CREATE TABLE location_tags (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  location_id BIGINT UNSIGNED NOT NULL                COMMENT 'FK → locations.id',
  tag_id      BIGINT UNSIGNED NOT NULL                COMMENT 'FK → tags.id',
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm gán tag cho địa điểm',

  PRIMARY KEY (id),
  UNIQUE KEY uq_location_tag (location_id, tag_id),
  CONSTRAINT fk_location_tags_location FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_location_tags_tag      FOREIGN KEY (tag_id)      REFERENCES tags      (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Liên kết nhiều-nhiều giữa địa điểm và tag';


-- ============================================================
-- BẢNG: amenities
-- Mục đích: Tiện ích của địa điểm (WiFi, bãi đỗ xe, điều hòa...)
-- ============================================================
CREATE TABLE amenities (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  name       VARCHAR(50)     NOT NULL                COMMENT 'Tên tiện ích, ví dụ: WiFi miễn phí',
  icon       VARCHAR(50)     NULL                    COMMENT 'Tên icon hiển thị, ví dụ: fa-wifi',
  category   VARCHAR(30)     NULL                    COMMENT 'Nhóm tiện ích: connectivity | parking | comfort | payment',
  created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm tạo',
  updated_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Thời điểm cập nhật',

  PRIMARY KEY (id),
  UNIQUE KEY uq_amenities_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Tiện ích của địa điểm';


-- ============================================================
-- BẢNG: location_amenities (TRUNG GIAN)
-- Mục đích: Liên kết nhiều-nhiều giữa locations và amenities
-- ============================================================
CREATE TABLE location_amenities (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  location_id BIGINT UNSIGNED NOT NULL                COMMENT 'FK → locations.id',
  amenity_id  BIGINT UNSIGNED NOT NULL                COMMENT 'FK → amenities.id',
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm gán tiện ích cho địa điểm',

  PRIMARY KEY (id),
  UNIQUE KEY uq_location_amenity (location_id, amenity_id),
  CONSTRAINT fk_location_amenities_location FOREIGN KEY (location_id) REFERENCES locations  (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_location_amenities_amenity  FOREIGN KEY (amenity_id)  REFERENCES amenities  (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Liên kết nhiều-nhiều giữa địa điểm và tiện ích';


-- ============================================================
-- BẢNG: ratings (QUAN TRỌNG)
-- Mục đích: Bài đánh giá của user về địa điểm
-- Luồng: pending → approved (trừ point) | rejected (không trừ)
-- Ràng buộc: 1 user chỉ đánh giá 1 lần cho 1 địa điểm
-- ============================================================
CREATE TABLE ratings (
  id              BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT   COMMENT 'Khóa chính, tự tăng',
  user_id         BIGINT UNSIGNED  NOT NULL                  COMMENT 'FK → users.id, người viết đánh giá',
  location_id     BIGINT UNSIGNED  NOT NULL                  COMMENT 'FK → locations.id, địa điểm được đánh giá',
  score           TINYINT UNSIGNED NOT NULL                  COMMENT 'Số sao đánh giá từ 1 đến 5',
  comment         TEXT             NULL                      COMMENT 'Nội dung bình luận (có thể để trống)',
  image_count     TINYINT UNSIGNED NOT NULL DEFAULT 0        COMMENT 'Số ảnh đính kèm, tối đa 5 ảnh/bài',
  point_cost      INT              NOT NULL DEFAULT 0        COMMENT 'Số point bị trừ khi duyệt: 2 (không ảnh) | 3 (có ảnh)',
  status          VARCHAR(20)      NOT NULL DEFAULT 'pending' COMMENT 'Trạng thái duyệt: pending | approved | rejected',
  rejected_reason VARCHAR(255)     NULL                      COMMENT 'Lý do từ chối, chỉ có giá trị khi status=rejected',
  approved_by     BIGINT UNSIGNED  NULL                      COMMENT 'FK → users.id, admin đã duyệt/từ chối bài này',
  approved_at     TIMESTAMP        NULL                      COMMENT 'Thời điểm admin xử lý bài đánh giá',
  helpful_count   INT              NOT NULL DEFAULT 0        COMMENT 'Số lượt user đánh dấu bài này là hữu ích',
  created_at      TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm user gửi bài đánh giá',
  updated_at      TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Thời điểm chỉnh sửa (chỉ cho phép khi còn pending)',

  PRIMARY KEY (id),
  UNIQUE KEY uq_user_location_rating (user_id, location_id),
  INDEX idx_ratings_user (user_id),
  INDEX idx_ratings_location (location_id),
  INDEX idx_ratings_status (status),
  INDEX idx_ratings_created (created_at),
  INDEX idx_ratings_score (score),
  CONSTRAINT chk_ratings_score CHECK (score BETWEEN 1 AND 5),
  CONSTRAINT chk_ratings_image_count CHECK (image_count <= 5),
  CONSTRAINT fk_ratings_user     FOREIGN KEY (user_id)     REFERENCES users     (id) ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_ratings_location FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE CASCADE  ON UPDATE CASCADE,
  CONSTRAINT fk_ratings_approver FOREIGN KEY (approved_by) REFERENCES users     (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Bài đánh giá của user về địa điểm, qua quy trình kiểm duyệt';


-- ============================================================
-- BẢNG: rating_images
-- Mục đích: Ảnh đính kèm trong bài đánh giá (tối đa 5 ảnh/bài)
-- ============================================================
CREATE TABLE rating_images (
  id         BIGINT UNSIGNED  NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  rating_id  BIGINT UNSIGNED  NOT NULL                COMMENT 'FK → ratings.id, bài đánh giá chứa ảnh này',
  image_url  VARCHAR(255)     NOT NULL                COMMENT 'URL ảnh đã upload lên Cloudinary',
  sort_order TINYINT UNSIGNED NOT NULL DEFAULT 0      COMMENT 'Thứ tự hiển thị ảnh trong bài, bắt đầu từ 0',
  created_at TIMESTAMP        NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm upload ảnh',

  PRIMARY KEY (id),
  INDEX idx_rating_images_rating (rating_id),
  CONSTRAINT fk_rating_images_rating FOREIGN KEY (rating_id) REFERENCES ratings (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Ảnh đính kèm trong bài đánh giá';


-- ============================================================
-- BẢNG: favorites
-- Mục đích: Danh sách địa điểm yêu thích của user
-- ============================================================
CREATE TABLE favorites (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  user_id     BIGINT UNSIGNED NOT NULL                COMMENT 'FK → users.id, user đã lưu yêu thích',
  location_id BIGINT UNSIGNED NOT NULL                COMMENT 'FK → locations.id, địa điểm được lưu',
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm thêm vào yêu thích',

  PRIMARY KEY (id),
  UNIQUE KEY uq_user_location_fav (user_id, location_id),
  INDEX idx_favorites_location (location_id),
  CONSTRAINT fk_favorites_user     FOREIGN KEY (user_id)     REFERENCES users     (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_favorites_location FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Danh sách địa điểm yêu thích của user';


-- ============================================================
-- BẢNG: views
-- Mục đích: Ghi lại lượt xem trang chi tiết địa điểm
-- Lưu ý: Bảng tăng nhanh, nên định kỳ aggregate dữ liệu cũ
-- ============================================================
CREATE TABLE views (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  user_id     BIGINT UNSIGNED NULL                    COMMENT 'FK → users.id, NULL nếu là khách chưa đăng nhập',
  location_id BIGINT UNSIGNED NOT NULL                COMMENT 'FK → locations.id, địa điểm được xem',
  session_id  VARCHAR(100)    NULL                    COMMENT 'Session ID của trình duyệt, dùng để track guest',
  time_spent  INT             NOT NULL DEFAULT 0      COMMENT 'Thời gian xem trang (giây), dùng để đo mức độ quan tâm',
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm xem',

  PRIMARY KEY (id),
  INDEX idx_views_user (user_id),
  INDEX idx_views_location (location_id),
  INDEX idx_views_created (created_at),
  INDEX idx_views_session (session_id),
  CONSTRAINT fk_views_user     FOREIGN KEY (user_id)     REFERENCES users     (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_views_location FOREIGN KEY (location_id) REFERENCES locations (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Lượt xem trang chi tiết địa điểm, dùng cho thống kê và gợi ý';


-- ============================================================
-- BẢNG: point_transactions
-- Mục đích: Lịch sử thay đổi point của user (audit trail)
-- Loại: purchase | spend | bonus | refund
-- ============================================================
CREATE TABLE point_transactions (
  id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  user_id          BIGINT UNSIGNED NOT NULL                COMMENT 'FK → users.id, chủ sở hữu giao dịch',
  transaction_code VARCHAR(50)     NOT NULL                COMMENT 'Mã giao dịch duy nhất, dùng để tra cứu',
  type             VARCHAR(30)     NOT NULL                COMMENT 'Loại: purchase | spend | bonus | refund',
  amount           INT             NOT NULL                COMMENT 'Số point thay đổi: dương (+) khi nhận, âm (-) khi tiêu',
  balance_before   INT             NOT NULL                COMMENT 'Số dư point trước giao dịch, dùng để audit',
  balance_after    INT             NOT NULL                COMMENT 'Số dư point sau giao dịch, dùng để audit',
  reference_id     BIGINT UNSIGNED NULL                    COMMENT 'ID của đối tượng liên quan (rating_id, purchase_id...)',
  reference_type   VARCHAR(50)     NULL                    COMMENT 'Loại đối tượng liên quan: rating | purchase',
  description      VARCHAR(255)    NULL                    COMMENT 'Mô tả giao dịch, ví dụ: Duyệt bài đánh giá #123',
  payment_method   VARCHAR(30)     NULL                    COMMENT 'Phương thức nạp tiền (mô phỏng): momo | vnpay | bank',
  status           VARCHAR(20)     NOT NULL DEFAULT 'completed' COMMENT 'Trạng thái: pending | completed | failed',
  created_at       TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm giao dịch',

  PRIMARY KEY (id),
  UNIQUE KEY uq_transaction_code (transaction_code),
  INDEX idx_point_tx_user (user_id),
  INDEX idx_point_tx_created (created_at),
  INDEX idx_point_tx_reference (reference_id, reference_type),
  CONSTRAINT fk_point_transactions_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Lịch sử thay đổi point của user';


-- ============================================================
-- BẢNG: notifications
-- Mục đích: Thông báo hệ thống gửi đến user
-- Loại: rating_approved | rating_rejected | point_credited
-- ============================================================
CREATE TABLE notifications (
  id         BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  user_id    BIGINT UNSIGNED NOT NULL                COMMENT 'FK → users.id, người nhận thông báo',
  type       VARCHAR(30)     NOT NULL                COMMENT 'Loại thông báo: rating_approved | rating_rejected | point_credited',
  title      VARCHAR(255)    NOT NULL                COMMENT 'Tiêu đề thông báo hiển thị cho user',
  content    TEXT            NOT NULL                COMMENT 'Nội dung chi tiết thông báo',
  data       JSON            NULL                    COMMENT 'Dữ liệu bổ sung dạng JSON, ví dụ: {"rating_id":5}',
  is_read    TINYINT(1)      NOT NULL DEFAULT 0      COMMENT '0 = chưa đọc, 1 = đã đọc',
  read_at    TIMESTAMP       NULL                    COMMENT 'Thời điểm user đọc thông báo, NULL nếu chưa đọc',
  created_at TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm tạo thông báo',

  PRIMARY KEY (id),
  INDEX idx_notifications_user_read (user_id, is_read),
  INDEX idx_notifications_created (created_at),
  CONSTRAINT fk_notifications_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Thông báo hệ thống gửi đến user';


-- ============================================================
-- BẢNG: search_logs
-- Mục đích: Lịch sử tìm kiếm, dùng cho phân tích và gợi ý
-- ============================================================
CREATE TABLE search_logs (
  id            BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  user_id       BIGINT UNSIGNED NULL                    COMMENT 'FK → users.id, NULL nếu là khách chưa đăng nhập',
  session_id    VARCHAR(100)    NULL                    COMMENT 'Session ID để track hành vi guest',
  query         VARCHAR(255)    NOT NULL                COMMENT 'Từ khóa người dùng đã tìm kiếm',
  results_count INT             NOT NULL DEFAULT 0      COMMENT 'Số kết quả trả về, 0 = không tìm thấy',
  filters       JSON            NULL                    COMMENT 'Bộ lọc đã áp dụng dạng JSON',
  created_at    TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm tìm kiếm',

  PRIMARY KEY (id),
  INDEX idx_search_logs_user (user_id),
  INDEX idx_search_logs_query (query),
  INDEX idx_search_logs_created (created_at),
  INDEX idx_search_logs_session (session_id),
  CONSTRAINT fk_search_logs_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Lịch sử tìm kiếm, dùng cho phân tích từ khóa và hệ thống gợi ý';


-- ============================================================
-- BẢNG: blog_posts
-- Mục đích: Bài viết cẩm nang du lịch Đà Nẵng
-- ============================================================
CREATE TABLE blog_posts (
  id             BIGINT UNSIGNED NOT NULL AUTO_INCREMENT   COMMENT 'Khóa chính, tự tăng',
  title          VARCHAR(255)    NOT NULL                  COMMENT 'Tiêu đề bài viết',
  slug           VARCHAR(280)    NOT NULL                  COMMENT 'URL thân thiện, tự sinh từ title',
  excerpt        VARCHAR(500)    NULL                      COMMENT 'Tóm tắt ngắn hiển thị trên danh sách bài viết',
  content        LONGTEXT        NOT NULL                  COMMENT 'Nội dung đầy đủ bài viết (HTML hoặc Markdown)',
  featured_image VARCHAR(255)    NULL                      COMMENT 'URL ảnh bìa bài viết lưu trên Cloudinary',
  author_id      BIGINT UNSIGNED NOT NULL                  COMMENT 'FK → users.id, admin viết bài',
  view_count     INT             NOT NULL DEFAULT 0        COMMENT 'Tổng lượt xem bài viết',
  status         VARCHAR(20)     NOT NULL DEFAULT 'draft'  COMMENT 'Trạng thái: draft | published | archived',
  published_at   TIMESTAMP       NULL                      COMMENT 'Thời điểm xuất bản, NULL nếu còn là draft',
  created_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm tạo bài',
  updated_at     TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Thời điểm chỉnh sửa gần nhất',

  PRIMARY KEY (id),
  UNIQUE KEY uq_blog_posts_slug (slug),
  INDEX idx_blog_posts_author (author_id),
  INDEX idx_blog_posts_status (status),
  INDEX idx_blog_posts_published (published_at),
  CONSTRAINT fk_blog_posts_author FOREIGN KEY (author_id) REFERENCES users (id) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Bài viết cẩm nang du lịch Đà Nẵng';


-- ============================================================
-- BẢNG: blog_categories
-- Mục đích: Danh mục bài viết blog (tách biệt với categories địa điểm)
-- ============================================================
CREATE TABLE blog_categories (
  id          BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  name        VARCHAR(50)     NOT NULL                COMMENT 'Tên danh mục blog, ví dụ: Ẩm thực, Lưu trú',
  slug        VARCHAR(60)     NOT NULL                COMMENT 'URL thân thiện của danh mục blog',
  description TEXT            NULL                    COMMENT 'Mô tả danh mục blog',
  created_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'Thời điểm tạo',
  updated_at  TIMESTAMP       NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Thời điểm cập nhật',

  PRIMARY KEY (id),
  UNIQUE KEY uq_blog_categories_name (name),
  UNIQUE KEY uq_blog_categories_slug (slug)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Danh mục bài viết blog (tách biệt với categories địa điểm)';


-- ============================================================
-- BẢNG: blog_post_categories (TRUNG GIAN)
-- Mục đích: Liên kết nhiều-nhiều giữa blog_posts và blog_categories
-- ============================================================
CREATE TABLE blog_post_categories (
  id               BIGINT UNSIGNED NOT NULL AUTO_INCREMENT COMMENT 'Khóa chính, tự tăng',
  post_id          BIGINT UNSIGNED NOT NULL                COMMENT 'FK → blog_posts.id',
  blog_category_id BIGINT UNSIGNED NOT NULL                COMMENT 'FK → blog_categories.id',

  PRIMARY KEY (id),
  UNIQUE KEY uq_post_blog_category (post_id, blog_category_id),
  CONSTRAINT fk_blog_post_cat_post FOREIGN KEY (post_id)          REFERENCES blog_posts       (id) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT fk_blog_post_cat_cat  FOREIGN KEY (blog_category_id) REFERENCES blog_categories  (id) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
  COMMENT='Liên kết nhiều-nhiều giữa bài viết blog và danh mục blog';


SET FOREIGN_KEY_CHECKS = 1;


-- ============================================================
-- TRIGGER: Cập nhật avg_rating và review_count khi duyệt rating
-- ============================================================
DELIMITER //

CREATE TRIGGER trg_after_rating_approved
AFTER UPDATE ON ratings
FOR EACH ROW
BEGIN
  -- Khi admin duyệt bài (pending → approved)
  IF OLD.status != 'approved' AND NEW.status = 'approved' THEN
    UPDATE locations
    SET
      review_count = review_count + 1,
      avg_rating   = ROUND(
        (avg_rating * review_count + NEW.score) / (review_count + 1),
        2
      ),
      updated_at   = CURRENT_TIMESTAMP
    WHERE id = NEW.location_id;
  END IF;

  -- Khi admin thu hồi duyệt (approved → rejected/pending)
  IF OLD.status = 'approved' AND NEW.status != 'approved' THEN
    UPDATE locations
    SET
      review_count = GREATEST(review_count - 1, 0),
      avg_rating   = CASE
        WHEN review_count - 1 <= 0 THEN 0.00
        ELSE ROUND(
          (avg_rating * review_count - OLD.score) / (review_count - 1),
          2
        )
      END,
      updated_at   = CURRENT_TIMESTAMP
    WHERE id = NEW.location_id;
  END IF;
END//

-- ============================================================
-- TRIGGER: Cập nhật favorite_count khi thêm/xóa yêu thích
-- ============================================================
CREATE TRIGGER trg_after_favorite_insert
AFTER INSERT ON favorites
FOR EACH ROW
BEGIN
  UPDATE locations
  SET favorite_count = favorite_count + 1
  WHERE id = NEW.location_id;
END//

CREATE TRIGGER trg_after_favorite_delete
AFTER DELETE ON favorites
FOR EACH ROW
BEGIN
  UPDATE locations
  SET favorite_count = GREATEST(favorite_count - 1, 0)
  WHERE id = OLD.location_id;
END//

-- ============================================================
-- TRIGGER: Cập nhật view_count khi có lượt xem mới
-- ============================================================
CREATE TRIGGER trg_after_view_insert
AFTER INSERT ON views
FOR EACH ROW
BEGIN
  UPDATE locations
  SET view_count = view_count + 1
  WHERE id = NEW.location_id;
END//

DELIMITER ;
