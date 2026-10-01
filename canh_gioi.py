# -*- coding: utf-8 -*-
"""
canh_gioi.py
==============
Cấu trúc dữ liệu cốt lõi của hệ thống cảnh giới (Bot Tu Tiên).

Mỗi phần tử trong ``REALMS`` là MỘT cấp độ nhỏ nhất (tầng / kỳ), gồm các key:

    realm_id      (int)        Tăng dần từ 1. ID cao hơn = mạnh hơn.
    major_realm   (str)        Đại cảnh giới.      VD: "Phàm Cảnh"
    minor_realm   (str)        Tiểu cảnh giới.     VD: "Nhục Thân Cảnh"
    stage         (str|None)   Giai đoạn.          VD: "Sơ Kỳ", "Nhất Suy"
    name          (str)        Tên ghép hoàn chỉnh. VD: "Nhục Thân Cảnh - Sơ Kỳ"
    required_exp  (int)        Tu vi cần để đột phá LÊN cấp này.
                               (realm_id = 1 là cấp khởi đầu nên = 0)
    success_rate  (float)      Tỷ lệ đột phá thành công LÊN cấp này (0.01 -> 1.0).

    -- Key bổ sung (không bắt buộc dùng, nhưng giữ lại để không mất dữ liệu gốc) --
    realm_group   (str|None)   Nhóm cảnh giới, hiện chỉ dùng cho "Thiên Đạo Cảnh".
    aliases       (tuple)      Các tên gọi khác của tiểu cảnh giới.

Danh sách được SINH TỰ ĐỘNG từ ``REALM_BLUEPRINT`` (liệt kê đầy đủ toàn bộ
34 cảnh giới), nên muốn cân bằng lại game chỉ cần chỉnh các hằng số cấu hình
ngay bên dưới, không phải sửa tay hàng trăm dòng.
"""
from __future__ import annotations

from typing import Any, Optional

# =============================================================================
# 1. CẤU HÌNH CÂN BẰNG (chỉnh ở đây để tune game)
# =============================================================================
EXP_BASE = 100          # Tu vi cần để lên realm_id = 2
EXP_GROWTH = 1.18       # Mỗi cấp nhân thêm 18% -> cấp số nhân
EXP_SIG_DIGITS = 3      # Làm tròn 3 chữ số có nghĩa cho số đẹp (VD: 513000000000)

SUCCESS_START = 0.95    # Tỷ lệ đột phá lên realm_id = 2
SUCCESS_MIN = 0.01      # Tỷ lệ đột phá lên cấp cuối cùng
SUCCESS_CURVE = 1.5     # > 1: giảm nhanh ở đầu, chậm dần về cuối; = 1: giảm tuyến tính

# Giá trị `stage` cho cảnh giới không chia giai đoạn (Tàn Tiên Cảnh, ...).
# Đổi thành "Viên Mãn" nếu muốn -> name sẽ thành "Tàn Tiên Cảnh - Viên Mãn".
NO_STAGE: Optional[str] = None

# =============================================================================
# 2. CÁC BỘ GIAI ĐOẠN DÙNG CHUNG
# =============================================================================
STAGES_KY = ("Sơ Kỳ", "Trung Kỳ", "Hậu Kỳ", "Đỉnh Phong")

STAGES_TRONG_THIEN = (
    "Nhất Trọng Thiên", "Nhị Trọng Thiên", "Tam Trọng Thiên",
    "Tứ Trọng Thiên", "Ngũ Trọng Thiên", "Lục Trọng Thiên",
    "Thất Trọng Thiên", "Bát Trọng Thiên", "Cửu Trọng Thiên",
)

STAGES_DAI_DAO_TO = ("Sơ Thiệp", "Cố Nguyên", "Xá Vu", "Thăng Hoa", "Cực Tẫn", "Phá Toái")

# =============================================================================
# 3. BLUEPRINT: TOÀN BỘ CẢNH GIỚI (từ thấp đến cao)
# =============================================================================
THIEN_DAO_GROUP = "Thiên Đạo Cảnh"

# Tên gọi khác của Đại cảnh giới / Nhóm cảnh giới (giữ lại từ danh sách gốc)
MAJOR_REALM_ALIASES = {
    "Đạo Cảnh": ("Siêu Thoát Chi Lộ Cảnh",),
    "Đạo Tổ Cảnh": ("Vô Thượng Đạo Cảnh",),
}
REALM_GROUP_ALIASES = {
    THIEN_DAO_GROUP: ("Hằng Thiên Cảnh", "Dị Đạo Cảnh", "Phong Thiên Cảnh"),
}


def _minor(name: str, stages=None, aliases=(), group: Optional[str] = None) -> dict:
    """Khai báo một tiểu cảnh giới. `stages=None` nghĩa là không chia giai đoạn."""
    return {
        "name": name,
        "stages": tuple(stages) if stages else (NO_STAGE,),
        "aliases": tuple(aliases),
        "group": group,
    }


REALM_BLUEPRINT = (
    # ---------------------------------------------------------------- I
    ("Phàm Cảnh", (
        _minor("Nhục Thân Cảnh", STAGES_KY),
        _minor("Linh Hải Cảnh", STAGES_KY),
        _minor("Hồn Cung Cảnh", STAGES_KY),
        _minor("Thần Thông Cảnh", STAGES_KY),
        _minor("Đại Năng Cảnh", STAGES_KY, aliases=("Hoàng Chủ Cảnh",)),
        _minor("Thánh Chủ Cảnh", STAGES_KY),
        _minor("Phong Hầu Cảnh", STAGES_KY),
        _minor("Phong Vương Cảnh", STAGES_KY, aliases=("Vương Giả Cảnh",)),
    )),
    # --------------------------------------------------------------- II
    ("Thần Cảnh", (
        _minor("Hư Thần Cảnh", STAGES_KY),
        _minor("Chân Thần Cảnh", STAGES_KY),
        _minor("Thiên Thần Cảnh", STAGES_KY),
        _minor("Thần Vương Cảnh", STAGES_KY),
    )),
    # -------------------------------------------------------------- III
    ("Thánh Cảnh", (
        _minor("Chuẩn Thánh Cảnh", STAGES_KY, aliases=("Bán Thánh Cảnh",)),
        _minor("Thánh Nhân Cảnh", STAGES_KY),
        _minor("Chí Thánh Cảnh", STAGES_KY),
        _minor("Đại Thánh Cảnh", STAGES_KY),
    )),
    # --------------------------------------------------------------- IV
    ("Chí Tôn Lưỡng Cảnh", (
        _minor("Chuẩn Chí Tôn Cảnh", STAGES_TRONG_THIEN),
        _minor("Chí Tôn Cảnh", STAGES_TRONG_THIEN),
    )),
    # ---------------------------------------------------------------- V
    ("Đế Cảnh", (
        _minor("Chuẩn Đế Cảnh", STAGES_TRONG_THIEN),
        _minor("Đế Giả Cảnh", STAGES_TRONG_THIEN,
               aliases=("Niết Đạo Cảnh", "Thành Đạo Giả Cảnh")),
    )),
    # --------------------------------------------------------------- VI
    ("Tiên Cảnh", (
        _minor("Tàn Tiên Cảnh"),
        _minor("Chân Tiên Cảnh"),
        _minor("Chuẩn Tiên Vương Cảnh"),
        _minor("Tiên Vương Cảnh"),
        _minor("Chuẩn Tiên Đế Cảnh"),
        _minor("Tiên Đế Cảnh"),
    )),
    # -------------------------------------------------------------- VII
    ("Đạo Cảnh", (
        _minor("Hư Đạo Cảnh", ("Nhất Suy", "Nhị Suy", "Tam Suy")),
        _minor("Chân Đạo Cảnh", ("Tứ Suy", "Ngũ Suy", "Lục Suy")),
        _minor("Tổ Đạo Cảnh", ("Thất Suy", "Bát Suy", "Cửu Suy")),
    )),
    # ------------------------------------------------------------- VIII
    ("Đạo Tổ Cảnh", (
        _minor("Tiểu Đạo Tổ Cảnh", aliases=("Lộ Tẫn Cấp",)),
        _minor("Đại Đạo Tổ Cảnh", STAGES_DAI_DAO_TO,
               aliases=("Vô Thượng Phá Toái Cảnh", "Chân Lộ Lĩnh Vực Cảnh")),
    )),
    # --------------------------------------------------------------- IX
    ("Thiên Cảnh", (
        # 32. Thiên Đạo Cảnh (Hằng Thiên Cảnh / Dị Đạo Cảnh / Phong Thiên Cảnh)
        _minor("Thiên Nhân Cảnh", ("Nhất Trọng", "Nhị Trọng", "Tam Trọng"),
               group=THIEN_DAO_GROUP),
        _minor("Thiên Quân Cảnh", ("Tứ Trọng", "Ngũ Trọng", "Lục Trọng"),
               group=THIEN_DAO_GROUP),
        _minor("Thiên Vương Cảnh", ("Thất Trọng", "Bát Trọng", "Cửu Trọng"),
               group=THIEN_DAO_GROUP),
        _minor("Thiên Hoàng Cảnh", ("Thập Trọng", "Thập Nhất Trọng", "Thập Nhị Trọng"),
               group=THIEN_DAO_GROUP),
        _minor("Thiên Tổ Cảnh", ("Thập Tam Trọng",), group=THIEN_DAO_GROUP),
        # 33.
        _minor("Chân Tổ Cảnh",
               aliases=("Bổn Nguyên Chân Tổ Cảnh", "Hoá Thân Thiên Đạo Cảnh",
                        "Căn Nguyên Chân Lý Cảnh")),
        # 34.
        _minor("Tiêu Dao Tự Tại Đại La Cảnh"),
    )),
)

# =============================================================================
# 4. CÔNG THỨC SINH SỐ LIỆU
# =============================================================================


def _round_sig(value: float, digits: int = EXP_SIG_DIGITS) -> int:
    """Làm tròn về `digits` chữ số có nghĩa rồi trả về int."""
    return int(float(f"{value:.{digits}g}"))


def _calc_required_exp(realm_id: int) -> int:
    """Tu vi cần để lên `realm_id`: cấp số nhân. Cấp khởi đầu (id=1) = 0."""
    if realm_id <= 1:
        return 0
    return _round_sig(EXP_BASE * EXP_GROWTH ** (realm_id - 2))


def _calc_success_rate(realm_id: int, total: int) -> float:
    """Tỷ lệ đột phá lên `realm_id`: giảm dần từ SUCCESS_START về SUCCESS_MIN."""
    if realm_id <= 1:
        return 1.0
    t = (realm_id - 2) / (total - 2)  # 0.0 (id=2) -> 1.0 (id cuối)
    rate = SUCCESS_MIN + (SUCCESS_START - SUCCESS_MIN) * (1 - t) ** SUCCESS_CURVE
    return round(max(SUCCESS_MIN, min(1.0, rate)), 3)


def _build_realms() -> list[dict[str, Any]]:
    total = sum(len(m["stages"]) for _, minors in REALM_BLUEPRINT for m in minors)
    realms: list[dict[str, Any]] = []
    realm_id = 0

    for major_name, minors in REALM_BLUEPRINT:
        for minor in minors:
            for stage in minor["stages"]:
                realm_id += 1
                realms.append({
                    "realm_id": realm_id,
                    "major_realm": major_name,
                    "minor_realm": minor["name"],
                    "stage": stage,
                    "name": f'{minor["name"]} - {stage}' if stage else minor["name"],
                    "required_exp": _calc_required_exp(realm_id),
                    "success_rate": _calc_success_rate(realm_id, total),
                    "realm_group": minor["group"],
                    "aliases": minor["aliases"],
                })
    return realms


def _validate_realms(realms: list[dict[str, Any]]) -> None:
    """Kiểm tra tính toàn vẹn dữ liệu ngay khi import (fail sớm nếu cấu hình sai)."""
    if [r["realm_id"] for r in realms] != list(range(1, len(realms) + 1)):
        raise ValueError("realm_id phải liên tục từ 1 đến hết.")

    names = [r["name"] for r in realms]
    if len(set(names)) != len(names):
        raise ValueError("Tên cảnh giới (name) bị trùng lặp.")

    for prev, cur in zip(realms, realms[1:]):
        if cur["required_exp"] <= prev["required_exp"]:
            raise ValueError(f'required_exp không tăng dần tại {cur["name"]}.')
        if cur["success_rate"] > prev["success_rate"]:
            raise ValueError(f'success_rate tăng ngược tại {cur["name"]}.')

    for r in realms:
        if not (0.01 <= r["success_rate"] <= 1.0):
            raise ValueError(f'success_rate ngoài khoảng [0.01, 1.0] tại {r["name"]}.')


# =============================================================================
# 5. DỮ LIỆU CHÍNH + HELPER FUNCTIONS
# =============================================================================
REALMS: list[dict[str, Any]] = _build_realms()
_validate_realms(REALMS)

_REALM_BY_ID: dict[int, dict[str, Any]] = {r["realm_id"]: r for r in REALMS}

MIN_REALM_ID: int = REALMS[0]["realm_id"]
MAX_REALM_ID: int = REALMS[-1]["realm_id"]


def get_realm_info(realm_id: int) -> Optional[dict[str, Any]]:
    """
    Trả về toàn bộ thông tin của một cảnh giới theo `realm_id`.

    Trả về bản sao (copy) nên sửa dict kết quả sẽ không làm hỏng dữ liệu gốc.
    Trả về None nếu `realm_id` không tồn tại.
    """
    realm = _REALM_BY_ID.get(realm_id)
    return dict(realm) if realm is not None else None


def get_next_realm(current_realm_id: int) -> Optional[dict[str, Any]]:
    """
    Trả về thông tin cảnh giới liền kề tiếp theo (phục vụ logic đột phá).

    Trả về None nếu `current_realm_id` không hợp lệ hoặc đã ở cảnh giới cao nhất.
    """
    if current_realm_id not in _REALM_BY_ID:
        return None
    return get_realm_info(current_realm_id + 1)


if __name__ == "__main__":
    import json

    print(f"Tổng số cấp độ: {len(REALMS)} (realm_id {MIN_REALM_ID} -> {MAX_REALM_ID})\n")
    for rid in (1, 5, 33, 65, 101, 116, 135, MAX_REALM_ID):
        info = get_realm_info(rid)
        print(f'#{info["realm_id"]:>3} | {info["major_realm"]:<20} | {info["name"]:<50} '
              f'| exp={info["required_exp"]:>15,} | rate={info["success_rate"]:.3f}')

    print("\nNext của cấp cuối:", get_next_realm(MAX_REALM_ID))
    print("\nVí dụ một bản ghi:")
    print(json.dumps(get_realm_info(4), ensure_ascii=False, indent=2))