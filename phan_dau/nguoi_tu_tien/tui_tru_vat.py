# -*- coding: utf-8 -*-
"""
tui_tru_vat.py
==============
Hệ thống Túi Trữ Vật (Túi đồ của Người Tu Tiên) trong Chu Thiên Vạn Giới:
- Đóng vai trò là không gian nạp vật, cất giữ bảo bối, tài nguyên, pháp bảo, đan dược của người tu tiên.
- Quản lý phẩm cấp túi trữ vật (từ Túi Vải Sơ Cấp đến Tu Di Giới Chỉ, Hỗn Độn Không Gian).
- Phân loại vật phẩm theo danh mục chuyên biệt (Đan Dược, Pháp Bảo, Linh Thú, Phù Triện, Linh Thạch, Kỳ Vật).
- Cung cấp các tiện ích tính toán sức chứa, phân loại, sắp xếp và kiểm tra dung lượng túi đồ.
"""
from typing import Optional, Dict, Any, List, Tuple
from dataclasses import dataclass, field


# =============================================================================
# DANH MỤC PHÂN LOẠI VẬT PHẨM TRONG TÚI TRỮ VẬT
# =============================================================================
ITEM_CATEGORIES: Dict[str, Dict[str, Any]] = {
    "dan_duoc": {
        "key": "dan_duoc",
        "name": "Đan Dược",
        "icon": "💊",
        "description": "Linh đan diệu dược bồi bổ khí huyết, tăng trưởng tu vi hoặc đột phá cảnh giới.",
    },
    "phap_bao": {
        "key": "phap_bao",
        "name": "Pháp Bảo",
        "icon": "⚔️",
        "description": "Binh khí, pháp bảo công phòng gia tăng lực chiến và phòng thủ cho tu sĩ.",
    },
    "linh_thu": {
        "key": "linh_thu",
        "name": "Linh Thú",
        "icon": "🐉",
        "description": "Thần thú, yêu sủng hộ đạo đồng hành trong các trận chiến đấu pháp.",
    },
    "phu_trien": {
        "key": "phu_trien",
        "name": "Phù Triện",
        "icon": "📜",
        "description": "Linh phù phong ấn thần thông, độn thuật, phòng ngự lâm thời.",
    },
    "nguyen_lieu": {
        "key": "nguyen_lieu",
        "name": "Nguyên Liệu",
        "icon": "🌿",
        "description": "Khoáng thạch, linh thảo, yêu đan dùng để luyện đan, rèn bảo.",
    },
    "linh_thach": {
        "key": "linh_thach",
        "name": "Linh Thạch",
        "icon": "💎",
        "description": "Tiền tệ giao dịch phổ thông và nguồn năng lượng tu luyện trong tu chân giới.",
    },
    "ky_vat": {
        "key": "ky_vat",
        "name": "Kỳ Vật & Truyền Thừa",
        "icon": "🏺",
        "description": "Ngọc giản bí tịch, tàn đồ bí cảnh, cơ duyên viễn cổ đặc thù.",
    },
}

# =============================================================================
# CÁC BẬC PHẨM CẤP CỦA TÚI TRỮ VẬT
# =============================================================================
TUI_TRU_VAT_TIERS: List[Dict[str, Any]] = [
    {
        "tier": 1,
        "key": "tui_vai_so_cap",
        "name": "Túi Vải Sơ Cấp",
        "icon": "🎒",
        "max_slots": 15,
        "cost_linh_thach": 0,
        "required_realm": "Ngưng Khí Sơ Kỳ",
        "description": "Túi vải thô sơ chứa một chút phù chú không gian đơn sơ, dùng cho người mới bước vào tu đạo.",
    },
    {
        "tier": 2,
        "key": "tui_tru_vat_ha_pham",
        "name": "Túi Trữ Vật Hạ Phẩm",
        "icon": "👜",
        "max_slots": 30,
        "cost_linh_thach": 500,
        "required_realm": "Ngưng Khí Đỉnh Phong",
        "description": "Túi trữ vật tiêu chuẩn của đệ tử ngoại môn, không gian bên trong bằng một gian phòng nhỏ.",
    },
    {
        "tier": 3,
        "key": "tui_tru_vat_trung_pham",
        "name": "Túi Trữ Vật Trung Phẩm",
        "icon": "👝",
        "max_slots": 60,
        "cost_linh_thach": 2_000,
        "required_realm": "Trúc Cơ Sơ Kỳ",
        "description": "Chế tác từ da yêu thú Trúc Cơ, kết hợp trận pháp không gian bền vững.",
    },
    {
        "tier": 4,
        "key": "can_khon_dai",
        "name": "Càn Khôn Đại (Thượng Phẩm)",
        "icon": "👛",
        "max_slots": 120,
        "cost_linh_thach": 10_000,
        "required_realm": "Kết Đan Sơ Kỳ",
        "description": "Túi Càn Khôn thu nạp sơn hà, đệ tử nội môn hoặc chân truyền các đại phái mới đủ tư cách sở hữu.",
    },
    {
        "tier": 5,
        "key": "gioi_chi_tru_vat",
        "name": "Giới Chỉ Trữ Vật (Cực Phẩm)",
        "icon": "💍",
        "max_slots": 250,
        "cost_linh_thach": 50_000,
        "required_realm": "Nguyên Anh Sơ Kỳ",
        "description": "Nhẫn không gian khắc sâu cấm chế thần thức, chỉ có chủ nhân nhận chủ mới mở được.",
    },
    {
        "tier": 6,
        "key": "tu_di_gioi_chi",
        "name": "Tu Di Giới Chỉ (Tiên Phẩm)",
        "icon": "💎",
        "max_slots": 500,
        "cost_linh_thach": 200_000,
        "required_realm": "Hóa Thần Sơ Kỳ",
        "description": "Hạt cát Tu Di chứa càn khôn vô tận, bảo vật cấp bậc đại năng vấn đỉnh tinh không.",
    },
    {
        "tier": 7,
        "key": "hon_don_khong_gian",
        "name": "Hỗn Độn Không Gian (Thần Cấp)",
        "icon": "🌌",
        "max_slots": 9999,
        "cost_linh_thach": 1_000_000,
        "required_realm": "Đạp Thiên Sơ Kỳ",
        "description": "Khai mở một tiểu vũ trụ độc lập bên trong đan điền, dung lượng gần như vô cùng vô tận.",
    },
]

TIER_BY_LEVEL: Dict[int, Dict[str, Any]] = {t["tier"]: t for t in TUI_TRU_VAT_TIERS}
TIER_BY_KEY: Dict[str, Dict[str, Any]] = {t["key"]: t for t in TUI_TRU_VAT_TIERS}


# =============================================================================
# CÁC HÀM QUẢN LÝ TÚI TRỮ VẬT
# =============================================================================
def get_all_tiers() -> List[Dict[str, Any]]:
    """Trả về danh sách tất cả các phẩm cấp của Túi Trữ Vật."""
    return TUI_TRU_VAT_TIERS


def get_tier_by_level(tier_level: int) -> Optional[Dict[str, Any]]:
    """Tra cứu thông tin túi trữ vật theo cấp bậc (1 -> 7)."""
    return TIER_BY_LEVEL.get(tier_level)


def get_tier_by_key(key: str) -> Optional[Dict[str, Any]]:
    """Tra cứu túi trữ vật theo định danh key."""
    return TIER_BY_KEY.get(key.strip().lower())


def get_max_slots(tier_level: int) -> int:
    """Trả về số ô chứa tối đa theo cấp bậc túi."""
    tier_info = get_tier_by_level(tier_level)
    return tier_info["max_slots"] if tier_info else 15


def check_can_add_item(current_used_slots: int, tier_level: int, item_exists: bool = False) -> bool:
    """
    Kiểm tra túi còn chỗ chứa không.
    Nếu vật phẩm đã có trong túi (xếp chồng), không tốn thêm ô chứa.
    """
    if item_exists:
        return True
    return current_used_slots < get_max_slots(tier_level)


def detect_item_category(item_key: str) -> str:
    """
    Phân loại vật phẩm dựa trên tiền tố hoặc tên định danh key.
    """
    k = item_key.lower()
    if k.endswith("_dan") or "dan_" in k or "thuoc" in k:
        return "dan_duoc"
    if "phap_bao" in k or "kiem" in k or "thuẫn" in k or "giap" in k or "kinh" in k:
        return "phap_bao"
    if "linh_thu" in k or "yeu_thu" in k or "long" in k or "phuong" in k:
        return "linh_thu"
    if "phu" in k or "trien" in k:
        return "phu_trien"
    if "linh_thach" in k:
        return "linh_thach"
    if "khoang" in k or "thao" in k or "tinh_huyet" in k:
        return "nguyen_lieu"
    return "ky_vat"


@dataclass
class TuiTruVat:
    """
    Lớp biểu diễn Túi Trữ Vật của một Người Tu Tiên.
    Dùng để quản lý, sắp xếp và kiểm soát sức chứa trong runtime.
    """
    user_id: int
    tier_level: int = 1
    items: Dict[str, int] = field(default_factory=dict)

    @property
    def tier_info(self) -> Dict[str, Any]:
        return get_tier_by_level(self.tier_level) or TUI_TRU_VAT_TIERS[0]

    @property
    def max_slots(self) -> int:
        return self.tier_info["max_slots"]

    @property
    def used_slots(self) -> int:
        return len(self.items)

    @property
    def is_full(self) -> bool:
        return self.used_slots >= self.max_slots

    def add_item(self, item_key: str, quantity: int = 1) -> Tuple[bool, str]:
        """Thêm vật phẩm vào túi trữ vật."""
        if quantity <= 0:
            return False, "Số lượng vật phẩm phải lớn hơn 0."
        if item_key not in self.items and self.is_full:
            return False, f"Túi trữ vật đã đầy ({self.used_slots}/{self.max_slots} ô). Hãy nâng cấp túi hoặc dọn dẹp bớt đồ."

        self.items[item_key] = self.items.get(item_key, 0) + quantity
        return True, f"Đã cất {quantity}x {item_key} vào túi trữ vật."

    def remove_item(self, item_key: str, quantity: int = 1) -> Tuple[bool, str]:
        """Lấy bớt hoặc tiêu hao vật phẩm từ túi trữ vật."""
        if quantity <= 0:
            return False, "Số lượng vật phẩm phải lớn hơn 0."
        if item_key not in self.items or self.items[item_key] < quantity:
            return False, f"Số lượng {item_key} trong túi không đủ để sử dụng."

        self.items[item_key] -= quantity
        if self.items[item_key] <= 0:
            del self.items[item_key]
        return True, f"Đã lấy ra {quantity}x {item_key} từ túi trữ vật."

    def get_items_by_category(self, category_key: str) -> Dict[str, int]:
        """Lọc danh sách vật phẩm trong túi theo nhóm phân loại."""
        res = {}
        for k, v in self.items.items():
            if detect_item_category(k) == category_key:
                res[k] = v
        return res
