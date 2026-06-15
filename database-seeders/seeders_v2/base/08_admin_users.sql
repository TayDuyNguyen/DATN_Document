BEGIN;
INSERT INTO "users" ("id", "username", "email", "password", "full_name", "avatar", "phone", "birthdate", "gender", "city", "role", "status", "email_verified_at", "last_login_at", "created_at", "updated_at") VALUES
(1, 'admin_tay', 'admin@danangtrip.vn', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Nguyen Duy Tay', NULL, '0905123456', NULL, NULL, NULL, 'admin', 'active', NULL, '2026-06-05 21:21:14', '2026-06-13 10:19:14', '2026-06-13 10:21:14'),
(2, 'operator_danang', 'operator@danangtrip.vn', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'Le Thi Thanh Thao', NULL, '0905654321', NULL, NULL, NULL, 'operator', 'active', NULL, '2026-05-30 02:21:14', '2026-06-13 10:19:14', '2026-06-13 10:21:14')
ON CONFLICT (id) DO UPDATE SET email = EXCLUDED.email, full_name = EXCLUDED.full_name, role = EXCLUDED.role, status = EXCLUDED.status, updated_at = NOW();

COMMIT;
