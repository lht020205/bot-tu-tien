# -*- coding: utf-8 -*-
"""
linh_can.py
===========
Hệ thống Linh Căn của Người Tu Tiên trong Chu Thiên Vạn Giới:
Gồm 2 Nhánh Linh Căn:
1. Nhánh Linh Căn Chính Đạo:
   - Ngũ Hành Thiên Linh Căn: Tinh thuần nhất, tăng uy lực công pháp cùng hệ (Hợp nhất Thượng Tiên Tộc).
   - Hạo Nhiên Linh Căn (Siêu hiếm): Hạo nhiên chính khí, giảm sát thương Ma đạo, miễn nhiễm huyễn thuật & tâm ma (Tương thích vạn năng Chính đạo).
   - Hồng Mông Nhục Căn: SSR Cổ Thần, cùi pháp thuật nhưng tăng HP và Vật Phòng (DEF) khổng lồ.
   - Thánh Thú Tương Ấn Căn: Dấu ấn Chân Long/Thiên Phượng, Thần Uy làm choáng kẻ địch tốc độ thấp (Hợp nhất Thánh Yêu Tộc).
   - Tạo Hóa Mộc Linh Căn: Tăng sản lượng chế đan, hồi HP mỗi lượt (Chân ái Dược Mộc Tộc).

2. Nhánh Linh Căn Ma Đạo:
   - Cực Âm / Cửu U Linh Căn: Hút tử khí thiên địa, sát thương linh hồn bỏ qua Pháp Phòng MDEF (Hợp nhất U Hồn Tộc).
   - Huyết Đạo Biến Dị Căn: Hút máu Lifesteal, tăng vọt EXP khi trảm sát sinh linh (Đặc quyền Huyết Sát Tộc).
   - Tu La Ám Căn: Tu bằng sát khí, Cuồng Hóa khi mất máu tăng ATK và SPD (Bạo chúa Cổ Ma Tộc).
   - Thiên Độc Phệ Căn: Kịch độc DoT theo %HP tối đa, cấm đối thủ uống đan dược hồi phục (Tuyệt phối Thiên Yêu Tộc).
   - Phệ Hồn Linh Căn (Siêu hiếm): Cắn nuốt 100% tu vi, thọ nguyên và linh thạch khi trảm sát (SSR tà ác dùng chung 4 tộc Ma đạo).
"""
from typing import Optional, Dict, Any, List
import unicodedata


def _normalize_str(text: str) -> str:
    """Chuẩn hóa chuỗi tìm kiếm (chữ thường, loại bỏ khoảng trắng thừa)."""
    return " ".join(text.strip().lower().split())


FACTION_CHINH_DAO = "Chính Đạo"
FACTION_MA_DAO = "Ma Đạo"

# =============================================================================
# DANH SÁCH CHI TIẾT TẤT CẢ CÁC LINH CĂN
# =============================================================================
LINH_CAN_DATA: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # I. NHÁNH LINH CĂN CHÍNH ĐẠO
    # -------------------------------------------------------------------------
    {
        "id": 1,
        "key": "ngu_hanh_thien_linh_can",
        "name": "Ngũ Hành Thiên Linh Căn",
        "faction": FACTION_CHINH_DAO,
        "faction_id": "chinh_dao",
        "rarity": "Thượng Phẩm",
        "is_super_rare": False,
        "aliases": ["Thiên Linh Căn", "Ngũ Hành Căn"],
        "icon": "🌈",
        "description": "Linh căn tinh thuần nhất của người tu đạo. Tăng uy lực khi sử dụng công pháp cùng hệ. Phù hợp nhất với Thượng Tiên Tộc.",
        "hieu_ung": "Tăng mạnh sát thương khi sử dụng công pháp cùng thuộc tính Ngũ Hành (+25%). Tốc độ khôi phục Chân Nguyên tăng 20%.",
        "toc_phu_hop": ["Thượng Tiên Tộc"],
    },
    {
        "id": 2,
        "key": "hao_nhien_linh_can",
        "name": "Hạo Nhiên Linh Căn",
        "subtitle": "Siêu Hiếm",
        "faction": FACTION_CHINH_DAO,
        "faction_id": "chinh_dao",
        "rarity": "Siêu Hiếm (SSR)",
        "is_super_rare": True,
        "aliases": ["Hạo Nhiên Chính Khí", "Hạo Nhiên Căn", "Chính Khí Căn"],
        "icon": "☀️",
        "description": "Sinh ra đã mang hạo nhiên chính khí. Giảm sát thương nhận vào từ người chơi phe Ma đạo và miễn nhiễm hoàn toàn các loại huyễn thuật, tâm ma. Rất khó quay trúng, tương thích vạn năng với Chính đạo.",
        "hieu_ung": "Giảm 30% toàn bộ sát thương nhận vào từ phe Ma Đạo. Miễn nhiễm 100% các loại huyễn thuật, mê hoặc và tâm ma quấy nhiễu. Tương thích toàn bộ 4 tộc Chính Đạo.",
        "toc_phu_hop": ["Thượng Tiên Tộc", "Cổ Thần Tộc", "Thánh Yêu Tộc", "Dược Mộc Tộc"],
    },
    {
        "id": 3,
        "key": "hong_mong_nhuc_can",
        "name": "Hồng Mông Nhục Căn",
        "faction": FACTION_CHINH_DAO,
        "faction_id": "chinh_dao",
        "rarity": "Cực Phẩm Thể Tu",
        "is_super_rare": False,
        "aliases": ["Hồng Mông Căn", "Nhục Căn", "SSR Cổ Thần"],
        "icon": "🛡️",
        "description": "Cực kỳ cùi bắp trong việc học pháp thuật, nhưng là 'SSR' của Cổ Thần Tộc. Linh khí trực tiếp đập vào da thịt, mỗi cấp tu vi tăng lượng HP và Vật Phòng (DEF) khổng lồ.",
        "hieu_ung": "Pháp công bị giảm 80%, nhưng mỗi cấp tu vi tăng lượng Sinh Lực (HP) và Vật Phòng (VP) khổng lồ (+50%). Nhục thân ngưng luyện đao thương bất nhập.",
        "toc_phu_hop": ["Cổ Thần Tộc"],
    },
    {
        "id": 4,
        "key": "thanh_thu_tuong_an_can",
        "name": "Thánh Thú Tương Ấn Căn",
        "faction": FACTION_CHINH_DAO,
        "faction_id": "chinh_dao",
        "rarity": "Cực Phẩm",
        "is_super_rare": False,
        "aliases": ["Thánh Thú Căn", "Thần Thú Ấn Căn", "Tương Ấn Căn"],
        "icon": "🐾",
        "description": "Linh căn mang dấu ấn của Chân Long hoặc Thiên Phượng. Khi chiến đấu có xác suất bộc phát 'Thần Uy', gây choáng (Stun) toàn bộ kẻ địch có Tốc Độ (SPD) thấp hơn mình trong 1 lượt. Mảnh ghép hoàn hảo cho Thánh Yêu Tộc.",
        "hieu_ung": "Khi xuất chiêu có 35% tỷ lệ bộc phát 'Thần Uy': Gây choáng (Stun) trong 1 lượt toàn bộ kẻ địch có Tốc Độ (SPD) thấp hơn bản thân.",
        "toc_phu_hop": ["Thánh Yêu Tộc"],
    },
    {
        "id": 5,
        "key": "tao_hoa_moc_linh_can",
        "name": "Tạo Hóa Mộc Linh Căn",
        "faction": FACTION_CHINH_DAO,
        "faction_id": "chinh_dao",
        "rarity": "Cực Phẩm",
        "is_super_rare": False,
        "aliases": ["Tạo Hóa Mộc Căn", "Mộc Linh Căn", "Tạo Hóa Căn"],
        "icon": "🌱",
        "description": "Tốc độ tu vi mức khá, nhưng Ngộ Tính luyện đan cao. Nhận hiệu ứng tăng số lượng đan dược khi craft và tự động hồi HP mỗi lượt đánh. Đây là linh căn 'chân ái' của Dược Mộc Tộc.",
        "hieu_ung": "Tăng số lượng đan dược thu được khi luyện đan (+30% tỷ lệ ra đan gấp đôi). Tự động hồi phục 8% Sinh Lực (HP) tối đa vào mỗi lượt thi đấu.",
        "toc_phu_hop": ["Dược Mộc Tộc"],
    },

    # -------------------------------------------------------------------------
    # II. NHÁNH LINH CĂN MA ĐẠO
    # -------------------------------------------------------------------------
    {
        "id": 6,
        "key": "cuc_am_cuu_u_linh_can",
        "name": "Cực Âm / Cửu U Linh Căn",
        "faction": FACTION_MA_DAO,
        "faction_id": "ma_dao",
        "rarity": "Cực Phẩm",
        "is_super_rare": False,
        "aliases": ["Cực Âm Linh Căn", "Cửu U Linh Căn", "Cửu U Căn", "Cực Âm Căn"],
        "icon": "🌌",
        "description": "Không hấp thụ linh khí mà hút tử khí thiên địa. Đòn đánh mang theo sát thương linh hồn, bỏ qua Pháp Phòng (MDEF) của kẻ địch. Phù hợp tuyệt đối với U Hồn Tộc.",
        "hieu_ung": "Đòn đánh hóa thành sát thương hồn phách trực diện, bỏ qua 100% Pháp Phòng (PP - Linh Thuẫn) của kẻ địch.",
        "toc_phu_hop": ["U Hồn Tộc"],
    },
    {
        "id": 7,
        "key": "huyet_dao_bien_di_can",
        "name": "Huyết Đạo Biến Dị Căn",
        "faction": FACTION_MA_DAO,
        "faction_id": "ma_dao",
        "rarity": "Cực Phẩm",
        "is_super_rare": False,
        "aliases": ["Huyết Đạo Căn", "Huyết Biến Dị Căn", "Biến Dị Huyết Căn"],
        "icon": "🩸",
        "description": "Hút linh khí rất chậm, nhưng tăng lượng lớn EXP Tu vi mỗi khi kết liễu quái vật hoặc người chơi khác. Sở hữu nội tại Hút Máu (Lifesteal) sát thương gây ra. Đặc quyền sinh ra dành cho Huyết Sát Tộc.",
        "hieu_ung": "Nội tại Hút Máu (Lifesteal): Hồi phục Sinh Lực bằng 25% tổng sát thương tạo ra. Tăng +50% EXP Tu vi khi hạ sát quái vật hoặc tu sĩ khác.",
        "toc_phu_hop": ["Huyết Sát Tộc"],
    },
    {
        "id": 8,
        "key": "tu_la_am_can",
        "name": "Tu La Ám Căn",
        "faction": FACTION_MA_DAO,
        "faction_id": "ma_dao",
        "rarity": "Cực Phẩm Bạo Chúa",
        "is_super_rare": False,
        "aliases": ["Tu La Căn", "Ám Căn", "Tu La Ám Khí"],
        "icon": "⚔️",
        "description": "Tu luyện bằng sát khí. Kích hoạt cơ chế 'Cuồng Hóa': Khi HP bản thân giảm, Lực công kích (ATK) và Tốc độ xuất chiêu (SPD) tăng. Linh căn bạo chúa của Cổ Ma Tộc.",
        "hieu_ung": "Kích hoạt trạng thái 'Cuồng Hóa': Cứ mỗi 10% HP tổn hao, tăng +15% Vật Công (VC) và +10% Tốc Độ (TĐ). Dưới 30% HP bạo phát thêm 20% Bạo Kích.",
        "toc_phu_hop": ["Cổ Ma Tộc"],
    },
    {
        "id": 9,
        "key": "thien_doc_phe_can",
        "name": "Thiên Độc Phệ Căn",
        "faction": FACTION_MA_DAO,
        "faction_id": "ma_dao",
        "rarity": "Cực Phẩm Tà Độc",
        "is_super_rare": False,
        "aliases": ["Thiên Độc Căn", "Phệ Độc Căn", "Độc Phệ Căn"],
        "icon": "☣️",
        "description": "Mọi đòn tấn công vật lý hay pháp thuật đều mang theo kịch độc. Gây hiệu ứng 'Rút máu' (DoT - Damage over Time) bằng %HP tối đa của kẻ địch mỗi lượt, đồng thời vô hiệu hóa khả năng dùng Đan dược hồi phục của đối thủ. Tuyệt phối cho Thiên Yêu Tộc.",
        "hieu_ung": "Đòn đánh đính kèm kịch độc: Rút 6% HP tối đa của kẻ địch mỗi lượt trong 3 lượt (DoT), đồng thời vô hiệu hóa hoàn toàn việc dùng Đan dược hồi phục của đối thủ.",
        "toc_phu_hop": ["Thiên Yêu Tộc"],
    },
    {
        "id": 10,
        "key": "phe_hon_linh_can",
        "name": "Phệ Hồn Linh Căn",
        "subtitle": "Siêu Hiếm",
        "faction": FACTION_MA_DAO,
        "faction_id": "ma_dao",
        "rarity": "Siêu Hiếm (SSR)",
        "is_super_rare": True,
        "aliases": ["Phệ Hồn Căn", "Cắn Nuốt Linh Căn", "Thôn Phệ Căn"],
        "icon": "💀",
        "description": "Người có linh căn này gần như không thể ngồi thiền tăng cấp, bù lại, tỷ lệ cắn nuốt (Steal) trực tiếp Tu vi, Thọ Nguyên và cả Linh thạch của nạn nhân bị giết là 100%. Đây là linh căn tà ác nhất, dùng chung cho cả 4 tộc Ma đạo nếu đủ nhân phẩm quay trúng.",
        "hieu_ung": "Giảm 70% EXP khi ngồi thiền tĩnh tọa. Bù lại: Khi tiêu diệt mục tiêu, tỷ lệ cắn nuốt 100% đoạt lấy 15% Linh Thạch và một lượng Tu Vi, Thọ Nguyên của đối thủ.",
        "toc_phu_hop": ["Cổ Ma Tộc", "Huyết Sát Tộc", "U Hồn Tộc", "Thiên Yêu Tộc"],
    },
]

# =============================================================================
# HỆ THỐNG TRA CỨU NHANH O(1)
# =============================================================================
TOTAL_LINH_CAN: int = len(LINH_CAN_DATA)
LINH_CAN_LIST: List[Dict[str, Any]] = LINH_CAN_DATA

LINH_CAN_BY_ID: Dict[int, Dict[str, Any]] = {lc["id"]: lc for lc in LINH_CAN_DATA}
LINH_CAN_BY_KEY: Dict[str, Dict[str, Any]] = {lc["key"]: lc for lc in LINH_CAN_DATA}

LINH_CAN_BY_NAME: Dict[str, Dict[str, Any]] = {}
for lc in LINH_CAN_DATA:
    LINH_CAN_BY_NAME[_normalize_str(lc["name"])] = lc
    for alias in lc.get("aliases", []):
        LINH_CAN_BY_NAME[_normalize_str(alias)] = lc

LINH_CAN_BY_FACTION: Dict[str, List[Dict[str, Any]]] = {
    "chinh_dao": [lc for lc in LINH_CAN_DATA if lc["faction_id"] == "chinh_dao"],
    "ma_dao": [lc for lc in LINH_CAN_DATA if lc["faction_id"] == "ma_dao"],
}


# =============================================================================
# CÁC HÀM TRA CỨU TIỆN ÍCH
# =============================================================================
def get_all_linh_can() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách 10 loại linh căn."""
    return LINH_CAN_LIST


def get_linh_can_by_id(lc_id: int) -> Optional[Dict[str, Any]]:
    """Tra cứu linh căn theo ID (1 -> 10)."""
    return LINH_CAN_BY_ID.get(lc_id)


def get_linh_can_by_key(key: str) -> Optional[Dict[str, Any]]:
    """Tra cứu linh căn theo key (ví dụ: 'hao_nhien_linh_can')."""
    return LINH_CAN_BY_KEY.get(key.strip().lower())


def get_linh_can_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Tra cứu linh căn theo tên hoặc bí danh."""
    return LINH_CAN_BY_NAME.get(_normalize_str(name))


def get_linh_can_by_faction(faction_or_id: str) -> List[Dict[str, Any]]:
    """Tra cứu linh căn theo trận doanh Chính Đạo hoặc Ma Đạo."""
    norm = _normalize_str(faction_or_id)
    if "chinh" in norm:
        return LINH_CAN_BY_FACTION.get("chinh_dao", [])
    if "ma" in norm:
        return LINH_CAN_BY_FACTION.get("ma_dao", [])
    return []


def search_linh_can(query: str) -> List[Dict[str, Any]]:
    """Tìm kiếm linh căn theo từ khóa."""
    q = _normalize_str(query)
    results = []
    for lc in LINH_CAN_DATA:
        searchable_text = " ".join([
            lc["name"],
            lc.get("subtitle", ""),
            lc["faction"],
            lc.get("rarity", ""),
            " ".join(lc.get("aliases", [])),
            lc.get("description", ""),
            lc.get("hieu_ung", ""),
            " ".join(lc.get("toc_phu_hop", [])),
        ])
        if q in _normalize_str(searchable_text):
            results.append(lc)
    return results
