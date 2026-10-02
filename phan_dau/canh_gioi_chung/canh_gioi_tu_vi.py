# -*- coding: utf-8 -*-
"""
canh_gioi_tu_vi.py
==================
Lưu trữ toàn bộ danh sách cảnh giới tu vi (tu tiên) theo hệ thống Tiên Nghịch:
- Nhất Bộ Cảnh (Tung Hoành Cảnh)
- Nhị Bộ Cảnh (Phi Thiên Cảnh)
- Tam Bộ Cảnh (Vô Biên Cảnh - Không Chi Cảnh)
- Tứ Bộ Cảnh (Đạp Thiên Cảnh - Không Diệt Cảnh - Siêu Thoát Cảnh)
- Ngũ Bộ Cảnh (Vĩnh Hằng Cảnh)
- Lục Bộ Cảnh (Vô Cảnh - Cực Đạo Chi Đỉnh)

File này thuần túy lưu trữ dữ liệu cảnh giới và các hàm tra cứu cơ bản,
không chứa logic tính EXP hay tỷ lệ đột phá để các file khác dễ dàng tái sử dụng.
"""
from typing import Optional, Dict, Any, List

# Các bộ giai đoạn dùng chung
# 1. Bộ 4 tầng: Sơ Kỳ -> Trung Kỳ -> Hậu Kỳ -> Đỉnh Phong (Dùng từ Nhất Bộ đến Tứ Bộ Cảnh)
STAGES_SO_TRUNG_HAU_DINH_PHONG = ("Sơ Kỳ", "Trung Kỳ", "Hậu Kỳ", "Đỉnh Phong")

# 2. Bộ 6 tầng: Sơ Kỳ -> Trung Kỳ -> Hậu Kỳ -> Đỉnh Phong -> Viên Mãn -> Cực Hạn (Dùng cho Ngũ Bộ Cảnh)
STAGES_NGU_BO = ("Sơ Kỳ", "Trung Kỳ", "Hậu Kỳ", "Đỉnh Phong", "Viên Mãn", "Cực Hạn")


# Blueprint toàn bộ cảnh giới theo đúng thứ tự từ thấp đến cao
REALM_BLUEPRINT = [
    # -------------------------------------------------------------
    # I - Nhất Bộ Cảnh ( Tung Hoành Cảnh )
    # -------------------------------------------------------------
    ("Nhất Bộ Cảnh ( Tung Hoành Cảnh )", [
        ("Ngưng Khí Kỳ", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Trúc Cơ Kỳ", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Kết Đan Kỳ", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Nguyên Anh Kỳ", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Hóa Thần Kỳ", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Anh Biến Kỳ", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Vấn Đỉnh Kỳ", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Âm Hư Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Dương Thực Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
    ]),

    # -------------------------------------------------------------
    # II - Nhị Bộ Cảnh ( Phi Thiên Cảnh )
    # -------------------------------------------------------------
    ("Nhị Bộ Cảnh ( Phi Thiên Cảnh )", [
        ("Khuy Niết Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Tịnh Niết Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Toái Niết Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
    ]),

    # -------------------------------------------------------------
    # III - Tam Bộ Cảnh ( Vô Biên Cảnh - Không Chi Cảnh )
    # -------------------------------------------------------------
    ("Tam Bộ Cảnh ( Vô Biên Cảnh - Không Chi Cảnh )", [
        ("Không Niết Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Không Linh Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Không Huyền Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Đại Thiên Tôn Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
    ]),

    # -------------------------------------------------------------
    # IV - Tứ Bộ Cảnh ( Đạp Thiên - Không Diệt - Siêu Thoát )
    # -------------------------------------------------------------
    ("Tứ Bộ Cảnh ( Đạp Thiên Cảnh - Không Diệt Cảnh - Siêu Thoát Cảnh )", [
        ("Đạp Thiên Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Không Diệt Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
        ("Siêu Thoát Cảnh", STAGES_SO_TRUNG_HAU_DINH_PHONG),
    ]),

    # -------------------------------------------------------------
    # V - Ngũ Bộ Cảnh ( Vĩnh Hằng Cảnh )
    # -------------------------------------------------------------
    ("Ngũ Bộ Cảnh ( Vĩnh Hằng Cảnh )", [
        ("Vĩnh Hằng Cảnh", STAGES_NGU_BO),
    ]),

    # -------------------------------------------------------------
    # VI - Lục Bộ Cảnh ( Vô Cảnh - Cảnh Giới Tối Cao )
    # -------------------------------------------------------------
    ("Lục Bộ Cảnh ( Vô Cảnh )", [
        ("Vô Cảnh", (None,)),
    ]),
]


def _build_realms() -> List[Dict[str, Any]]:
    """Xây dựng danh sách phẳng chứa tất cả các tầng cảnh giới tu vi."""
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


# Danh sách toàn bộ cảnh giới tu vi
REALMS: List[Dict[str, Any]] = _build_realms()
TOTAL_REALMS: int = len(REALMS)

# Bảng băm tra cứu theo ID và theo Tên đầy đủ
REALM_BY_ID: Dict[int, Dict[str, Any]] = {r["id"]: r for r in REALMS}
REALM_BY_NAME: Dict[str, Dict[str, Any]] = {r["name"]: r for r in REALMS}

# Bổ sung các alias linh hoạt giúp tra cứu dễ dàng
for r in REALMS:
    name = r["name"]
    minor = r["minor_realm"]
    stage = r["stage"]
    major = r["major_realm"]

    # 1. Tra cứu theo tên rút gọn của Ngưng Khí
    if "Ngưng Khí Kỳ" in minor and stage:
        REALM_BY_NAME.setdefault(f"Ngưng Khí Kỳ - {stage}", r)
        REALM_BY_NAME.setdefault(f"Ngưng Khí - {stage}", r)
        REALM_BY_NAME.setdefault(f"Ngưng Khí {stage}", r)

    # 2. Tra cứu rút gọn cho Âm Hư Cảnh và Dương Thực Cảnh
    if "Âm Hư Cảnh" in minor and stage:
        REALM_BY_NAME.setdefault(f"Âm Hư - {stage}", r)
        REALM_BY_NAME.setdefault(f"Âm Hư {stage}", r)
    if "Dương Thực Cảnh" in minor and stage:
        REALM_BY_NAME.setdefault(f"Dương Thực - {stage}", r)
        REALM_BY_NAME.setdefault(f"Dương Thực {stage}", r)

    # 3. Tra cứu Tứ Bộ Cảnh theo các tên gọi
    if "Tứ Bộ Cảnh" in major and stage:
        REALM_BY_NAME.setdefault(f"{minor} {stage}", r)

    # 4. Tra cứu Ngũ Bộ Cảnh (Vĩnh Hằng Cảnh)
    if "Ngũ Bộ Cảnh" in major and stage:
        REALM_BY_NAME.setdefault(f"Vĩnh Hằng - {stage}", r)
        REALM_BY_NAME.setdefault(f"Vĩnh Hằng {stage}", r)
        REALM_BY_NAME.setdefault(f"Ngũ Bộ - {stage}", r)

    # 5. Tra cứu Lục Bộ Cảnh (Vô Cảnh)
    if "Vô Cảnh" in minor:
        REALM_BY_NAME.setdefault("Vô Cảnh", r)
        REALM_BY_NAME.setdefault("Lục Bộ", r)
        REALM_BY_NAME.setdefault("Lục Bộ Cảnh", r)

# Bảng tra cứu không phân biệt hoa thường
REALM_BY_LOWER: Dict[str, Dict[str, Any]] = {k.lower(): v for k, v in REALM_BY_NAME.items()}

# Alias ngữ nghĩa riêng cho tu vi
TU_VI_REALMS = REALMS
TOTAL_TU_VI_REALMS = TOTAL_REALMS


# =============================================================================
# CÁC HÀM TRA CỨU CƠ BẢN (DÙNG ĐỂ GỌI TRONG CÁC FILE KHÁC)
# =============================================================================

def get_all_realms() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách cảnh giới tu vi."""
    return REALMS


def get_realm_by_id(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới tu vi theo ID.
    Trả về None nếu ID không tồn tại.
    """
    return REALM_BY_ID.get(realm_id)


def get_realm_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Lấy thông tin cảnh giới tu vi theo tên đầy đủ hoặc alias (không phân biệt hoa thường).
    Trả về None nếu tên không tồn tại.
    """
    if not name:
        return None
    if name in REALM_BY_NAME:
        return REALM_BY_NAME[name]
    return REALM_BY_LOWER.get(name.strip().lower())


def get_next_realm(realm_id: int) -> Optional[Dict[str, Any]]:
    """
    Lấy cảnh giới tu vi kế tiếp của một cảnh giới.
    Trả về None nếu đã ở cảnh giới cao nhất (hoặc realm_id không hợp lệ).
    """
    return REALM_BY_ID.get(realm_id + 1)


def is_max_realm(realm_id: int) -> bool:
    """Kiểm tra xem tu vi đã đạt cảnh giới cao nhất chưa."""
    return realm_id >= TOTAL_REALMS


# Alias hàm tương thích theo ngữ nghĩa tu vi
get_all_tu_vi_realms = get_all_realms
get_tu_vi_realm_by_id = get_realm_by_id
get_tu_vi_realm_by_name = get_realm_by_name
get_next_tu_vi_realm = get_next_realm
is_max_tu_vi_realm = is_max_realm


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(f"Tổng số cấp cảnh giới tu vi: {TOTAL_REALMS}")
    print(f"Cấp đầu tiên (id=1): {get_realm_by_id(1)}")
    print(f"Cấp cuối cùng (id={TOTAL_REALMS}): {get_realm_by_id(TOTAL_REALMS)}")
    print(f"Cảnh giới sau id=1: {get_next_realm(1)}")
    print(f"Cảnh giới sau id={TOTAL_REALMS}: {get_next_realm(TOTAL_REALMS)}")
    print("\n--- Test tra cứu linh hoạt ---")
    print(f"Tra cứu 'ngưng khí kỳ - sơ kỳ': {get_realm_by_name('ngưng khí kỳ - sơ kỳ')}")
    print(f"Tra cứu 'âm hư - sơ kỳ': {get_realm_by_name('âm hư - sơ kỳ')}")
    print(f"Tra cứu 'dương thực - đỉnh phong': {get_realm_by_name('dương thực - đỉnh phong')}")
    print(f"Tra cứu 'không niết cảnh - đỉnh phong': {get_realm_by_name('không niết cảnh - đỉnh phong')}")
    print(f"Tra cứu 'đại thiên tôn cảnh - hậu kỳ': {get_realm_by_name('đại thiên tôn cảnh - hậu kỳ')}")
    print(f"Tra cứu 'đạp thiên cảnh - đỉnh phong': {get_realm_by_name('đạp thiên cảnh - đỉnh phong')}")
    print(f"Tra cứu 'không diệt cảnh - đỉnh phong': {get_realm_by_name('không diệt cảnh - đỉnh phong')}")
    print(f"Tra cứu 'siêu thoát cảnh - đỉnh phong': {get_realm_by_name('siêu thoát cảnh - đỉnh phong')}")
    print(f"Tra cứu 'vĩnh hằng cảnh - cực hạn': {get_realm_by_name('vĩnh hằng cảnh - cực hạn')}")
    print(f"Tra cứu 'vô cảnh': {get_realm_by_name('vô cảnh')}")
