# -*- coding: utf-8 -*-
"""
canh_gioi_tu_vi.py
==================
Lưu trữ toàn bộ danh sách cảnh giới tu vi (tu tiên) của người chơi.
File này thuần túy lưu trữ dữ liệu cảnh giới và các hàm tra cứu cơ bản,
không chứa logic tính EXP hay tỷ lệ đột phá để các file khác (đột phá, hồ sơ...)
dễ dàng tái sử dụng.
"""
from typing import Optional, Dict, Any, List

# Các bộ giai đoạn dùng chung
STAGES_TU_KY = ("Sơ Kỳ", "Trung Kỳ", "Hậu Kỳ", "Đỉnh Phong")
STAGES_CUU_TRONG_THIEN = (
    "Nhất Trọng Thiên", "Nhị Trọng Thiên", "Tam Trọng Thiên",
    "Tứ Trọng Thiên", "Ngũ Trọng Thiên", "Lục Trọng Thiên",
    "Thất Trọng Thiên", "Bát Trọng Thiên", "Cửu Trọng Thiên",
)

# Blueprint toàn bộ cảnh giới theo đúng thứ tự từ thấp đến cao
REALM_BLUEPRINT = [
    # -------------------------------------------------------------
    # I - Phàm Cảnh
    # -------------------------------------------------------------
    ("Phàm Cảnh", [
        ("Nhục Thân Cảnh", STAGES_TU_KY),
        ("Linh Hải Cảnh", STAGES_TU_KY),
        ("Hồn Cung Cảnh", STAGES_TU_KY),
        ("Thần Thông Cảnh", STAGES_TU_KY),
        ("Hoàng Chủ Cảnh", STAGES_TU_KY),
        ("Thánh Chủ Cảnh", STAGES_TU_KY),
        ("Phong Hầu Cảnh", STAGES_TU_KY),
        ("Vương Giả Cảnh", STAGES_TU_KY),
    ]),

    # -------------------------------------------------------------
    # II - Thần Cảnh
    # -------------------------------------------------------------
    ("Thần Cảnh", [
        ("Hư Thần Cảnh", STAGES_TU_KY),
        ("Chân Thần Cảnh", STAGES_TU_KY),
        ("Thiên Thần Cảnh", STAGES_TU_KY),
        ("Thần Vương Cảnh", STAGES_TU_KY),
    ]),

    # -------------------------------------------------------------
    # III - Thánh Cảnh
    # -------------------------------------------------------------
    ("Thánh Cảnh", [
        ("Bán Thánh Cảnh", STAGES_TU_KY),
        ("Chuẩn Thánh Cảnh", STAGES_TU_KY),
        ("Thánh Nhân Cảnh", STAGES_TU_KY),
        ("Chí Thánh Cảnh", STAGES_TU_KY),
        ("Đại Thánh Cảnh", STAGES_TU_KY),
    ]),

    # -------------------------------------------------------------
    # IV - Chí Tôn Lưỡng Cảnh
    # -------------------------------------------------------------
    ("Chí Tôn Lưỡng Cảnh", [
        ("Chuẩn Chí Tôn Cảnh", STAGES_CUU_TRONG_THIEN),
        ("Chí Tôn Cảnh", STAGES_CUU_TRONG_THIEN),
    ]),

    # -------------------------------------------------------------
    # V - Đế Cảnh
    # -------------------------------------------------------------
    ("Đế Cảnh", [
        ("Chuẩn Đế Cảnh", STAGES_CUU_TRONG_THIEN),
        ("Đế Giả Cảnh", STAGES_CUU_TRONG_THIEN),
    ]),

    # -------------------------------------------------------------
    # VI - Tiên Cảnh
    # -------------------------------------------------------------
    ("Tiên Cảnh", [
        ("Tàn Tiên Cảnh", (None,)),
        ("Chân Tiên Cảnh", (None,)),
        ("Chuẩn Tiên Vương Cảnh", (None,)),
        ("Tiên Vương Cảnh", (None,)),
        ("Chuẩn Tiên Đế Cảnh", (None,)),
        ("Tiên Đế Cảnh", (None,)),
    ]),

    # -------------------------------------------------------------
    # VII - Đạo Cảnh
    # -------------------------------------------------------------
    ("Đạo Cảnh", [
        ("Hư Đạo Cảnh", ("Nhất Suy", "Nhị Suy", "Tam Suy")),
        ("Chân Đạo Cảnh", ("Tứ Suy", "Ngũ Suy", "Lục Suy")),
        ("Tổ Đạo Cảnh", ("Thất Suy", "Bát Suy", "Cửu Suy")),
    ]),

    # -------------------------------------------------------------
    # VIII - Vô Thượng Đạo Cảnh
    # -------------------------------------------------------------
    ("Vô Thượng Đạo Cảnh", [
        ("Tiểu Đạo Tổ Cảnh", (None,)),
        ("Đại Đạo Tổ Cảnh", ("Sơ Thiệp", "Cố Nguyên", "Xá Vu", "Thăng Hoa", "Cực Tẫn", "Phá Toái")),
    ]),

    # -------------------------------------------------------------
    # IX - Thiên Cảnh
    # -------------------------------------------------------------
    ("Thiên Cảnh", [
        ("Thiên Nhân Cảnh", ("Nhất Trọng", "Nhị Trọng", "Tam Trọng")),
        ("Thiên Quân Cảnh", ("Tứ Trọng", "Ngũ Trọng", "Lục Trọng")),
        ("Thiên Vương Cảnh", ("Thất Trọng", "Bát Trọng", "Cửu Trọng")),
        ("Thiên Hoàng Cảnh", ("Thập Trọng", "Thập Nhất Trọng", "Thập Nhị Trọng")),
        ("Thiên Tổ Cảnh", ("Thập Tam Trọng",)),
        ("Chân Tổ Cảnh", (None,)),
        ("Tiêu Dao Tự Tại Đại La Cảnh", (None,)),
    ]),
]


def _build_realms() -> List[Dict[str, Any]]:
    """Xây dựng danh sách phẳng chứa tất cả các tầng cảnh giới."""
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


# Danh sách toàn bộ cảnh giới
REALMS: List[Dict[str, Any]] = _build_realms()
TOTAL_REALMS: int = len(REALMS)

# Bảng băm tra cứu theo ID và theo Tên
REALM_BY_ID: Dict[int, Dict[str, Any]] = {r["id"]: r for r in REALMS}
REALM_BY_NAME: Dict[str, Dict[str, Any]] = {r["name"]: r for r in REALMS}


# =============================================================================
# CÁC HÀM TRA CỨU CƠ BẢN (DÙNG ĐỂ GỌI TRONG CÁC FILE KHÁC)
# =============================================================================

def get_all_realms() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách cảnh giới."""
    return REALMS


def get_realm_by_id(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới theo ID.
    Trả về None nếu ID không tồn tại.
    """
    return REALM_BY_ID.get(realm_id)


def get_realm_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới theo tên đầy đủ.
    Trả về None nếu tên không tồn tại.
    """
    return REALM_BY_NAME.get(name)


def get_next_realm(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy cảnh giới kế tiếp của một cảnh giới.
    Trả về None nếu đã ở cảnh giới cao nhất (hoặc realm_id không hợp lệ).
    """
    return REALM_BY_ID.get(realm_id + 1)


def is_max_realm(realm_id: int) -> bool:
    """Kiểm tra xem cảnh giới đã đạt đỉnh phong cao nhất chưa."""
    return realm_id >= TOTAL_REALMS


if __name__ == "__main__":
    print(f"Tổng số cấp cảnh giới: {TOTAL_REALMS}")
    print(f"Cấp đầu tiên (id=1): {get_realm_by_id(1)}")
    print(f"Cấp cuối cùng (id={TOTAL_REALMS}): {get_realm_by_id(TOTAL_REALMS)}")
    print(f"Cảnh giới sau id=1: {get_next_realm(1)}")
    print(f"Cảnh giới sau id={TOTAL_REALMS}: {get_next_realm(TOTAL_REALMS)}")
