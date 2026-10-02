# -*- coding: utf-8 -*-
"""
canh_gioi_di_tich.py
====================
Lưu trữ danh sách 9 cảnh giới (bậc) di tích trong hệ thống.
File này thuần túy lưu trữ dữ liệu cảnh giới và các hàm tra cứu cơ bản,
tương tự như các hệ thống cảnh giới khác trong canh_gioi_chung.
"""
from typing import Optional, Dict, Any, List

# Blueprint 9 bậc di tích theo đúng thứ tự từ thấp đến cao (tương đồng 9 đại cảnh giới tu vi)
REALM_BLUEPRINT = [
    ("Di Tích", [
        ("Phàm", (None,)),
        ("Thần", (None,)),
        ("Thánh", (None,)),
        ("Chí Tôn", (None,)),
        ("Đế", (None,)),
        ("Tiên", (None,)),
        ("Đạo", (None,)),
        ("Đạo Tổ", (None,)),
        ("Thiên", (None,)),
    ]),
]


def _build_realms() -> List[Dict[str, Any]]:
    """Xây dựng danh sách phẳng chứa tất cả các bậc di tích."""
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


# Danh sách toàn bộ cảnh giới di tích
REALMS: List[Dict[str, Any]] = _build_realms()
TOTAL_REALMS: int = len(REALMS)

# Bảng băm tra cứu theo ID và theo Tên
REALM_BY_ID: Dict[int, Dict[str, Any]] = {r["id"]: r for r in REALMS}
REALM_BY_NAME: Dict[str, Dict[str, Any]] = {r["name"]: r for r in REALMS}

# Bổ sung alias thuận tiện (hỗ trợ thêm đuôi "Cấp", tiền tố "Di Tích", "Bậc"...)
for r in REALMS:
    name = r["name"]
    REALM_BY_NAME.setdefault(f"{name} Cấp", r)
    REALM_BY_NAME.setdefault(f"Bậc {name}", r)
    REALM_BY_NAME.setdefault(f"Di Tích {name}", r)
    REALM_BY_NAME.setdefault(f"Di Tích {name} Cấp", r)
    REALM_BY_NAME.setdefault(f"Di Tích Bậc {name}", r)

# Bảng tra cứu không phân biệt hoa thường
REALM_BY_LOWER: Dict[str, Dict[str, Any]] = {k.lower(): v for k, v in REALM_BY_NAME.items()}

# Alias ngữ nghĩa riêng cho di tích
DI_TICH_REALMS = REALMS
RELIC_REALMS = REALMS
RUINS_REALMS = REALMS
TOTAL_DI_TICH_REALMS = TOTAL_REALMS
TOTAL_RELIC_REALMS = TOTAL_REALMS


# =============================================================================
# CÁC HÀM TRA CỨU CƠ BẢN
# =============================================================================

def get_all_realms() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách bậc di tích."""
    return REALMS


def get_realm_by_id(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin bậc di tích theo ID.
    Trả về None nếu ID không tồn tại.
    """
    return REALM_BY_ID.get(realm_id)


def get_realm_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin bậc di tích theo tên đầy đủ hoặc alias (không phân biệt hoa thường).
    Trả về None nếu tên không tồn tại.
    """
    if not name:
        return None
    if name in REALM_BY_NAME:
        return REALM_BY_NAME[name]
    return REALM_BY_LOWER.get(name.strip().lower())


def get_next_realm(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy bậc di tích kế tiếp.
    Trả về None nếu đã ở bậc cao nhất (hoặc realm_id không hợp lệ).
    """
    return REALM_BY_ID.get(realm_id + 1)


def is_max_realm(realm_id: int) -> bool:
    """Kiểm tra xem di tích đã đạt bậc cao nhất chưa."""
    return realm_id >= TOTAL_REALMS


# Alias hàm tương thích theo ngữ nghĩa di tích
get_all_di_tich_realms = get_all_realms
get_di_tich_realm_by_id = get_realm_by_id
get_di_tich_realm_by_name = get_realm_by_name
get_next_di_tich_realm = get_next_realm
is_max_di_tich_realm = is_max_realm

get_all_relic_realms = get_all_realms
get_relic_realm_by_id = get_realm_by_id
get_relic_realm_by_name = get_realm_by_name
get_next_relic_realm = get_next_realm
is_max_relic_realm = is_max_realm


if __name__ == "__main__":
    print(f"Tổng số bậc di tích: {TOTAL_REALMS}")
    print(f"Bậc đầu tiên (id=1): {get_realm_by_id(1)}")
    print(f"Bậc cuối cùng (id={TOTAL_REALMS}): {get_realm_by_id(TOTAL_REALMS)}")
    print(f"Bậc sau id=1: {get_next_realm(1)}")
    print(f"Bậc sau id={TOTAL_REALMS}: {get_next_realm(TOTAL_REALMS)}")
    print(f"Tra cứu 'phàm' (chữ thường): {get_realm_by_name('phàm')}")
    print(f"Tra cứu 'Tiên Cấp' qua alias: {get_realm_by_name('Tiên Cấp')}")
    print(f"Tra cứu 'di tích đạo tổ': {get_realm_by_name('di tích đạo tổ')}")
