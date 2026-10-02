# -*- coding: utf-8 -*-
"""
tien_thach.py
=============
Hệ thống Tiên Thạch (Tiên Ngọc) - Tiền tệ cao cấp trong Chu Thiên Vạn Giới:
- Chỉ dành riêng cho tu sĩ đạt từ Vấn Đỉnh Cảnh (cuối Nhất Bộ) hoặc Nhị Bộ Cảnh (Khuy Niết, Tịnh Niết, Toái Niết) trở lên.
- Ngưng tụ từ Tiên Khí thuần khiết của Tiên Giới viễn cổ, vượt xa Linh Thạch phàm tục.
- Hệ thống quy đổi đồng bộ theo bậc cấp số nhân 1,000:
  * 1,000 Cực Phẩm Linh Thạch = 1 Hạ Phẩm Tiên Thạch
  * 1,000 Hạ Phẩm Tiên Thạch = 1 Trung Phẩm Tiên Thạch
  * 1,000 Trung Phẩm Tiên Thạch = 1 Thượng Phẩm Tiên Thạch
  * 1,000 Thượng Phẩm Tiên Thạch = 1 Cực Phẩm Tiên Thạch (Chí Tôn Tiên Tinh)

Chia làm 4 phẩm cấp:
1. Hạ Phẩm Tiên Thạch: Tiên ngọc sơ cấp, dùng để chuyển hóa Linh Lực thành Tiên Lực lúc Vấn Đỉnh.
2. Trung Phẩm Tiên Thạch: Tinh thuần gấp 1,000 lần Hạ Phẩm, dành cho Khuy Niết, Tịnh Niết kích hoạt thần thông tiên thuật.
3. Thượng Phẩm Tiên Thạch: Tinh thuần gấp 1,000 lần Trung Phẩm, chứa đựng tia quy tắc đại đạo cho Toái Niết và Tam Bộ Cảnh.
4. Cực Phẩm Tiên Thạch (Chí Tôn Tiên Tinh): Tinh hoa tối thượng của Tiên Giới, nuôi dưỡng Bản Nguyên.
"""
from typing import Optional, Dict, Any, List, Tuple

from .linh_thach import VALUE_CUC_PHAM


# =============================================================================
# HẰNG SỐ VÀ TỶ LỆ QUY ĐỔI TIÊN THẠCH
# =============================================================================
RATE_CUC_LINH_TO_HA_TIEN = 1000     # 1,000 Cực Phẩm Linh Thạch = 1 Hạ Phẩm Tiên Thạch
RATE_HA_TO_TRUNG_TIEN = 1000        # 1,000 Hạ Phẩm Tiên Thạch = 1 Trung Phẩm Tiên Thạch
RATE_TRUNG_TO_THUONG_TIEN = 1000    # 1,000 Trung Phẩm Tiên Thạch = 1 Thượng Phẩm Tiên Thạch
RATE_THUONG_TO_CUC_TIEN = 1000      # 1,000 Thượng Phẩm Tiên Thạch = 1 Cực Phẩm Tiên Thạch

# 1 Hạ Phẩm Tiên Thạch = 1,000 Cực Phẩm Linh Thạch = 1,000,000,000,000 Hạ Phẩm Linh Thạch (1 nghìn tỷ)
TIEN_THACH_TO_LINH_THACH_RATE = RATE_CUC_LINH_TO_HA_TIEN * VALUE_CUC_PHAM

VALUE_HA_PHAM_TIEN = 1
VALUE_TRUNG_PHAM_TIEN = RATE_HA_TO_TRUNG_TIEN                             # 1,000
VALUE_THUONG_PHAM_TIEN = VALUE_TRUNG_PHAM_TIEN * RATE_TRUNG_TO_THUONG_TIEN # 1,000,000
VALUE_CUC_PHAM_TIEN = VALUE_THUONG_PHAM_TIEN * RATE_THUONG_TO_CUC_TIEN     # 1,000,000,000

# Cảnh giới tối thiểu để kích hoạt và sử dụng Tiên Thạch:
# Trong canh_gioi_tu_vi (83 cảnh giới): Vấn Đỉnh Sơ Kỳ bắt đầu từ ID 25
MIN_REALM_ID_FOR_TIEN_THACH = 25  # Vấn Đỉnh Sơ Kỳ
MIN_REALM_NAME_FOR_TIEN_THACH = "Vấn Đỉnh"

# =============================================================================
# DANH SÁCH CHI TIẾT 4 PHẨM CẤP TIÊN THẠCH
# =============================================================================
TIEN_THACH_DATA: List[Dict[str, Any]] = [
    {
        "id": 1,
        "key": "ha_pham_tien_thach",
        "code": "HPTT",
        "name": "Hạ Phẩm Tiên Thạch",
        "short_name": "Tiên Ngọc Hạ Phẩm",
        "tier": 1,
        "icon": "✨",
        "base_value": VALUE_HA_PHAM_TIEN,
        "required_realm": "Vấn Đỉnh Sơ Kỳ hoặc Nhị Bộ Cảnh",
        "color": 0x1ABC9C,  # Ngọc lam bích
        "description": "Tiên ngọc sơ cấp ẩn chứa tiên khí tinh thuần của Tiên Giới viễn cổ, tương đương 1,000 Cực Phẩm Linh Thạch, giúp tu sĩ phàm tục gột rửa linh căn, chuyển hóa linh lực thành Tiên Lực.",
        "usage": "Tu sĩ Vấn Đỉnh, Âm Hư, Dương Thực chuyển hóa Tiên Lực để tiến vào Nhị Bộ Cảnh, giao dịch tại Tinh Không Chợ Đen, mua Tiên Khí hạ phẩm.",
    },
    {
        "id": 2,
        "key": "trung_pham_tien_thach",
        "code": "TPTT",
        "name": "Trung Phẩm Tiên Thạch",
        "short_name": "Tiên Ngọc Trung Phẩm",
        "tier": 2,
        "icon": "💎",
        "base_value": VALUE_TRUNG_PHAM_TIEN,
        "required_realm": "Khuy Niết Sơ Kỳ (Nhị Bộ Cảnh)",
        "color": 0x00CED1,  # Bích ngọc thanh khiết
        "description": "Tiên ngọc tinh thuần gấp 1,000 lần Hạ Phẩm Tiên Thạch, tỏa ánh hào quang tiên gia rực rỡ, bên trong có thể thấy rõ các dòng tiên lực lưu chuyển như thác nước.",
        "usage": "Khuy Niết và Tịnh Niết lão quái dùng để độ kiếp, tu luyện thần thông tiên thuật, khởi động truyền tống trận xuyên qua các tinh vực lớn.",
    },
    {
        "id": 3,
        "key": "thuong_pham_tien_thach",
        "code": "TuPTT",
        "name": "Thượng Phẩm Tiên Thạch",
        "short_name": "Tiên Ngọc Thượng Phẩm",
        "tier": 3,
        "icon": "🌟",
        "base_value": VALUE_THUONG_PHAM_TIEN,
        "required_realm": "Toái Niết Đỉnh Phong / Tam Bộ Cảnh",
        "color": 0xFFD700,  # Hoàng kim tiên quang
        "description": "Tiên ngọc tinh thuần gấp 1,000 lần Trung Phẩm Tiên Thạch, chứa một tia Bản Nguyên Thiên Địa sơ khai. Chỉ có tại các cấm địa thượng cổ hoặc di tích Tiên Cung mới ngưng tụ thành khối.",
        "usage": "Hòa tan Bản Nguyên, tu luyện thần thông viễn cổ, giao dịch giữa các chưởng môn tinh vực và đại năng Tam Bộ (Không Niết, Không Linh, Không Huyền).",
    },
    {
        "id": 4,
        "key": "cuc_pham_tien_thach",
        "code": "CPTT",
        "name": "Cực Phẩm Tiên Thạch",
        "short_name": "Chí Tôn Tiên Tinh",
        "tier": 4,
        "icon": "🌌",
        "base_value": VALUE_CUC_PHAM_TIEN,
        "required_realm": "Không Niết / Không Linh / Không Huyền (Tam Bộ)",
        "color": 0xE056FD,  # Tím tử kim chí tôn
        "description": "Chí tôn tiên tinh tinh thuần gấp 1,000 lần Thượng Phẩm Tiên Thạch, mỗi một viên tương đương với cả một tiểu tinh cầu ngưng tụ hàng triệu năm. Chứa năng lượng sáng tạo và hủy diệt càn khôn.",
        "usage": "Đúc Thần Cách Đại Thiên Tôn, kích hoạt Thần Khí Thái Cổ, bồi dưỡng Bản Nguyên tối thượng và ngộ Quy Tắc Tịch Diệt.",
    },
]

# =============================================================================
# HỆ THỐNG TRA CỨU NHANH
# =============================================================================
TIEN_THACH_BY_ID: Dict[int, Dict[str, Any]] = {tt["id"]: tt for tt in TIEN_THACH_DATA}
TIEN_THACH_BY_KEY: Dict[str, Dict[str, Any]] = {tt["key"]: tt for tt in TIEN_THACH_DATA}
TIEN_THACH_BY_TIER: Dict[int, Dict[str, Any]] = {tt["tier"]: tt for tt in TIEN_THACH_DATA}
TIEN_THACH_BY_CODE: Dict[str, Dict[str, Any]] = {tt["code"].upper(): tt for tt in TIEN_THACH_DATA}


# =============================================================================
# CÁC HÀM TIỆN ÍCH QUY ĐỔI VÀ ĐIỀU KIỆN
# =============================================================================
def get_all_tien_thach() -> List[Dict[str, Any]]:
    """Trả về danh sách toàn bộ 4 phẩm cấp Tiên Thạch."""
    return TIEN_THACH_DATA


def get_tien_thach_by_id(tt_id: int) -> Optional[Dict[str, Any]]:
    """Tra cứu tiên thạch theo ID (1 -> 4)."""
    return TIEN_THACH_BY_ID.get(tt_id)


def get_tien_thach_by_key(key: str) -> Optional[Dict[str, Any]]:
    """Tra cứu tiên thạch theo key (ví dụ: 'ha_pham_tien_thach')."""
    return TIEN_THACH_BY_KEY.get(key.strip().lower())


def get_tien_thach_by_tier(tier: int) -> Optional[Dict[str, Any]]:
    """Tra cứu tiên thạch theo bậc phẩm (1: Hạ, 2: Trung, 3: Thượng, 4: Cực)."""
    return TIEN_THACH_BY_TIER.get(tier)


def kiem_tra_tu_vi_su_dung_tien_thach(realm_id: int) -> Tuple[bool, str]:
    """
    Kiểm tra xem cảnh giới của tu sĩ có đủ điều kiện để sử dụng Tiên Thạch hay chưa.
    Yêu cầu: Từ Vấn Đỉnh Cảnh (realm_id >= 25) hoặc Nhị Bộ Cảnh trở lên.
    """
    if realm_id < MIN_REALM_ID_FOR_TIEN_THACH:
        return False, (
            f"Tu vi chưa đủ! Tiên Thạch chỉ dành cho tu sĩ từ cảnh giới "
            f"[{MIN_REALM_NAME_FOR_TIEN_THACH}] hoặc Nhị Bộ Cảnh trở lên. "
            f"Tu sĩ cảnh giới thấp hấp thụ tiên khí sẽ bị bạo thể mà chết!"
        )
    return True, "Tu vi đạt yêu cầu để điều động và sử dụng Tiên Thạch."


def quy_doi_tien_thach_sang_linh_thach(so_luong_tien_thach: int, tier: int = 1) -> int:
    """
    Quy đổi số lượng Tiên Thạch sang Hạ Phẩm Linh Thạch tương đương.
    1 Hạ Phẩm Tiên Thạch = 1,000 Cực Phẩm Linh Thạch = 1,000,000,000,000 Hạ Phẩm Linh Thạch.
    """
    tt = get_tien_thach_by_tier(tier)
    base_mult = tt["base_value"] if tt else 1
    return so_luong_tien_thach * base_mult * TIEN_THACH_TO_LINH_THACH_RATE


def quy_doi_tu_ha_pham_tien(so_luong_ha_pham_tien: int) -> Dict[str, int]:
    """
    Phân rã số lượng Hạ Phẩm Tiên Thạch thành cơ cấu các phẩm cấp tối ưu nhất:
    Trả về dict: {'cuc_pham': X, 'thuong_pham': Y, 'trung_pham': Z, 'ha_pham': W}
    """
    con_lai = max(0, so_luong_ha_pham_tien)

    cuc_pham = con_lai // VALUE_CUC_PHAM_TIEN
    con_lai %= VALUE_CUC_PHAM_TIEN

    thuong_pham = con_lai // VALUE_THUONG_PHAM_TIEN
    con_lai %= VALUE_THUONG_PHAM_TIEN

    trung_pham = con_lai // VALUE_TRUNG_PHAM_TIEN
    con_lai %= VALUE_TRUNG_PHAM_TIEN

    ha_pham = con_lai

    return {
        "cuc_pham": cuc_pham,
        "thuong_pham": thuong_pham,
        "trung_pham": trung_pham,
        "ha_pham": ha_pham,
    }


def dinh_dang_tien_thach(so_luong_ha_pham_tien: int) -> str:
    """
    Định dạng hiển thị số lượng Tiên Thạch sang chuỗi thân thiện với người chơi.
    Ví dụ: 1,002,003,004 -> '1 Tiên Tinh Cực Phẩm, 2 Tiên Ngọc Thượng Phẩm, 3 Tiên Ngọc Trung Phẩm, 4 Tiên Ngọc Hạ Phẩm'
    """
    if so_luong_ha_pham_tien <= 0:
        return "0 Tiên Thạch"

    co_cau = quy_doi_tu_ha_pham_tien(so_luong_ha_pham_tien)
    parts = []
    if co_cau["cuc_pham"] > 0:
        parts.append(f"🌌 {co_cau['cuc_pham']:,} Tiên Tinh Cực Phẩm")
    if co_cau["thuong_pham"] > 0:
        parts.append(f"🌟 {co_cau['thuong_pham']:,} Tiên Ngọc Thượng Phẩm")
    if co_cau["trung_pham"] > 0:
        parts.append(f"💎 {co_cau['trung_pham']:,} Tiên Ngọc Trung Phẩm")
    if co_cau["ha_pham"] > 0 or not parts:
        parts.append(f"✨ {co_cau['ha_pham']:,} Tiên Ngọc Hạ Phẩm")

    return " ".join(parts)

