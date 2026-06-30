# Admin — Quản lý Chatbot (Chatbot Hub)

**Route:** `/admin/chatbot`  
**Source:** `danangtrip-admin/src/pages/Chatbot/`  
**Tabs:** Dashboard · Logs · Settings (Cache & Parameters)  
**API:**
- `GET /admin/chatbot/stats`
- `GET /admin/chatbot/logs` — `page`, `search`, `intent`, `cache_hit`, `rating`
- `GET /admin/chatbot/cache`
- `DELETE /admin/chatbot/cache/:hash`
- `DELETE /admin/chatbot/cache` (clear all)
- `PUT /admin/settings` (cấu hình chatbot qua `settings.chatbot`)

---

## 1. Phạm vi

| Hạng mục | Chi tiết |
|----------|----------|
| Vai trò | **Admin** (`PrivateRoute`) |
| Cấu trúc | 1 route, 3 tab nội bộ (state `activeTab`, không đổi URL) |
| Tab Dashboard | KPI cards, biểu đồ kỹ thuật & nghiệp vụ, bảng unknown intents / negative feedbacks |
| Tab Logs | Filter + bảng lịch sử hội thoại + modal chi tiết log |
| Tab Settings | Quản lý semantic cache + form tham số chatbot (toggle, TTL, ngưỡng similarity) |

## 2. Điều kiện tiên quyết

- Admin đã đăng nhập · dev server `:5173`
- Dữ liệu mẫu: stats có KPI/trends/business; logs phân trang ≥2 trang; cache ≥3 entry
- Settings API trả `chatbot.enabled`, `clarification_attempt_limit`, `cache_ttl_seconds`, `cache.threshold_*`

## 3. Test cases — Auth & Navigation (P0)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_CHAT_001 | Guest `/admin/chatbot` → redirect `/login` | ✅ |
| TC_AD_CHAT_002 | User `role=user` → redirect `/login` | ✅ |
| TC_AD_CHAT_003 | Sidebar "Chatbot" → mở route, tab Dashboard mặc định active | ✅ |
| TC_AD_CHAT_004 | Breadcrumb hiển thị đúng title i18n | ✅ |
| TC_AD_CHAT_005 | Chuyển tab Logs → render LogsTab, Dashboard ẩn | ✅ |
| TC_AD_CHAT_006 | Chuyển tab Settings → render CacheSettingsTab | ✅ |
| TC_AD_CHAT_007 | Reload giữ tab active qua `?tab=` trên URL | ✅ |

## 4. Tab Dashboard — Load & KPI (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_CHAT_010 | Loading state: spinner + text `dashboard.loading` | ⏳ |
| TC_AD_CHAT_011 | API stats 500 → error card + nút "Thử lại" | ✅ |
| TC_AD_CHAT_012 | Click "Thử lại" → gọi lại `GET /stats` | ✅ |
| TC_AD_CHAT_013 | 5 KPI cards hiển thị: total messages, cache hit %, avg latency, LLM cost, system errors | ✅ |
| TC_AD_CHAT_014 | Giá trị KPI khớp mock/API response | ✅ |
| TC_AD_CHAT_015 | `system_errors > 0` → card errors có style cảnh báo (pulse/rose) | ✅ |
| TC_AD_CHAT_016 | Nút "Refresh data" refetch stats, disabled khi `isFetching` | ✅ |

## 5. Tab Dashboard — Biểu đồ kỹ thuật (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_CHAT_020 | Biểu đồ Latency trend render với data `trends.latency` | ✅ |
| TC_AD_CHAT_021 | Biểu đồ Cache efficiency (`trends.cacheRate`) | ⏳ |
| TC_AD_CHAT_022 | Biểu đồ LLM cost trend (`trends.cost`) | ⏳ |
| TC_AD_CHAT_023 | Biểu đồ Errors/failover bar chart (`trends.errors`) | ⏳ |
| TC_AD_CHAT_024 | Hover tooltip hiển thị giá trị trên chart | ⏳ |
| TC_AD_CHAT_025 | Trends rỗng → chart không crash, trục vẫn render | ⏳ |

## 6. Tab Dashboard — Business insights (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_CHAT_030 | Pie chart Intent distribution + legend dịch qua `intents.*` | ✅ |
| TC_AD_CHAT_031 | `intentDistribution` rỗng → empty state `no_intent_data` | ✅ |
| TC_AD_CHAT_032 | Bar chart Top destinations | ⏳ |
| TC_AD_CHAT_033 | Bar chart Top tours, tên dài truncate >15 ký tự | ⏳ |
| TC_AD_CHAT_034 | Clarification completion rate ring + số liệu sessions | ⏳ |
| TC_AD_CHAT_035 | Handoff info card hiển thị mô tả support | ⏳ |

## 7. Tab Dashboard — Bảng phản hồi (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_CHAT_040 | Bảng Unknown intents: cột Thời gian + Câu hỏi | ✅ |
| TC_AD_CHAT_041 | Unknown intents rỗng → empty state `no_unknown_intents` | ⏳ |
| TC_AD_CHAT_042 | Danh sách Negative feedbacks: intent badge, Q&A | ✅ |
| TC_AD_CHAT_043 | Negative feedbacks rỗng → empty state `no_negative_feedbacks` | ⏳ |
| TC_AD_CHAT_044 | Format datetime theo locale VI/EN | ⏳ |

## 8. Tab Logs — Filter & List (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_CHAT_050 | Load logs mặc định trang 1 | ✅ |
| TC_AD_CHAT_051 | Search keyword → API `search=` + reset page=1 | ✅ |
| TC_AD_CHAT_052 | Filter intent (tour/booking/unknown/...) → API `intent=` | ⏳ |
| TC_AD_CHAT_053 | Filter cache hit/miss → API `cache_hit=true/false` | ⏳ |
| TC_AD_CHAT_054 | Filter rating positive/negative → API `rating=` | ⏳ |
| TC_AD_CHAT_055 | Có filter active → hiện nút Reset, click xóa hết filter | ✅ |
| TC_AD_CHAT_056 | Loading / error / empty state logs | ✅ |
| TC_AD_CHAT_057 | Bảng cột: Thời gian, Intent, Câu hỏi, Nguồn, Latency, Rating, Chi tiết | ⏳ |
| TC_AD_CHAT_058 | Badge intent `unknown` (amber) vs `handoff` (rose) vs default (teal) | ✅ |
| TC_AD_CHAT_059 | Cache hit hiển thị dot teal; cache miss dot xám | ✅ |
| TC_AD_CHAT_060 | Rating positive/negative badge hoặc `-` nếu không có | ⏳ |

## 9. Tab Logs — Pagination & Modal (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_CHAT_065 | `last_page > 1` → pagination prev/next | ✅ |
| TC_AD_CHAT_066 | Prev disabled ở trang 1; Next disabled ở trang cuối | ✅ |
| TC_AD_CHAT_067 | Click nút Chi tiết → mở modal với session_id | ✅ |
| TC_AD_CHAT_068 | Modal hiển thị hội thoại KH + AI, metadata grid | ⏳ |
| TC_AD_CHAT_069 | Log có `session_slots` / `understanding` → hiển thị JSON | ⏳ |
| TC_AD_CHAT_070 | Log có `warnings` → guardrail alert amber | ✅ |
| TC_AD_CHAT_071 | Log có rating negative → banner phản hồi tiêu cực | ⏳ |
| TC_AD_CHAT_072 | Đóng modal bằng nút X | ✅ |
| TC_AD_CHAT_073 | Footer link "Cập nhật RAG" mở `/admin/blog-posts` tab mới | ✅ |

## 10. Tab Settings — Semantic Cache (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_CHAT_080 | Load danh sách cache từ `GET /admin/chatbot/cache` | ✅ |
| TC_AD_CHAT_081 | Loading cache → spinner | ⏳ |
| TC_AD_CHAT_082 | Cache rỗng → empty state `no_cache` | ⏳ |
| TC_AD_CHAT_083 | Search local filter theo `normalized_question` / `intent` | ✅ |
| TC_AD_CHAT_084 | Nút refresh cache refetch, icon spin khi fetching | ⏳ |
| TC_AD_CHAT_085 | Xóa 1 entry → confirm → `DELETE /cache/:hash` → list cập nhật | ✅ |
| TC_AD_CHAT_086 | Clear all → confirm → `DELETE /cache` → list trống | ⏳ |
| TC_AD_CHAT_087 | Nút Clear all chỉ hiện khi `caches.length > 0` | ✅ |
| TC_AD_CHAT_088 | Delete pending → nút disabled | ⏳ |

## 11. Tab Settings — Tham số Chatbot (P1)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_CHAT_090 | Load settings → form sync `enabled`, `clarification_limit`, `cache_ttl`, thresholds | ✅ |
| TC_AD_CHAT_091 | Settings API lỗi → banner error đỏ | ⏳ |
| TC_AD_CHAT_092 | Toggle bật/tắt chatbot (`enabled`) | ⏳ |
| TC_AD_CHAT_093 | `clarification_attempt_limit` min=1 max=5 | ⏳ |
| TC_AD_CHAT_094 | `cache_ttl_seconds` min=60 | ⏳ |
| TC_AD_CHAT_095 | Slider threshold transactional 0.80–1.00, step 0.01 | ⏳ |
| TC_AD_CHAT_096 | Slider threshold FAQ 0.80–1.00 | ⏳ |
| TC_AD_CHAT_097 | Submit form → `PUT /admin/settings` với payload `chatbot` đầy đủ | ✅ |
| TC_AD_CHAT_098 | Save thành công → toast success | ✅ |
| TC_AD_CHAT_099 | Save API lỗi → toast error, form giữ giá trị | ⏳ |
| TC_AD_CHAT_100 | Nút Save disabled khi `isSaving` | ⏳ |

## 12. Responsive & i18n (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| TC_AD_CHAT_110 | Mobile 375px: KPI grid 1 cột, charts resize | ⏳ |
| TC_AD_CHAT_111 | Logs filter stack dọc trên mobile | ⏳ |
| TC_AD_CHAT_112 | Settings layout 1 cột trên mobile, 3 cột trên xl | ⏳ |
| TC_AD_CHAT_113 | Đổi EN ↔ VI: tab labels, intent names, empty states | ⏳ |

## 13. API contract (P2)

| ID | Mô tả | Auto |
|----|--------|------|
| API_CHAT_001 | GET stats không auth → 401 | ✅ |
| API_CHAT_002 | GET stats admin → 200 + schema kpis/trends/business | ✅ |
| API_CHAT_003 | GET logs pagination params | ✅ |
| API_CHAT_004 | DELETE cache hash không tồn tại → 404 | ✅ |
| API_CHAT_005 | PUT settings chatbot invalid TTL → 422 | ⏳ |

---

## 14. Ghi chú kỹ thuật

- Tab state **không** sync URL — chuyển tab không tạo history entry riêng.
- Tab Settings dùng chung `useSettings` / `useUpdateSettings` với màn Settings chung; chỉ cập nhật block `chatbot`.
- Intent labels dùng namespace `chatbot` key `intents.*`.
- Charts dùng Recharts (`AreaChart`, `BarChart`, `PieChart`).
- Playwright: `npm run test:admin:chatbot` — POM `ChatbotPage.ts`, mock `chatbot.mock.ts` + `settings.mock.ts`, `data-testid="chatbot-hub"` / `chatbot-tab-*`.

## 15. Checklist regression

- Auth guest/non-admin
- Stats load + retry + refresh
- Logs filter + pagination + modal detail
- Cache CRUD + clear all confirm
- Save chatbot settings + toggle enabled

**Trạng thái automation:** **39 TC ✅** (32 UI + 3 auth + 4 API) · ~24 TC ⏳ backlog (charts tooltip, filter intent/cache/rating, responsive/i18n, API_005, …)
