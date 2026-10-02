# -*- coding: utf-8 -*-
"""
canh_gioi_dan_duoc.py
=====================
Lưu trữ danh sách cảnh giới (phẩm cấp) đan dược trong hệ thống.
File này thuần túy lưu trữ dữ liệu cảnh giới và các hàm tra cứu cơ bản,
tương tự như các hệ thống cảnh giới khác trong canh_gioi_chung.
"""
from typing import Optional, Dict, Any, List

# Blueprint 8 phẩm cấp đan dược theo đúng thứ tự từ thấp đến cao
REALM_BLUEPRINT = [
    ("Đan Dược", [
        ("Ngũ Phẩm", (None,)),
        ("Tứ Phẩm", (None,)),
        ("Tam Phẩm", (None,)),
        ("Nhị Phẩm", (None,)),
        ("Nhất Phẩm", (None,)),
        ("Thánh Phẩm", (None,)),
        ("Chí Tôn Phẩm", (None,)),
        ("Đế Phẩm", (None,)),
    ]),
]


def _build_realms() -> List[Dict[str, Any]]:
    """Xây dựng danh sách phẳng chứa tất cả các phẩm cấp đan dược."""
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


# Danh sách toàn bộ cảnh giới đan dược
REALMS: List[Dict[str, Any]] = _build_realms()
TOTAL_REALMS: int = len(REALMS)

# Bảng băm tra cứu theo ID và theo Tên
REALM_BY_ID: Dict[int, Dict[str, Any]] = {r["id"]: r for r in REALMS}
REALM_BY_NAME: Dict[str, Dict[str, Any]] = {r["name"]: r for r in REALMS}

# Bổ sung alias thuận tiện (chữ thường, tiền tố Đan dược, dạng số như 1 phẩm, 5 phẩm...)
NUMBER_ALIASES = {
    "Ngũ Phẩm": ["5 phẩm", "5 pham", "ngu pham"],
    "Tứ Phẩm": ["4 phẩm", "4 pham", "tu pham"],
    "Tam Phẩm": ["3 phẩm", "3 pham", "tam pham"],
    "Nhị Phẩm": ["2 phẩm", "2 pham", "nhi pham"],
    "Nhất Phẩm": ["1 phẩm", "1 pham", "nhat pham"],
    "Thánh Phẩm": ["thanh pham"],
    "Chí Tôn Phẩm": ["chi ton pham"],
    "Đế Phẩm": ["de pham"],
}

for r in REALMS:
    name = r["name"]
    REALM_BY_NAME.setdefault(f"Đan Dược {name}", r)
    REALM_BY_NAME.setdefault(f"Đan dược {name.lower()}", r)
    if name in NUMBER_ALIASES:
        for alias in NUMBER_ALIASES[name]:
            REALM_BY_NAME.setdefault(alias, r)
            REALM_BY_NAME.setdefault(f"đan dược {alias}", r)

# Bảng tra cứu không phân biệt hoa thường
REALM_BY_LOWER: Dict[str, Dict[str, Any]] = {k.lower(): v for k, v in REALM_BY_NAME.items()}

# Alias ngữ nghĩa riêng cho đan dược
DAN_DUOC_REALMS = REALMS
PILL_REALMS = REALMS
ELIXIR_REALMS = REALMS
TOTAL_DAN_DUOC_REALMS = TOTAL_REALMS
TOTAL_PILL_REALMS = TOTAL_REALMS


# =============================================================================
# CÁC HÀM TRA CỨU CƠ BẢN
# =============================================================================

def get_all_realms() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách phẩm cấp đan dược."""
    return REALMS


def get_realm_by_id(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin phẩm cấp đan dược theo ID.
    Trả về None nếu ID không tồn tại.
    """
    return REALM_BY_ID.get(realm_id)


def get_realm_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin phẩm cấp đan dược theo tên đầy đủ hoặc alias (không phân biệt hoa thường).
    Trả về None nếu tên không tồn tại.
    """
    if not name:
        return None
    if name in REALM_BY_NAME:
        return REALM_BY_NAME[name]
    return REALM_BY_LOWER.get(name.strip().lower())


def get_next_realm(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy phẩm cấp đan dược kế tiếp.
    Trả về None nếu đã ở phẩm cấp cao nhất (hoặc realm_id không hợp lệ).
    """
    return REALM_BY_ID.get(realm_id + 1)


def is_max_realm(realm_id: int) -> bool:
    """Kiểm tra xem đan dược đã đạt phẩm cấp cao nhất chưa."""
    return realm_id >= TOTAL_REALMS


# Alias hàm tương thích theo ngữ nghĩa đan dược
get_all_dan_duoc_realms = get_all_realms
get_dan_duoc_realm_by_id = get_realm_by_id
get_dan_duoc_realm_by_name = get_realm_by_name
get_next_dan_duoc_realm = get_next_realm
is_max_dan_duoc_realm = is_max_realm

get_all_pill_realms = get_all_realms
get_pill_realm_by_id = get_realm_by_id
get_pill_realm_by_name = get_realm_by_name
get_next_pill_realm = get_next_realm
is_max_pill_realm = is_max_realm


if __name__ == "__main__":
    print(f"Tổng số phẩm cấp đan dược: {TOTAL_REALMS}")
    print(f"Cấp đầu tiên (id=1): {get_realm_by_id(1)}")
    print(f"Cấp cuối cùng (id={TOTAL_REALMS}): {get_realm_by_id(TOTAL_REALMS)}")
    print(f"Cảnh giới sau id=1: {get_next_realm(1)}")
    print(f"Cảnh giới sau id={TOTAL_REALMS}: {get_next_realm(TOTAL_REALMS)}")
    print(f"Tra cứu 'ngũ phẩm' (chữ thường): {get_realm_by_name('ngũ phẩm')}")
    print(f"Tra cứu '1 phẩm' qua alias số: {get_realm_by_name('1 phẩm')}")
    print(f"Tra cứu 'Đế Phẩm': {get_realm_by_name('Đế Phẩm')}")
