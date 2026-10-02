# -*- coding: utf-8 -*-
"""
diem_cong_hien.py
=================
Hệ thống Điểm Cống Hiến Tông Môn trong Chu Thiên Vạn Giới:
- Đơn vị tích lũy công lao của đệ tử đối với Tông Môn hoặc Giáo Phái.
- Dùng để:
  + Đổi Công Pháp, Tâm Pháp, Tuyệt Kỹ Thần Thông tại Tàng Kinh Các.
  + Đổi Đan Dược đột phá, linh dược quý hiếm tại Vạn Bảo Đường.
  + Đổi Binh khí, Pháp bảo, Linh giáp hộ thân trấn phái.
  + Đổi Đặc Quyền Tông Môn: Tu luyện Tụ Linh Trận (x2 EXP), thăng cấp đệ tử (Ngoại môn -> Nội môn -> Chân truyền).
- Cung cấp danh mục vật phẩm đổi thưởng, phương thức tích lũy và hàm kiểm tra giao dịch.
"""
from typing import Optional, Dict, Any, List, Tuple


# =============================================================================
# HẰNG SỐ NGUỒN TÍCH LŨY ĐIỂM CỐNG HIẾN
# =============================================================================
NGUON_TICH_LUY: Dict[str, Dict[str, Any]] = {
    "diem_danh_tong_mon": {
        "key": "diem_danh_tong_mon",
        "name": "Thắp Hương Tổ Sư Đường",
        "points_min": 10,
        "points_max": 25,
        "description": "Điểm danh hàng ngày tại Tổ Sư Đường, tỏ lòng tôn kính với các bậc tiền bối khai sơn phá thạch.",
    },
    "nhiem_vu_tuan_tra": {
        "key": "nhiem_vu_tuan_tra",
        "name": "Nhiệm Vụ Tuần Tra Sơn Môn",
        "points_min": 30,
        "points_max": 60,
        "description": "Tuần phòng biên giới tông môn, ngăn chặn gián điệp và yêu thú xâm phạm.",
    },
    "nhiem_vu_tram_yeu": {
        "key": "nhiem_vu_tram_yeu",
        "name": "Nhiệm Vụ Trảm Yêu Trừ Ma",
        "points_min": 80,
        "points_max": 200,
        "description": "Xuống núi tiêu diệt tà tu hoặc yêu thú gây họa nhân gian theo lệnh bài tông môn.",
    },
    "hien_tang_tai_nguyen": {
        "key": "hien_tang_tai_nguyen",
        "name": "Hiến Tặng Linh Thạch & Dược Thảo",
        "rate": "100 Hạ Phẩm Linh Thạch = 1 Điểm Cống Hiến",
        "description": "Đóng góp tài nguyên vào Tông Môn Khố để duy trì đại trận và bồi dưỡng thế hệ sau.",
    },
    "tong_mon_dai_chien": {
        "key": "tong_mon_dai_chien",
        "name": "Tông Môn Đại Chiến & Đoạt Mỏ",
        "points_min": 300,
        "points_max": 1000,
        "description": "Chiến đấu giành giật linh mạch, mỏ khoáng sản hoặc tranh thứ hạng trên Thiên Kiêu Bảng.",
    },
}

# =============================================================================
# DANH MỤC ĐỔI THƯỞNG BẰNG ĐIỂM CỐNG HIẾN (TÀNG KINH CÁC & VẠN BẢO ĐƯỜNG)
# =============================================================================
DANH_MUC_DOI_THUONG: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # 1. CÔNG PHÁP & THẦN THÔNG
    # -------------------------------------------------------------------------
    {
        "id": 1,
        "key": "cong_phap_dan_khi_quyet",
        "name": "Dẫn Khí Thần Quyết",
        "category": "cong_phap",
        "category_name": "Công Pháp",
        "cost_points": 50,
        "required_rank": "Ngoại Môn Đệ Tử",
        "icon": "📜",
        "description": "Tâm pháp nhập môn tông môn, khai mở các đại huyệt đạo, tăng 15% tốc độ hấp thu exp tu luyện.",
    },
    {
        "id": 2,
        "key": "cong_phap_cuu_chuyen_kim_than",
        "name": "Cửu Chuyển Kim Thân Quyết",
        "category": "cong_phap",
        "category_name": "Công Pháp",
        "cost_points": 300,
        "required_rank": "Nội Môn Đệ Tử",
        "icon": "🥋",
        "description": "Tuyệt kỹ Thể Tu, tôi luyện huyết nhục gân cốt thành đồng da sắt, tăng vĩnh viễn +30 Vật Phòng và +100 HP.",
    },
    {
        "id": 3,
        "key": "cong_phap_thanh_van_kiem_quyet",
        "name": "Thanh Vân Ngự Kiếm Quyết",
        "category": "cong_phap",
        "category_name": "Công Pháp",
        "cost_points": 500,
        "required_rank": "Nội Môn Đệ Tử",
        "icon": "⚔️",
        "description": "Kiếm pháp thượng thừa phiêu dật như mây trời, tăng 25% sát thương kiếm khí và +10 Tốc Độ xuất chiêu.",
    },
    {
        "id": 4,
        "key": "than_thong_dai_hoang_than_chi",
        "name": "Đại Hoang Thần Chỉ",
        "category": "cong_phap",
        "category_name": "Thần Thông",
        "cost_points": 1200,
        "required_rank": "Chân Truyền Đệ Tử",
        "icon": "☝️",
        "description": "Một chỉ phá toái hư không, ngưng tụ sát khí đại hoang giáng đòn chí mạng bỏ qua 30% phòng ngự mục tiêu.",
    },
    {
        "id": 5,
        "key": "than_thong_thai_co_te_than",
        "name": "Thái Cổ Tế Thần Bí Thuật",
        "category": "cong_phap",
        "category_name": "Bí Tịch Trấn Phái",
        "cost_points": 3000,
        "required_rank": "Trưởng Lão Tông Môn",
        "icon": "🔮",
        "description": "Bí thuật tối thượng trấn phái, hiến tế một tia thọ nguyên để triệu hồi tàn ảnh Cổ Thần giáng lâm diệt thế.",
    },

    # -------------------------------------------------------------------------
    # 2. ĐAN DƯỢC ĐỘT PHÁ & BỔ TRỢ
    # -------------------------------------------------------------------------
    {
        "id": 6,
        "key": "dan_truc_co_tong_mon",
        "name": "Trúc Cơ Đan (Tông Môn Luyện)",
        "category": "dan_duoc",
        "category_name": "Đan Dược",
        "cost_points": 80,
        "required_rank": "Ngoại Môn Đệ Tử",
        "icon": "💊",
        "description": "Đan dược thượng phẩm do Dược Đường tông môn luyện chế, tăng tỷ lệ đột phá Trúc Cơ thêm 20%.",
    },
    {
        "id": 7,
        "key": "dan_ket_kim_dan_tong_mon",
        "name": "Kết Kim Đan (Thuần Khiết)",
        "category": "dan_duoc",
        "category_name": "Đan Dược",
        "cost_points": 250,
        "required_rank": "Nội Môn Đệ Tử",
        "icon": "🟡",
        "description": "Trợ lực ngưng kết hạt châu Kim Đan viên mãn, triệt tiêu nguy cơ nổ đan điền lúc Kết Đan.",
    },
    {
        "id": 8,
        "key": "dan_cuu_chuyen_hoan_hon",
        "name": "Cửu Chuyển Hoàn Hồn Đan",
        "category": "dan_duoc",
        "category_name": "Đan Dược",
        "cost_points": 600,
        "required_rank": "Nội Môn Đệ Tử",
        "icon": "💖",
        "description": "Thần dược bảo mệnh, khi Sinh Lực về 0 lập tức hồi sinh với 50% HP và xua tan mọi trạng thái dị thường.",
    },

    # -------------------------------------------------------------------------
    # 3. PHÁP BẢO & KHÍ CỤ TÔNG MÔN
    # -------------------------------------------------------------------------
    {
        "id": 9,
        "key": "phap_bao_thanh_hu_linh_thuan",
        "name": "Thanh Hư Linh Thuẫn",
        "category": "phap_bao",
        "category_name": "Pháp Bảo",
        "cost_points": 350,
        "required_rank": "Nội Môn Đệ Tử",
        "icon": "🛡️",
        "description": "Linh thuẫn khắc đại trận hộ thể môn phái, hấp thụ 200 sát thương pháp thuật trước khi vỡ vụn.",
    },
    {
        "id": 10,
        "key": "phap_bao_thanh_van_phi_chu",
        "name": "Thanh Vân Phi Chu",
        "category": "phap_bao",
        "category_name": "Pháp Bảo",
        "cost_points": 800,
        "required_rank": "Chân Truyền Đệ Tử",
        "icon": "⛵",
        "description": "Phi chu ngự phong tốc độ cực cao, giảm 50% thời gian chờ (cooldown) khi lịch luyện bí cảnh.",
    },

    # -------------------------------------------------------------------------
    # 4. ĐẶC QUYỀN TÔNG MÔN
    # -------------------------------------------------------------------------
    {
        "id": 11,
        "key": "dac_quyen_tu_linh_tran_1h",
        "name": "Lệnh Bài Tụ Linh Trận (1 Giờ)",
        "category": "dac_quyen",
        "category_name": "Đặc Quyền",
        "cost_points": 100,
        "required_rank": "Ngoại Môn Đệ Tử",
        "icon": "🌀",
        "description": "Bước vào động phủ Tụ Linh Trận trung tâm tông môn, nhân đôi (+100%) lượng exp nhận được khi tĩnh tọa tu luyện.",
    },
    {
        "id": 12,
        "key": "dac_quyen_thang_chuc_noi_mon",
        "name": "Đề Bạt Thăng Cấp Nội Môn",
        "category": "dac_quyen",
        "category_name": "Đặc Quyền",
        "cost_points": 500,
        "required_rank": "Ngoại Môn Đệ Tử",
        "icon": "🏅",
        "description": "Chứng nhận cống hiến to lớn, miễn sát hạch tiến cử trực tiếp trở thành Nội Môn Đệ Tử tông môn.",
    },
]

# =============================================================================
# HỆ THỐNG TRA CỨU NHANH
# =============================================================================
TOTAL_MUC_DOI: int = len(DANH_MUC_DOI_THUONG)
MUC_DOI_BY_ID: Dict[int, Dict[str, Any]] = {m["id"]: m for m in DANH_MUC_DOI_THUONG}
MUC_DOI_BY_KEY: Dict[str, Dict[str, Any]] = {m["key"]: m for m in DANH_MUC_DOI_THUONG}


# =============================================================================
# CÁC HÀM TIỆN ÍCH QUẢN LÝ ĐIỂM CỐNG HIẾN
# =============================================================================
def get_all_muc_doi() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh mục đổi thưởng bằng Điểm Cống Hiến."""
    return DANH_MUC_DOI_THUONG


def get_muc_doi_by_id(muc_id: int) -> Optional[Dict[str, Any]]:
    """Tra cứu mục đổi thưởng theo ID."""
    return MUC_DOI_BY_ID.get(muc_id)


def get_muc_doi_by_key(key: str) -> Optional[Dict[str, Any]]:
    """Tra cứu mục đổi thưởng theo key."""
    return MUC_DOI_BY_KEY.get(key.strip().lower())


def get_muc_doi_by_category(category: str) -> List[Dict[str, Any]]:
    """Lọc danh mục đổi thưởng theo loại ('cong_phap', 'dan_duoc', 'phap_bao', 'dac_quyen')."""
    cat = category.strip().lower()
    return [m for m in DANH_MUC_DOI_THUONG if m["category"] == cat]


def kiem_tra_du_diem_doi(current_points: int, muc_id_or_key: Any) -> Tuple[bool, str, int]:
    """
    Kiểm tra xem người chơi có đủ Điểm Cống Hiến để đổi vật phẩm hay không.
    Trả về: (Có đủ không, Thông báo, Số điểm còn thiếu nếu không đủ)
    """
    if isinstance(muc_id_or_key, int):
        muc = get_muc_doi_by_id(muc_id_or_key)
    else:
        muc = get_muc_doi_by_key(str(muc_id_or_key))

    if not muc:
        return False, "Không tìm thấy vật phẩm hoặc công pháp trong danh mục Tông Môn.", 0

    cost = muc["cost_points"]
    if current_points < cost:
        thieu = cost - current_points
        return False, f"Không đủ Điểm Cống Hiến! Cần {cost:,} điểm, bạn còn thiếu {thieu:,} điểm.", thieu

    return True, f"Đủ điều kiện đổi [{muc['name']}] với giá {cost:,} Điểm Cống Hiến.", 0
