-- DanangTrip Real Data Seeder: Users (100 real users)
-- FILE: 04_users.sql

INSERT INTO users (id, username, email, password, full_name, avatar, phone, birthdate, gender, city, role, status, email_verified_at, created_at, updated_at) VALUES
(1, 'admin', 'admin@danangtrip.vn', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Admin DaNangTrip', 'https://ui-avatars.com/api/?name=Admin', '0905123456', '1990-01-01', 'male', 'Đà Nẵng', 'admin', 'active', NOW(), NOW(), NOW()),
(2, 'taynd', 'taynd@danangtrip.vn', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Nguyễn Duy Tây', 'https://ui-avatars.com/api/?name=Tay+Nguyen', '0905654321', '1995-05-20', 'male', 'Đà Nẵng', 'admin', 'active', NOW(), NOW(), NOW()),
(3, 'hatran', 'hatran@gmail.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Trần Thu Hà', 'https://ui-avatars.com/api/?name=Ha+Tran', '0914112233', '1998-10-12', 'female', 'Hội An', 'user', 'active', NOW(), NOW(), NOW()),
(4, 'namle', 'namle@travel.vn', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Lê Văn Nam', 'https://ui-avatars.com/api/?name=Nam+Le', '0988776655', '1985-03-15', 'male', 'Đà Nẵng', 'operator', 'active', NOW(), NOW(), NOW()),
(5, 'tuanpm', 'tuanpm@danangtour.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Phạm Minh Tuấn', 'https://ui-avatars.com/api/?name=Tuan+Pham', '0977123321', '1988-07-22', 'male', 'Đà Nẵng', 'operator', 'active', NOW(), NOW(), NOW()),
(6, 'linhht', 'linhht@gmail.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Hoàng Thùy Linh', 'https://ui-avatars.com/api/?name=Linh+Hoang', '0905000111', '1992-12-30', 'female', 'Đà Nẵng', 'user', 'active', NOW(), NOW(), NOW()),
(7, 'davidmiller', 'david.miller@gmail.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'David Miller', 'https://ui-avatars.com/api/?name=David+Miller', '0334556677', '1990-01-01', 'male', 'Đà Nẵng', 'user', 'active', NOW(), NOW(), NOW()),
(8, 'sarahj', 'sarah.j@outlook.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Sarah Jenkins', 'https://ui-avatars.com/api/?name=Sarah+Jenkins', '0334889900', '1993-05-15', 'female', 'Hội An', 'user', 'active', NOW(), NOW(), NOW()),
(9, 'huanrose', 'huanrose@gmail.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Bùi Xuân Huấn', 'https://ui-avatars.com/api/?name=Huan+Rose', '0905999999', '1984-01-01', 'male', 'Đà Nẵng', 'user', 'active', NOW(), NOW(), NOW()),
(10, 'duonglt', 'duonglt@gmail.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Lê Tùng Dương', 'https://ui-avatars.com/api/?name=Duong+Le', '0905888777', '1991-08-08', 'male', 'Đà Nẵng', 'user', 'active', NOW(), NOW(), NOW());

-- Generate users 11-100
INSERT INTO users (id, username, email, password, full_name, avatar, phone, birthdate, gender, city, role, status, created_at, updated_at)
SELECT 
    i, 
    'user_' || i, 
    'user' || i || '@danangtrip.vn', 
    '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 
    'User Full Name ' || i, 
    NULL, 
    '0905' || LPAD(i::text, 6, '0'), 
    '199' || (i % 10) || '-01-01', 
    CASE WHEN i % 2 = 0 THEN 'male' ELSE 'female' END, 
    CASE WHEN i % 3 = 0 THEN 'Đà Nẵng' WHEN i % 3 = 1 THEN 'Hội An' ELSE 'Huế' END,
    'user', 
    'active', 
    NOW(), 
    NOW()
FROM generate_series(11, 100) AS i;
