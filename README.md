# 🪷 Bot Tu Tiên Discord (Tiên Nghịch)

Bot Discord thể loại Tu Tiên hoàn chỉnh mô phỏng hành trình nghịch thiên tu hành, tích hợp trọn vẹn hệ thống cảnh giới chuẩn thế giới Tiên Nghịch (106 bậc Tu Vi, 13 bậc Pháp Bảo, 92 cấp Đan Dược, 8 bậc Phù Triện, 9 cấp Linh Thú), cùng gameplay nhập vai RPG phong phú (Tọa thiền, Đột phá, Vạn Bảo Các, Lịch luyện bí cảnh, Tỷ thí PvP, Song tu).

---

## ⚡ Các Tính Năng & Lệnh Slash Commands (14 Lệnh)

### ⛩️ 0. Trung Tâm Điều Khiển Chính (HUB)
* **`/menu`**: **[Khuyên dùng]** Mở Bảng Điều Khiển Tu Tiên tương tác trực quan với đầy đủ thanh trạng thái (Khí Huyết HP, Tu Vi EXP, Linh Thạch, Pháp Bảo, Linh Thú) và hệ thống nút bấm:
  * Nếu chưa có nhân vật: Hiện nút **"✨ Khai Mở Tiên Lộ"** mở bảng Modal popup nhập Đạo Hiệu trực tiếp.
  * Nếu đã có nhân vật: Hiện thanh Hub và các nút bấm nhanh: **[🧘 Tọa Thiền]**, **[⚡ Trùng Kích]**, **[🎒 Túi Đồ]**, **[🏪 Vạn Bảo Các]**, **[🗺️ Lịch Luyện]**, **[🏅 Thiên Kiêu Bảng]**, **[🔄 Làm Mới]**.

### 🌀 1. Tu Hành & Cảnh Giới
* **`/khoi_dau <dao_hieu>`**: Định danh đạo hiệu, khai mở tiên lộ, nhận linh thạch và khởi đầu tại *Ngưng Khí Tầng 1*.
* **`/ho_so [dao_huu]`**: Xem thẻ tu sĩ chi tiết: Đại/Tiểu Cảnh Giới, Khí Huyết (HP), Công Kích, Phòng Ngự, Pháp Bảo, Linh Thú, thanh tiến độ EXP, tỷ lệ đột phá (kèm buff đan dược), chiến tích PvP.
* **`/tu_luyen`**: Tọa thiền hấp thu linh khí (hồi 5 phút), xác suất kích hoạt **Tiểu Ngộ Đạo (x1.5 EXP)** hoặc **Đại Ngộ Đạo (x2.2 EXP)**.
* **`/dot_pha`**: Trùng kích phá vỡ bình cảnh:
  * Thành công: Thăng cấp cảnh giới mới kèm **Thiên Địa Dị Tượng** (Tử khí đông lai 3 vạn dặm).
  * Thất bại: Tẩu hỏa nhập ma, tổn hao một lượng chân khí.
* **`/bang_xep_hang`**: Bảng vàng Thiên Kiêu vinh danh Top 10 đại năng tu vi cao nhất.
* **`/tra_cuu <he_thong> [tu_khoa]`**: Tra cứu danh bạ cảnh giới (Tu Vi 106 bậc, Pháp Bảo 13 bậc, Đan Dược 92 cấp, Phù Triện 8 bậc, Linh Thú 9 cấp).

### 🏪 2. Vạn Bảo Các & Túi Trữ Vật
* **`/van_bao_cac`**: Xem danh mục đan dược thần hiệu (Tụ Khí Đan, Trúc Cơ Đan, Kim Nguyên Đan, Cửu Chuyển Hoàn Hồn Đan), Pháp Bảo và Linh Thú hộ thân.
* **`/mua <vat_pham> [so_luong]`**: Mua vật phẩm bằng Linh Thạch (hỗ trợ autocomplete).
* **`/tui_do`**: Mở túi trữ vật kiểm tra số lượng đan dược, bảo vật sở hữu.
* **`/su_dung <dan_duoc>`**: Uống đan dược để hồi phục toàn bộ Khí Huyết, tăng vọt EXP hoặc gia tăng tỷ lệ Đột Phá cho lần kế tiếp.
* **`/trang_bi <vat_pham>`**: Trang bị Pháp Bảo tăng Công Kích hoặc Linh Thú tăng Khí Huyết/Phòng Ngự.

### 🗺️ 3. Lịch Luyện, Đấu Pháp & Đạo Lữ
* **`/lich_luyen <bi_canh>`**: Thám hiểm các bí cảnh cổ đại (*U Minh Sơn Mạch*, *Vạn Kiếm Cổ Trủng*, *Hóa Thần Cấm Địa*, *Cổ Thần Chi Địa*). Trảm sát yêu thú nhận lượng lớn EXP, Linh Thạch và xác suất nhặt được Đan Dược/Kỳ Bảo.
* **`/dau_phap @daohuu`**: Tỷ thí luận đạo so tài chiến lực PvP giữa 2 tu sĩ tại Luận Đạo Đài, người thắng nhận thưởng Linh Thạch và ghi danh chiến tích.
* **`/song_tu @daohuu`**: Mời đạo hữu cùng nhau vận chuyển đại chu thiên, nhận gấp 1.8 lần EXP và Linh Thạch so với tọa thiền đơn độc.

---

## 🚀 Hướng Dẫn Cài Đặt & Chạy Bot

### 1. Cài đặt thư viện
```powershell
pip install -r requirements.txt
```

### 2. Cấu hình Bot Discord
1. Truy cập [Discord Developer Portal](https://discord.com/developers/applications).
2. Tạo mới Application ➔ Vào tab **Bot** ➔ Click **Reset Token** để copy Token.
3. Mở file `.env` và dán token:
```env
DISCORD_TOKEN=your_discord_bot_token_here
GUILD_ID=   # (Tùy chọn: ID server Discord để đồng bộ lệnh tức thì)
```
4. Vào tab **OAuth2** -> **URL Generator**:
   * Scopes: chọn `bot` và `applications.commands`.
   * Bot Permissions: chọn `Send Messages`, `Embed Links`, `Read Message History`, `Use Slash Commands`.
   * Copy link dán vào trình duyệt để mời bot vào máy chủ.

### 3. Khởi chạy Bot
```powershell
python bot.py
```

---

## 📂 Cấu Trúc Dự Án

```
bot-tu-tien/
├── phan_dau/                  # Thư viện hệ thống cơ sở (Phần Đầu)
│   ├── canh_gioi_chung/       # Thư viện hệ thống cảnh giới chuẩn Tiên Nghịch
│   │   ├── canh_gioi_tu_vi.py     # 83 bậc tu vi (từ Ngưng Khí đến Vô Cảnh)
│   │   ├── canh_gioi_phap_bao.py  # 13 bậc pháp bảo
│   │   ├── canh_gioi_dan_duoc.py  # Phẩm cấp đan dược (Phàm, Linh, Tiên Đan)
│   │   ├── canh_gioi_phu_trien.py # 8 bậc phù triện
│   │   ├── canh_gioi_linh_thu.py  # 9 cấp linh thú
│   │   └── __init__.py
│   ├── dan_duoc/              # Danh mục 56 loại đan dược trong thế giới Tu Tiên
│   │   ├── tat_ca_dan_duoc.py     # Dữ liệu & hàm tra cứu đan dược
│   │   ├── tat_ca_dan_duoc.md     # Tài liệu tra cứu chi tiết
│   │   ├── tat_ca_dan_duoc.json   # Dữ liệu JSON chuẩn hóa
│   │   └── __init__.py
│   ├── nguoi_tu_tien/         # Hệ thống định hình bản thể & thuộc tính người tu tiên
│   │   ├── toc.py                 # 8 Chủng Tộc (Chính Đạo & Ma Đạo)
│   │   ├── linh_can.py            # 10 Linh Căn (Chính Đạo & Ma Đạo)
│   │   ├── tui_tru_vat.py         # Quản lý túi trữ vật & phân loại đồ
│   │   ├── chi_so.py              # 14 Chỉ số (Cơ bản, Chiến đấu, Ẩn)
│   │   └── __init__.py
│   ├── tai_nguyen/            # Hệ thống tiền tệ & tài nguyên tu tiên
│   │   ├── linh_thach.py          # Tiền tệ cơ bản (Hạ - Trung - Thượng - Cực phẩm)
│   │   ├── tien_thach.py          # Tiền tệ cao cấp (từ Vấn Đỉnh / Nhị Bộ Cảnh)
│   │   ├── diem_cong_hien.py      # Điểm cống hiến Tông Môn đổi công pháp & vật phẩm
│   │   └── __init__.py
│   └── cong_phap/             # Hệ thống Công Pháp, Thần Thông & Thân Pháp
│       ├── cong_phap.py           # Công Pháp Chủ Tu (Passive Engine & Cộng hưởng hệ)
│       ├── than_thong.py          # Thần Thông (Active Skills: Đơn thể, AoE, CC, Shield)
│       ├── than_phap.py           # Thân Pháp & Độn Thuật (Tiên thủ, Né tránh, Escape)
│       └── __init__.py
├── cogs/
│   ├── tu_tien.py             # Lệnh cốt lõi (/khoi_dau, /ho_so, /tu_luyen, /dot_pha, /bang_xep_hang)
│   ├── tra_cuu.py             # Lệnh tra cứu từ điển (/tra_cuu)
│   ├── van_bao_cac.py         # Lệnh mua sắm & túi đồ (/van_bao_cac, /mua, /tui_do, /su_dung, /trang_bi)
│   └── lich_luyen.py          # Lịch luyện & PvP (/lich_luyen, /dau_phap, /song_tu)
├── bot.py                     # Entry point khởi chạy bot và sync Slash Commands
├── config.py                  # Cấu hình chỉ số chiến đấu, bí cảnh, cửa hàng, công thức EXP
├── database.py                # Quản lý SQLite bất đồng bộ (aiosqlite)
├── requirements.txt           # Dependencies
└── .env                       # Token bí mật
```