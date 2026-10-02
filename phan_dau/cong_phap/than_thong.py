# -*- coding: utf-8 -*-
"""
than_thong.py
=============
Hệ thống Thần Thông / Pháp Thuật (Ngoại Công / Active Skills) trong Chu Thiên Vạn Giới:
- Kỹ năng chủ động tung ra trong lượt đánh (Turn) hoặc xâu chuỗi combo đấu pháp.
- Người chơi có thể trang bị nhiều thần thông cùng lúc, nhưng phải tiêu hao Chân Nguyên (LL) hoặc Khí Huyết (SL).

4 Nhóm Phân Loại Cơ Bản:
1. Công Kích Đơn Thể (Single-target): Dồn toàn bộ sát thương cực hạn vào 1 mục tiêu duy nhất.
   - Ví dụ: Tịch Diệt Nhất Chỉ (Tiêu hao 500 Chân Nguyên, gây 200% Pháp Công, bỏ qua 20% Pháp Phòng).
2. Công Kích Quần Thể (AoE): Tấn công đa mục tiêu, càn quét yêu thú và địch nhân.
   - Ví dụ: Vạn Kiếm Quy Tông (Tiêu hao 1000 Chân Nguyên, chia đều sát thương, xác suất gây Chảy máu DoT).
3. Khống Chế & Quấy Nhiễu (Crowd Control): Khóa chặt hành động, mê hoặc, phong bế đối phương.
   - Ví dụ: Huyễn Cảnh Mê Tung (Mê hoặc 1-2 lượt; phụ thuộc vào Thần Thức và Đạo Tâm).
4. Bổ Trợ & Phòng Ngự (Buff/Shield): Dựng khiên hộ thân, bộc phát tiềm năng sinh mệnh.
   - Ví dụ: Bát Quái Trận Đồ (Linh Thuẫn hấp thụ 5,000 sát thương trong 3 lượt).
   - Ví dụ: Huyết Tế Bạo Khí (Đốt 30% Khí Huyết đổi lấy +100% Pháp Công trong 2 lượt).
"""
from typing import Optional, Dict, Any, List, Tuple
import random


# =============================================================================
# HẰNG SỐ PHÂN LOẠI THẦN THÔNG
# =============================================================================
CAT_DON_THE = "cong_kich_don_the"
CAT_QUAN_THE = "cong_kich_quan_the"
CAT_KHONG_CHE = "khong_che_quay_nhieu"
CAT_BO_TRO = "bo_tro_phong_ngu"

THAN_THONG_CATEGORIES: Dict[str, Dict[str, Any]] = {
    CAT_DON_THE: {
        "key": CAT_DON_THE,
        "name": "Công Kích Đơn Thể",
        "icon": "🎯",
        "description": "Dồn sát thương cực đại vào một mục tiêu duy nhất, phá vỡ phòng ngự cá nhân.",
    },
    CAT_QUAN_THE: {
        "key": CAT_QUAN_THE,
        "name": "Công Kích Quần Thể (AoE)",
        "icon": "🌊",
        "description": "Tấn công diện rộng, càn quét đám đông yêu thú hoặc nhiều địch nhân cùng lúc.",
    },
    CAT_KHONG_CHE: {
        "key": CAT_KHONG_CHE,
        "name": "Khống Chế & Quấy Nhiễu (CC)",
        "icon": "🕸️",
        "description": "Tê liệt, mê hoặc, cấm xuất chiêu đối thủ dựa trên Thần Thức và Đạo Tâm.",
    },
    CAT_BO_TRO: {
        "key": CAT_BO_TRO,
        "name": "Bổ Trợ & Phòng Ngự (Buff/Shield)",
        "icon": "🛡️",
        "description": "Tạo màng chắn linh lực, hồi máu hoặc thiêu đốt sinh mạng bạo phát lực công kích.",
    },
}

# =============================================================================
# DANH SÁCH CHI TIẾT TẤT CẢ CÁC THẦN THÔNG
# =============================================================================
THAN_THONG_DATA: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # 1. CÔNG KÍCH ĐƠN THỂ (SINGLE-TARGET)
    # -------------------------------------------------------------------------
    {
        "id": 1,
        "key": "tich_diet_nhat_chi",
        "name": "Tịch Diệt Nhất Chỉ",
        "category": CAT_DON_THE,
        "element": "Ám",
        "icon": "👉",
        "cost_type": "chan_nguyen",
        "cost_value": 500,
        "cooldown_turns": 2,
        "damage_multiplier": 2.0,  # 200% Pháp Công
        "armor_pierce_percent": 20, # Bỏ qua 20% Pháp Phòng
        "description": "Dồn chân nguyên vào đầu ngón tay, điểm xuất một tia tịch diệt chỉ mang quy tắc hư vô hủy diệt sinh mệnh mục tiêu.",
        "effect_text": "Tiêu hao 500 Chân Nguyên, gây sát thương bằng 200% Pháp Công. Bỏ qua 20% Pháp Phòng của mục tiêu (Xuyên giáp).",
    },
    {
        "id": 2,
        "key": "dai_hoang_khau_than_chi",
        "name": "Đại Hoang Khâu Thần Chỉ",
        "category": CAT_DON_THE,
        "element": "Thể/Ma",
        "icon": "☝️",
        "cost_type": "hon_hop",
        "cost_value": 800,  # 800 Chân Nguyên + 10% Khí Huyết
        "cost_hp_percent": 10,
        "cooldown_turns": 3,
        "damage_multiplier": 3.0,  # 300% Vật Công
        "armor_pierce_percent": 30,
        "description": "Tuyệt kỹ cổ xưa ngưng tụ quyền ý vỡ trời, giáng xuống một chỉ như cột chống trời nghiền nát thân xác kẻ địch.",
        "effect_text": "Tiêu hao 800 Chân Nguyên và 10% Khí Huyết hiện tại, bộc phát đòn đánh bằng 300% Vật Công xuyên thấu 30% giáp.",
    },

    # -------------------------------------------------------------------------
    # 2. CÔNG KÍCH QUẦN THỂ (AOE)
    # -------------------------------------------------------------------------
    {
        "id": 3,
        "key": "van_kiem_quy_tong",
        "name": "Vạn Kiếm Quy Tông",
        "category": CAT_QUAN_THE,
        "element": "Kiếm",
        "icon": "🗡️",
        "cost_type": "chan_nguyen",
        "cost_value": 1000,
        "cooldown_turns": 3,
        "damage_multiplier": 1.5,  # 150% Pháp Công chia đều
        "bleed_rate": 40.0,        # 40% tỷ lệ gây Chảy Máu
        "bleed_turns": 3,
        "bleed_dot_percent": 5.0,  # Rút 5% HP mỗi lượt
        "description": "Hiệu triệu ngàn vạn đạo kiếm khí từ hư không giáng xuống như mưa bão, xé rách toàn bộ mục tiêu trong phạm vi.",
        "effect_text": "Tiêu hao 1000 Chân Nguyên, chia đều sát thương 150% Pháp Công cho toàn bộ kẻ địch. Có 40% xác suất gây hiệu ứng 'Chảy máu' (DoT rút 5% HP mỗi lượt trong 3 lượt).",
    },
    {
        "id": 4,
        "key": "liet_diem_phan_thien",
        "name": "Liệt Diễm Phần Thiên",
        "category": CAT_QUAN_THE,
        "element": "Hỏa",
        "icon": "🔥",
        "cost_type": "chan_nguyen",
        "cost_value": 750,
        "cooldown_turns": 2,
        "damage_multiplier": 1.3,
        "burn_rate": 50.0,
        "burn_turns": 2,
        "burn_dot_percent": 6.0,
        "description": "Triệu hồi biển lửa cuồn cuộn thiêu đốt vạn dặm, biến chiến trường thành lò luyện đan thiêu rụi toàn bộ kẻ thù.",
        "effect_text": "Tiêu hao 750 Chân Nguyên, gây 130% sát thương Pháp Công lan diện rộng và có 50% tỷ lệ gây bỏng thiêu đốt 6% HP trong 2 lượt.",
    },

    # -------------------------------------------------------------------------
    # 3. KHỐNG CHẾ & QUẤY NHIỄU (CROWD CONTROL)
    # -------------------------------------------------------------------------
    {
        "id": 5,
        "key": "huyen_canh_me_tung",
        "name": "Huyễn Cảnh Mê Tung",
        "category": CAT_KHONG_CHE,
        "element": "Ám",
        "icon": "🌀",
        "cost_type": "chan_nguyen",
        "cost_value": 400,
        "cooldown_turns": 3,
        "cc_type": "me_hoac",
        "cc_duration_turns": 2,
        "description": "Tạo ra ảo cảnh ma mị đánh vào tâm ma, khiến đối phương chìm đắm trong huyễn hoặc mà mất đi khả năng hành động.",
        "effect_text": "Gây trạng thái Mê Hoặc (Bỏ lượt) trong 1-2 turn. Nếu Thần Thức (ĐCX) của địch cao hơn người tung chiêu, kỹ năng bị vô hiệu hóa hoàn toàn.",
    },
    {
        "id": 6,
        "key": "dinh_than_chu",
        "name": "Định Thân Chú",
        "category": CAT_KHONG_CHE,
        "element": "Hỗn Độn",
        "icon": "✋",
        "cost_type": "chan_nguyen",
        "cost_value": 350,
        "cooldown_turns": 3,
        "cc_type": "te_liet",
        "cc_duration_turns": 1,
        "description": "Một chữ 'Định' phong tỏa toàn bộ nguyên thần và chân khí đối thủ, làm ngưng đọng thời không trong khoảnh khắc.",
        "effect_text": "Phong bế hành động của kẻ địch trong 1 lượt đấu. Yêu cầu Đạo Tâm (ĐT) của bản thân phải cao hơn mục tiêu.",
    },

    # -------------------------------------------------------------------------
    # 4. BỔ TRỢ & PHÒNG NGỰ (BUFF/SHIELD)
    # -------------------------------------------------------------------------
    {
        "id": 7,
        "key": "bat_quai_tran_do",
        "name": "Bát Quái Trận Đồ",
        "category": CAT_BO_TRO,
        "element": "Mộc",
        "icon": "☯️",
        "cost_type": "chan_nguyen",
        "cost_value": 600,
        "cooldown_turns": 4,
        "shield_value": 5000,
        "shield_turns": 3,
        "description": "Triển khai đồ hình bát quái dưới chân, dựng lên lồng chắn linh lực vững chắc như núi cao che chở cho bản thể.",
        "effect_text": "Kích hoạt Linh Thuẫn hấp thụ 5,000 điểm sát thương trong 3 lượt đấu.",
    },
    {
        "id": 8,
        "key": "huyet_te_bao_khi",
        "name": "Huyết Tế Bạo Khí",
        "category": CAT_BO_TRO,
        "element": "Huyết",
        "icon": "🩸",
        "cost_type": "khi_huyet",
        "cost_hp_percent": 30,  # Thiêu đốt 30% HP hiện tại
        "cooldown_turns": 4,
        "buff_pc_percent": 100, # Tăng 100% Pháp Công
        "buff_duration_turns": 2,
        "description": "Tự rạch da thịt thiêu đốt tinh huyết tổ truyền, đổi lấy luồng ma lực bạo phát cuồng dại trong thời gian ngắn ngủi.",
        "effect_text": "Thiêu đốt 30% Khí Huyết hiện tại để đổi lấy +100% Pháp Công trong 2 lượt tới (Con dao hai lưỡi của ma đạo).",
    },
]

# =============================================================================
# HỆ THỐNG TRA CỨU NHANH
# =============================================================================
THAN_THONG_BY_ID: Dict[int, Dict[str, Any]] = {tt["id"]: tt for tt in THAN_THONG_DATA}
THAN_THONG_BY_KEY: Dict[str, Dict[str, Any]] = {tt["key"]: tt for tt in THAN_THONG_DATA}
THAN_THONG_BY_CAT: Dict[str, List[Dict[str, Any]]] = {
    CAT_DON_THE: [tt for tt in THAN_THONG_DATA if tt["category"] == CAT_DON_THE],
    CAT_QUAN_THE: [tt for tt in THAN_THONG_DATA if tt["category"] == CAT_QUAN_THE],
    CAT_KHONG_CHE: [tt for tt in THAN_THONG_DATA if tt["category"] == CAT_KHONG_CHE],
    CAT_BO_TRO: [tt for tt in THAN_THONG_DATA if tt["category"] == CAT_BO_TRO],
}


# =============================================================================
# CÁC HÀM TIỆN ÍCH QUẢN LÝ VÀ TÍNH TOÁN THẦN THÔNG
# =============================================================================
def get_all_than_thong() -> List[Dict[str, Any]]:
    """Trả về danh sách toàn bộ thần thông."""
    return THAN_THONG_DATA


def get_than_thong_by_id(tt_id: int) -> Optional[Dict[str, Any]]:
    """Tra cứu thần thông theo ID."""
    return THAN_THONG_BY_ID.get(tt_id)


def get_than_thong_by_key(key: str) -> Optional[Dict[str, Any]]:
    """Tra cứu thần thông theo key (ví dụ: 'tich_diet_nhat_chi')."""
    return THAN_THONG_BY_KEY.get(key.strip().lower())


def get_than_thong_by_category(category: str) -> List[Dict[str, Any]]:
    """Lọc danh sách thần thông theo nhóm phân loại."""
    return THAN_THONG_BY_CAT.get(category.strip().lower(), [])


def kiem_tra_tieu_hao_thi_trien(than_thong_key: str, current_hp: int, current_mp: int) -> Tuple[bool, str]:
    """
    Kiểm tra xem tu sĩ có đủ Chân Nguyên (MP) hoặc Khí Huyết (HP) để tung chiêu hay không.
    """
    skill = get_than_thong_by_key(than_thong_key)
    if not skill:
        return False, "Không tìm thấy thần thông!"

    cost_type = skill.get("cost_type", "chan_nguyen")
    if cost_type == "chan_nguyen":
        cost_val = skill.get("cost_value", 0)
        if current_mp < cost_val:
            return False, f"Chân Nguyên không đủ! Cần {cost_val} Chân Nguyên, hiện có {current_mp}."
    elif cost_type == "khi_huyet":
        hp_pct = skill.get("cost_hp_percent", 0)
        cost_val = int(current_hp * hp_pct / 100)
        if current_hp <= cost_val:
            return False, f"Khí Huyết không đủ để thiêu đốt! Cần ít nhất {cost_val + 1} HP."
    elif cost_type == "hon_hop":
        cost_mp = skill.get("cost_value", 0)
        hp_pct = skill.get("cost_hp_percent", 0)
        cost_hp = int(current_hp * hp_pct / 100)
        if current_mp < cost_mp or current_hp <= cost_hp:
            return False, f"Khí huyết hoặc chân nguyên không đủ để thi triển tuyệt kỹ hỗn hợp!"

    return True, "Đủ điều kiện thi triển thần thông."


def tinh_ty_le_khong_che_thanh_cong(attacker_than_thuc: int, target_than_thuc: int, target_dao_tam: int) -> Tuple[bool, float]:
    """
    Tính toán tỷ lệ khống chế thành công dựa trên chênh lệch Thần Thức và Đạo Tâm của mục tiêu.
    Nếu Thần Thức của địch cao hơn người tung chiêu: Tỷ lệ khống chế = 0% (vô hiệu hóa).
    """
    if target_than_thuc > attacker_than_thuc:
        return False, 0.0

    chenh_lech = attacker_than_thuc - target_than_thuc
    ty_le_co_ban = 60.0 + (chenh_lech * 0.5)
    giam_tru_dao_tam = target_dao_tam * 0.3
    ty_le_chot = max(10.0, min(95.0, ty_le_co_ban - giam_tru_dao_tam))

    is_success = random.random() * 100 <= ty_le_chot
    return is_success, ty_le_chot
