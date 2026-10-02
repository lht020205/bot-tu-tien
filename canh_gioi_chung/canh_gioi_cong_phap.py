# -*- coding: utf-8 -*-
"""
canh_gioi_cong_phap.py
======================
Lưu trữ toàn bộ danh sách cảnh giới (phẩm cấp) công pháp trong hệ thống.
File này thuần túy lưu trữ dữ liệu cảnh giới và các hàm tra cứu cơ bản,
tương tự như cảnh giới tu vi (canh_gioi_tu_vi.py).
"""
from typing import Optional, Dict, Any, List

# Blueprint toàn bộ cảnh giới công pháp theo đúng thứ tự từ thấp đến cao
REALM_BLUEPRINT = [
    ("Công Pháp", [
        ("Hoàng Cấp", (None,)),
        ("Huyền Cấp", (None,)),
        ("Địa Cấp", (None,)),
        ("Thiên Cấp", (None,)),
        ("Thần Cấp", (None,)),
        ("Thánh Cấp", (None,)),
        ("Chí Tôn Cấp", (None,)),
        ("Đế Cấp", (None,)),
        ("Tiên Cấp", (None,)),
        ("Đạo Cấp", (None,)),
    ]),
]


def _build_realms() -> List[Dict[str, Any]]:
    """Xây dựng danh sách phẳng chứa tất cả các cấp cảnh giới công pháp."""
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


# Danh sách toàn bộ cảnh giới công pháp
REALMS: List[Dict[str, Any]] = _build_realms()
TOTAL_REALMS: int = len(REALMS)

# Bảng băm tra cứu theo ID và theo Tên
REALM_BY_ID: Dict[int, Dict[str, Any]] = {r["id"]: r for r in REALMS}
REALM_BY_NAME: Dict[str, Dict[str, Any]] = {r["name"]: r for r in REALMS}

# Alias ngữ nghĩa riêng cho công pháp
CONG_PHAP_REALMS = REALMS
SKILL_REALMS = REALMS
TOTAL_CONG_PHAP_REALMS = TOTAL_REALMS


# =============================================================================
# CÁC HÀM TRA CỨU CƠ BẢN
# =============================================================================

def get_all_realms() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách cảnh giới công pháp."""
    return REALMS


def get_realm_by_id(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới công pháp theo ID.
    Trả về None nếu ID không tồn tại.
    """
    return REALM_BY_ID.get(realm_id)


def get_realm_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới công pháp theo tên đầy đủ.
    Trả về None nếu tên không tồn tại.
    """
    return REALM_BY_NAME.get(name)


def get_next_realm(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy cảnh giới công pháp kế tiếp.
    Trả về None nếu đã ở cảnh giới cao nhất (hoặc realm_id không hợp lệ).
    """
    return REALM_BY_ID.get(realm_id + 1)


def is_max_realm(realm_id: int) -> bool:
    """Kiểm tra xem công pháp đã đạt cấp cao nhất chưa."""
    return realm_id >= TOTAL_REALMS


# Alias hàm tương thích theo ngữ nghĩa công pháp
get_all_cong_phap_realms = get_all_realms
get_cong_phap_realm_by_id = get_realm_by_id
get_cong_phap_realm_by_name = get_realm_by_name
get_next_cong_phap_realm = get_next_realm
is_max_cong_phap_realm = is_max_realm


if __name__ == "__main__":
    print(f"Tổng số cấp cảnh giới công pháp: {TOTAL_REALMS}")
    print(f"Cấp đầu tiên (id=1): {get_realm_by_id(1)}")
    print(f"Cấp cuối cùng (id={TOTAL_REALMS}): {get_realm_by_id(TOTAL_REALMS)}")
    print(f"Cảnh giới sau id=1: {get_next_realm(1)}")
    print(f"Cảnh giới sau id={TOTAL_REALMS}: {get_next_realm(TOTAL_REALMS)}")
