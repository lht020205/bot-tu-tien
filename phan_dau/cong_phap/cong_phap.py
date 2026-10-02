# -*- coding: utf-8 -*-
"""
cong_phap.py
============
Hệ thống Công Pháp Chủ Tu (Nội Công / Passive Engine) trong Chu Thiên Vạn Giới:
- Đây là gốc rễ của người tu tiên: Mỗi nhân vật chỉ được phép trang bị duy nhất 1 Công Pháp Chủ Tu tại một thời điểm.
- Việc thay đổi công pháp (Phế tu vi tu lại) sẽ tốn rất nhiều tài nguyên và đan dược bồi bổ.

Cơ chế hoạt động cốt lõi:
1. Định hình Thuộc tính: Quyết định hệ linh lực của tu sĩ (Băng, Hỏa, Lôi, Mộc, Ám, Huyết, Kiếm, Thể...).
   - Dùng thần thông cùng hệ với Công Pháp Chủ Tu sẽ kích hoạt "Cộng Hưởng Linh Lực" (tăng +30% uy lực sát thương).
2. Chỉ số Thụ động (Passive Buffs): Cung cấp các chỉ số cộng thẳng hoặc hệ số nhân (%) cho Khí Huyết (SL), Chân Nguyên (LL), Vật Phòng (VP), Pháp Phòng (PP)...
3. Giới hạn Cảnh giới: Mỗi công pháp có giới hạn cảnh giới tối đa có thể dẫn dắt tu luyện (Trúc Cơ, Nguyên Anh, Vấn Đỉnh, Toái Niết, Vô Cảnh). Muốn đột phá cao hơn phải tìm công pháp cấp cao tương ứng.
"""
from typing import Optional, Dict, Any, List, Tuple


# =============================================================================
# HẰNG SỐ HỆ THUỘC TÍNH LINH LỰC
# =============================================================================
HE_MOC = "Mộc"
HE_HOA = "Hỏa"
HE_BANG = "Băng"
HE_LOI = "Lôi"
HE_AM = "Ám"
HE_HUYET = "Huyết"
HE_KIEM = "Kiếm"
HE_THE_MA = "Thể/Ma"
HE_HON_DON = "Hỗn Độn"

# Hệ số tăng sát thương khi thần thông cùng hệ với công pháp chủ tu
CONG_HUONG_HE_BONUS = 0.30  # +30% sát thương

# =============================================================================
# DANH SÁCH CHI TIẾT CÁC CÔNG PHÁP CHỦ TU
# =============================================================================
CONG_PHAP_DATA: List[Dict[str, Any]] = [
    {
        "id": 1,
        "key": "thanh_mộc_truong_sinh_quyet",
        "name": "Thanh Mộc Trường Sinh Quyết",
        "element": HE_MOC,
        "rank": "Địa Giai Thượng Phẩm",
        "icon": "🌿",
        "max_realm_id": 20,  # Tu luyện tối đa đến Hóa Thần Đỉnh Phong
        "max_realm_name": "Hóa Thần Kỳ",
        "description": "Tâm pháp thượng thừa của Mộc Tộc, dẫn dắt linh khí thảo mộc trời đất nuôi dưỡng sinh cơ, kéo dài tuổi thọ và hồi phục thương thế cực nhanh.",
        "passive_buffs": {
            "sl_percent": 20,       # +20% Sinh Lực / Thọ Nguyên tối đa
            "hoi_hp_turn": 5.0,     # Tự động hồi phục 5% Khí Huyết mỗi lượt
            "pp_percent": 15,       # +15% Pháp Phòng
        },
        "hieu_ung_dac_biet": "Tăng 20% Thọ Nguyên tối đa. Mỗi lượt (turn) tự động hồi phục 5% Khí Huyết. Phù hợp nhất cho Dược Mộc Tộc.",
        "suitable_toc": ["Dược Mộc Tộc", "Thánh Yêu Tộc"],
    },
    {
        "id": 2,
        "key": "cuu_chuyen_ma_cong",
        "name": "Cửu Chuyển Ma Công",
        "element": HE_THE_MA,
        "rank": "Địa Giai Cực Phẩm",
        "icon": "🗿",
        "max_realm_id": 28,  # Tu luyện tối đa đến Vấn Đỉnh Đỉnh Phong
        "max_realm_name": "Vấn Đỉnh Kỳ",
        "description": "Tà công rèn luyện thể phách cuồng bạo của Cổ Ma và Thể Tu, đập tan kinh mạch pháp thuật để chuyển hóa toàn bộ linh lực thành sức mạnh cơ bắp đao thương bất nhập.",
        "passive_buffs": {
            "convert_pc_to_vc": 50,  # Chuyển hóa 50% Pháp Công thành Vật Công
            "vp_percent": 60,        # +60% Hộ Thể Cương Khí (Vật Phòng)
            "sl_percent": 30,        # +30% Sinh Lực
            "exp_rate": -0.20,       # Giảm 20% tốc độ hấp thụ linh khí tĩnh tọa
        },
        "hieu_ung_dac_biet": "Chuyển hóa 50% Pháp Công (MATK) thành Vật Công (ATK). Tăng cực mạnh Hộ Thể Cương Khí (DEF) nhưng làm giảm 20% tốc độ hấp thụ linh khí thiên địa.",
        "suitable_toc": ["Cổ Ma Tộc", "Cổ Thần Tộc"],
    },
    {
        "id": 3,
        "key": "thai_thuong_kiem_dien",
        "name": "Thái Thượng Kiếm Điển",
        "element": HE_KIEM,
        "rank": "Thiên Giai Hạ Phẩm",
        "icon": "⚔️",
        "max_realm_id": 40,  # Tu luyện tối đa đến Khuy Niết Đỉnh Phong (Nhị Bộ)
        "max_realm_name": "Khuy Niết Cảnh",
        "description": "Kiếm điển tuyệt đỉnh của kiếm tu thượng cổ, tôn sùng duy nhất một thanh kiếm phá vạn pháp. Hoàn toàn vứt bỏ phòng thủ để đổi lấy sát thương bộc phát chí mạng.",
        "passive_buffs": {
            "bk_bonus": 35.0,        # +35% Tỷ lệ Bạo Kích
            "bt_bonus": 80.0,        # +80% Sát thương Bạo Thương
            "sl_percent": 0,         # Không tăng Khí Huyết
            "vp_percent": 0,         # Không tăng Vật Phòng
        },
        "hieu_ung_dac_biet": "Không tăng Khí Huyết hay Phòng ngự, dồn 100% sức mạnh vào việc tăng Bạo Kích (Tỉ lệ chí mạng) và Bạo Thương (Sát thương chí mạng).",
        "suitable_toc": ["Thượng Tiên Tộc", "Thánh Yêu Tộc"],
    },
    {
        "id": 4,
        "key": "cuu_u_hoang_tuyen_kinh",
        "name": "Cửu U Hoàng Tuyền Kinh",
        "element": HE_AM,
        "rank": "Thiên Giai Trung Phẩm",
        "icon": "🌌",
        "max_realm_id": 48,  # Tu luyện tối đa đến Tịnh Niết Đỉnh Phong (Nhị Bộ)
        "max_realm_name": "Tịnh Niết Cảnh",
        "description": "Kinh văn bắt nguồn từ U Minh Tử Giới, dẫn dắt tử khí hoàng tuyền ăn mòn nguyên thần đối phương, đòn đánh u minh quỷ quyệt không thể phòng bị.",
        "passive_buffs": {
            "pc_percent": 40,        # +40% Pháp Công
            "xuyen_pp": 25,          # Bỏ qua 25% Pháp Phòng kẻ địch
            "dcx_bonus": 20,         # +20 Thần Thức (Độ Chính Xác)
        },
        "hieu_ung_dac_biet": "Đòn đánh kèm theo tử khí ăn mòn. Tăng +40% Pháp Công (PC) và bỏ qua 25% Pháp Phòng của mục tiêu.",
        "suitable_toc": ["U Hồn Tộc"],
    },
    {
        "id": 5,
        "key": "huyet_hai_vo_bien_quyet",
        "name": "Huyết Hải Vô Biên Quyết",
        "element": HE_HUYET,
        "rank": "Địa Giai Thượng Phẩm",
        "icon": "🩸",
        "max_realm_id": 24,  # Tu luyện tối đa đến Anh Biến Đỉnh Phong
        "max_realm_name": "Anh Biến Kỳ",
        "description": "Bí pháp ma đạo luyện huyết hóa khí, biến huyết mạch toàn thân thành một vùng huyết hải cuộn trào, càng đổ máu thì sát thương bộc phát càng khủng khiếp.",
        "passive_buffs": {
            "lifesteal": 30.0,       # +30% Hút Máu (Lifesteal)
            "sl_percent": 25,        # +25% Sinh Lực tối đa
        },
        "hieu_ung_dac_biet": "Sở hữu 30% Hút Máu (Lifesteal) sát thương tạo ra. Sinh lực càng dồi dào thì uy lực chiêu thức hệ Huyết càng bạo phát.",
        "suitable_toc": ["Huyết Sát Tộc"],
    },
    {
        "id": 6,
        "key": "cuu_thien_dan_loi_chan_quyet",
        "name": "Cửu Thiên Dẫn Lôi Chân Quyết",
        "element": HE_LOI,
        "rank": "Thiên Giai Thượng Phẩm",
        "icon": "⚡",
        "max_realm_id": 52,  # Tu luyện tối đa đến Toái Niết Đỉnh Phong (Nhị Bộ)
        "max_realm_name": "Toái Niết Cảnh",
        "description": "Chính đạo tuyệt học dẫn cửu thiên thần lôi nhập thể rèn thần hồn, linh lực biến thành cương lôi lấp lánh, tốc độ xuất chiêu nhanh như điện chớp.",
        "passive_buffs": {
            "td_percent": 30,        # +30% Tốc Độ xuất chiêu
            "pc_percent": 25,        # +25% Pháp Công
            "te_liet_rate": 20.0,    # 20% tỷ lệ làm tê liệt đối phương
        },
        "hieu_ung_dac_biet": "Tăng 30% Tốc Độ (TĐ), đòn đánh có 20% xác suất làm tê liệt (giảm 50% TĐ của địch trong 2 lượt).",
        "suitable_toc": ["Thượng Tiên Tộc", "Thánh Yêu Tộc"],
    },
    {
        "id": 7,
        "key": "han_bang_quyet",
        "name": "Hàn Băng Quyết (Cơ Bản)",
        "element": HE_BANG,
        "rank": "Hoàng Giai Hạ Phẩm",
        "icon": "❄️",
        "max_realm_id": 8,   # Tu luyện tối đa đến Trúc Cơ Đỉnh Phong
        "max_realm_name": "Trúc Cơ Kỳ",
        "description": "Công pháp nhập môn cơ bản ngưng tụ hàn khí, thích hợp cho người mới bước vào tu đạo. Giới hạn tu vi chỉ đến Trúc Cơ Kỳ, muốn lên Kết Đan bắt buộc phải đổi công pháp.",
        "passive_buffs": {
            "pc_percent": 10,        # +10% Pháp Công hệ Băng
            "pp_percent": 10,        # +10% Pháp Phòng
        },
        "hieu_ung_dac_biet": "Tăng nhẹ 10% Pháp Công hệ Băng. Giới hạn cảnh giới tối đa là Trúc Cơ Kỳ.",
        "suitable_toc": ["Thượng Tiên Tộc"],
    },
    {
        "id": 8,
        "key": "thai_co_ban_nguyen_kinh",
        "name": "Thái Cổ Bản Nguyên Kinh",
        "element": HE_HON_DON,
        "rank": "Thần Giai Vô Thượng",
        "icon": "🌌",
        "max_realm_id": 83,  # Tu luyện đến tận Vô Cảnh
        "max_realm_name": "Vô Cảnh",
        "description": "Kinh văn tối thượng thai nghén trong thuở hồng mông sơ khai, dung hợp vạn vật linh khí thành Hỗn Độn Bản Nguyên, có thể cộng hưởng với bất kỳ hệ thần thông nào.",
        "passive_buffs": {
            "all_stats_percent": 50, # +50% toàn bộ chỉ số chiến đấu
            "sl_percent": 50,
            "ll_percent": 50,
            "vc_percent": 50,
            "pc_percent": 50,
            "vp_percent": 50,
            "pp_percent": 50,
        },
        "hieu_ung_dac_biet": "Tăng 50% toàn bộ thuộc tính cơ bản và chiến đấu. Tự động kích hoạt +30% cộng hưởng linh lực với TẤT CẢ các hệ thần thông.",
        "suitable_toc": ["Thượng Tiên Tộc", "Cổ Thần Tộc", "Cổ Ma Tộc", "U Hồn Tộc"],
    },
]

# =============================================================================
# HỆ THỐNG TRA CỨU NHANH
# =============================================================================
CONG_PHAP_BY_ID: Dict[int, Dict[str, Any]] = {cp["id"]: cp for cp in CONG_PHAP_DATA}
CONG_PHAP_BY_KEY: Dict[str, Dict[str, Any]] = {cp["key"]: cp for cp in CONG_PHAP_DATA}


# =============================================================================
# CÁC HÀM TIỆN ÍCH QUẢN LÝ CÔNG PHÁP
# =============================================================================
def get_all_cong_phap() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách Công Pháp Chủ Tu."""
    return CONG_PHAP_DATA


def get_cong_phap_by_id(cp_id: int) -> Optional[Dict[str, Any]]:
    """Tra cứu công pháp theo ID."""
    return CONG_PHAP_BY_ID.get(cp_id)


def get_cong_phap_by_key(key: str) -> Optional[Dict[str, Any]]:
    """Tra cứu công pháp theo key (ví dụ: 'thanh_mộc_truong_sinh_quyet')."""
    return CONG_PHAP_BY_KEY.get(key.strip().lower())


def get_cong_phap_by_element(element: str) -> List[Dict[str, Any]]:
    """Lọc danh sách công pháp theo hệ linh lực (Băng, Hỏa, Mộc, Kiếm...)."""
    el = element.strip().lower()
    return [cp for cp in CONG_PHAP_DATA if el in cp["element"].lower()]


def tinh_sat_thuong_cong_huong(cong_phap_key: str, than_thong_element: str) -> Tuple[bool, float]:
    """
    Kiểm tra và tính toán hệ số cộng hưởng giữa Công Pháp Chủ Tu và Thần Thông.
    Nếu cùng hệ hoặc Công pháp là Hỗn Độn: Tăng +30% sát thương (hệ số 1.30).
    Trả về: (Có cộng hưởng không, Hệ số nhân sát thương)
    """
    cp = get_cong_phap_by_key(cong_phap_key)
    if not cp:
        return False, 1.0

    cp_element = cp["element"]
    if cp_element == HE_HON_DON or cp_element.lower() in than_thong_element.lower() or than_thong_element.lower() in cp_element.lower():
        return True, 1.0 + CONG_HUONG_HE_BONUS

    return False, 1.0


def kiem_tra_gioi_han_canh_gioi(cong_phap_key: str, current_realm_id: int) -> Tuple[bool, str]:
    """
    Kiểm tra xem công pháp chủ tu hiện tại có đủ cấp bậc để dẫn dắt tu sĩ đột phá tiếp hay không.
    """
    cp = get_cong_phap_by_key(cong_phap_key)
    if not cp:
        return False, "Chưa trang bị Công Pháp Chủ Tu!"

    if current_realm_id >= cp["max_realm_id"]:
        return False, (
            f"Công pháp [{cp['name']}] đã đạt đến cực hạn tu luyện "
            f"(chỉ hỗ trợ đến {cp['max_realm_name']}). Cần tìm công pháp cao cấp hơn để tiếp tục đột phá!"
        )

    return True, f"Công pháp [{cp['name']}] vẫn đủ khả năng dẫn dắt cảnh giới hiện tại."
