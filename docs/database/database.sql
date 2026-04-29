-- DanangTrip PostgreSQL schema (aligned with Laravel migrations)
-- Source: d:/DATN/danangtrip-api/database/migrations

CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE users (
  id BIGSERIAL PRIMARY KEY,
  username VARCHAR(50) NOT NULL UNIQUE,
  email VARCHAR(100) NOT NULL UNIQUE,
  password VARCHAR(255) NOT NULL,
  full_name VARCHAR(100) NOT NULL,
  avatar VARCHAR(255),
  phone VARCHAR(20),
  birthdate DATE,
  gender VARCHAR(20),
  city VARCHAR(100),
  role VARCHAR(20) NOT NULL DEFAULT 'user',
  status VARCHAR(20) NOT NULL DEFAULT 'pending',
  email_verified_at TIMESTAMP NULL,
  last_login_at TIMESTAMP NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL
);
CREATE INDEX users_role_idx ON users(role);
CREATE INDEX users_status_idx ON users(status);

CREATE TABLE password_reset_tokens (
  email VARCHAR(255) PRIMARY KEY,
  token VARCHAR(255) NOT NULL,
  created_at TIMESTAMP NULL
);

CREATE TABLE sessions (
  id VARCHAR(255) PRIMARY KEY,
  user_id BIGINT NULL,
  ip_address VARCHAR(45),
  user_agent TEXT,
  payload TEXT NOT NULL,
  last_activity INTEGER NOT NULL
);
CREATE INDEX sessions_user_id_idx ON sessions(user_id);
CREATE INDEX sessions_last_activity_idx ON sessions(last_activity);

CREATE TABLE cache (
  key VARCHAR(255) PRIMARY KEY,
  value TEXT NOT NULL,
  expiration INTEGER NOT NULL
);
CREATE INDEX cache_expiration_idx ON cache(expiration);

CREATE TABLE cache_locks (
  key VARCHAR(255) PRIMARY KEY,
  owner VARCHAR(255) NOT NULL,
  expiration INTEGER NOT NULL
);
CREATE INDEX cache_locks_expiration_idx ON cache_locks(expiration);

CREATE TABLE jobs (
  id BIGSERIAL PRIMARY KEY,
  queue VARCHAR(255) NOT NULL,
  payload TEXT NOT NULL,
  attempts SMALLINT NOT NULL,
  reserved_at INTEGER NULL,
  available_at INTEGER NOT NULL,
  created_at INTEGER NOT NULL
);
CREATE INDEX jobs_queue_idx ON jobs(queue);

CREATE TABLE job_batches (
  id VARCHAR(255) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  total_jobs INTEGER NOT NULL,
  pending_jobs INTEGER NOT NULL,
  failed_jobs INTEGER NOT NULL,
  failed_job_ids TEXT NOT NULL,
  options TEXT NULL,
  cancelled_at INTEGER NULL,
  created_at INTEGER NOT NULL,
  finished_at INTEGER NULL
);

CREATE TABLE failed_jobs (
  id BIGSERIAL PRIMARY KEY,
  uuid VARCHAR(255) NOT NULL UNIQUE,
  connection TEXT NOT NULL,
  queue TEXT NOT NULL,
  payload TEXT NOT NULL,
  exception TEXT NOT NULL,
  failed_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  slug VARCHAR(60) NOT NULL UNIQUE,
  icon VARCHAR(50),
  description TEXT,
  image VARCHAR(255),
  sort_order INTEGER NOT NULL DEFAULT 0,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL
);
CREATE INDEX categories_status_idx ON categories(status);

CREATE TABLE subcategories (
  id BIGSERIAL PRIMARY KEY,
  category_id BIGINT NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
  name VARCHAR(50) NOT NULL,
  slug VARCHAR(60) NOT NULL UNIQUE,
  description TEXT,
  sort_order INTEGER NOT NULL DEFAULT 0,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL
);
CREATE INDEX subcategories_category_id_idx ON subcategories(category_id);
CREATE INDEX subcategories_status_idx ON subcategories(status);

CREATE TABLE tags (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  slug VARCHAR(60) NOT NULL UNIQUE,
  type VARCHAR(30) NOT NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL
);
CREATE INDEX tags_type_idx ON tags(type);

CREATE TABLE amenities (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  icon VARCHAR(50) NOT NULL,
  category VARCHAR(30) NOT NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL
);

CREATE TABLE locations (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  slug VARCHAR(220) NOT NULL UNIQUE,
  category_id BIGINT NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
  subcategory_id BIGINT NULL REFERENCES subcategories(id) ON DELETE SET NULL,
  description TEXT NOT NULL,
  short_description VARCHAR(500) NOT NULL,
  address VARCHAR(255) NOT NULL,
  district VARCHAR(50) NOT NULL,
  ward VARCHAR(50) NULL,
  latitude NUMERIC(10,8) NOT NULL,
  longitude NUMERIC(11,8) NOT NULL,
  phone VARCHAR(20) NULL,
  email VARCHAR(100) NULL,
  website VARCHAR(255) NULL,
  opening_hours JSON NULL,
  price_min NUMERIC(12,2) NULL,
  price_max NUMERIC(12,2) NULL,
  price_level SMALLINT NULL,
  avg_rating NUMERIC(3,2) NOT NULL DEFAULT 0,
  review_count INTEGER NOT NULL DEFAULT 0,
  view_count INTEGER NOT NULL DEFAULT 0,
  favorite_count INTEGER NOT NULL DEFAULT 0,
  thumbnail VARCHAR(255) NULL,
  images JSON NULL,
  video_url VARCHAR(255) NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  is_featured BOOLEAN NOT NULL DEFAULT FALSE,
  created_by BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL,
  CONSTRAINT locations_lat_chk CHECK (latitude BETWEEN -90 AND 90),
  CONSTRAINT locations_lng_chk CHECK (longitude BETWEEN -180 AND 180),
  CONSTRAINT locations_price_chk CHECK (
    (price_min IS NULL OR price_min >= 0) AND
    (price_max IS NULL OR price_max >= 0) AND
    (price_min IS NULL OR price_max IS NULL OR price_min <= price_max)
  )
);
CREATE INDEX locations_category_id_idx ON locations(category_id);
CREATE INDEX locations_subcategory_id_idx ON locations(subcategory_id);
CREATE INDEX locations_district_idx ON locations(district);
CREATE INDEX locations_avg_rating_idx ON locations(avg_rating);
CREATE INDEX locations_view_count_idx ON locations(view_count);
CREATE INDEX locations_status_idx ON locations(status);
CREATE INDEX locations_is_featured_idx ON locations(is_featured);
CREATE INDEX locations_search_fulltext ON locations USING GIN (to_tsvector('simple', coalesce(name,'') || ' ' || coalesce(address,'') || ' ' || coalesce(description,'') || ' ' || coalesce(short_description,'')));

CREATE TABLE location_tags (
  id BIGSERIAL PRIMARY KEY,
  location_id BIGINT NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
  tag_id BIGINT NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_location_tag UNIQUE(location_id, tag_id)
);
CREATE INDEX location_tags_created_at_idx ON location_tags(created_at);

CREATE TABLE location_amenities (
  id BIGSERIAL PRIMARY KEY,
  location_id BIGINT NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
  amenity_id BIGINT NOT NULL REFERENCES amenities(id) ON DELETE CASCADE,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT uq_location_amenity UNIQUE(location_id, amenity_id)
);
CREATE INDEX location_amenities_created_at_idx ON location_amenities(created_at);

CREATE TABLE search_logs (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  session_id VARCHAR(100) NOT NULL,
  query VARCHAR(255) NOT NULL,
  results_count INTEGER NOT NULL DEFAULT 0,
  filters JSON NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX search_logs_user_id_idx ON search_logs(user_id);
CREATE INDEX search_logs_session_id_idx ON search_logs(session_id);
CREATE INDEX search_logs_query_idx ON search_logs(query);
CREATE INDEX search_logs_created_at_idx ON search_logs(created_at);
CREATE INDEX search_logs_query_trgm_idx ON search_logs USING GIN (query gin_trgm_ops);
CREATE INDEX search_logs_filters_gin_idx ON search_logs USING GIN ((filters::jsonb) jsonb_path_ops);

CREATE TABLE notifications (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  type VARCHAR(30) NOT NULL,
  title VARCHAR(255) NOT NULL,
  content TEXT NOT NULL,
  data JSON NULL,
  is_read BOOLEAN NOT NULL DEFAULT FALSE,
  read_at TIMESTAMP NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX notifications_user_read_idx ON notifications(user_id, is_read);
CREATE INDEX notifications_created_at_idx ON notifications(created_at);

CREATE TABLE blog_categories (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  slug VARCHAR(60) NOT NULL UNIQUE,
  description TEXT NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL
);

CREATE TABLE blog_posts (
  id BIGSERIAL PRIMARY KEY,
  title VARCHAR(255) NOT NULL,
  slug VARCHAR(280) NOT NULL UNIQUE,
  excerpt VARCHAR(500) NULL,
  content TEXT NOT NULL,
  featured_image VARCHAR(255) NULL,
  author_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  view_count INTEGER NOT NULL DEFAULT 0,
  status VARCHAR(20) NOT NULL DEFAULT 'draft',
  published_at TIMESTAMP NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL
);
CREATE INDEX blog_posts_author_id_idx ON blog_posts(author_id);
CREATE INDEX blog_posts_status_idx ON blog_posts(status);
CREATE INDEX blog_posts_published_at_idx ON blog_posts(published_at);

CREATE TABLE blog_post_categories (
  id BIGSERIAL PRIMARY KEY,
  post_id BIGINT NOT NULL REFERENCES blog_posts(id) ON DELETE CASCADE,
  blog_category_id BIGINT NOT NULL REFERENCES blog_categories(id) ON DELETE CASCADE,
  CONSTRAINT uq_post_blog_category UNIQUE(post_id, blog_category_id)
);

CREATE TABLE tour_categories (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(50) NOT NULL UNIQUE,
  slug VARCHAR(60) NOT NULL UNIQUE,
  description TEXT NULL,
  icon VARCHAR(50) NULL,
  sort_order INTEGER NOT NULL DEFAULT 0 UNIQUE,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL
);
CREATE INDEX tour_categories_status_idx ON tour_categories(status);

CREATE TABLE tours (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  slug VARCHAR(220) NOT NULL UNIQUE,
  tour_category_id BIGINT NOT NULL REFERENCES tour_categories(id) ON DELETE RESTRICT,
  description TEXT NULL,
  short_desc VARCHAR(500) NULL,
  itinerary JSON NULL,
  inclusions JSON NULL,
  exclusions JSON NULL,
  price_adult NUMERIC(12,2) NOT NULL,
  price_child NUMERIC(12,2) NOT NULL DEFAULT 0,
  price_infant NUMERIC(12,2) NOT NULL DEFAULT 0,
  discount_percent INTEGER NOT NULL DEFAULT 0,
  duration VARCHAR(50) NULL,
  start_time VARCHAR(50) NULL,
  meeting_point VARCHAR(255) NULL,
  max_people INTEGER NOT NULL DEFAULT 0,
  min_people INTEGER NOT NULL DEFAULT 1,
  available_from DATE NULL,
  available_to DATE NULL,
  thumbnail VARCHAR(255) NULL,
  images JSON NULL,
  video_url VARCHAR(255) NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'active',
  booking_availability VARCHAR(20) NOT NULL DEFAULT 'open',
  is_featured BOOLEAN NOT NULL DEFAULT FALSE,
  is_hot BOOLEAN NOT NULL DEFAULT FALSE,
  view_count INTEGER NOT NULL DEFAULT 0,
  booking_count INTEGER NOT NULL DEFAULT 0,
  rating_count INTEGER NOT NULL DEFAULT 0,
  rating_avg NUMERIC(3,2) NOT NULL DEFAULT 0,
  created_by BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL,
  CONSTRAINT tours_people_chk CHECK (min_people >= 1 AND max_people >= 0 AND min_people <= max_people),
  CONSTRAINT tours_price_chk CHECK (price_adult >= 0 AND price_child >= 0 AND price_infant >= 0 AND discount_percent BETWEEN 0 AND 100),
  CONSTRAINT tours_booking_availability_chk CHECK (booking_availability IN ('open','sold_out'))
);
CREATE INDEX tours_price_adult_idx ON tours(price_adult);
CREATE INDEX tours_available_range_idx ON tours(available_from, available_to);
CREATE INDEX tours_status_idx ON tours(status);
CREATE INDEX tours_booking_availability_idx ON tours(booking_availability);
CREATE INDEX tours_is_featured_idx ON tours(is_featured);
CREATE INDEX tours_is_hot_idx ON tours(is_hot);
CREATE INDEX tours_rating_avg_idx ON tours(rating_avg);
CREATE INDEX tours_list_idx ON tours(status, booking_availability, tour_category_id, price_adult, created_at DESC);
CREATE INDEX tours_search_fulltext ON tours USING GIN (to_tsvector('simple', coalesce(name,'') || ' ' || coalesce(description,'') || ' ' || coalesce(itinerary::text,'') || ' ' || coalesce(inclusions::text,'') || ' ' || coalesce(exclusions::text,'')));

CREATE TABLE tour_schedules (
  id BIGSERIAL PRIMARY KEY,
  tour_id BIGINT NOT NULL REFERENCES tours(id) ON DELETE CASCADE,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  max_people INTEGER NOT NULL DEFAULT 0,
  booked_people INTEGER NOT NULL DEFAULT 0,
  price_adult NUMERIC(12,2) NULL,
  price_child NUMERIC(12,2) NULL,
  price_infant NUMERIC(12,2) NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'available',
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL,
  CONSTRAINT uq_tour_schedule UNIQUE(tour_id, start_date),
  CONSTRAINT tour_schedules_people_chk CHECK (max_people >= 0 AND booked_people >= 0 AND booked_people <= max_people)
);
CREATE INDEX tour_schedules_start_date_idx ON tour_schedules(start_date);
CREATE INDEX tour_schedules_status_idx ON tour_schedules(status);

CREATE TABLE bookings (
  id BIGSERIAL PRIMARY KEY,
  booking_code VARCHAR(20) NOT NULL UNIQUE,
  user_id BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  customer_name VARCHAR(100) NOT NULL,
  customer_email VARCHAR(100) NOT NULL,
  customer_phone VARCHAR(20) NOT NULL,
  customer_address TEXT NULL,
  customer_note TEXT NULL,
  total_amount NUMERIC(12,2) NOT NULL,
  discount_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
  final_amount NUMERIC(12,2) NOT NULL,
  deposit_amount NUMERIC(12,2) NOT NULL DEFAULT 0,
  payment_method VARCHAR(30) NOT NULL,
  payment_status VARCHAR(30) NOT NULL DEFAULT 'unpaid',
  booking_status VARCHAR(30) NOT NULL DEFAULT 'pending',
  cancellation_reason TEXT NULL,
  booked_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  confirmed_at TIMESTAMP NULL,
  cancelled_at TIMESTAMP NULL,
  completed_at TIMESTAMP NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL,
  CONSTRAINT bookings_amount_chk CHECK (total_amount >= 0 AND discount_amount >= 0 AND final_amount >= 0 AND deposit_amount >= 0),
  CONSTRAINT bookings_payment_status_chk CHECK (payment_status IN ('pending','success','failed','refunded','unpaid','partially_paid'))
);
CREATE INDEX bookings_booking_status_idx ON bookings(booking_status);
CREATE INDEX bookings_payment_status_idx ON bookings(payment_status);
CREATE INDEX bookings_booked_at_idx ON bookings(booked_at);
CREATE INDEX bookings_created_at_idx ON bookings(created_at);
CREATE INDEX bookings_user_id_idx ON bookings(user_id);
CREATE INDEX bookings_status_booked_idx ON bookings(booking_status, booked_at DESC);

CREATE TABLE booking_items (
  id BIGSERIAL PRIMARY KEY,
  booking_id BIGINT NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
  tour_id BIGINT NOT NULL REFERENCES tours(id) ON DELETE CASCADE,
  tour_schedule_id BIGINT NOT NULL REFERENCES tour_schedules(id) ON DELETE CASCADE,
  item_type VARCHAR(30) NOT NULL DEFAULT 'tour',
  item_name VARCHAR(200) NOT NULL,
  travel_date DATE NOT NULL,
  quantity_adult INTEGER NOT NULL DEFAULT 0,
  quantity_child INTEGER NOT NULL DEFAULT 0,
  quantity_infant INTEGER NOT NULL DEFAULT 0,
  unit_price_adult NUMERIC(12,0) NOT NULL,
  unit_price_child NUMERIC(12,0) NOT NULL,
  unit_price_infant NUMERIC(12,0) NOT NULL,
  subtotal NUMERIC(12,0) NOT NULL,
  status VARCHAR(30) NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL
);
CREATE INDEX booking_items_booking_tour_idx ON booking_items(booking_id, tour_id);
CREATE INDEX booking_items_travel_date_idx ON booking_items(travel_date);

CREATE TABLE payments (
  id BIGSERIAL PRIMARY KEY,
  booking_id BIGINT NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
  transaction_code VARCHAR(100) NOT NULL UNIQUE,
  amount NUMERIC(12,2) NOT NULL,
  payment_method VARCHAR(30) NOT NULL,
  payment_status VARCHAR(30) NOT NULL DEFAULT 'pending',
  payment_gateway VARCHAR(50) NULL,
  gateway_response JSON NULL,
  paid_at TIMESTAMP NULL,
  refunded_at TIMESTAMP NULL,
  refund_reason TEXT NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL,
  CONSTRAINT payments_status_chk CHECK (payment_status IN ('pending','success','failed','refunded')),
  CONSTRAINT payments_amount_chk CHECK (amount >= 0)
);
CREATE INDEX payments_payment_status_idx ON payments(payment_status);
CREATE INDEX payments_booking_id_idx ON payments(booking_id);
CREATE INDEX payments_payment_gateway_idx ON payments(payment_gateway);
CREATE INDEX payments_created_at_idx ON payments(created_at);
CREATE INDEX payments_paid_at_idx ON payments(paid_at);
CREATE INDEX payments_success_paid_idx ON payments(paid_at DESC, booking_id) WHERE payment_status = 'success' AND paid_at IS NOT NULL;

CREATE TABLE contacts (
  id BIGSERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  phone VARCHAR(20) NULL,
  subject VARCHAR(200) NULL,
  message TEXT NOT NULL,
  status VARCHAR(20) NOT NULL DEFAULT 'new',
  replied_by BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  replied_at TIMESTAMP NULL,
  reply TEXT NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL
);
CREATE INDEX contacts_status_idx ON contacts(status);

CREATE TABLE favorites (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  location_id BIGINT NULL REFERENCES locations(id) ON DELETE SET NULL,
  tour_id BIGINT NULL REFERENCES tours(id) ON DELETE SET NULL,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT favorites_exactly_one_target_chk CHECK (num_nonnulls(location_id, tour_id) = 1)
);
CREATE INDEX favorites_location_id_idx ON favorites(location_id);
CREATE INDEX favorites_tour_id_idx ON favorites(tour_id);
CREATE INDEX favorites_created_at_idx ON favorites(created_at);
CREATE UNIQUE INDEX favorites_user_location_unique ON favorites(user_id, location_id) WHERE location_id IS NOT NULL;
CREATE UNIQUE INDEX favorites_user_tour_unique ON favorites(user_id, tour_id) WHERE tour_id IS NOT NULL;

CREATE TABLE views (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  location_id BIGINT NULL REFERENCES locations(id) ON DELETE SET NULL,
  tour_id BIGINT NULL REFERENCES tours(id) ON DELETE SET NULL,
  session_id VARCHAR(100) NOT NULL,
  time_spent INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT views_exactly_one_target_chk CHECK (num_nonnulls(location_id, tour_id) = 1)
);
CREATE INDEX views_user_id_idx ON views(user_id);
CREATE INDEX views_location_id_idx ON views(location_id);
CREATE INDEX views_tour_id_idx ON views(tour_id);
CREATE INDEX views_session_id_idx ON views(session_id);
CREATE INDEX views_created_at_idx ON views(created_at);

CREATE TABLE ratings (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  location_id BIGINT NULL REFERENCES locations(id) ON DELETE CASCADE,
  tour_id BIGINT NULL REFERENCES tours(id) ON DELETE CASCADE,
  booking_id BIGINT NULL REFERENCES bookings(id) ON DELETE SET NULL,
  score SMALLINT NOT NULL,
  comment TEXT NULL,
  image_count SMALLINT NOT NULL DEFAULT 0,
  status VARCHAR(20) NOT NULL DEFAULT 'approved',
  rejected_reason VARCHAR(255) NULL,
  approved_by BIGINT NULL REFERENCES users(id) ON DELETE SET NULL,
  approved_at TIMESTAMP NULL,
  helpful_count INTEGER NOT NULL DEFAULT 0,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL,
  CONSTRAINT uq_user_location_rating UNIQUE(user_id, location_id),
  CONSTRAINT ratings_exactly_one_target_chk CHECK (num_nonnulls(location_id, tour_id, booking_id) = 1),
  CONSTRAINT ratings_score_chk CHECK (score BETWEEN 1 AND 5),
  CONSTRAINT ratings_image_count_chk CHECK (image_count >= 0)
);
CREATE INDEX ratings_created_at_idx ON ratings(created_at);
CREATE INDEX ratings_status_created_at_index ON ratings(status, created_at);
CREATE INDEX ratings_tour_status_created_at_idx ON ratings(tour_id, status, created_at);
CREATE INDEX ratings_location_status_created_idx ON ratings(location_id, status, created_at DESC);
CREATE UNIQUE INDEX ratings_user_tour_unique ON ratings(user_id, tour_id) WHERE tour_id IS NOT NULL;
CREATE UNIQUE INDEX ratings_user_booking_unique ON ratings(user_id, booking_id) WHERE booking_id IS NOT NULL;

CREATE TABLE rating_images (
  id BIGSERIAL PRIMARY KEY,
  rating_id BIGINT NOT NULL REFERENCES ratings(id) ON DELETE CASCADE,
  image_url VARCHAR(255) NOT NULL,
  sort_order SMALLINT NOT NULL DEFAULT 0,
  created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX rating_images_rating_id_idx ON rating_images(rating_id);
CREATE INDEX rating_images_created_at_idx ON rating_images(created_at);

CREATE TABLE refresh_tokens (
  id BIGSERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  token VARCHAR(64) NOT NULL UNIQUE,
  expires_at TIMESTAMP NOT NULL,
  used_at TIMESTAMP NULL,
  previous_token_id BIGINT NULL REFERENCES refresh_tokens(id) ON DELETE SET NULL,
  created_at TIMESTAMP NULL,
  updated_at TIMESTAMP NULL
);
CREATE INDEX refresh_tokens_user_created_idx ON refresh_tokens(user_id, created_at);
CREATE INDEX refresh_tokens_expires_idx ON refresh_tokens(expires_at);
CREATE INDEX refresh_tokens_used_idx ON refresh_tokens(used_at);

CREATE TABLE tour_locations (
  id BIGSERIAL PRIMARY KEY,
  tour_id BIGINT NOT NULL REFERENCES tours(id) ON DELETE CASCADE,
  location_id BIGINT NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
  created_at TIMESTAMP NULL,
  CONSTRAINT tour_locations_tour_location_unique UNIQUE(tour_id, location_id)
);
CREATE INDEX tour_locations_tour_id_idx ON tour_locations(tour_id);
CREATE INDEX tour_locations_location_id_idx ON tour_locations(location_id);
