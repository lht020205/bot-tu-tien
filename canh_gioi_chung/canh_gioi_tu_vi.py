# -*- coding: utf-8 -*-
"""
canh_gioi_tu_vi.py
==================
Lưu trữ toàn bộ danh sách cảnh giới tu vi (tu tiên) theo hệ thống Tiên Nghịch:
- Nhất Bộ Cảnh (Tung Hoành Cảnh)
- Nhị Bộ Cảnh (Phi Thiên Cảnh)
- Tam Bộ Cảnh (Vô Biên Cảnh - Đại Năng Cảnh - Không Chi Tứ Cảnh - Niết Linh Huyền Kiếp)
- Tứ Bộ Cảnh (Đạp Thiên Cảnh - Không Diệt Cảnh - Siêu Thoát Cảnh)

File này thuần túy lưu trữ dữ liệu cảnh giới và các hàm tra cứu cơ bản,
không chứa logic tính EXP hay tỷ lệ đột phá để các file khác dễ dàng tái sử dụng.
"""
from typing import Optional, Dict, Any, List

# Các bộ giai đoạn dùng chung
STAGES_SO_TRUNG_HAU_VIEN_MAN = ("Sơ Kỳ", "Trung Kỳ", "Hậu Kỳ", "Viên Mãn")

STAGES_NGUNG_KHI = (
    "Tầng 1", "Tầng 2", "Tầng 3", "Tầng 4", "Tầng 5",
    "Tầng 6", "Tầng 7", "Tầng 8", "Tầng 9", "Tầng 10",
    "Tầng 11", "Tầng 12", "Tầng 13", "Tầng 14", "Tầng 15 (Viên Mãn)",
)

STAGES_Y_CANH = ("Tiểu Thành", "Đại Thành", "Viên Mãn")

STAGES_THIEN_NHAN_NGU_SUY = (
    "Đệ Nhất Suy / Đệ Nhất Chỉ",
    "Đệ Nhị Suy / Đệ Nhị Chỉ",
    "Đệ Tam Suy / Đệ Tam Chỉ",
    "Đệ Tứ Suy / Đệ Tứ Chỉ",
    "Đệ Ngũ Suy / Đệ Ngũ Chỉ",
)

STAGES_DAP_THIEN_CUU_KIEU = (
    "Nhất Kiều: Quy Tắc Thiên Địa",
    "Nhị Kiều: Đạp Thiên Nhãn",
    "Tam Kiều: Vấn Đạo Tâm",
    "Tứ Kiều: Chứng Đạo",
    "Ngũ Kiều: Súc Thế",
    "Lục Kiều: Thăng Thiên",
    "Thất Kiều: Vấn Thiên",
    "Bát Kiều: Vấn Thiên Viên Mãn",
    "Cửu Kiều: Đạp Thiên Đạo",
)

STAGES_TU_BO = ("Sơ Kỳ", "Trung Kỳ", "Hậu Kỳ", "Đỉnh Phong", "Cực Hạn")


# Blueprint toàn bộ cảnh giới theo đúng thứ tự từ thấp đến cao
REALM_BLUEPRINT = [
    # -------------------------------------------------------------
    # I - Nhất Bộ Cảnh ( Tung Hoành Cảnh )
    # -------------------------------------------------------------
    ("Nhất Bộ Cảnh ( Tung Hoành Cảnh )", [
        ("Ngưng Khí Kỳ / Linh Động Kỳ", STAGES_NGUNG_KHI),
        ("Trúc Cơ Kỳ", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Kết Đan Kỳ", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Nguyên Anh Kỳ", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Hóa Thần Kỳ", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Ý Cảnh", STAGES_Y_CANH),
        ("Anh Biến Kỳ", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Vấn Đỉnh Kỳ", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Âm Hư Cảnh", (None,)),
        ("Dương Thực Cảnh", (None,)),
    ]),

    # -------------------------------------------------------------
    # II - Nhị Bộ Cảnh ( Phi Thiên Cảnh )
    # -------------------------------------------------------------
    ("Nhị Bộ Cảnh ( Phi Thiên Cảnh )", [
        ("Khuy Niết Cảnh", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Tịnh Niết Cảnh", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Toái Niết Cảnh", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Thiên Nhân Ngũ Suy / Phá Không Ngũ Chỉ", STAGES_THIEN_NHAN_NGU_SUY),
    ]),

    # -------------------------------------------------------------
    # III - Tam Bộ ( Vô Biên Cảnh - Đại Năng Cảnh - Không Chi Tứ Cảnh - Niết Linh Huyền Kiếp )
    # -------------------------------------------------------------
    ("Tam Bộ ( Vô Biên Cảnh - Đại Năng Cảnh - Không Chi Tứ Cảnh - Niết Linh Huyền Kiếp )", [
        ("Không Niết Cảnh", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Không Linh Cảnh", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Không Huyền Cảnh", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Độ Huyền Kiếp (Ngoại Kiếp)", ("Tuyết Kiếp", "Phong Kiếp", "Lôi Kiếp")),
        ("Độ Huyền Kiếp (Nội Kiếp)", ("Trảm Ly Kiếp", "Huyết Ảnh Kiếp", "Vô Danh Kiếp (???)")),
        ("Độ Huyền Kiếp (Hồn Kiếp)", ("Thập Tức Khô Thần Kiếp", "Hồn Thọ Kiếp", "Luân Hồi Kiếp")),
        ("Không Kiếp Cảnh (Đại Tôn Cảnh)", ("Sơ Kỳ", "Trung Kỳ", "Hậu Kỳ")),
        ("Không Kiếp Cảnh (Kim Tôn Cảnh)", ("Hậu Kỳ Đỉnh Phong",)),
        ("Không Kiếp Cảnh (Thiên Tôn Cảnh)", ("Viên Mãn",)),
        ("Không Kiếp Cảnh (Dược Thiên Tôn Cảnh)", ("Siêu Việt Viên Mãn",)),
        ("Đại Thiên Tôn Cảnh", STAGES_SO_TRUNG_HAU_VIEN_MAN),
        ("Đạp Thiên Cửu Kiều ( Bán Bộ Đạp Thiên - Bán Bộ Siêu Thoát )", STAGES_DAP_THIEN_CUU_KIEU),
    ]),

    # -------------------------------------------------------------
    # IV - Tứ Bộ Cảnh ( Đạp Thiên Cảnh - Không Diệt Cảnh - Siêu Thoát Cảnh )
    # -------------------------------------------------------------
    ("Tứ Bộ Cảnh ( Đạp Thiên Cảnh - Không Diệt Cảnh - Siêu Thoát Cảnh )", [
        ("Đạp Thiên Cảnh", STAGES_TU_BO),
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

    # 1. Tra cứu theo tên rút gọn của Ngưng Khí / Linh Động
    if "Ngưng Khí Kỳ / Linh Động Kỳ" in minor and stage:
        REALM_BY_NAME.setdefault(f"Ngưng Khí Kỳ - {stage}", r)
        REALM_BY_NAME.setdefault(f"Linh Động Kỳ - {stage}", r)
        REALM_BY_NAME.setdefault(f"Ngưng Khí {stage}", r)
        REALM_BY_NAME.setdefault(f"Linh Động {stage}", r)

    # 2. Tra cứu theo tên rút gọn của Thiên Nhân Ngũ Suy / Phá Không Ngũ Chỉ
    if "Thiên Nhân Ngũ Suy" in minor and stage:
        suy_part, chi_part = stage.split(" / ")
        REALM_BY_NAME.setdefault(f"Thiên Nhân Ngũ Suy - {suy_part}", r)
        REALM_BY_NAME.setdefault(f"Phá Không Ngũ Chỉ - {chi_part}", r)
        REALM_BY_NAME.setdefault(suy_part, r)
        REALM_BY_NAME.setdefault(chi_part, r)

    # 3. Tra cứu theo từng Kiếp nạn cụ thể (Huyền Kiếp)
    if "Độ Huyền Kiếp" in minor and stage:
        REALM_BY_NAME.setdefault(stage, r)
        REALM_BY_NAME.setdefault(f"Huyền Kiếp - {stage}", r)
        if "Vô Danh Kiếp" in stage or "???" in stage:
            REALM_BY_NAME.setdefault("???", r)
            REALM_BY_NAME.setdefault("Kiếp Thứ 6", r)
            REALM_BY_NAME.setdefault("Kiếp Thứ Sáu", r)
            REALM_BY_NAME.setdefault("Vô Danh Kiếp", r)

    # 4. Tra cứu Không Kiếp Cảnh theo từng Tôn Vị
    if "Không Kiếp Cảnh" in minor:
        if "Đại Tôn Cảnh" in minor and stage:
            REALM_BY_NAME.setdefault(f"Đại Tôn Cảnh - {stage}", r)
            REALM_BY_NAME.setdefault(f"Đại Tôn - {stage}", r)
        elif "Kim Tôn Cảnh" in minor:
            REALM_BY_NAME.setdefault("Kim Tôn Cảnh", r)
            REALM_BY_NAME.setdefault("Kim Tôn", r)
        elif "Thiên Tôn Cảnh" in minor and "Đại Thiên Tôn" not in minor:
            REALM_BY_NAME.setdefault("Thiên Tôn Cảnh", r)
            REALM_BY_NAME.setdefault("Thiên Tôn", r)
        elif "Dược Thiên Tôn Cảnh" in minor:
            REALM_BY_NAME.setdefault("Dược Thiên Tôn Cảnh", r)
            REALM_BY_NAME.setdefault("Dược Thiên Tôn", r)

    # 5. Tra cứu Đạp Thiên Cửu Kiều theo tên kiều hoặc tên đạo
    if "Đạp Thiên Cửu Kiều" in minor and stage:
        kieu_part, dao_part = stage.split(": ")
        REALM_BY_NAME.setdefault(f"Đạp Thiên Cửu Kiều - {kieu_part}", r)
        REALM_BY_NAME.setdefault(kieu_part, r)
        REALM_BY_NAME.setdefault(dao_part, r)
        REALM_BY_NAME.setdefault(stage, r)
        if "Cửu Kiều" in kieu_part:
            REALM_BY_NAME.setdefault("Bán Bộ Đạp Thiên", r)
            REALM_BY_NAME.setdefault("Bán Bộ Siêu Thoát", r)

    # 6. Tra cứu Tứ Bộ Cảnh theo các tên gọi tương đương
    if "Tứ Bộ Cảnh" in r["major_realm"] and stage:
        REALM_BY_NAME.setdefault(f"Tứ Bộ Cảnh - {stage}", r)
        REALM_BY_NAME.setdefault(f"Không Diệt Cảnh - {stage}", r)
        REALM_BY_NAME.setdefault(f"Siêu Thoát Cảnh - {stage}", r)

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
    print(f"Tổng số cấp cảnh giới tu vi: {TOTAL_REALMS}")
    print(f"Cấp đầu tiên (id=1): {get_realm_by_id(1)}")
    print(f"Cấp cuối cùng (id={TOTAL_REALMS}): {get_realm_by_id(TOTAL_REALMS)}")
    print(f"Cảnh giới sau id=1: {get_next_realm(1)}")
    print(f"Cảnh giới sau id={TOTAL_REALMS}: {get_next_realm(TOTAL_REALMS)}")
    print("\n--- Test tra cứu linh hoạt ---")
    print(f"Tra cứu 'ngưng khí kỳ - tầng 1': {get_realm_by_name('ngưng khí kỳ - tầng 1')}")
    print(f"Tra cứu 'linh động kỳ - tầng 15 (viên mãn)': {get_realm_by_name('linh động kỳ - tầng 15 (viên mãn)')}")
    print(f"Tra cứu 'âm hư cảnh': {get_realm_by_name('âm hư cảnh')}")
    print(f"Tra cứu 'đệ nhất suy': {get_realm_by_name('đệ nhất suy')}")
    print(f"Tra cứu 'tuyết kiếp': {get_realm_by_name('tuyết kiếp')}")
    print(f"Tra cứu '???': {get_realm_by_name('???')}")
    print(f"Tra cứu 'kim tôn': {get_realm_by_name('kim tôn')}")
    print(f"Tra cứu 'cửu kiều': {get_realm_by_name('cửu kiều')}")
    print(f"Tra cứu 'đạp thiên cảnh - cực hạn': {get_realm_by_name('đạp thiên cảnh - cực hạn')}")
