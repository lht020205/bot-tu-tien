# -*- coding: utf-8 -*-
"""
canh_gioi_phu_trien.py
======================
Lưu trữ toàn bộ danh sách cảnh giới (phẩm cấp) phù triện theo hệ thống Tiên Nghịch:
1. Linh Phù: Hạ Phẩm --- Trung Phẩm --- Thượng Phẩm --- Cực Phẩm
2. Tiên Phù: Hạ Phẩm --- Trung Phẩm --- Thượng Phẩm --- Cực Phẩm

File này thuần túy lưu trữ dữ liệu cảnh giới và các hàm tra cứu cơ bản,
tương tự như các hệ thống cảnh giới khác trong canh_gioi_chung.
"""
from typing import Optional, Dict, Any, List

# Các phẩm cấp dùng chung
STAGES_PHAM_CAP = ("Hạ Phẩm", "Trung Phẩm", "Thượng Phẩm", "Cực Phẩm")

# Blueprint cảnh giới phù triện theo đúng thứ tự từ thấp đến cao
REALM_BLUEPRINT = [
    ("Phù Triện", [
        ("Linh Phù", STAGES_PHAM_CAP),
        ("Tiên Phù", STAGES_PHAM_CAP),
    ]),
]


def _build_realms() -> List[Dict[str, Any]]:
    """Xây dựng danh sách phẳng chứa tất cả các cấp cảnh giới phù triện."""
    realm_list = []
    current_id = 1

    for major_name, minors in REALM_BLUEPRINT:
        for minor_name, stages in minors:
            for stage in stages:
                full_name = f"{minor_name} - {stage}" if stage else minor_name
                realm_list.append({
                    "id": current_id,
                    "major_realm": major_name,
                    "minor_realm": minor_name,
                    "stage": stage,
                    "name": full_name,
                })
                current_id += 1

    return realm_list


# Danh sách toàn bộ cảnh giới phù triện
REALMS: List[Dict[str, Any]] = _build_realms()
TOTAL_REALMS: int = len(REALMS)

# Bảng băm tra cứu theo ID và theo Tên
REALM_BY_ID: Dict[int, Dict[str, Any]] = {r["id"]: r for r in REALMS}
REALM_BY_NAME: Dict[str, Dict[str, Any]] = {r["name"]: r for r in REALMS}

# Bổ sung alias thuận tiện
for r in REALMS:
    name = r["name"]
    minor = r["minor_realm"]
    stage = r["stage"]
    if stage:
        REALM_BY_NAME.setdefault(f"{minor} {stage}", r)
        REALM_BY_NAME.setdefault(f"Phù Triện {name}", r)
        REALM_BY_NAME.setdefault(f"Phù Triện {minor} {stage}", r)

# Bảng tra cứu không phân biệt hoa thường
REALM_BY_LOWER: Dict[str, Dict[str, Any]] = {k.lower(): v for k, v in REALM_BY_NAME.items()}

# Alias ngữ nghĩa riêng cho phù triện và công pháp (tương thích ngược)
PHU_TRIEN_REALMS = REALMS
TALISMAN_REALMS = REALMS
CONG_PHAP_REALMS = REALMS
SKILL_REALMS = REALMS

TOTAL_PHU_TRIEN_REALMS = TOTAL_REALMS
TOTAL_TALISMAN_REALMS = TOTAL_REALMS
TOTAL_CONG_PHAP_REALMS = TOTAL_REALMS
TOTAL_SKILL_REALMS = TOTAL_REALMS


# =============================================================================
# CÁC HÀM TRA CỨU CƠ BẢN
# =============================================================================

def get_all_realms() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách cảnh giới phù triện."""
    return REALMS


def get_realm_by_id(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới phù triện theo ID.
    Trả về None nếu ID không tồn tại.
    """
    return REALM_BY_ID.get(realm_id)


def get_realm_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới phù triện theo tên đầy đủ hoặc alias (không phân biệt hoa thường).
    Trả về None nếu tên không tồn tại.
    """
    if not name:
        return None
    if name in REALM_BY_NAME:
        return REALM_BY_NAME[name]
    return REALM_BY_LOWER.get(name.strip().lower())


def get_next_realm(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy cảnh giới phù triện kế tiếp.
    Trả về None nếu đã ở cảnh giới cao nhất (hoặc realm_id không hợp lệ).
    """
    return REALM_BY_ID.get(realm_id + 1)


def is_max_realm(realm_id: int) -> bool:
    """Kiểm tra xem phù triện đã đạt cấp cao nhất chưa."""
    return realm_id >= TOTAL_REALMS


# Alias hàm tương thích theo ngữ nghĩa phù triện & công pháp
get_all_phu_trien_realms = get_all_realms
get_phu_trien_realm_by_id = get_realm_by_id
get_phu_trien_realm_by_name = get_realm_by_name
get_next_phu_trien_realm = get_next_realm
is_max_phu_trien_realm = is_max_realm

get_all_talisman_realms = get_all_realms
get_talisman_realm_by_id = get_realm_by_id
get_talisman_realm_by_name = get_realm_by_name
get_next_talisman_realm = get_next_realm
is_max_talisman_realm = is_max_realm

get_all_cong_phap_realms = get_all_realms
get_cong_phap_realm_by_id = get_realm_by_id
get_cong_phap_realm_by_name = get_realm_by_name
get_next_cong_phap_realm = get_next_realm
is_max_cong_phap_realm = is_max_realm

get_all_skill_realms = get_all_realms
get_skill_realm_by_id = get_realm_by_id
get_skill_realm_by_name = get_realm_by_name
get_next_skill_realm = get_next_realm
is_max_skill_realm = is_max_realm


if __name__ == "__main__":
    print(f"Tổng số cấp cảnh giới phù triện: {TOTAL_REALMS}")
    print(f"Cấp đầu tiên (id=1): {get_realm_by_id(1)}")
    print(f"Cấp cuối cùng (id={TOTAL_REALMS}): {get_realm_by_id(TOTAL_REALMS)}")
    print(f"Cảnh giới sau id=1: {get_next_realm(1)}")
    print(f"Cảnh giới sau id={TOTAL_REALMS}: {get_next_realm(TOTAL_REALMS)}")
    print("\n--- Test tra cứu linh hoạt ---")
    print(f"Tra cứu 'linh phù - hạ phẩm': {get_realm_by_name('linh phù - hạ phẩm')}")
    print(f"Tra cứu 'linh phù cực phẩm': {get_realm_by_name('linh phù cực phẩm')}")
    print(f"Tra cứu 'tiên phù thượng phẩm': {get_realm_by_name('tiên phù thượng phẩm')}")
