# -*- coding: utf-8 -*-
"""
canh_gioi_phap_bao.py
=====================
Lưu trữ toàn bộ danh sách cảnh giới pháp bảo trong hệ thống.
File này thuần túy lưu trữ dữ liệu cảnh giới và các hàm tra cứu cơ bản,
tương tự như cảnh giới binh khí (canh_gioi_binh_khi.py).
"""
from typing import Optional, Dict, Any, List

# Blueprint toàn bộ cảnh giới pháp bảo theo đúng thứ tự từ thấp đến cao (tương đồng binh khí)
REALM_BLUEPRINT = [
    ("Pháp Bảo", [
        ("Phàm Khí", (None,)),
        ("Hoàng Khí", (None,)),
        ("Thần Khí", (None,)),
        ("Thiên Thần Khí", (None,)),
        ("Chuẩn Thánh Khí", (None,)),
        ("Thánh Khí", (None,)),
        ("Chuẩn Chí Tôn Khí", (None,)),
        ("Chí Tôn Khí", (None,)),
        ("Chuẩn Đế Khí", (None,)),
        ("Đế Khí", (None,)),
        ("Văn Minh Chí Bảo", (None,)),
        ("Sơ Đại Văn Minh Chí Bảo", (None,)),
    ]),
]


def _build_realms() -> List[Dict[str, Any]]:
    """Xây dựng danh sách phẳng chứa tất cả các cấp cảnh giới pháp bảo."""
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


# Danh sách toàn bộ cảnh giới pháp bảo
REALMS: List[Dict[str, Any]] = _build_realms()
TOTAL_REALMS: int = len(REALMS)

# Bảng băm tra cứu theo ID và theo Tên
REALM_BY_ID: Dict[int, Dict[str, Any]] = {r["id"]: r for r in REALMS}
REALM_BY_NAME: Dict[str, Dict[str, Any]] = {r["name"]: r for r in REALMS}

# Bổ sung alias tra cứu thuận tiện (cả tên đuôi "Khí" lẫn "Bảo", và alias Thành Đạo Khí / Đế Bảo)
for r in REALMS:
    name = r["name"]
    # Nếu tên kết thúc bằng "Khí", thêm alias tương ứng kết thúc bằng "Bảo"
    if name.endswith("Khí"):
        bao_alias = name[:-3] + "Bảo"
        REALM_BY_NAME.setdefault(bao_alias, r)

    if r["minor_realm"] == "Đế Khí":
        REALM_BY_NAME["Thành Đạo Khí"] = r
        REALM_BY_NAME["Đế Khí ( Thành Đạo Khí )"] = r
        REALM_BY_NAME["Đế Khí (Thành Đạo Khí)"] = r
        REALM_BY_NAME["Đế Bảo"] = r

# Alias ngữ nghĩa riêng cho pháp bảo
PHAP_BAO_REALMS = REALMS
TREASURE_REALMS = REALMS
TOTAL_PHAP_BAO_REALMS = TOTAL_REALMS
TOTAL_TREASURE_REALMS = TOTAL_REALMS


# =============================================================================
# CÁC HÀM TRA CỨU CƠ BẢN
# =============================================================================

def get_all_realms() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách cảnh giới pháp bảo."""
    return REALMS


def get_realm_by_id(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới pháp bảo theo ID.
    Trả về None nếu ID không tồn tại.
    """
    return REALM_BY_ID.get(realm_id)


def get_realm_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới pháp bảo theo tên đầy đủ hoặc alias.
    Trả về None nếu tên không tồn tại.
    """
    return REALM_BY_NAME.get(name)


def get_next_realm(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy cảnh giới pháp bảo kế tiếp.
    Trả về None nếu đã ở cảnh giới cao nhất (hoặc realm_id không hợp lệ).
    """
    return REALM_BY_ID.get(realm_id + 1)


def is_max_realm(realm_id: int) -> bool:
    """Kiểm tra xem pháp bảo đã đạt phẩm cấp cao nhất chưa."""
    return realm_id >= TOTAL_REALMS


# Alias hàm tương thích theo ngữ nghĩa pháp bảo
get_all_phap_bao_realms = get_all_realms
get_phap_bao_realm_by_id = get_realm_by_id
get_phap_bao_realm_by_name = get_realm_by_name
get_next_phap_bao_realm = get_next_realm
is_max_phap_bao_realm = is_max_realm

get_all_treasure_realms = get_all_realms
get_treasure_realm_by_id = get_realm_by_id
get_treasure_realm_by_name = get_realm_by_name
get_next_treasure_realm = get_next_realm
is_max_treasure_realm = is_max_realm


if __name__ == "__main__":
    print(f"Tổng số cấp cảnh giới pháp bảo: {TOTAL_REALMS}")
    print(f"Cấp đầu tiên (id=1): {get_realm_by_id(1)}")
    print(f"Cấp cuối cùng (id={TOTAL_REALMS}): {get_realm_by_id(TOTAL_REALMS)}")
    print(f"Cảnh giới sau id=1: {get_next_realm(1)}")
    print(f"Cảnh giới sau id={TOTAL_REALMS}: {get_next_realm(TOTAL_REALMS)}")
    print(f"Tra cứu qua alias 'Thánh Bảo': {get_realm_by_name('Thánh Bảo')}")
    print(f"Tra cứu Đế Khí qua alias: {get_realm_by_name('Đế Khí')}")
