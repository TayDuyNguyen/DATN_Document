# Test Cases

Thu muc nay dung de chuan bi test case cho cac man hinh va API cua du an DaNangTrip.

## Cau truc

| Thu muc | Noi dung |
| --- | --- |
| `01_guest_flows/` | Test case cho man hinh khach chua dang nhap. |
| `02_user_flows/` | Test case cho man hinh nguoi dung da dang nhap. |
| `03_admin_flows/` | Test case cho man hinh quan tri. |
| `04_api/` | Test case API va workflow backend. |

## Mau test case de xuat

Moi file nen theo format:

```md
# Ten man hinh / chuc nang

## Pham vi

- Route:
- API lien quan:
- Vai tro:

## Dieu kien truoc

- Tai khoan:
- Du lieu mau:
- Moi truong:

## Test cases

| TT | Test Case ID | Chuc nang | Mo ta Test Case | Dieu kien tien quyet | Buoc thuc hien | Du lieu test | Ket qua mong doi | Ket qua thuc te | Status | Ghi chu |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | TC_LOGIN_001 | Dang nhap | Dang nhap thanh cong | Tai khoan ton tai | 1. Mo man hinh<br>2. Nhap tai khoan<br>3. Nhan Dang nhap | admin@test.com / 123456 | Chuyen den Dashboard |  | Pass/Fail |  |

## Ghi chu

-
```

## Quy uoc cot

| Cot | Y nghia |
| --- | --- |
| `TT` | So thu tu test case trong file. |
| `Test Case ID` | Ma test case duy nhat, vi du `TC_LOGIN_001`, `TC_ADMIN_TOUR_001`. |
| `Chuc nang` | Ten chuc nang/man hinh can test. |
| `Mo ta Test Case` | Muc tieu kiem thu ngan gon. |
| `Dieu kien tien quyet` | Dieu kien can co truoc khi test. |
| `Buoc thuc hien` | Cac buoc thao tac theo thu tu. |
| `Du lieu test` | Tai khoan, input, file upload, request body hoac du lieu mau. |
| `Ket qua mong doi` | Ket qua dung theo nghiep vu/tai lieu. |
| `Ket qua thuc te` | Ket qua ghi nhan khi test that. |
| `Status` | `Pass`, `Fail`, `Blocked`, `Not Run`. |
| `Ghi chu` | Loi, link issue, anh chup man hinh hoac canh bao. |
