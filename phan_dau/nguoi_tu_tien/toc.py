# -*- coding: utf-8 -*-
"""
toc.py
======
Hệ thống Chủng Tộc (Tộc) của Người Tu Tiên trong thế giới Chu Thiên Vạn Giới:
Gồm 2 Đại Trận Doanh:
1. Nhánh Tộc Chính Đạo:
   - Thượng Tiên Tộc: Tư chất ngộ đạo cực cao, thần thức mạnh mẽ, linh lực dồi dào.
   - Cổ Thần Tộc: Cự nhân viễn cổ, thuần túy rèn luyện nhục thể đến vạn kiếp bất diệt.
   - Thánh Yêu Tộc (Huyết Mạch Thần Thú): Dòng máu Chân Long, Thiên Phượng, Kỳ Lân quang minh lỗi lạc.
   - Dược Mộc Tộc (Tinh Linh Thiên Địa): Hóa hình từ linh thảo thần mộc vạn năm, sinh cơ bất tuyệt.

2. Nhánh Tộc Ma Đạo:
   - Cổ Ma Tộc: Bản ngã tàn ác của Cổ Thần, dùng ma khí và oán hận tu luyện, cuồng bạo hiếu chiến.
   - Huyết Sát Tộc: Chuyên tu tà công huyết mạch, hút tinh huyết vạn vật để cường đại bản thân.
   - U Hồn Tộc (Ám Quỷ Tộc): Sinh ra từ tử tinh u minh, tồn tại dưới dạng nguyên thần ngưng kết.
   - Thiên Yêu Tộc (Hung Thú Hoang Cổ): Nhánh tà ác yêu tộc, chuyên cắn nuốt sinh linh đoạt tu vi.
"""
from typing import Optional, Dict, Any, List
import unicodedata


def _normalize_str(text: str) -> str:
    """Chuẩn hóa chuỗi tìm kiếm (chữ thường, loại bỏ khoảng trắng thừa)."""
    return " ".join(text.strip().lower().split())


# =============================================================================
# HẰNG SỐ PHÂN NHÁNH TRẬN DOANH
# =============================================================================
FACTION_CHINH_DAO = "Chính Đạo"
FACTION_MA_DAO = "Ma Đạo"

TOC_FACTIONS = {
    "chinh_dao": {
        "id": "chinh_dao",
        "name": FACTION_CHINH_DAO,
        "description": "Tu tâm dưỡng tính, thuận theo ý trời, mượn sức mạnh thiên địa quang minh chính đại.",
        "icon": "☯️",
    },
    "ma_dao": {
        "id": "ma_dao",
        "name": FACTION_MA_DAO,
        "description": "Nghịch thiên đoạt mệnh, sát phạt vô tình, cắn nuốt vạn vật để chứng đạo cực đoan.",
        "icon": "🩸",
    },
}

# =============================================================================
# DANH SÁCH CHI TIẾT TẤT CẢ CÁC TỘC
# =============================================================================
TOC_DATA: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # I. NHÁNH TỘC CHÍNH ĐẠO
    # -------------------------------------------------------------------------
    {
        "id": 1,
        "key": "thuong_tien_toc",
        "name": "Thượng Tiên Tộc",
        "subtitle": "Con Cưng Của Thiên Đạo",
        "faction": FACTION_CHINH_DAO,
        "faction_id": "chinh_dao",
        "aliases": ["Tiên Tộc", "Thượng Tiên"],
        "icon": "✨",
        "description": "Những kẻ được thiên đạo sủng ái, tư chất ngộ đạo cực cao. Thân thể có thể yếu, nhưng thần thức mạnh mẽ và linh lực dồi dào.",
        "dac_tinh": "Tăng mạnh Thần Thức (Độ Chính Xác), Linh Lực (Chân Nguyên) và Pháp Công. Nhược điểm: Phòng ngự vật lý ban đầu tương đối thấp.",
        "chi_so_uu_the": ["LL", "PC", "ĐCX", "NT"],
        "linh_can_phu_hop": ["Ngũ Hành Thiên Linh Căn", "Hạo Nhiên Linh Căn"],
    },
    {
        "id": 2,
        "key": "co_than_toc",
        "name": "Cổ Thần Tộc",
        "subtitle": "Viễn Cổ Cự Thần",
        "faction": FACTION_CHINH_DAO,
        "faction_id": "chinh_dao",
        "aliases": ["Cổ Thần", "Cự Nhân Tộc"],
        "icon": "🗿",
        "description": "Tộc người khổng lồ viễn cổ mang tín ngưỡng vỡ nát thiên địa. Họ không tu pháp thuật, không ngộ ý cảnh ảo diệu, chỉ thuần túy rèn luyện nhục thể đến mức vạn kiếp bất diệt.",
        "dac_tinh": "Tăng cực đại Sinh Lực (HP), Vật Công (Nhục Thân Lực) và Vật Phòng (VP). Hoàn toàn dựa vào sức mạnh quyền cước chấn thiên.",
        "chi_so_uu_the": ["SL", "VC", "VP", "KB"],
        "linh_can_phu_hop": ["Hồng Mông Nhục Căn", "Hạo Nhiên Linh Căn"],
    },
    {
        "id": 3,
        "key": "thanh_yeu_toc",
        "name": "Thánh Yêu Tộc",
        "subtitle": "Huyết Mạch Thần Thú",
        "faction": FACTION_CHINH_DAO,
        "faction_id": "chinh_dao",
        "aliases": ["Huyết Mạch Thần Thú", "Thần Thú Tộc", "Thánh Yêu"],
        "icon": "🐉",
        "description": "Những linh thú mang trong mình dòng máu tinh thuần của Chân Long, Thiên Phượng hay Kỳ Lân. Hành sự quang minh, mượn sức mạnh thiên nhiên.",
        "dac_tinh": "Công thủ toàn diện, sở hữu thần uy áp chế kẻ địch tốc độ thấp, tốc độ xuất chiêu và bạo kích cực cao.",
        "chi_so_uu_the": ["TĐ", "BK", "BT", "SL"],
        "linh_can_phu_hop": ["Thánh Thú Tương Ấn Căn", "Hạo Nhiên Linh Căn"],
    },
    {
        "id": 4,
        "key": "duoc_moc_toc",
        "name": "Dược Mộc Tộc",
        "subtitle": "Tinh Linh Thiên Địa",
        "faction": FACTION_CHINH_DAO,
        "faction_id": "chinh_dao",
        "aliases": ["Tinh Linh Thiên Địa", "Mộc Tộc", "Dược Tộc"],
        "icon": "🌿",
        "description": "Tu sĩ hóa hình từ những gốc linh thảo, thần mộc vạn năm tuổi. Bản tính hiền hòa, không thích sát sinh nhưng sinh cơ bất tuyệt.",
        "dac_tinh": "Sinh cơ vô tận, khả năng tự hồi phục HP mỗi lượt cực mạnh, tăng tỉ lệ và sản lượng khi luyện chế đan dược.",
        "chi_so_uu_the": ["SL", "PP", "NT", "CD"],
        "linh_can_phu_hop": ["Tạo Hóa Mộc Linh Căn", "Hạo Nhiên Linh Căn"],
    },

    # -------------------------------------------------------------------------
    # II. NHÁNH TỘC MA ĐẠO
    # -------------------------------------------------------------------------
    {
        "id": 5,
        "key": "co_ma_toc",
        "name": "Cổ Ma Tộc",
        "subtitle": "Ma Đạo Bạo Chúa",
        "faction": FACTION_MA_DAO,
        "faction_id": "ma_dao",
        "aliases": ["Cổ Ma", "Ma Tộc"],
        "icon": "👿",
        "description": "Bản ngã tàn ác của Cổ Thần. Dùng ma khí và oán hận để tu luyện nhục thân. Điên cuồng, hiếu chiến, coi vạn vật là sâu kiến.",
        "dac_tinh": "Nhục thân bạo liệt, khi máu càng giảm thì Lực công kích (ATK) và Tốc độ (SPD) càng tăng vọt (Cuồng Hóa).",
        "chi_so_uu_the": ["VC", "TĐ", "BK", "BT"],
        "linh_can_phu_hop": ["Tu La Ám Căn", "Phệ Hồn Linh Căn"],
    },
    {
        "id": 6,
        "key": "huyet_sat_toc",
        "name": "Huyết Sát Tộc",
        "subtitle": "Huyết Ma Tà Tộc",
        "faction": FACTION_MA_DAO,
        "faction_id": "ma_dao",
        "aliases": ["Huyết Tộc", "Sát Tộc"],
        "icon": "🩸",
        "description": "Chuyên tu tà công huyết mạch, hấp thụ tinh huyết của vạn vật để làm cường đại bản thân.",
        "dac_tinh": "Nội tại Hút Máu (Lifesteal), hấp thu sinh lực đối phương chuyển thành chân khí, tăng mạnh EXP khi trảm sát kẻ địch.",
        "chi_so_uu_the": ["SL", "VC", "BK", "CD"],
        "linh_can_phu_hop": ["Huyết Đạo Biến Dị Căn", "Phệ Hồn Linh Căn"],
    },
    {
        "id": 7,
        "key": "u_hon_toc",
        "name": "U Hồn Tộc",
        "subtitle": "Ám Quỷ Tộc",
        "faction": FACTION_MA_DAO,
        "faction_id": "ma_dao",
        "aliases": ["Ám Quỷ Tộc", "U Hồn", "Quỷ Tộc"],
        "icon": "👻",
        "description": "Những sinh vật sinh ra từ dải ngân hà chết hoặc u minh luân hồi, không có nhục thể thực sự mà tồn tại dưới dạng nguyên thần ngưng kết.",
        "dac_tinh": "Đòn đánh mang tính chất linh hồn, bỏ qua Pháp Phòng (PP - Linh Thuẫn) của kẻ địch, né tránh vật lý cực cao.",
        "chi_so_uu_the": ["PC", "ĐCX", "TĐ", "ĐT"],
        "linh_can_phu_hop": ["Cực Âm / Cửu U Linh Căn", "Phệ Hồn Linh Căn"],
    },
    {
        "id": 8,
        "key": "thien_yeu_toc",
        "name": "Thiên Yêu Tộc",
        "subtitle": "Hung Thú Hoang Cổ",
        "faction": FACTION_MA_DAO,
        "faction_id": "ma_dao",
        "aliases": ["Hung Thú Hoang Cổ", "Yêu Ma", "Thiên Yêu"],
        "icon": "🐍",
        "description": "Nhánh tà ác của Yêu Tộc, đam mê cắn nuốt sinh linh và đồng loại để cướp đoạt tu vi (như Thao Thiết, Cửu Đầu Xà). Bản tính xảo trá, độc ác.",
        "dac_tinh": "Mọi đòn đánh đều mang theo kịch độc rút máu theo %HP mỗi lượt và vô hiệu hóa khả năng dùng Đan dược hồi phục của kẻ thù.",
        "chi_so_uu_the": ["VC", "PC", "TĐ", "BT"],
        "linh_can_phu_hop": ["Thiên Độc Phệ Căn", "Phệ Hồn Linh Căn"],
    },
]

# =============================================================================
# HỆ THỐNG TRA CỨU NHANH O(1)
# =============================================================================
TOTAL_TOC: int = len(TOC_DATA)
TOC_LIST: List[Dict[str, Any]] = TOC_DATA

TOC_BY_ID: Dict[int, Dict[str, Any]] = {t["id"]: t for t in TOC_DATA}
TOC_BY_KEY: Dict[str, Dict[str, Any]] = {t["key"]: t for t in TOC_DATA}

TOC_BY_NAME: Dict[str, Dict[str, Any]] = {}
for t in TOC_DATA:
    TOC_BY_NAME[_normalize_str(t["name"])] = t
    for alias in t.get("aliases", []):
        TOC_BY_NAME[_normalize_str(alias)] = t

TOC_BY_FACTION: Dict[str, List[Dict[str, Any]]] = {
    "chinh_dao": [t for t in TOC_DATA if t["faction_id"] == "chinh_dao"],
    "ma_dao": [t for t in TOC_DATA if t["faction_id"] == "ma_dao"],
}


# =============================================================================
# CÁC HÀM TRA CỨU TIỆN ÍCH
# =============================================================================
def get_all_toc() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách các tộc tu tiên."""
    return TOC_LIST


def get_toc_by_id(toc_id: int) -> Optional[Dict[str, Any]]:
    """Tra cứu tộc theo ID số nguyên (1 -> 8)."""
    return TOC_BY_ID.get(toc_id)


def get_toc_by_key(key: str) -> Optional[Dict[str, Any]]:
    """Tra cứu tộc theo mã định danh key (ví dụ: 'co_than_toc')."""
    return TOC_BY_KEY.get(key.strip().lower())


def get_toc_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Tra cứu tộc theo tên hoặc bí danh (không phân biệt hoa thường)."""
    return TOC_BY_NAME.get(_normalize_str(name))


def get_toc_by_faction(faction_or_id: str) -> List[Dict[str, Any]]:
    """Tra cứu danh sách tộc thuộc trận doanh (Chính Đạo hoặc Ma Đạo)."""
    norm = _normalize_str(faction_or_id)
    if "chinh" in norm:
        return TOC_BY_FACTION.get("chinh_dao", [])
    if "ma" in norm:
        return TOC_BY_FACTION.get("ma_dao", [])
    return []


def search_toc(query: str) -> List[Dict[str, Any]]:
    """Tìm kiếm tộc theo từ khóa bất kỳ trong tên, bí danh, mô tả hoặc đặc tính."""
    q = _normalize_str(query)
    results = []
    for t in TOC_DATA:
        searchable_text = " ".join([
            t["name"],
            t.get("subtitle", ""),
            t["faction"],
            " ".join(t.get("aliases", [])),
            t.get("description", ""),
            t.get("dac_tinh", ""),
        ])
        if q in _normalize_str(searchable_text):
            results.append(t)
    return results
