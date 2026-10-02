# -*- coding: utf-8 -*-
"""
chi_so.py
=========
Hệ thống Toàn Diện Các Chỉ Số Của Người Tu Tiên trong Chu Thiên Vạn Giới:
Gồm 3 Nhóm Chỉ Số Lớn:
1. Nhóm Chỉ Số Cơ Bản:
   - Sinh Lực (SL - Huyết Khí): Máu mủ và sinh cơ nhục thân. Cạn kiệt thì thân xác sụp đổ, chỉ còn Nguyên Thần trốn chạy.
   - Linh Lực (LL - Chân Nguyên): Năng lượng đan điền thi triển pháp thuật, ngự kiếm hoặc kích hoạt Pháp bảo.

2. Nhóm Chỉ Số Chiến Đấu:
   - Vật Công (VC - Nhục Thân Lực): Sát thương ngoại công bằng quyền cước, binh khí cận chiến (thế mạnh Thể Tu như Cổ Thần).
   - Pháp Công (PC - Đạo Pháp Lực): Sát thương nội công từ xa dựa trên phẩm chất công pháp và mức độ tinh thuần Chân Nguyên.
   - Vật Phòng (VP - Hộ Thể Cương Khí): Độ cứng cáp cơ bắp, da thịt hoặc hộ giáp giảm trừ sát thương vật lý.
   - Pháp Phòng (PP - Linh Thuẫn): Lớp màng linh lực quanh người hoặc từ trang sức kháng đòn pháp thuật (Lôi, Hỏa, Độc).
   - Tốc Độ (TĐ - Thân Pháp): Linh hoạt cước bộ, ngự kiếm; quyết định ai xuất chiêu trước và tỷ lệ Né Tránh (Dodge).
   - Độ Chính Xác (ĐCX - Thần Thức): Sức mạnh tinh thần khóa mục tiêu, phá ảo ảnh, đánh xuyên Hộ Thể Cương Khí vào linh hồn.
   - Bạo Kích (BK - Tỷ Lệ Hội Tâm): Xác suất đánh trúng tử huyệt hoặc bạo phát công pháp vượt giới hạn.
   - Bạo Thương (BT - Uy Lực Hội Tâm): Hệ số khuếch đại sát thương khi đòn Bạo Kích kích hoạt.
   - Kháng Bạo (KB - Kiên Cốt): Khả năng ngạnh kháng, ép sát thương bạo phát của kẻ địch trở về mức cơ bản.

3. Nhóm Chỉ Số Ẩn:
   - Cơ Duyên (CD - Khí Vận): Mệnh cách nhân vật; khí vận cao dễ gặp kỳ ngộ, rơi đồ hiếm, luyện đan ra Cực Phẩm, té núi nhặt truyền thừa.
   - Ngộ Tính (NT): Khả năng lĩnh ngộ thiên địa; rút ngắn học thần thông, tăng tỷ lệ ngộ Ý Cảnh (kiếm ý, sinh tử ý cảnh) để đột phá cảnh giới cao.
   - Đạo Tâm (ĐT): Độ kiên định ý chí; kháng tâm ma quấy nhiễu, giảm tẩu hỏa nhập ma, kháng hiệu ứng Mê Hoặc/Huyễn Thuật/Khống Tâm.
"""
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field
import unicodedata


def _normalize_str(text: str) -> str:
    """Chuẩn hóa chuỗi tìm kiếm."""
    return " ".join(text.strip().lower().split())


# =============================================================================
# HẰNG SỐ PHÂN NHÓM CHỈ SỐ
# =============================================================================
GROUP_CO_BAN = "co_ban"
GROUP_CHIEN_DAU = "chien_dau"
GROUP_CHI_SO_AN = "chi_so_an"

CHI_SO_GROUPS = {
    GROUP_CO_BAN: {
        "id": GROUP_CO_BAN,
        "name": "Chỉ Số Cơ Bản",
        "description": "Nền tảng tồn tại của một tu sĩ gồm Khí Huyết nuôi thân và Chân Nguyên thi triển đạo thuật.",
        "icon": "❤️",
    },
    GROUP_CHIEN_DAU: {
        "id": GROUP_CHIEN_DAU,
        "name": "Chỉ Số Chiến Đấu",
        "description": "Các chỉ số trực tiếp quyết định thắng bại trong giao tranh, đấu pháp và lịch luyện bí cảnh.",
        "icon": "⚔️",
    },
    GROUP_CHI_SO_AN: {
        "id": GROUP_CHI_SO_AN,
        "name": "Chỉ Số Ẩn",
        "description": "Mệnh cách, thiên tư và định lực tâm tính vô hình tác động sâu sắc đến con đường trường sinh.",
        "icon": "🔮",
    },
}

# =============================================================================
# DANH SÁCH CHI TIẾT TẤT CẢ CÁC CHỈ SỐ
# =============================================================================
CHI_SO_DATA: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # 1. CHỈ SỐ CƠ BẢN
    # -------------------------------------------------------------------------
    {
        "id": 1,
        "key": "sinh_luc",
        "code": "SL",
        "name": "Sinh Lực",
        "subtitle": "Huyết Khí",
        "group_id": GROUP_CO_BAN,
        "group_name": "Chỉ Số Cơ Bản",
        "icon": "🩸",
        "unit": "Điểm",
        "base_default": 100,
        "description": "Sinh cơ và máu mủ của nhục thân. Khí huyết cạn kiệt thì thân xác sụp đổ, chỉ còn Nguyên Thần trốn chạy.",
        "tac_dung": "Quyết định khả năng sinh tồn. Khi Sinh Lực về 0, nhân vật rơi vào trạng thái trọng thương hoặc nhục thân vỡ nát.",
    },
    {
        "id": 2,
        "key": "linh_luc",
        "code": "LL",
        "name": "Linh Lực",
        "subtitle": "Chân Nguyên",
        "group_id": GROUP_CO_BAN,
        "group_name": "Chỉ Số Cơ Bản",
        "icon": "🌀",
        "unit": "Điểm",
        "base_default": 100,
        "description": "Năng lượng dung nạp trong đan điền, dùng để thi triển pháp thuật, ngự kiếm hoặc kích hoạt Pháp bảo.",
        "tac_dung": "Tiêu hao mỗi khi phóng xuất đại thần thông hoặc kích phát uy lực tối đa của Pháp bảo.",
    },

    # -------------------------------------------------------------------------
    # 2. CHỈ SỐ CHIẾN ĐẤU
    # -------------------------------------------------------------------------
    {
        "id": 3,
        "key": "vat_cong",
        "code": "VC",
        "name": "Vật Công",
        "subtitle": "Nhục Thân Lực",
        "group_id": GROUP_CHIEN_DAU,
        "group_name": "Chỉ Số Chiến Đấu",
        "icon": "🥊",
        "unit": "Điểm",
        "base_default": 20,
        "description": "Sát thương ngoại công bằng quyền cước, binh khí cận chiến. Các Thể Tu (như Cổ Thần Tộc) cực kỳ mạnh ở chỉ số này.",
        "tac_dung": "Gây sát thương vật lý trực tiếp, đối kháng lại Vật Phòng của mục tiêu.",
    },
    {
        "id": 4,
        "key": "phap_cong",
        "code": "PC",
        "name": "Pháp Công",
        "subtitle": "Đạo Pháp Lực",
        "group_id": GROUP_CHIEN_DAU,
        "group_name": "Chỉ Số Chiến Đấu",
        "icon": "🔮",
        "unit": "Điểm",
        "base_default": 20,
        "description": "Sát thương nội công từ khoảng cách xa, dựa trên phẩm chất công pháp và mức độ tinh thuần của Chân Nguyên.",
        "tac_dung": "Gây sát thương đạo pháp huyền ảo, đối kháng lại Pháp Phòng của mục tiêu.",
    },
    {
        "id": 5,
        "key": "vat_phong",
        "code": "VP",
        "name": "Vật Phòng",
        "subtitle": "Hộ Thể Cương Khí",
        "group_id": GROUP_CHIEN_DAU,
        "group_name": "Chỉ Số Chiến Đấu",
        "icon": "🛡️",
        "unit": "Điểm",
        "base_default": 10,
        "description": "Độ cứng cáp của cơ bắp, da thịt hoặc áo giáp, giúp giảm trừ sát thương vật lý.",
        "tac_dung": "Giảm thiểu sát thương nhận vào từ các đòn đánh ngoại công quyền cước, binh đao kiếm kích.",
    },
    {
        "id": 6,
        "key": "phap_phong",
        "code": "PP",
        "name": "Pháp Phòng",
        "subtitle": "Linh Thuẫn",
        "group_id": GROUP_CHIEN_DAU,
        "group_name": "Chỉ Số Chiến Đấu",
        "icon": "💠",
        "unit": "Điểm",
        "base_default": 10,
        "description": "Lớp màng linh lực bao bọc quanh người hoặc hiệu ứng từ trang sức (Ngọc bội, Hộ kính) để kháng lại các đòn pháp thuật (Lôi, Hỏa, Độc).",
        "tac_dung": "Giảm trừ sát thương nhận vào từ các đòn tấn công pháp thuật, phong lôi thủy hỏa.",
    },
    {
        "id": 7,
        "key": "toc_do",
        "code": "TĐ",
        "name": "Tốc Độ",
        "subtitle": "Thân Pháp",
        "group_id": GROUP_CHIEN_DAU,
        "group_name": "Chỉ Số Chiến Đấu",
        "icon": "⚡",
        "unit": "Điểm",
        "base_default": 15,
        "description": "Sự linh hoạt của cước bộ hoặc đài ngự kiếm. Quyết định ai là người xuất chiêu trước, cũng như gia tăng Tỷ Lệ Né Tránh (Dodge) đòn đánh.",
        "tac_dung": "Quyết định quyền tiên thủ trong lượt đấu và tăng tỷ lệ né hoàn toàn đòn tấn công của đối thủ.",
    },
    {
        "id": 8,
        "key": "do_chinh_xac",
        "code": "ĐCX",
        "name": "Độ Chính Xác",
        "subtitle": "Thần Thức",
        "group_id": GROUP_CHIEN_DAU,
        "group_name": "Chỉ Số Chiến Đấu",
        "icon": "👁️",
        "unit": "Điểm",
        "base_default": 85,
        "description": "Sức mạnh tinh thần. Thần thức cường đại giúp khóa chặt mục tiêu (tăng Tỷ lệ trúng mục tiêu), phá vỡ ảo ảnh, hoặc dùng để giáng đòn công kích thẳng vào linh hồn kẻ địch xuyên qua Hộ Thể Cương Khí.",
        "tac_dung": "Giảm tỷ lệ né tránh của kẻ thù, bảo đảm đòn đánh đánh trúng mục tiêu và xuyên thấu một phần phòng ngự linh hồn.",
    },
    {
        "id": 9,
        "key": "bao_kich",
        "code": "BK",
        "name": "Bạo Kích",
        "subtitle": "Tỷ Lệ Hội Tâm",
        "group_id": GROUP_CHIEN_DAU,
        "group_name": "Chỉ Số Chiến Đấu",
        "icon": "💥",
        "unit": "%",
        "base_default": 5.0,
        "description": "Xác suất đánh trúng tử huyệt hoặc bạo phát công pháp vượt giới hạn.",
        "tac_dung": "Tỷ lệ phần trăm bộc phát đòn đánh chí mạng, nhân sát thương theo chỉ số Bạo Thương.",
    },
    {
        "id": 10,
        "key": "bao_thuong",
        "code": "BT",
        "name": "Bạo Thương",
        "subtitle": "Uy Lực Hội Tâm",
        "group_id": GROUP_CHIEN_DAU,
        "group_name": "Chỉ Số Chiến Đấu",
        "icon": "🗡️",
        "unit": "%",
        "base_default": 150.0,
        "description": "Hệ số khuếch đại sát thương khi đòn Bạo Kích kích hoạt.",
        "tac_dung": "Khi Bạo Kích nổ, sát thương sẽ nhân với hệ số này (ví dụ 150% = x1.5 lần sát thương gốc).",
    },
    {
        "id": 11,
        "key": "khang_bao",
        "code": "KB",
        "name": "Kháng Bạo",
        "subtitle": "Kiên Cốt",
        "group_id": GROUP_CHIEN_DAU,
        "group_name": "Chỉ Số Chiến Đấu",
        "icon": "🧱",
        "unit": "%",
        "base_default": 0.0,
        "description": "Khả năng ngạnh kháng, ép sát thương bạo phát của kẻ địch trở về mức sát thương cơ bản.",
        "tac_dung": "Giảm trừ tỷ lệ nổ bạo kích và sát thương bạo kích của kẻ thù khi tấn công vào bản thân.",
    },

    # -------------------------------------------------------------------------
    # 3. CHỈ SỐ ẨN
    # -------------------------------------------------------------------------
    {
        "id": 12,
        "key": "co_duyen",
        "code": "CD",
        "name": "Cơ Duyên",
        "subtitle": "Khí Vận",
        "group_id": GROUP_CHI_SO_AN,
        "group_name": "Chỉ Số Ẩn",
        "icon": "🍀",
        "unit": "Điểm",
        "base_default": 10,
        "description": "Mệnh cách của nhân vật. Khí vận cao dễ gặp kỳ ngộ, rớt vật phẩm hiếm, luyện đan ra Cực Phẩm, hoặc rơi xuống vực không chết mà nhặt được truyền thừa.",
        "tac_dung": "Tăng tỷ lệ rơi bảo vật quý hiếm trong lịch luyện bí cảnh, tăng tỷ lệ ra biến dị đan dược và kỳ ngộ ngẫu nhiên.",
    },
    {
        "id": 13,
        "key": "ngo_tinh",
        "code": "NT",
        "name": "Ngộ Tính",
        "subtitle": "Lĩnh Ngộ Thiên Địa",
        "group_id": GROUP_CHI_SO_AN,
        "group_name": "Chỉ Số Ẩn",
        "icon": "🧠",
        "unit": "Điểm",
        "base_default": 10,
        "description": "Khả năng lĩnh ngộ thiên địa. Rút ngắn thời gian học xong thần thông mới, tăng tỷ lệ ngộ ra 'Ý Cảnh' (kiếm ý, sinh tử ý cảnh) để thăng cấp ở các cảnh giới cao (như Hóa Thần).",
        "tac_dung": "Rút ngắn thời gian lĩnh ngộ công pháp, tăng exp thu nhận khi tĩnh tọa và tỷ lệ lĩnh ngộ Ý Cảnh khi đột phá cảnh giới.",
    },
    {
        "id": 14,
        "key": "dao_tam",
        "code": "ĐT",
        "name": "Đạo Tâm",
        "subtitle": "Độ Kiên Định Của Ý Chí",
        "group_id": GROUP_CHI_SO_AN,
        "group_name": "Chỉ Số Ẩn",
        "icon": "🧘",
        "unit": "Điểm",
        "base_default": 10,
        "description": "Độ kiên định của ý chí. Kháng lại tâm ma quấy nhiễu lúc đột phá, giảm thiểu xác suất tẩu hỏa nhập ma, và kháng các hiệu ứng khống chế trong chiến đấu (Mê Hoặc, Huyễn Thuật, Khống Tâm).",
        "tac_dung": "Giảm tỷ lệ thất bại khi độ kiếp đột phá đại cảnh giới, kháng các hiệu ứng khống chế tinh thần từ kẻ địch.",
    },
]

# =============================================================================
# HỆ THỐNG TRA CỨU NHANH O(1)
# =============================================================================
TOTAL_CHI_SO: int = len(CHI_SO_DATA)
CHI_SO_LIST: List[Dict[str, Any]] = CHI_SO_DATA

CHI_SO_BY_ID: Dict[int, Dict[str, Any]] = {c["id"]: c for c in CHI_SO_DATA}
CHI_SO_BY_KEY: Dict[str, Dict[str, Any]] = {c["key"]: c for c in CHI_SO_DATA}
CHI_SO_BY_CODE: Dict[str, Dict[str, Any]] = {c["code"].upper(): c for c in CHI_SO_DATA}

CHI_SO_BY_NAME: Dict[str, Dict[str, Any]] = {}
for c in CHI_SO_DATA:
    CHI_SO_BY_NAME[_normalize_str(c["name"])] = c
    if c.get("subtitle"):
        CHI_SO_BY_NAME[_normalize_str(c["subtitle"])] = c

CHI_SO_BY_GROUP: Dict[str, List[Dict[str, Any]]] = {
    GROUP_CO_BAN: [c for c in CHI_SO_DATA if c["group_id"] == GROUP_CO_BAN],
    GROUP_CHIEN_DAU: [c for c in CHI_SO_DATA if c["group_id"] == GROUP_CHIEN_DAU],
    GROUP_CHI_SO_AN: [c for c in CHI_SO_DATA if c["group_id"] == GROUP_CHI_SO_AN],
}


# =============================================================================
# CÁC HÀM TRA CỨU TIỆN ÍCH
# =============================================================================
def get_all_chi_so() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách 14 chỉ số của người tu tiên."""
    return CHI_SO_LIST


def get_chi_so_by_id(cs_id: int) -> Optional[Dict[str, Any]]:
    """Tra cứu chỉ số theo ID (1 -> 14)."""
    return CHI_SO_BY_ID.get(cs_id)


def get_chi_so_by_key(key: str) -> Optional[Dict[str, Any]]:
    """Tra cứu chỉ số theo key (ví dụ: 'sinh_luc', 'vat_cong')."""
    return CHI_SO_BY_KEY.get(key.strip().lower())


def get_chi_so_by_code(code: str) -> Optional[Dict[str, Any]]:
    """Tra cứu chỉ số theo mã viết tắt (SL, LL, VC, PC, VP, PP, TĐ, ĐCX, BK, BT, KB, CD, NT, ĐT)."""
    return CHI_SO_BY_CODE.get(code.strip().upper())


def get_chi_so_by_name(name: str) -> Optional[Dict[str, Any]]:
    """Tra cứu chỉ số theo tên hoặc tên phụ (ví dụ: 'Sinh Lực' hoặc 'Huyết Khí')."""
    return CHI_SO_BY_NAME.get(_normalize_str(name))


def get_chi_so_by_group(group_id: str) -> List[Dict[str, Any]]:
    """Tra cứu danh sách chỉ số theo nhóm ('co_ban', 'chien_dau', 'chi_so_an')."""
    return CHI_SO_BY_GROUP.get(group_id.strip().lower(), [])


def search_chi_so(query: str) -> List[Dict[str, Any]]:
    """Tìm kiếm chỉ số theo từ khóa bất kỳ."""
    q = _normalize_str(query)
    results = []
    for c in CHI_SO_DATA:
        searchable_text = " ".join([
            c["name"],
            c.get("subtitle", ""),
            c["code"],
            c["group_name"],
            c.get("description", ""),
            c.get("tac_dung", ""),
        ])
        if q in _normalize_str(searchable_text):
            results.append(c)
    return results


# =============================================================================
# DATA CLASS BẢNG CHỈ SỐ TOÀN DIỆN CỦA MỘT TU SĨ
# =============================================================================
@dataclass
class BangChiSoTuSi:
    """
    Bảng tổng hợp chỉ số thực tế của một tu sĩ sau khi cộng gộp:
    Căn bản + Cảnh giới + Chủng tộc + Linh căn + Trang bị.
    """
    sinh_luc: int = 100
    linh_luc: int = 100
    vat_cong: int = 20
    phap_cong: int = 20
    vat_phong: int = 10
    phap_phong: int = 10
    toc_do: int = 15
    do_chinh_xac: int = 85
    bao_kich: float = 5.0
    bao_thuong: float = 150.0
    khang_bao: float = 0.0
    co_duyen: int = 10
    ngo_tinh: int = 10
    dao_tam: int = 10

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi bảng chỉ số thành dictionary dễ đọc."""
        return {
            "SL": self.sinh_luc,
            "LL": self.linh_luc,
            "VC": self.vat_cong,
            "PC": self.phap_cong,
            "VP": self.vat_phong,
            "PP": self.phap_phong,
            "TĐ": self.toc_do,
            "ĐCX": self.do_chinh_xac,
            "BK": f"{self.bao_kich:.1f}%",
            "BT": f"{self.bao_thuong:.1f}%",
            "KB": f"{self.khang_bao:.1f}%",
            "CD": self.co_duyen,
            "NT": self.ngo_tinh,
            "ĐT": self.dao_tam,
        }
