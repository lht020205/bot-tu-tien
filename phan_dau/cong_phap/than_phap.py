# -*- coding: utf-8 -*-
"""
than_phap.py
============
Hệ thống Thân Pháp / Độn Thuật (Movement / Evasion Skills) trong Chu Thiên Vạn Giới:
- Quyết định khả năng sinh tồn khi chênh lệch cảnh giới, tác động trực tiếp vào chỉ số Tốc Độ (TĐ - Thân Pháp).

3 Cơ chế cốt lõi trong chiến đấu:
1. Xác định Thứ tự Xuất chiêu: Kẻ có Thân pháp (Tốc Độ) cao hơn sẽ giành quyền Tiên Thủ đánh trước.
2. Tỷ lệ Né Tránh (Dodge Rate): Khi né tránh thành công, đòn đánh của địch báo "Miss", hoàn toàn không nhận sát thương.
3. Tỷ lệ Độn tẩu (Escape): Khi gặp địch nhân quá mạnh, kích hoạt Độn Thuật bỏ chạy dựa trên chênh lệch Tốc Độ giữa 2 bên.

Sự Tiến Hóa Của Thân Pháp Theo 4 Giai Đoạn Cảnh Giới:
- Giai đoạn I (Luyện Khí / Trúc Cơ): Tật Phong Bộ, Lăng Ba Vi Bộ. Di chuyển cước bộ mặt đất, tăng cố định Tốc Độ, né tránh 5-10%.
- Giai đoạn II (Kết Đan / Nguyên Anh): Ngự Kiếm Thuật, Hóa Huyết Độn. Di chuyển trên không, tăng mạnh SPD; tiêu hao tinh huyết để bỏ trốn tỷ lệ cao, kèm hiệu ứng "Trọng thương".
- Giai đoạn III (Hóa Thần / Vấn Đỉnh): Súc Địa Thành Thốn. Thao túng không gian cục bộ, né đòn chí mạng 1 lần/trận, một bước thu hẹp vạn dặm thành một tấc.
- Giai đoạn IV (Nhị Bộ / Tam Bộ Cảnh): Thuấn Di, Tê Liệt Hư Không. Nhảy vọt qua các chiều không gian, né Thiên Kiếp, bỏ trốn 100% (trừ khi bị phong tỏa không gian).
"""
from typing import Optional, Dict, Any, List, Tuple
import random


# =============================================================================
# HẰNG SỐ 4 GIAI ĐOẠN TIẾN HÓA THÂN PHÁP
# =============================================================================
STAGE_BO_PHAP = "giai_doan_1_bo_phap"       # Luyện Khí / Trúc Cơ (Mặt đất)
STAGE_DON_THUAT = "giai_doan_2_don_thuat"   # Kết Đan / Nguyên Anh (Trên không)
STAGE_KHONG_GIAN = "giai_doan_3_khong_gian" # Hóa Thần / Vấn Đỉnh (Không gian cục bộ)
STAGE_THUAN_DI = "giai_doan_4_thuan_di"     # Nhị Bộ / Tam Bộ (Nhảy vọt chiều không gian)

STAGES_MAP = {
    STAGE_BO_PHAP: "Giai đoạn I: Luyện Khí / Trúc Cơ (Cước Bộ)",
    STAGE_DON_THUAT: "Giai đoạn II: Kết Đan / Nguyên Anh (Ngự Kiếm & Độn Thuật)",
    STAGE_KHONG_GIAN: "Giai đoạn III: Hóa Thần / Vấn Đỉnh (Thao Túng Không Gian)",
    STAGE_THUAN_DI: "Giai đoạn IV: Nhị Bộ / Tam Bộ Cảnh (Thuấn Di Hư Không)",
}

# =============================================================================
# DANH SÁCH CHI TIẾT TẤT CẢ CÁC THÂN PHÁP
# =============================================================================
THAN_PHAP_DATA: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # GIAI ĐOẠN I: LUYỆN KHÍ / TRÚC CƠ (DI CHUYỂN BẰNG CHÂN)
    # -------------------------------------------------------------------------
    {
        "id": 1,
        "key": "tat_phong_bo",
        "name": "Tật Phong Bộ",
        "stage": STAGE_BO_PHAP,
        "required_realm": "Ngưng Khí Sơ Kỳ",
        "icon": "🍃",
        "speed_bonus": 15,          # Tăng cố định 15 Tốc Độ
        "dodge_rate": 5.0,          # 5% tỷ lệ né tránh
        "escape_bonus": 10.0,       # +10% tỷ lệ chạy trốn
        "description": "Thân pháp nhập môn mượn sức gió dưới lòng bàn chân, cước bộ nhẹ nhàng thoăn thoắt trên mặt đất.",
        "effect_text": "Tăng cố định +15 Tốc Độ, gia tăng 5% Tỷ Lệ Né Tránh đòn đánh của kẻ địch.",
    },
    {
        "id": 2,
        "key": "lang_ba_vi_bo",
        "name": "Lăng Ba Vi Bộ",
        "stage": STAGE_BO_PHAP,
        "required_realm": "Trúc Cơ Sơ Kỳ",
        "icon": "🌊",
        "speed_bonus": 25,
        "dodge_rate": 10.0,         # 10% tỷ lệ né tránh
        "escape_bonus": 20.0,
        "description": "Bộ pháp dẫm lên sóng nước không chìm, thân hình uốn lượn như cánh nhạn lướt sóng né tránh công kích hiểm hóc.",
        "effect_text": "Tăng cố định +25 Tốc Độ, gia tăng 10% Tỷ Lệ Né Tránh.",
    },

    # -------------------------------------------------------------------------
    # GIAI ĐOẠN II: KẾT ĐAN / NGUYÊN ANH (DI CHUYỂN TRÊN KHÔNG)
    # -------------------------------------------------------------------------
    {
        "id": 3,
        "key": "ngu_kiem_thuat",
        "name": "Ngự Kiếm Thuật",
        "stage": STAGE_DON_THUAT,
        "required_realm": "Kết Đan Sơ Kỳ",
        "icon": "🗡️",
        "speed_bonus": 60,
        "dodge_rate": 20.0,
        "escape_bonus": 40.0,
        "description": "Nhân kiếm hợp nhất, đạp phi kiếm phá không bay lượn trên tầng mây, tốc độ vượt xa phàm nhân trên mặt đất.",
        "effect_text": "Tăng mạnh +60 Tốc Độ, 20% Tỷ Lệ Né Tránh. Có thể ngự kiếm bay qua các chướng ngại địa hình hiểm trở.",
    },
    {
        "id": 4,
        "key": "hoa_huyet_don",
        "name": "Hóa Huyết Độn",
        "stage": STAGE_DON_THUAT,
        "required_realm": "Nguyên Anh Sơ Kỳ",
        "icon": "🩸",
        "speed_bonus": 100,
        "dodge_rate": 25.0,
        "escape_bonus": 85.0,       # 85% tỷ lệ trốn thoát
        "has_debuff": True,
        "debuff_desc": "Bị hiệu ứng 'Trọng thương' (giảm 50% HP và suy yếu trong 10 phút sau khi thoát).",
        "description": "Bí thuật độn tẩu tà đạo, tự thiêu đốt một ngụm tinh huyết bản mệnh hóa thành một dải huyết quang xé gió bay xa ngàn dặm trong nháy mắt.",
        "effect_text": "Tăng vọt +100 Tốc Độ. Kích hoạt Độn Thuật tiêu hao tinh huyết để bỏ trốn với tỷ lệ thành công 85%, nhưng dính hiệu ứng Trọng Thương sau khi thoát.",
    },

    # -------------------------------------------------------------------------
    # GIAI ĐOẠN III: HÓA THẦN / VẤN ĐỈNH (THAO TÚNG KHÔNG GIAN CỤC BỘ)
    # -------------------------------------------------------------------------
    {
        "id": 5,
        "key": "suc_dia_thanh_thon",
        "name": "Súc Địa Thành Thốn",
        "stage": STAGE_KHONG_GIAN,
        "required_realm": "Hóa Thần Sơ Kỳ",
        "icon": "👣",
        "speed_bonus": 150,
        "dodge_rate": 35.0,
        "escape_bonus": 90.0,
        "cheat_death_dodge": True,   # Miễn tử né 1 lần sát thương chí mạng
        "description": "Đại thần thông không gian của tu sĩ Hóa Thần, bước một bước thu hẹp khoảng cách vạn dặm thành một tấc. Thần quỷ khó lường, thoắt ẩn thoắt hiện.",
        "effect_text": "Tăng +150 Tốc Độ, 35% Né Tránh. Sở hữu nội tại độc nhất: Tự động né tránh hoàn toàn đòn đánh chí mạng 1 lần duy nhất trong mỗi trận chiến!",
    },

    # -------------------------------------------------------------------------
    # GIAI ĐOẠN IV: NHỊ BỘ / TAM BỘ CẢNH (NHẢY VỌT CHIỀU KHÔNG GIAN)
    # -------------------------------------------------------------------------
    {
        "id": 6,
        "key": "thuan_di_thuat",
        "name": "Thuấn Di Thuật",
        "stage": STAGE_THUAN_DI,
        "required_realm": "Khuy Niết Sơ Kỳ (Nhị Bộ)",
        "icon": "⚡",
        "speed_bonus": 300,
        "dodge_rate": 50.0,
        "escape_bonus": 99.0,
        "dodge_heaven_tribulation": True,
        "description": "Thao túng quy tắc không gian tuyệt đối, cơ thể tức thời tan biến vào hư vô và xuất hiện tại tọa độ bất kỳ trong tinh vực. Tốc độ xuất chiêu gần như tuyệt đối, có thể né cả Thiên Kiếp.",
        "effect_text": "Tăng +300 Tốc Độ, 50% Né Tránh. Đạt tốc độ xuất chiêu tuyệt đối và có thể né tránh các đòn đánh Lôi Kiếp của Thiên Đạo.",
    },
    {
        "id": 7,
        "key": "te_liet_hu_khong",
        "name": "Tê Liệt Hư Không",
        "stage": STAGE_THUAN_DI,
        "required_realm": "Toái Niết / Không Niết Cảnh",
        "icon": "🌌",
        "speed_bonus": 500,
        "dodge_rate": 65.0,
        "escape_bonus": 100.0,       # 100% tỷ lệ bỏ trốn
        "description": "Dùng tay không xé rách hư không vô tận, bước qua khe nứt không gian để vượt qua các tinh cầu. Bỏ trốn thành công 100% trừ khi bị đối thủ dùng đại thần thông phong tỏa không gian.",
        "effect_text": "Tăng cực đại +500 Tốc Độ, 65% Né Tránh. Bỏ trốn thành công 100% khỏi mọi trận chiến trừ khi gặp kẻ địch phong tỏa không gian.",
    },
]

# =============================================================================
# HỆ THỐNG TRA CỨU NHANH
# =============================================================================
THAN_PHAP_BY_ID: Dict[int, Dict[str, Any]] = {tp["id"]: tp for tp in THAN_PHAP_DATA}
THAN_PHAP_BY_KEY: Dict[str, Dict[str, Any]] = {tp["key"]: tp for tp in THAN_PHAP_DATA}
THAN_PHAP_BY_STAGE: Dict[str, List[Dict[str, Any]]] = {
    STAGE_BO_PHAP: [tp for tp in THAN_PHAP_DATA if tp["stage"] == STAGE_BO_PHAP],
    STAGE_DON_THUAT: [tp for tp in THAN_PHAP_DATA if tp["stage"] == STAGE_DON_THUAT],
    STAGE_KHONG_GIAN: [tp for tp in THAN_PHAP_DATA if tp["stage"] == STAGE_KHONG_GIAN],
    STAGE_THUAN_DI: [tp for tp in THAN_PHAP_DATA if tp["stage"] == STAGE_THUAN_DI],
}


# =============================================================================
# CÁC HÀM TIỆN ÍCH QUẢN LÝ VÀ TÍNH TOÁN THÂN PHÁP
# =============================================================================
def get_all_than_phap() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách Thân Pháp."""
    return THAN_PHAP_DATA


def get_than_phap_by_id(tp_id: int) -> Optional[Dict[str, Any]]:
    """Tra cứu thân pháp theo ID."""
    return THAN_PHAP_BY_ID.get(tp_id)


def get_than_phap_by_key(key: str) -> Optional[Dict[str, Any]]:
    """Tra cứu thân pháp theo key (ví dụ: 'suc_dia_thanh_thon')."""
    return THAN_PHAP_BY_KEY.get(key.strip().lower())


def get_than_phap_by_stage(stage: str) -> List[Dict[str, Any]]:
    """Tra cứu thân pháp theo giai đoạn cảnh giới."""
    return THAN_PHAP_BY_STAGE.get(stage.strip().lower(), [])


def tinh_thu_tu_xuat_chieu(spd_tu_si_a: int, spd_tu_si_b: int) -> Tuple[str, int]:
    """
    Xác định ai là người xuất chiêu trước (Tiên Thủ) dựa trên Thân pháp (Tốc Độ).
    Trả về: (Người đánh trước: 'A' hoặc 'B', Chênh lệch tốc độ)
    """
    chenh_lech = abs(spd_tu_si_a - spd_tu_si_b)
    if spd_tu_si_a >= spd_tu_si_b:
        return "A", chenh_lech
    return "B", chenh_lech


def tinh_ty_le_ne_tranh(than_phap_key: str, spd_ban_than: int, spd_doi_thu: int) -> Tuple[bool, float]:
    """
    Tính toán tỷ lệ né tránh đòn đánh.
    Nếu né thành công, đòn đánh báo "Miss", hoàn toàn miễn nhiễm sát thương.
    """
    tp = get_than_phap_by_key(than_phap_key)
    base_dodge = tp["dodge_rate"] if tp else 5.0

    # Chênh lệch tốc độ hỗ trợ gia tăng hoặc giảm trừ tỷ lệ né
    diff = spd_ban_than - spd_doi_thu
    bonus_dodge = max(-15.0, min(30.0, diff * 0.1))
    final_dodge = max(5.0, min(80.0, base_dodge + bonus_dodge))

    is_dodged = random.random() * 100 <= final_dodge
    return is_dodged, final_dodge


def tinh_ty_le_don_tau(than_phap_key: str, spd_ban_than: int, spd_doi_thu: int, is_space_locked: bool = False) -> Tuple[bool, str, float]:
    """
    Tính toán tỷ lệ bỏ trốn (Độn tẩu / Escape) khi đối đầu kẻ địch mạnh hoặc bị cướp tiêu.
    Nếu bị phong tỏa không gian: không thể tẩu thoát bằng thân pháp thông thường.
    """
    if is_space_locked:
        return False, "Không gian xung quanh đã bị kẻ địch phong tỏa hoàn toàn! Không thể độn tẩu!", 0.0

    tp = get_than_phap_by_key(than_phap_key)
    base_escape = tp["escape_bonus"] if tp else 30.0

    if base_escape >= 100.0:
        return True, "Kích hoạt Tê Liệt Hư Không, bước vào khe nứt không gian trốn thoát 100% thành công!", 100.0

    diff = spd_ban_than - spd_doi_thu
    adjusted_rate = max(10.0, min(95.0, base_escape + (diff * 0.2)))

    is_escaped = random.random() * 100 <= adjusted_rate
    if is_escaped:
        msg = f"Độn tẩu thành công! (Tỷ lệ: {adjusted_rate:.1f}%)"
        if tp and tp.get("has_debuff"):
            msg += f" [Cảnh báo: {tp['debuff_desc']}]"
        return True, msg, adjusted_rate
    else:
        return False, f"Độn tẩu thất bại! Kẻ địch quá nhanh đã chặn đứng đường lui! (Tỷ lệ: {adjusted_rate:.1f}%)", adjusted_rate
