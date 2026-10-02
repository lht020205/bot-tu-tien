# -*- coding: utf-8 -*-
"""
canh_gioi_binh_khi.py
=====================
Lưu trữ toàn bộ danh sách cảnh giới binh khí trong hệ thống.
File này thuần túy lưu trữ dữ liệu cảnh giới và các hàm tra cứu cơ bản,
tương tự như cảnh giới tu vi (canh_gioi_tu_vi.py).
"""
from typing import Optional, Dict, Any, List

# Blueprint toàn bộ cảnh giới binh khí theo đúng thứ tự từ thấp đến cao
REALM_BLUEPRINT = [
    ("Binh Khí", [
        ("Phàm Khí", (None,)),
        ("Hoàng Khí", (None,)),
        ("Thần Khí", (None,)),
        ("Thiên Thần Khí", (None,)),
        ("Chuẩn Thánh Khí", (None,)),
        ("Thánh Khí", (None,)),
        ("Chuẩn Chí Tôn Khí", (None,)),
        ("Chí Tôn Khí", (None,)),
        ("Chuẩn Đế Khí", (None,)),
        ("Đế Khí ( Thành Đạo Khí )", (None,)),
        ("Văn Minh Chí Bảo", (None,)),
        ("Sơ Đại Văn Minh Chí Bảo", (None,)),
    ]),
]


def _build_realms() -> List[Dict[str, Any]]:
    """Xây dựng danh sách phẳng chứa tất cả các cấp cảnh giới binh khí."""
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


# Danh sách toàn bộ cảnh giới binh khí
REALMS: List[Dict[str, Any]] = _build_realms()
TOTAL_REALMS: int = len(REALMS)

# Bảng băm tra cứu theo ID và theo Tên
REALM_BY_ID: Dict[int, Dict[str, Any]] = {r["id"]: r for r in REALMS}
REALM_BY_NAME: Dict[str, Dict[str, Any]] = {r["name"]: r for r in REALMS}

# Bổ sung alias tra cứu thuận tiện cho Đế Khí ( Thành Đạo Khí )
for r in REALMS:
    if r["minor_realm"] == "Đế Khí ( Thành Đạo Khí )":
        REALM_BY_NAME["Đế Khí"] = r
        REALM_BY_NAME["Thành Đạo Khí"] = r
        REALM_BY_NAME["Đế Khí (Thành Đạo Khí)"] = r

# Alias ngữ nghĩa riêng cho binh khí
WEAPON_REALMS = REALMS
TOTAL_WEAPON_REALMS = TOTAL_REALMS


# =============================================================================
# CÁC HÀM TRA CỨU CƠ BẢN
# =============================================================================

def get_all_realms() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách cảnh giới binh khí."""
    return REALMS


def get_realm_by_id(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới binh khí theo ID.
    Trả về None nếu ID không tồn tại.
    """
    return REALM_BY_ID.get(realm_id)


def get_realm_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới binh khí theo tên đầy đủ hoặc alias.
    Trả về None nếu tên không tồn tại.
    """
    return REALM_BY_NAME.get(name)


def get_next_realm(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy cảnh giới binh khí kế tiếp.
    Trả về None nếu đã ở cảnh giới cao nhất (hoặc realm_id không hợp lệ).
    """
    return REALM_BY_ID.get(realm_id + 1)


def is_max_realm(realm_id: int) -> bool:
    """Kiểm tra xem binh khí đã đạt phẩm cấp cao nhất chưa."""
    return realm_id >= TOTAL_REALMS


# Alias hàm tương thích theo ngữ nghĩa binh khí
get_all_weapon_realms = get_all_realms
get_weapon_realm_by_id = get_realm_by_id
get_weapon_realm_by_name = get_realm_by_name
get_next_weapon_realm = get_next_realm
is_max_weapon_realm = is_max_realm


if __name__ == "__main__":
    print(f"Tổng số cấp cảnh giới binh khí: {TOTAL_REALMS}")
    print(f"Cấp đầu tiên (id=1): {get_realm_by_id(1)}")
    print(f"Cấp cuối cùng (id={TOTAL_REALMS}): {get_realm_by_id(TOTAL_REALMS)}")
    print(f"Cảnh giới sau id=1: {get_next_realm(1)}")
    print(f"Cảnh giới sau id={TOTAL_REALMS}: {get_next_realm(TOTAL_REALMS)}")
    print(f"Tra cứu Đế Khí qua alias: {get_realm_by_name('Đế Khí')}")
