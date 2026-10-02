# -*- coding: utf-8 -*-
"""
config.py
=========
Cấu hình hệ thống bot tu tiên:
- Token và cài đặt kết nối Discord
- Công thức tính EXP và tỷ lệ đột phá theo từng cảnh giới (1 -> 106)
- Cấu hình thời gian chờ (cooldown) và phần thưởng tu luyện, lịch luyện, song tu
- Chỉ số chiến đấu (HP, ATK, DEF, SPEED)
- Vạn Bảo Các (Vật phẩm, Đan Dược, Pháp Bảo, Linh Thú)
- Danh sách Bí Cảnh Thám Hiểm
- Giao diện, màu sắc Embed và các biểu tượng tu tiên
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Tải cấu hình từ .env
load_dotenv()

DISCORD_TOKEN: str = os.getenv("DISCORD_TOKEN", "")
GUILD_ID: str = os.getenv("GUILD_ID", "").strip()

# Đường dẫn Database SQLite
BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "tu_tien.db"

# Thời gian cooldown (giây)
CULTIVATE_COOLDOWN_SECONDS: int = 300   # 5 phút tọa thiền
EXPLORE_COOLDOWN_SECONDS: int = 180     # 3 phút lịch luyện bí cảnh
DUEL_COOLDOWN_SECONDS: int = 180        # 3 phút tỷ thí đấu pháp
SONG_TU_COOLDOWN_SECONDS: int = 600     # 10 phút song tu đạo lữ

# Màu sắc Embed tiên hiệp
COLOR_DEFAULT = 0x1E88E5      # Xanh lam trầm mặc
COLOR_SUCCESS = 0x2ECC71      # Xanh ngọc đột phá thành công
COLOR_FAIL = 0xE74C3C         # Đỏ tẩu hỏa nhập ma
COLOR_GOLD = 0xF1C40F         # Vàng kim đan / bảo vật
COLOR_PURPLE = 0x9B59B6       # Tím huyền kiếp / đại năng
COLOR_CYAN = 0x1ABC9C         # Xanh bích ngọc
COLOR_ORANGE = 0xE67E22       # Cam chiến đấu

# Emoji tu tiên sinh động
EMOJI_YANG = "☯️"
EMOJI_EXP = "✨"
EMOJI_STONE = "💎"
EMOJI_FIRE = "🔥"
EMOJI_LIGHTNING = "⚡"
EMOJI_MEDAL = "🏅"
EMOJI_SWORD = "⚔️"
EMOJI_SHIELD = "🛡️"
EMOJI_HEART = "❤️"
EMOJI_PILL = "💊"
EMOJI_BEAST = "🐉"
EMOJI_TALISMAN = "📜"
EMOJI_LOTUS = "🪷"
EMOJI_TEMPLE = "⛩️"
EMOJI_BAG = "🎒"
EMOJI_SHOP = "🏪"
EMOJI_MAP = "🗺️"


# =============================================================================
# CÔNG THỨC TU VI & ĐỘT PHÁ
# =============================================================================

def get_required_exp(realm_id: int) -> int:
    """Tính lượng EXP cần thiết để có thể Đột Phá tại cảnh giới hiện tại."""
    if realm_id <= 0:
        return 100
    if realm_id >= 106:
        return 999_999_999

    # 1. Nhất Bộ Cảnh:
    if realm_id <= 15:
        return realm_id * 100
    if realm_id <= 19:
        step = realm_id - 16
        return 2500 + step * 1000
    if realm_id <= 23:
        step = realm_id - 20
        return 8000 + step * 3000
    if realm_id <= 27:
        step = realm_id - 24
        return 25000 + step * 10000
    if realm_id <= 31:
        step = realm_id - 28
        return 80000 + step * 30000
    if realm_id <= 34:
        step = realm_id - 32
        return 250000 + step * 100000
    if realm_id <= 38:
        step = realm_id - 35
        return 600000 + step * 200000
    if realm_id <= 42:
        step = realm_id - 39
        return 1600000 + step * 400000
    if realm_id <= 44:
        step = realm_id - 43
        return 3500000 + step * 1000000

    # 2. Nhị Bộ Cảnh (ID 45 -> 61):
    if realm_id <= 61:
        step = realm_id - 45
        return 6000000 + step * 1500000

    # 3. Tam Bộ Cảnh (ID 62 -> 101):
    if realm_id <= 101:
        step = realm_id - 62
        return 35000000 + step * 5000000

    # 4. Tứ Bộ Cảnh (ID 102 -> 105):
    step = realm_id - 102
    return 300000000 + step * 100000000


def get_breakthrough_rate(realm_id: int) -> float:
    """Tính tỷ lệ đột phá cơ bản (từ 0.05 đến 0.95)."""
    if realm_id >= 106:
        return 0.0
    if realm_id <= 5:
        return 0.95
    if realm_id <= 15:
        return 0.85
    if realm_id <= 19:
        return 0.75
    if realm_id <= 23:
        return 0.65
    if realm_id <= 27:
        return 0.55
    if realm_id <= 31:
        return 0.45
    if realm_id <= 34:
        return 0.40
    if realm_id <= 38:
        return 0.35
    if realm_id <= 44:
        return 0.30
    if realm_id <= 61:
        return 0.25
    if realm_id <= 70:
        return 0.20
    if realm_id <= 79:
        return 0.15
    if realm_id <= 101:
        return 0.10
    return 0.05


def get_cultivate_reward(realm_id: int) -> tuple[int, int]:
    """Tính lượng EXP và Linh Thạch khi tọa thiền."""
    factor = max(1, realm_id // 5 + 1)
    base_exp = 30 + factor * 15
    base_stone = 5 + factor * 3
    return base_exp, base_stone


def render_progress_bar(current: int, total: int, length: int = 10) -> str:
    """Tạo thanh tiến trình trực quan dạng văn bản."""
    if total <= 0:
        return "░" * length + " 0%"
    progress = min(1.0, max(0.0, current / total))
    filled = int(round(length * progress))
    empty = length - filled
    percent = int(progress * 100)
    return f"`[{'█' * filled}{'░' * empty}]` **{percent}%**"


# =============================================================================
# CHỈ SỐ CHIẾN ĐẤU (COMBAT STATS)
# =============================================================================

def get_combat_stats(realm_id: int, phap_bao_id: int = None, linh_thu_id: int = None) -> dict:
    """
    Tính toàn bộ chỉ số chiến đấu của tu sĩ dựa trên cảnh giới và trang bị.
    """
    max_hp = 100 + realm_id * 60
    atk = 15 + realm_id * 18
    defense = 8 + realm_id * 10
    speed = 10 + realm_id * 2

    # Bonus từ Pháp Bảo (Tăng mạnh ATK)
    if phap_bao_id:
        # Mỗi bậc pháp bảo cộng thêm 30 ATK
        atk += phap_bao_id * 35

    # Bonus từ Linh Thú (Tăng HP & DEF)
    if linh_thu_id:
        max_hp += linh_thu_id * 150
        defense += linh_thu_id * 25

    return {
        "max_hp": max_hp,
        "atk": atk,
        "def": defense,
        "speed": speed,
    }


# =============================================================================
# VẠN BẢO CÁC (DANH MỤC CỬA HÀNG)
# =============================================================================

SHOP_ITEMS = {
    # 1. Đan Dược
    "tu_khi_dan": {
        "name": "Tụ Khí Đan",
        "type": "dan_duoc",
        "category": "consumable",
        "price": 150,
        "description": "Linh đan ngưng tụ khí tức thiên địa. Tăng ngay +500 Tu Vi.",
        "effect": {"type": "add_exp", "value": 500}
    },
    "truc_co_dan": {
        "name": "Trúc Cơ Đan",
        "type": "dan_duoc",
        "category": "consumable",
        "price": 800,
        "description": "Đan dược thượng phẩm tẩy kinh phạt tủy. Tăng +15% tỷ lệ đột phá lần tới.",
        "effect": {"type": "breakthrough_buff", "value": 0.15}
    },
    "kim_nguyen_dan": {
        "name": "Kim Nguyên Đan",
        "type": "dan_duoc",
        "category": "consumable",
        "price": 2500,
        "description": "Linh đan quý giá ngưng tụ kim đan. Tăng ngay +5,000 Tu Vi và +20% tỷ lệ đột phá.",
        "effect": {"type": "add_exp_and_buff", "exp": 5000, "buff": 0.20}
    },
    "hoan_hon_dan": {
        "name": "Cửu Chuyển Hoàn Hồn Đan",
        "type": "dan_duoc",
        "category": "consumable",
        "price": 300,
        "description": "Linh đan thần diệu trị thương. Lập tức hồi phục đầy 100% Khí Huyết (HP).",
        "effect": {"type": "heal_full", "value": 1.0}
    },

    # 2. Pháp Bảo (Trang bị vũ khí)
    "thanh_phong_kiem": {
        "name": "Thanh Phong Kiếm (Pháp Khí - Hạ Phẩm)",
        "type": "phap_bao",
        "category": "equipment",
        "item_id": 1,  # ID trong canh_gioi_phap_bao
        "price": 500,
        "description": "Phi kiếm thanh thoát nhanh như gió thoảng. Gia tăng +35 Công Kích.",
    },
    "tu_dien_thuong": {
        "name": "Tử Điện Thương (Pháp Khí - Thượng Phẩm)",
        "type": "phap_bao",
        "category": "equipment",
        "item_id": 3,
        "price": 2000,
        "description": "Trường thương lôi điện bao quanh. Gia tăng +105 Công Kích.",
    },
    "son_ha_dinh": {
        "name": "Sơn Hà Đỉnh (Bảo Khí - Trung Phẩm)",
        "type": "phap_bao",
        "category": "equipment",
        "item_id": 6,
        "price": 8000,
        "description": "Bảo đỉnh trấn áp sơn hà đại hải. Gia tăng +210 Công Kích.",
    },

    # 3. Linh Thú (Trang bị thủ hộ)
    "thanh_duy_ho": {
        "name": "Thanh Dực Hổ (Linh Thú - Hạ Phẩm)",
        "type": "linh_thu",
        "category": "pet",
        "item_id": 1,  # ID trong canh_gioi_linh_thu
        "price": 1000,
        "description": "Linh hổ có cánh xanh biếc, trung thành hộ chủ. Tăng +150 Khí Huyết, +25 Phòng Ngự.",
    },
    "hoa_lan_dieu": {
        "name": "Hỏa Lân Điêu (Linh Thú - Thượng Phẩm)",
        "type": "linh_thu",
        "category": "pet",
        "item_id": 3,
        "price": 5000,
        "description": "Linh điêu mang vảy rồng bốc lửa. Tăng +450 Khí Huyết, +75 Phòng Ngự.",
    },
}


# =============================================================================
# BÍ CẢNH THÁM HIỂM (BÍ CẢNH LỊCH LUYỆN)
# =============================================================================

BI_CANH_LIST = [
    {
        "id": "u_minh",
        "name": "U Minh Sơn Mạch",
        "min_realm": 1,
        "description": "Dãy núi sương mù bao phủ quanh năm, thích hợp cho tu sĩ Ngưng Khí rèn luyện.",
        "monster_name": "U Hồn Sói Xám",
        "exp_range": (60, 150),
        "stone_range": (15, 40),
    },
    {
        "id": "van_kiem",
        "name": "Vạn Kiếm Cổ Trủng",
        "min_realm": 16,
        "description": "Di tích vạn thanh tàn kiếm của kiếm tông cổ đại, sát khí lẫm liệt.",
        "monster_name": "Kiếm Linh Tàn Phách",
        "exp_range": (200, 500),
        "stone_range": (50, 150),
    },
    {
        "id": "hoa_than",
        "name": "Hóa Thần Cấm Địa",
        "min_realm": 28,
        "description": "Khu vực cấm kỵ ẩn chứa ý cảnh thiên đạo của các bậc Hóa Thần đại năng.",
        "monster_name": "Ý Cảnh Huyết Ma",
        "exp_range": (800, 2000),
        "stone_range": (200, 600),
    },
    {
        "id": "co_than",
        "name": "Cổ Thần Chi Địa",
        "min_realm": 45,
        "description": "Chiến trường vẫn lạc của Cổ Thần bát tinh thời viễn cổ.",
        "monster_name": "Viễn Cổ Hư Ảnh",
        "exp_range": (5000, 15000),
        "stone_range": (1000, 3000),
    }
]
