# -*- coding: utf-8 -*-
"""
linh_thach.py
=============
Hệ thống Linh Thạch (Đơn vị tiền tệ cơ bản của người tu tiên trong Chu Thiên Vạn Giới):
Chia làm 4 phẩm cấp:
1. Hạ Phẩm Linh Thạch (HPLT): Tiền tệ giao dịch thông dụng nhất, dùng cho tu sĩ sơ nhập đạo.
2. Trung Phẩm Linh Thạch (TPLT): Tinh thuần hơn, 1 Trung Phẩm = 1,000 Hạ Phẩm.
3. Thượng Phẩm Linh Thạch (TuPLT): Tinh hoa linh mạch, 1 Thượng Phẩm = 1,000 Trung Phẩm (= 1,000,000 Hạ Phẩm).
4. Cực Phẩm Linh Thạch (CPLT): Thuần khiết vô tạp chất, 1 Cực Phẩm = 1,000 Thượng Phẩm (= 1,000,000,000 Hạ Phẩm).

Cung cấp đầy đủ cấu trúc dữ liệu, hằng số quy đổi, hàm tính toán và hiển thị định dạng tiền tệ.
"""
from typing import Optional, Dict, Any, List, Tuple


# =============================================================================
# HẰNG SỐ VÀ TỶ LỆ QUY ĐỔI LINH THẠCH
# =============================================================================
RATE_HA_TO_TRUNG = 1000        # 1000 Hạ Phẩm = 1 Trung Phẩm
RATE_TRUNG_TO_THUONG = 1000    # 1000 Trung Phẩm = 1 Thượng Phẩm
RATE_THUONG_TO_CUC = 1000      # 1000 Thượng Phẩm = 1 Cực Phẩm

VALUE_HA_PHAM = 1
VALUE_TRUNG_PHAM = RATE_HA_TO_TRUNG                                # 1,000
VALUE_THUONG_PHAM = VALUE_TRUNG_PHAM * RATE_TRUNG_TO_THUONG        # 1,000,000
VALUE_CUC_PHAM = VALUE_THUONG_PHAM * RATE_THUONG_TO_CUC            # 1,000,000,000

# =============================================================================
# DANH SÁCH CHI TIẾT 4 PHẨM CẤP LINH THẠCH
# =============================================================================
LINH_THACH_DATA: List[Dict[str, Any]] = [
    {
        "id": 1,
        "key": "ha_pham_linh_thach",
        "code": "HPLT",
        "name": "Hạ Phẩm Linh Thạch",
        "short_name": "Hạ Phẩm",
        "tier": 1,
        "icon": "⚪",
        "base_value": VALUE_HA_PHAM,
        "color": 0xBDC3C7,  # Bạc xám nhạt
        "description": "Linh thạch phẩm cấp cơ bản, chứa linh khí loãng, dùng cho tu sĩ Ngưng Khí và Trúc Cơ giao dịch hàng ngày hoặc kích hoạt tiểu trận pháp.",
        "usage": "Giao dịch sơ cấp, mua đan dược phàm giai, khôi phục lượng nhỏ linh khí.",
    },
    {
        "id": 2,
        "key": "trung_pham_linh_thach",
        "code": "TPLT",
        "name": "Trung Phẩm Linh Thạch",
        "short_name": "Trung Phẩm",
        "tier": 2,
        "icon": "🟢",
        "base_value": VALUE_TRUNG_PHAM,
        "color": 0x2ECC71,  # Xanh ngọc
        "description": "Linh khí tinh thuần hơn gấp ngàn lần Hạ Phẩm, sáng bóng óng ánh. Tiền tệ phổ biến ở các buổi đấu giá lớn và phường thị tu chân cấp cao.",
        "usage": "Tu luyện Kết Đan, mua sắm pháp bảo trung phẩm, duy trì trận pháp hộ sơn.",
    },
    {
        "id": 3,
        "key": "thuong_pham_linh_thach",
        "code": "TuPLT",
        "name": "Thượng Phẩm Linh Thạch",
        "short_name": "Thượng Phẩm",
        "tier": 3,
        "icon": "🔵",
        "base_value": VALUE_THUONG_PHAM,
        "color": 0x3498DB,  # Xanh lam đậm
        "description": "Tinh hoa được thai nghén từ lõi của các long mạch cổ xưa. Linh khí nồng đượm ngưng kết thành dạng tinh thể bán trong suốt.",
        "usage": "Đại năng Nguyên Anh, Hóa Thần sử dụng để hồi phục Chân Nguyên cấp tốc hoặc đấu giá kỳ trân dị bảo.",
    },
    {
        "id": 4,
        "key": "cuc_pham_linh_thach",
        "code": "CPLT",
        "name": "Cực Phẩm Linh Thạch",
        "short_name": "Cực Phẩm",
        "tier": 4,
        "icon": "🟣",
        "base_value": VALUE_CUC_PHAM,
        "color": 0x9B59B6,  # Tím tử tinh
        "description": "Linh thạch vô tạp chất đạt tới độ hoàn mỹ tối thượng, ẩn chứa một luồng linh nguyên thuần khiết của thiên địa, cực kỳ hiếm thấy.",
        "usage": "Làm mắt trận truyền tống liên tinh cầu, kích hoạt Hộ Phái Đại Trận hoặc bồi dưỡng linh mạch môn phái.",
    },
]

# =============================================================================
# HỆ THỐNG TRA CỨU NHANH
# =============================================================================
LINH_THACH_BY_ID: Dict[int, Dict[str, Any]] = {lt["id"]: lt for lt in LINH_THACH_DATA}
LINH_THACH_BY_KEY: Dict[str, Dict[str, Any]] = {lt["key"]: lt for lt in LINH_THACH_DATA}
LINH_THACH_BY_TIER: Dict[int, Dict[str, Any]] = {lt["tier"]: lt for lt in LINH_THACH_DATA}
LINH_THACH_BY_CODE: Dict[str, Dict[str, Any]] = {lt["code"].upper(): lt for lt in LINH_THACH_DATA}


# =============================================================================
# CÁC HÀM TIỆN ÍCH QUY ĐỔI VÀ ĐỊNH DẠNG
# =============================================================================
def get_all_linh_thach() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách 4 phẩm cấp linh thạch."""
    return LINH_THACH_DATA


def get_linh_thach_by_id(lt_id: int) -> Optional[Dict[str, Any]]:
    """Tra cứu linh thạch theo ID (1 -> 4)."""
    return LINH_THACH_BY_ID.get(lt_id)


def get_linh_thach_by_key(key: str) -> Optional[Dict[str, Any]]:
    """Tra cứu linh thạch theo key (ví dụ: 'ha_pham_linh_thach')."""
    return LINH_THACH_BY_KEY.get(key.strip().lower())


def get_linh_thach_by_tier(tier: int) -> Optional[Dict[str, Any]]:
    """Tra cứu linh thạch theo bậc phẩm (1: Hạ, 2: Trung, 3: Thượng, 4: Cực)."""
    return LINH_THACH_BY_TIER.get(tier)


def quy_doi_sang_ha_pham(so_luong: int, tier_hoac_key: Any) -> int:
    """
    Quy đổi số lượng linh thạch bất kỳ sang số lượng Hạ Phẩm Linh Thạch tương đương.
    """
    if isinstance(tier_hoac_key, int):
        lt = get_linh_thach_by_tier(tier_hoac_key)
    else:
        lt = get_linh_thach_by_key(str(tier_hoac_key))

    if not lt:
        return so_luong
    return so_luong * lt["base_value"]


def quy_doi_tu_ha_pham(so_luong_ha_pham: int) -> Dict[str, int]:
    """
    Phân rã số lượng Hạ Phẩm Linh Thạch thành cơ cấu các phẩm cấp tối ưu nhất:
    Trả về dict: {'cuc_pham': X, 'thuong_pham': Y, 'trung_pham': Z, 'ha_pham': W}
    """
    con_lai = max(0, so_luong_ha_pham)

    cuc_pham = con_lai // VALUE_CUC_PHAM
    con_lai %= VALUE_CUC_PHAM

    thuong_pham = con_lai // VALUE_THUONG_PHAM
    con_lai %= VALUE_THUONG_PHAM

    trung_pham = con_lai // VALUE_TRUNG_PHAM
    con_lai %= VALUE_TRUNG_PHAM

    ha_pham = con_lai

    return {
        "cuc_pham": cuc_pham,
        "thuong_pham": thuong_pham,
        "trung_pham": trung_pham,
        "ha_pham": ha_pham,
    }


def dinh_dang_linh_thach(so_luong_ha_pham: int) -> str:
    """
    Định dạng hiển thị số lượng linh thạch sang chuỗi thân thiện với người chơi.
    Ví dụ: 1,234,567 HPLT -> '1 Cực Phẩm, 23 Thượng Phẩm, 45 Trung Phẩm, 67 Hạ Phẩm'
    """
    if so_luong_ha_pham <= 0:
        return "0 Hạ Phẩm Linh Thạch"

    co_cau = quy_doi_tu_ha_pham(so_luong_ha_pham)
    parts = []
    if co_cau["cuc_pham"] > 0:
        parts.append(f"🟣 {co_cau['cuc_pham']:,} Cực Phẩm")
    if co_cau["thuong_pham"] > 0:
        parts.append(f"🔵 {co_cau['thuong_pham']:,} Thượng Phẩm")
    if co_cau["trung_pham"] > 0:
        parts.append(f"🟢 {co_cau['trung_pham']:,} Trung Phẩm")
    if co_cau["ha_pham"] > 0 or not parts:
        parts.append(f"⚪ {co_cau['ha_pham']:,} Hạ Phẩm")

    return " ".join(parts)
