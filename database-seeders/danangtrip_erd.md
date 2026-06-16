# DanangTrip — Sơ đồ Cơ sở Dữ liệu rút gọn (ERD 10 bảng cốt lõi)

> File DBML tương ứng để import vào **dbdiagram.io**: `danangtrip_erd_top10.dbml`

## Sơ đồ ERD (Mermaid — nhúng vào báo cáo)

```mermaid
erDiagram
    %% ===== NHÓM NGƯỜI DÙNG =====
    users {
        bigint   id PK
        varchar  username UK
        varchar  email    UK
        varchar  full_name
        varchar  role     "user|admin"
        varchar  status   "active|blocked|pending"
        timestamp created_at
    }

    %% ===== NHÓM ĐỊA ĐIỂM =====
    locations {
        bigint      id PK
        varchar     name
        varchar     slug UK
        bigint      category_id
        varchar     address
        varchar     district
        decimal     latitude
        decimal     longitude
        decimal     avg_rating
        varchar     status "active|inactive"
        boolean     is_featured
    }

    %% ===== NHÓM TOUR =====
    tours {
        bigint      id PK
        varchar     name
        varchar     slug UK
        bigint      tour_category_id
        decimal     price_adult
        decimal     price_child
        integer     discount_percent
        varchar     duration
        integer     max_people
        integer     min_people
        decimal     rating_avg
        varchar     status        "active|inactive"
        varchar     booking_availability "open|sold_out"
        boolean     is_featured
        boolean     is_hot
    }

    tour_schedules {
        bigint  id PK
        bigint  tour_id    FK
        date    start_date
        date    end_date
        integer max_people
        integer booked_people
        decimal price_adult "Override giá"
        varchar status     "available|full|cancelled"
    }

    %% ===== NHÓM ĐẶT TOUR & THANH TOÁN =====
    bookings {
        bigint      id PK
        varchar     booking_code UK
        bigint      user_id      FK
        bigint      promotion_id
        varchar     customer_name
        varchar     customer_email
        decimal     total_amount
        decimal     discount_amount
        decimal     final_amount
        varchar     payment_status  "unpaid|success|refunded"
        varchar     booking_status  "pending|confirmed|completed|cancelled"
        timestamp   booked_at
    }

    booking_items {
        bigint  id PK
        bigint  booking_id       FK
        bigint  tour_id          FK
        bigint  tour_schedule_id FK
        date    travel_date
        integer quantity_adult
        integer quantity_child
        decimal subtotal
    }

    payments {
        bigint  id PK
        bigint  booking_id       FK
        varchar transaction_code UK
        decimal amount
        varchar payment_method
        varchar payment_status  "pending|success|failed|refunded"
        varchar payment_gateway "sepay|..."
        timestamp paid_at
    }

    %% ===== NHÓM ĐÁNH GIÁ =====
    ratings {
        bigint  id PK
        bigint  user_id     FK
        bigint  location_id FK "nullable"
        bigint  tour_id     FK "nullable"
        bigint  booking_id  FK "nullable"
        tinyint score       "1-5"
        text    comment
        varchar status      "pending|approved|rejected"
        integer helpful_count
    }

    %% ===== NHÓM BLOG =====
    blog_posts {
        bigint  id PK
        varchar title
        varchar slug UK
        text    content
        bigint  author_id    FK
        varchar status       "draft|published"
        timestamp published_at
    }

    %% ===== NHÓM CHATBOT =====
    chat_knowledge_base {
        bigint  id PK
        varchar type           "tour|location|blog|policy"
        varchar title
        text    content
        bigint  reference_id   "FK logic"
        varchar reference_slug
        json    metadata       "Giá, rating, slug..."
        json    embedding      "Vector 768 chiều"
        boolean is_active
        timestamp last_embedded_at
    }

    %% ===== QUAN HỆ =====

    %% Người dùng
    users ||--o{ bookings          : "đặt"
    users ||--o{ ratings           : "đánh giá"
    users ||--o{ blog_posts        : "viết"

    %% Lịch tour
    tours     ||--o{ tour_schedules   : "có lịch"

    %% Đặt tour
    bookings      ||--o{ booking_items    : "gồm"
    bookings      ||--o{ payments         : "thanh toán"
    tours         ||--o{ booking_items    : "được đặt"
    tour_schedules||--o{ booking_items    : "theo lịch"

    %% Đánh giá
    locations     ||--o{ ratings         : "được đánh giá"
    tours         ||--o{ ratings         : "được đánh giá"
    bookings      ||--o{ ratings         : "sau đặt"
```

---

## Bảng tóm tắt các nhóm bảng cốt lõi (10 bảng)

| Nhóm                      | Bảng                                    | Vai trò                                                             |
| ------------------------- | --------------------------------------- | ------------------------------------------------------------------- |
| **Người dùng**            | `users`                                 | Tài khoản khách hàng và quản trị viên                               |
| **Địa điểm**              | `locations`                             | Quản lý thông tin điểm tham quan, ẩm thực, vui chơi tại Đà Nẵng     |
| **Tour**                  | `tours`, `tour_schedules`               | Quản lý sản phẩm tour du lịch và lịch khởi hành chi tiết            |
| **Đặt tour & Thanh toán** | `bookings`, `booking_items`, `payments` | Quản lý toàn bộ vòng đời giao dịch và trạng thái thanh toán         |
| **Đánh giá & Blog**       | `ratings`, `blog_posts`                 | Hệ thống phản hồi khách hàng và các bài viết cẩm nang du lịch (SEO) |
| **Chatbot AI**            | `chat_knowledge_base`                   | Cơ sở dữ liệu tri thức của chatbot phục vụ cho tính năng RAG        |

**Tổng cộng: 10 bảng quan trọng nhất của hệ thống** (đáp ứng trọn vẹn mô hình đặt tour, tìm kiếm địa điểm, và trợ lý chatbot AI).
