# -*- coding: utf-8 -*-
"""
canh_gioi_linh_thu.py
=====================
Lưu trữ toàn bộ danh sách cảnh giới linh thú (yêu thú / linh sủng) trong hệ thống:
1. Linh Thú: Hạ Phẩm --- Trung Phẩm --- Thượng Phẩm
2. Hoang Thú: Hạ Phẩm --- Trung Phẩm --- Thượng Phẩm
3. Tiên Thú: Hạ Phẩm --- Trung Phẩm --- Thượng Phẩm

File này thuần túy lưu trữ dữ liệu cảnh giới và các hàm tra cứu cơ bản,
tương tự như các hệ thống cảnh giới khác trong canh_gioi_chung.
"""
from typing import Optional, Dict, Any, List

# Phẩm cấp chất lượng linh thú
STAGES_PHAM_CAP = ("Hạ Phẩm", "Trung Phẩm", "Thượng Phẩm")

# Blueprint linh thú theo đúng thứ tự từ thấp đến cao
REALM_BLUEPRINT = [
    ("Linh Thú", [
        ("Linh Thú", STAGES_PHAM_CAP),
        ("Hoang Thú", STAGES_PHAM_CAP),
        ("Tiên Thú", STAGES_PHAM_CAP),
    ]),
]


def _build_realms() -> List[Dict[str, Any]]:
    """Xây dựng danh sách phẳng chứa tất cả các cấp cảnh giới linh thú."""
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


# Danh sách toàn bộ cảnh giới linh thú
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
        REALM_BY_NAME.setdefault(f"Thú {minor} {stage}", r)

# Bảng tra cứu không phân biệt hoa thường
REALM_BY_LOWER: Dict[str, Dict[str, Any]] = {k.lower(): v for k, v in REALM_BY_NAME.items()}

# Alias ngữ nghĩa riêng cho linh thú
LINH_THU_REALMS = REALMS
BEAST_REALMS = REALMS
PET_REALMS = REALMS
TOTAL_LINH_THU_REALMS = TOTAL_REALMS
TOTAL_BEAST_REALMS = TOTAL_REALMS
TOTAL_PET_REALMS = TOTAL_REALMS


# =============================================================================
# CÁC HÀM TRA CỨU CƠ BẢN
# =============================================================================

def get_all_realms() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách cảnh giới linh thú."""
    return REALMS


def get_realm_by_id(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới linh thú theo ID.
    Trả về None nếu ID không tồn tại.
    """
    return REALM_BY_ID.get(realm_id)


def get_realm_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới linh thú theo tên đầy đủ hoặc alias (không phân biệt hoa thường).
    Trả về None nếu tên không tồn tại.
    """
    if not name:
        return None
    if name in REALM_BY_NAME:
        return REALM_BY_NAME[name]
    return REALM_BY_LOWER.get(name.strip().lower())


def get_next_realm(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy cảnh giới linh thú kế tiếp.
    Trả về None nếu đã ở cảnh giới cao nhất (hoặc realm_id không hợp lệ).
    """
    return REALM_BY_ID.get(realm_id + 1)


def is_max_realm(realm_id: int) -> bool:
    """Kiểm tra xem linh thú đã đạt cảnh giới cao nhất chưa."""
    return realm_id >= TOTAL_REALMS


# Alias hàm tương thích theo ngữ nghĩa linh thú
get_all_linh_thu_realms = get_all_realms
get_linh_thu_realm_by_id = get_realm_by_id
get_linh_thu_realm_by_name = get_realm_by_name
get_next_linh_thu_realm = get_next_realm
is_max_linh_thu_realm = is_max_realm

get_all_beast_realms = get_all_realms
get_beast_realm_by_id = get_realm_by_id
get_beast_realm_by_name = get_realm_by_name
get_next_beast_realm = get_next_realm
is_max_beast_realm = is_max_realm

get_all_pet_realms = get_all_realms
get_pet_realm_by_id = get_realm_by_id
get_pet_realm_by_name = get_realm_by_name
get_next_pet_realm = get_next_realm
is_max_pet_realm = is_max_realm


if __name__ == "__main__":
    print(f"Tổng số cấp cảnh giới linh thú: {TOTAL_REALMS}")
    print(f"Cấp đầu tiên (id=1): {get_realm_by_id(1)}")
    print(f"Cấp cuối cùng (id={TOTAL_REALMS}): {get_realm_by_id(TOTAL_REALMS)}")
    print(f"Cảnh giới sau id=1: {get_next_realm(1)}")
    print(f"Cảnh giới sau id={TOTAL_REALMS}: {get_next_realm(TOTAL_REALMS)}")
    print("\n--- Test tra cứu linh hoạt ---")
    print(f"Tra cứu 'linh thú - hạ phẩm': {get_realm_by_name('linh thú - hạ phẩm')}")
    print(f"Tra cứu 'hoang thú thượng phẩm': {get_realm_by_name('hoang thú thượng phẩm')}")
    print(f"Tra cứu 'tiên thú - cực phẩm' (None vì chỉ có thượng phẩm): {get_realm_by_name('tiên thú - cực phẩm')}")
    print(f"Tra cứu 'tiên thú thượng phẩm': {get_realm_by_name('tiên thú thượng phẩm')}")
