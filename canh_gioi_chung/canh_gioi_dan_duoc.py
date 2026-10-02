# -*- coding: utf-8 -*-
"""
canh_gioi_dan_duoc.py
=====================
Lưu trữ toàn bộ danh sách phẩm cấp đan dược trong hệ thống:
1. Đan Dược (Phàm Đan): Nhất Phẩm ---> Thập Phẩm [Sơ Cấp --- Trung Cấp --- Cao Cấp]
2. Linh Đan: Bán Phẩm --- Nhất Phẩm ---> Thập Phẩm [Sơ Cấp --- Trung Cấp --- Cao Cấp]
3. Tiên Đan: Bán Phẩm --- Nhất Phẩm ---> Thập Phẩm [Sơ Cấp --- Trung Cấp --- Cao Cấp]

File này thuần túy lưu trữ dữ liệu cảnh giới và các hàm tra cứu cơ bản,
tương tự như các hệ thống cảnh giới khác trong canh_gioi_chung.
"""
from typing import Optional, Dict, Any, List

# Phẩm cấp chất lượng đan dược
STAGES_SO_TRUNG_CAO = ("Sơ Cấp", "Trung Cấp", "Cao Cấp")

# Blueprint đan dược theo đúng thứ tự từ thấp đến cao
REALM_BLUEPRINT = [
    # -------------------------------------------------------------
    # I - Đan Dược thường (Phàm Đan): Nhất Phẩm -> Thập Phẩm
    # -------------------------------------------------------------
    ("Đan Dược", [
        ("Nhất Phẩm", STAGES_SO_TRUNG_CAO),
        ("Nhị Phẩm", STAGES_SO_TRUNG_CAO),
        ("Tam Phẩm", STAGES_SO_TRUNG_CAO),
        ("Tứ Phẩm", STAGES_SO_TRUNG_CAO),
        ("Ngũ Phẩm", STAGES_SO_TRUNG_CAO),
        ("Lục Phẩm", STAGES_SO_TRUNG_CAO),
        ("Thất Phẩm", STAGES_SO_TRUNG_CAO),
        ("Bát Phẩm", STAGES_SO_TRUNG_CAO),
        ("Cửu Phẩm", STAGES_SO_TRUNG_CAO),
        ("Thập Phẩm", STAGES_SO_TRUNG_CAO),
    ]),

    # -------------------------------------------------------------
    # II - Linh Đan: Bán Phẩm, Nhất Phẩm -> Thập Phẩm
    # -------------------------------------------------------------
    ("Linh Đan", [
        ("Linh Đan - Bán Phẩm", (None,)),
        ("Linh Đan - Nhất Phẩm", STAGES_SO_TRUNG_CAO),
        ("Linh Đan - Nhị Phẩm", STAGES_SO_TRUNG_CAO),
        ("Linh Đan - Tam Phẩm", STAGES_SO_TRUNG_CAO),
        ("Linh Đan - Tứ Phẩm", STAGES_SO_TRUNG_CAO),
        ("Linh Đan - Ngũ Phẩm", STAGES_SO_TRUNG_CAO),
        ("Linh Đan - Lục Phẩm", STAGES_SO_TRUNG_CAO),
        ("Linh Đan - Thất Phẩm", STAGES_SO_TRUNG_CAO),
        ("Linh Đan - Bát Phẩm", STAGES_SO_TRUNG_CAO),
        ("Linh Đan - Cửu Phẩm", STAGES_SO_TRUNG_CAO),
        ("Linh Đan - Thập Phẩm", STAGES_SO_TRUNG_CAO),
    ]),

    # -------------------------------------------------------------
    # III - Tiên Đan: Bán Phẩm, Nhất Phẩm -> Thập Phẩm
    # -------------------------------------------------------------
    ("Tiên Đan", [
        ("Tiên Đan - Bán Phẩm", (None,)),
        ("Tiên Đan - Nhất Phẩm", STAGES_SO_TRUNG_CAO),
        ("Tiên Đan - Nhị Phẩm", STAGES_SO_TRUNG_CAO),
        ("Tiên Đan - Tam Phẩm", STAGES_SO_TRUNG_CAO),
        ("Tiên Đan - Tứ Phẩm", STAGES_SO_TRUNG_CAO),
        ("Tiên Đan - Ngũ Phẩm", STAGES_SO_TRUNG_CAO),
        ("Tiên Đan - Lục Phẩm", STAGES_SO_TRUNG_CAO),
        ("Tiên Đan - Thất Phẩm", STAGES_SO_TRUNG_CAO),
        ("Tiên Đan - Bát Phẩm", STAGES_SO_TRUNG_CAO),
        ("Tiên Đan - Cửu Phẩm", STAGES_SO_TRUNG_CAO),
        ("Tiên Đan - Thập Phẩm", STAGES_SO_TRUNG_CAO),
    ]),
]


def _build_realms() -> List[Dict[str, Any]]:
    """Xây dựng danh sách phẳng chứa tất cả các cấp phẩm đan dược."""
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


# Danh sách toàn bộ phẩm cấp đan dược
REALMS: List[Dict[str, Any]] = _build_realms()
TOTAL_REALMS: int = len(REALMS)

# Bảng băm tra cứu theo ID và theo Tên
REALM_BY_ID: Dict[int, Dict[str, Any]] = {r["id"]: r for r in REALMS}
REALM_BY_NAME: Dict[str, Dict[str, Any]] = {r["name"]: r for r in REALMS}

# Bổ sung alias thuận tiện
NUMBER_MAP = {
    "Nhất": "1", "Nhị": "2", "Tam": "3", "Tứ": "4", "Ngũ": "5",
    "Lục": "6", "Thất": "7", "Bát": "8", "Cửu": "9", "Thập": "10",
}

for r in REALMS:
    name = r["name"]
    major = r["major_realm"]
    minor = r["minor_realm"]
    stage = r["stage"]

    # 1. Tra cứu dạng bỏ dấu gạch ngang
    if stage:
        REALM_BY_NAME.setdefault(f"{minor} {stage}", r)
        REALM_BY_NAME.setdefault(f"{major} {minor} {stage}", r)

    # 2. Xử lý alias riêng cho Linh Đan & Tiên Đan
    if major in ("Linh Đan", "Tiên Đan"):
        if "Bán Phẩm" in minor:
            REALM_BY_NAME.setdefault(f"Bán Phẩm {major}", r)
            REALM_BY_NAME.setdefault(f"{major} Bán Phẩm", r)
        elif stage:
            # e.g. minor = "Linh Đan - Nhất Phẩm", stage = "Sơ Cấp"
            # alias: "Nhất Phẩm Linh Đan - Sơ Cấp", "Nhất Phẩm Linh Đan Sơ Cấp"
            prefix, pham = minor.split(" - ")
            REALM_BY_NAME.setdefault(f"{pham} {prefix} - {stage}", r)
            REALM_BY_NAME.setdefault(f"{pham} {prefix} {stage}", r)
            REALM_BY_NAME.setdefault(f"{prefix} {pham} {stage}", r)

            # Dạng số: "1 Phẩm Linh Đan", "Linh Đan 1 Phẩm Sơ Cấp"
            word = pham.replace(" Phẩm", "")
            if word in NUMBER_MAP:
                num = NUMBER_MAP[word]
                REALM_BY_NAME.setdefault(f"{prefix} {num} Phẩm {stage}", r)
                REALM_BY_NAME.setdefault(f"{prefix} {num} Phẩm - {stage}", r)
                REALM_BY_NAME.setdefault(f"{num} Phẩm {prefix} {stage}", r)
    elif major == "Đan Dược" and stage:
        # e.g. "Đan Dược Nhất Phẩm Sơ Cấp", "1 Phẩm Sơ Cấp"
        word = minor.replace(" Phẩm", "")
        if word in NUMBER_MAP:
            num = NUMBER_MAP[word]
            REALM_BY_NAME.setdefault(f"{num} Phẩm {stage}", r)
            REALM_BY_NAME.setdefault(f"{num} Phẩm - {stage}", r)

# Bảng tra cứu không phân biệt hoa thường
REALM_BY_LOWER: Dict[str, Dict[str, Any]] = {k.lower(): v for k, v in REALM_BY_NAME.items()}

# Alias ngữ nghĩa riêng cho đan dược
DAN_DUOC_REALMS = REALMS
PILL_REALMS = REALMS
ELIXIR_REALMS = REALMS
TOTAL_DAN_DUOC_REALMS = TOTAL_REALMS
TOTAL_PILL_REALMS = TOTAL_REALMS

# Tương thích ngược với di tích
DI_TICH_REALMS = REALMS
RELIC_REALMS = REALMS
RUINS_REALMS = REALMS
TOTAL_DI_TICH_REALMS = TOTAL_REALMS
TOTAL_RELIC_REALMS = TOTAL_REALMS


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

# Alias hàm tương thích ngược với di tích
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
    print(f"Tổng số cấp phẩm đan dược: {TOTAL_REALMS}")
    print(f"Cấp đầu tiên (id=1): {get_realm_by_id(1)}")
    print(f"Cấp cuối cùng (id={TOTAL_REALMS}): {get_realm_by_id(TOTAL_REALMS)}")
    print(f"Cảnh giới sau id=1: {get_next_realm(1)}")
    print(f"Cảnh giới sau id={TOTAL_REALMS}: {get_next_realm(TOTAL_REALMS)}")
    print("\n--- Test tra cứu linh hoạt ---")
    print(f"Tra cứu 'nhất phẩm - sơ cấp': {get_realm_by_name('nhất phẩm - sơ cấp')}")
    print(f"Tra cứu 'linh đan - bán phẩm': {get_realm_by_name('linh đan - bán phẩm')}")
    print(f"Tra cứu 'linh đan bán phẩm': {get_realm_by_name('linh đan bán phẩm')}")
    print(f"Tra cứu 'linh đan thập phẩm cao cấp': {get_realm_by_name('linh đan thập phẩm cao cấp')}")
    print(f"Tra cứu 'tiên đan 1 phẩm sơ cấp': {get_realm_by_name('tiên đan 1 phẩm sơ cấp')}")
    print(f"Tra cứu 'tiên đan - thập phẩm - cao cấp': {get_realm_by_name('tiên đan - thập phẩm - cao cấp')}")
