# -*- coding: utf-8 -*-
"""
tat_ca_dan_duoc.py
===================
Lưu trữ danh sách toàn bộ 56 loại đan dược trong hệ thống Tu Tiên:
- Nhóm I: Đột Phá Cảnh Giới (Từ Ngưng Khí đến Vô Cảnh: Nhất Bộ, Nhị Bộ, Tam Bộ, Tứ Bộ, Ngũ Bộ, Lục Bộ Cảnh)
- Nhóm II: Đan Dược Nền Tảng & Tu Thân (Cơ Sở Luyện Khí)
- Nhóm III: Y Tế, Trị Thương & Khôi Phục Sinh Cơ
- Nhóm IV: Phụ Trợ Đặc Biệt & Tranh Đấu Khốc Liệt
- Nhóm V: Tà Đạo, Độc Dược & Khống Yêu

Cung cấp đầy đủ cấu trúc dữ liệu và các hàm tra cứu theo ID, tên, bí danh (alias) và phân nhóm.
"""
from typing import Optional, Dict, Any, List
import unicodedata


def _normalize_str(text: str) -> str:
    """Chuẩn hóa chuỗi tìm kiếm (chữ thường, bỏ khoảng trắng thừa)."""
    return " ".join(text.strip().lower().split())


# =============================================================================
# DANH SÁCH CHI TIẾT TOÀN BỘ ĐAN DƯỢC
# =============================================================================
DAN_DUOC_DATA: List[Dict[str, Any]] = [
    # -------------------------------------------------------------------------
    # I. NHÓM ĐỘT PHÁ CẢNH GIỚI (TỪ NGƯNG KHÍ ĐẾN VÔ CẢNH)
    # -------------------------------------------------------------------------
    # 1. Nhất Bộ Cảnh (Tung Hoành Cảnh)
    # Giai đoạn nền tảng, mượn linh khí và tài nguyên thiên địa để tu luyện thân thể và nguyên thần.
    {
        "id": 1,
        "key": "truc_co_dan",
        "name": "Trúc Cơ Đan",
        "aliases": [],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "1. Nhất Bộ Cảnh (Tung Hoành Cảnh)",
        "target_realm": "Từ Ngưng Khí Đỉnh Phong ➔ Trúc Cơ Sơ Kỳ",
        "description": "Nén linh khí dồi dào trong đan điền hóa thành dạng lỏng.",
    },
    {
        "id": 2,
        "key": "ket_kim_dan",
        "name": "Kết Kim Đan",
        "aliases": ["Thiên Ly Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "1. Nhất Bộ Cảnh (Tung Hoành Cảnh)",
        "target_realm": "Từ Trúc Cơ Đỉnh Phong ➔ Kết Đan Sơ Kỳ",
        "description": "Đan dược thượng cổ cường ép linh lực lỏng ngưng tụ thành hạt châu Kim Đan.",
    },
    {
        "id": 3,
        "key": "ket_anh_dan",
        "name": "Kết Anh Đan",
        "aliases": [],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "1. Nhất Bộ Cảnh (Tung Hoành Cảnh)",
        "target_realm": "Từ Kết Đan Đỉnh Phong ➔ Nguyên Anh Sơ Kỳ",
        "description": "Dùng hỏa diễm thiêu đốt, đập vỡ Kim Đan để hóa hình Nguyên Anh.",
    },
    {
        "id": 4,
        "key": "hoa_than_dan",
        "name": "Hóa Thần Đan",
        "aliases": [],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "1. Nhất Bộ Cảnh (Tung Hoành Cảnh)",
        "target_realm": "Từ Nguyên Anh Đỉnh Phong ➔ Hóa Thần Sơ Kỳ",
        "description": "Cung cấp linh lực bạo phát, kết hợp với đốn ngộ Ý Cảnh để ngưng tụ Nguyên Thần.",
    },
    {
        "id": 5,
        "key": "anh_bien_dan",
        "name": "Anh Biến Đan",
        "aliases": [],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "1. Nhất Bộ Cảnh (Tung Hoành Cảnh)",
        "target_realm": "Từ Hóa Thần Đỉnh Phong ➔ Anh Biến Sơ Kỳ",
        "description": "Đan dược chứa năng lượng của Tiên Ngọc, chuyển hóa linh lực phàm tục thành Tiên Lực.",
    },
    {
        "id": 6,
        "key": "van_dinh_ngo_tram_dan",
        "name": "Vấn Đỉnh Ngộ Trảm Đan",
        "aliases": [],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "1. Nhất Bộ Cảnh (Tung Hoành Cảnh)",
        "target_realm": "Từ Anh Biến Đỉnh Phong ➔ Vấn Đỉnh Sơ Kỳ",
        "description": "Giúp chém đứt phàm căn, ngưng tụ đạo tâm.",
    },
    {
        "id": 7,
        "key": "am_hu_duong_hon_dan",
        "name": "Âm Hư Dưỡng Hồn Đan",
        "aliases": ["Dưỡng Hồn Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "1. Nhất Bộ Cảnh (Tung Hoành Cảnh)",
        "target_realm": "Từ Vấn Đỉnh Đỉnh Phong ➔ Âm Hư Sơ Kỳ",
        "description": "Nuôi dưỡng nguyên thần hấp thụ hàn khí vũ trụ, củng cố Hư Thể.",
    },
    {
        "id": 8,
        "key": "duong_thuc_luyen_phach_dan",
        "name": "Dương Thực Luyện Phách Đan",
        "aliases": ["Luyện Phách Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "1. Nhất Bộ Cảnh (Tung Hoành Cảnh)",
        "target_realm": "Từ Âm Hư Đỉnh Phong ➔ Dương Thực Sơ Kỳ",
        "description": "Bổ sung dương khí cực hạn, biến Hư Thể thành Thực Thể hoàn mỹ.",
    },

    # 2. Nhị Bộ Cảnh (Phi Thiên Cảnh)
    # Bắt đầu cướp đoạt pháp tắc và thao túng không gian. Đan dược luyện từ máu thịt cường giả và tinh thần lực.
    {
        "id": 9,
        "key": "hu_khong_khuy_canh_dan",
        "name": "Hư Không Khuy Cảnh Đan",
        "aliases": ["Khuy Niết Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "2. Nhị Bộ Cảnh (Phi Thiên Cảnh)",
        "target_realm": "Từ Dương Thực Đỉnh Phong ➔ Khuy Niết Sơ Kỳ",
        "description": "Bào chế từ nhãn cầu tinh thú, giúp thần thức xuyên thủng bích chướng hư không.",
    },
    {
        "id": 10,
        "key": "niet_ban_tinh_huyet_dan",
        "name": "Niết Bàn Tịnh Huyết Đan",
        "aliases": ["Tịnh Niết Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "2. Nhị Bộ Cảnh (Phi Thiên Cảnh)",
        "target_realm": "Từ Khuy Niết Đỉnh Phong ➔ Tịnh Niết Sơ Kỳ",
        "description": "Đun sôi từ tinh huyết Cổ Tộc, thanh tẩy nhục thân chuẩn bị cho sự lột xác.",
    },
    {
        "id": 11,
        "key": "toai_tinh_doat_menh_dan",
        "name": "Toái Tinh Đoạt Mệnh Đan",
        "aliases": ["Toái Niết Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "2. Nhị Bộ Cảnh (Phi Thiên Cảnh)",
        "target_realm": "Từ Tịnh Niết Đỉnh Phong ➔ Toái Niết Sơ Kỳ",
        "description": "Nén từ lõi tu chân tinh đang sụp đổ, cung cấp bạo lực đập nát Niết Bàn để hòa nhập tinh không.",
    },

    # 3. Tam Bộ Cảnh (Vô Biên Cảnh - Không Chi Cảnh)
    # Hòa làm một với vũ trụ, đan dược là sự cụ thể hóa của Bản Nguyên Đại Đạo.
    {
        "id": 12,
        "key": "ban_nguyen_tu_luc_dan",
        "name": "Bản Nguyên Tụ Lực Đan",
        "aliases": ["Không Niết Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "3. Tam Bộ Cảnh (Vô Biên Cảnh - Không Chi Cảnh)",
        "target_realm": "Từ Toái Niết Đỉnh Phong ➔ Không Niết Sơ Kỳ",
        "description": "Một tia Bản Nguyên (Sinh Tử, Lôi, Hỏa) bị bóp nghẹt thành đan.",
    },
    {
        "id": 13,
        "key": "vo_gian_khong_linh_dan",
        "name": "Vô Gian Không Linh Đan",
        "aliases": ["Không Linh Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "3. Tam Bộ Cảnh (Vô Biên Cảnh - Không Chi Cảnh)",
        "target_realm": "Từ Không Niết Đỉnh Phong ➔ Không Linh Sơ Kỳ",
        "description": "Luyện từ \"Gió của Hư Vô\", đưa đạo tâm vào trạng thái rỗng tuếch, đồng hóa với ý chí vũ trụ.",
    },
    {
        "id": 14,
        "key": "thai_diet_khong_huyen_dan",
        "name": "Thái Diệt Không Huyền Đan",
        "aliases": ["Không Huyền Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "3. Tam Bộ Cảnh (Vô Biên Cảnh - Không Chi Cảnh)",
        "target_realm": "Từ Không Linh Đỉnh Phong ➔ Không Huyền Sơ Kỳ",
        "description": "Trộn lẫn tro tàn của ức vạn lôi kiếp, tạo lớp giáp tinh thần tuyệt đối để thao túng quy luật hưng suy.",
    },
    {
        "id": 15,
        "key": "huong_hoa_phong_than_dan",
        "name": "Hương Hỏa Phong Thần Đan",
        "aliases": ["Đại Thiên Tôn Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "3. Tam Bộ Cảnh (Vô Biên Cảnh - Không Chi Cảnh)",
        "target_realm": "Từ Không Huyền Đỉnh Phong ➔ Đại Thiên Tôn Sơ Kỳ",
        "description": "Luyện từ Tín Ngưỡng Lực của một giới trong hàng vạn năm, đúc lại thần cách Đại Thiên Tôn độc tôn tinh vực.",
    },

    # 4. Tứ Bộ Cảnh (Đạp Thiên - Không Diệt - Siêu Thoát)
    # Cảnh giới của các Đấng Sáng Tạo. Không còn dùng nguyên liệu, đan dược nặn ra từ hư vô và ý niệm.
    {
        "id": 16,
        "key": "chan_gia_dao_mong_dan",
        "name": "Chân Giả Đạo Mộng Đan",
        "aliases": ["Đạp Thiên Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "4. Tứ Bộ Cảnh (Đạp Thiên - Không Diệt - Siêu Thoát)",
        "target_realm": "Từ Đại Thiên Tôn Đỉnh Phong ➔ Đạp Thiên Sơ Kỳ",
        "description": "Cực hạn của thần thông \"Hóa Không Thành Có\". Đưa người dùng vào mộng cảnh để ngộ ra lằn ranh Chân - Giả của Thiên Đạo.",
    },
    {
        "id": 17,
        "key": "tao_hoa_van_vat_dan",
        "name": "Tạo Hóa Vạn Vật Đan",
        "aliases": ["Không Diệt Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "4. Tứ Bộ Cảnh (Đạp Thiên - Không Diệt - Siêu Thoát)",
        "target_realm": "Từ Đạp Thiên Đỉnh Phong ➔ Không Diệt Sơ Kỳ",
        "description": "Luyện hóa từ một vũ trụ sơ khai, cắn nuốt để có sức mạnh hủy diệt và dung nạp hàng tỷ tinh hệ.",
    },
    {
        "id": 18,
        "key": "quy_tac_tich_diet_dan",
        "name": "Quy Tắc Tịch Diệt Đan",
        "aliases": ["Siêu Thoát Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "4. Tứ Bộ Cảnh (Đạp Thiên - Không Diệt - Siêu Thoát)",
        "target_realm": "Từ Không Diệt Đỉnh Phong ➔ Siêu Thoát Sơ Kỳ",
        "description": "Tước đoạt trực tiếp quyền bính cốt lõi của Vận Mệnh, chém đứt mọi luân hồi nhân quả để siêu thoát khỏi kịch bản của thiên địa.",
    },

    # 5. Ngũ Bộ Cảnh (Vĩnh Hằng Cảnh)
    {
        "id": 19,
        "key": "vinh_hang_bat_diet_dan",
        "name": "Vĩnh Hằng Bất Diệt Đan",
        "aliases": ["Vĩnh Hằng Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "5. Ngũ Bộ Cảnh (Vĩnh Hằng Cảnh)",
        "target_realm": "Từ Siêu Thoát Đỉnh Phong ➔ Vĩnh Hằng Cảnh",
        "description": "Ở cảnh giới không còn Sơ - Trung - Hậu, viên \"đan\" này thực chất là việc hòa dung với dòng chảy thời gian của đại vũ trụ. Nuốt vào, quá khứ, hiện tại và tương lai hợp nhất thành một điểm bất diệt.",
    },

    # 6. Lục Bộ Cảnh (Vô Cảnh - Cảnh Giới Tối Cao)
    {
        "id": 20,
        "key": "vo_tu_hu_vo_dan",
        "name": "Vô Tự Hư Vô Đan",
        "aliases": ["Vô Cảnh Đan", "Đạo Đan"],
        "group_id": "I",
        "group_name": "Nhóm Đột Phá Cảnh Giới",
        "subgroup": "6. Lục Bộ Cảnh (Vô Cảnh - Cảnh Giới Tối Cao)",
        "target_realm": "Vô Cảnh (Cực Đạo Chi Đỉnh)",
        "description": "Điểm tận cùng của tu luyện. Không cần đột phá, không có cảnh giới nhỏ. Đây không phải thuốc để uống, mà là một ý niệm thuần túy: Khi bạn nghĩ nó là đan, nó là đan vạn năng; khi bạn xua tay, nó tan vào Hư Vô. Nó chính là \"Đạo\".",
    },

    # -------------------------------------------------------------------------
    # II. NHÓM ĐAN DƯỢC NỀN TẢNG & TU THÂN (CƠ SỞ LUYỆN KHÍ)
    # -------------------------------------------------------------------------
    {
        "id": 21,
        "key": "ich_coc_dan",
        "name": "Ích Cốc Đan",
        "aliases": [],
        "group_id": "II",
        "group_name": "Nhóm Đan Dược Nền Tảng & Tu Thân",
        "subgroup": "Cơ Sở Luyện Khí",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Cắt đứt nhu cầu ăn uống phàm tục khi bế quan.",
    },
    {
        "id": 22,
        "key": "tay_tuy_dan",
        "name": "Tẩy Tủy Đan",
        "aliases": [],
        "group_id": "II",
        "group_name": "Nhóm Đan Dược Nền Tảng & Tu Thân",
        "subgroup": "Cơ Sở Luyện Khí",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Bài trừ tạp chất xương tủy, thay đổi tư chất cùi bắp thành có thể tu luyện.",
    },
    {
        "id": 23,
        "key": "thoi_the_dan",
        "name": "Thối Thể Đan",
        "aliases": ["Luyện Cốt Đan"],
        "group_id": "II",
        "group_name": "Nhóm Đan Dược Nền Tảng & Tu Thân",
        "subgroup": "Cơ Sở Luyện Khí",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Cường hóa nhục thể, gân cốt, chịu tải áp lực linh lực.",
    },
    {
        "id": 24,
        "key": "thong_mach_dan",
        "name": "Thông Mạch Đan",
        "aliases": [],
        "group_id": "II",
        "group_name": "Nhóm Đan Dược Nền Tảng & Tu Thân",
        "subgroup": "Cơ Sở Luyện Khí",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Đả thông ách tắc, mở rộng đường dẫn linh lực trong kinh mạch.",
    },
    {
        "id": 25,
        "key": "ho_mach_dan",
        "name": "Hộ Mạch Đan",
        "aliases": [],
        "group_id": "II",
        "group_name": "Nhóm Đan Dược Nền Tảng & Tu Thân",
        "subgroup": "Cơ Sở Luyện Khí",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Ngăn kinh mạch đứt gãy khi bạo phát linh lực.",
    },
    {
        "id": 26,
        "key": "tinh_tam_dan",
        "name": "Tĩnh Tâm Đan",
        "aliases": ["Thanh Tâm Đan"],
        "group_id": "II",
        "group_name": "Nhóm Đan Dược Nền Tảng & Tu Thân",
        "subgroup": "Cơ Sở Luyện Khí",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Trấn an thần trí, chống tâm ma quấy nhiễu lúc nhập định.",
    },
    {
        "id": 27,
        "key": "uan_linh_dan",
        "name": "Uẩn Linh Đan",
        "aliases": [],
        "group_id": "II",
        "group_name": "Nhóm Đan Dược Nền Tảng & Tu Thân",
        "subgroup": "Cơ Sở Luyện Khí",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Cung cấp linh khí tinh thuần trực tiếp, không cần tốn thời gian hấp thụ.",
    },
    {
        "id": 28,
        "key": "dung_linh_dan",
        "name": "Dung Linh Đan",
        "aliases": [],
        "group_id": "II",
        "group_name": "Nhóm Đan Dược Nền Tảng & Tu Thân",
        "subgroup": "Cơ Sở Luyện Khí",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Dung hợp các luồng linh lực hệ tạp (băng, hỏa, lôi) không bị xung đột.",
    },
    {
        "id": 29,
        "key": "bo_thien_dan",
        "name": "Bổ Thiên Đan",
        "aliases": [],
        "group_id": "II",
        "group_name": "Nhóm Đan Dược Nền Tảng & Tu Thân",
        "subgroup": "Cơ Sở Luyện Khí",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Đoạt tạo hóa thiên địa, trực tiếp thăng cấp linh căn (từ Tạp linh căn lên Thiên linh căn).",
    },

    # -------------------------------------------------------------------------
    # III. NHÓM Y TẾ, TRỊ THƯƠNG & KHÔI PHỤC SINH CƠ
    # -------------------------------------------------------------------------
    {
        "id": 30,
        "key": "hoi_khi_dan",
        "name": "Hồi Khí Đan",
        "aliases": [],
        "group_id": "III",
        "group_name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "subgroup": "Khôi Phục Linh Lực",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Khôi phục nhanh linh lực khô cạn trong lúc chém giết.",
    },
    {
        "id": 31,
        "key": "bo_huyet_dan",
        "name": "Bổ Huyết Đan",
        "aliases": ["Hóa Ứ Đan"],
        "group_id": "III",
        "group_name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "subgroup": "Trị Thương Ngoại Thể",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Trị thương ngoài da, tái tạo máu thịt phàm nhân.",
    },
    {
        "id": 32,
        "key": "tieu_hoan_dan",
        "name": "Tiểu Hoàn Đan",
        "aliases": ["Đại Hoàn Đan"],
        "group_id": "III",
        "group_name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "subgroup": "Trị Nội Thương",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Trị nội thương nghiêm trọng, nối liền gân mạch đứt đoạn.",
    },
    {
        "id": 33,
        "key": "bach_thao_dan",
        "name": "Bách Thảo Đan",
        "aliases": [],
        "group_id": "III",
        "group_name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "subgroup": "Giải Độc",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Thanh lọc cơ thể, giải bách độc thông thường.",
    },
    {
        "id": 34,
        "key": "hoi_xuan_dan",
        "name": "Hồi Xuân Đan",
        "aliases": [],
        "group_id": "III",
        "group_name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "subgroup": "Sinh Cơ Liền Thương",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Cung cấp sinh cơ mãnh liệt, làm lành vết thương thấu xương.",
    },
    {
        "id": 35,
        "key": "phuc_nguyen_dan",
        "name": "Phục Nguyên Đan",
        "aliases": [],
        "group_id": "III",
        "group_name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "subgroup": "Khôi Phục Bản Nguyên",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Bù đắp bản nguyên tinh huyết bị tổn hao do dùng cấm thuật.",
    },
    {
        "id": 36,
        "key": "sinh_cot_dan",
        "name": "Sinh Cốt Đan",
        "aliases": [],
        "group_id": "III",
        "group_name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "subgroup": "Tái Sinh Nhục Thân",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Tái tạo tứ chi, mọc lại nhục thể chỉ cần nguyên thần còn sống.",
    },
    {
        "id": 37,
        "key": "tuc_menh_dan",
        "name": "Tục Mệnh Đan",
        "aliases": ["Điếu Mệnh Đan"],
        "group_id": "III",
        "group_name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "subgroup": "Kéo Dài Hơi Tàn",
        "target_realm": "Tu Sĩ Hấp Hối",
        "description": "Níu giữ tàn hồn, kéo dài sinh mệnh kẻ sắp chết thêm vài tháng.",
    },
    {
        "id": 38,
        "key": "tho_nguyen_dan",
        "name": "Thọ Nguyên Đan",
        "aliases": ["Diên Thọ Đan"],
        "group_id": "III",
        "group_name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "subgroup": "Gia Tăng Thọ Mệnh",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Tăng tuổi thọ (10 năm đến ngàn năm), chỉ có tác dụng một lần duy nhất trong đời.",
    },
    {
        "id": 39,
        "key": "cuu_chuyen_hoan_hon_dan",
        "name": "Cửu Chuyển Hoàn Hồn Đan",
        "aliases": [],
        "group_id": "III",
        "group_name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "subgroup": "Cải Tử Hoàn Sinh",
        "target_realm": "Tu Sĩ Vừa Tán Hồn",
        "description": "Kéo linh hồn vừa tiêu tán về lại thể xác, cải tử hoàn sinh cấp cao.",
    },
    {
        "id": 40,
        "key": "tao_hoa_than_dan",
        "name": "Tạo Hóa Thần Đan",
        "aliases": ["Chắp Vá Cõi Chết Đan"],
        "group_id": "III",
        "group_name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "subgroup": "Nghịch Chuyển Luân Hồi",
        "target_realm": "Cực Hạn Chắp Vá",
        "description": "Nghịch chuyển luân hồi, vá lại nguyên thần đã tan nát trong vũ trụ.",
    },

    # -------------------------------------------------------------------------
    # IV. NHÓM PHỤ TRỢ ĐẶC BIỆT & TRANH ĐẤU KHỐC LIỆT
    # -------------------------------------------------------------------------
    {
        "id": 41,
        "key": "bao_khi_dan",
        "name": "Bạo Khí Đan",
        "aliases": ["Cuồng Bạo Đan"],
        "group_id": "IV",
        "group_name": "Nhóm Phụ Trợ Đặc Biệt & Tranh Đấu Khốc Liệt",
        "subgroup": "Bộc Phát Sức Mạnh",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Tăng gấp ba sức mạnh tức thời, hậu quả suy nhược trầm trọng.",
    },
    {
        "id": 42,
        "key": "than_hanh_dan",
        "name": "Thần Hành Đan",
        "aliases": [],
        "group_id": "IV",
        "group_name": "Nhóm Phụ Trợ Đặc Biệt & Tranh Đấu Khốc Liệt",
        "subgroup": "Tốc Độ & Độn Thuật",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Đẩy tốc độ ngự kiếm lên đỉnh điểm để truy sát hoặc chạy trốn.",
    },
    {
        "id": 43,
        "key": "an_tuc_dan",
        "name": "Ẩn Tức Đan",
        "aliases": [],
        "group_id": "IV",
        "group_name": "Nhóm Phụ Trợ Đặc Biệt & Tranh Đấu Khốc Liệt",
        "subgroup": "Che Giấu Tu Vi",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Che giấu hoàn toàn tu vi và dao động linh lực trước kẻ địch mạnh hơn.",
    },
    {
        "id": 44,
        "key": "dich_dung_dan",
        "name": "Dịch Dung Đan",
        "aliases": [],
        "group_id": "IV",
        "group_name": "Nhóm Phụ Trợ Đặc Biệt & Tranh Đấu Khốc Liệt",
        "subgroup": "Ngụy Trang Diện Mạo",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Biến đổi xương cốt, khuôn mặt, và khí tức thành người khác.",
    },
    {
        "id": 45,
        "key": "tru_nhan_dan",
        "name": "Trú Nhan Đan",
        "aliases": ["Định Nhan Đan"],
        "group_id": "IV",
        "group_name": "Nhóm Phụ Trợ Đặc Biệt & Tranh Đấu Khốc Liệt",
        "subgroup": "Duy Trì Thanh Xuân",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Khóa chặt dung nhan ở độ tuổi thanh xuân vĩnh viễn.",
    },
    {
        "id": 46,
        "key": "ti_thuy_dan",
        "name": "Tị Thủy Đan",
        "aliases": ["Tị Độc Đan"],
        "group_id": "IV",
        "group_name": "Nhóm Phụ Trợ Đặc Biệt & Tranh Đấu Khốc Liệt",
        "subgroup": "Kháng Môi Trường Khắc Nghiệt",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Kháng áp lực biển sâu và vô hiệu hóa chướng khí đầm lầy.",
    },
    {
        "id": 47,
        "key": "hoa_linh_dan",
        "name": "Hỏa Linh Đan",
        "aliases": ["Băng Linh Đan"],
        "group_id": "IV",
        "group_name": "Nhóm Phụ Trợ Đặc Biệt & Tranh Đấu Khốc Liệt",
        "subgroup": "Kết Giới Nguyên Tố",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Tạo kết giới nguyên tố kháng lại môi trường dung nham hoặc hàn băng.",
    },
    {
        "id": 48,
        "key": "vong_tinh_dan",
        "name": "Vong Tình Đan",
        "aliases": [],
        "group_id": "IV",
        "group_name": "Nhóm Phụ Trợ Đặc Biệt & Tranh Đấu Khốc Liệt",
        "subgroup": "Đoạn Tuyệt Thất Tình",
        "target_realm": "Vô Tình Đạo / Thái Thượng Vong Tình",
        "description": "Cắt đứt thất tình lục dục, chuyên dùng cho người tu Vô Tình Đạo hoặc thái thượng vong tình.",
    },

    # -------------------------------------------------------------------------
    # V. NHÓM TÀ ĐẠO, ĐỘC DƯỢC & KHỐNG YÊU (ĐẬM CHẤT PHẢN DIỆN)
    # -------------------------------------------------------------------------
    {
        "id": 49,
        "key": "huyet_sat_dan",
        "name": "Huyết Sát Đan",
        "aliases": [],
        "group_id": "V",
        "group_name": "Nhóm Tà Đạo, Độc Dược & Khống Yêu",
        "subgroup": "Thiêu Đốt Tinh Huyết",
        "target_realm": "Toàn Bộ Tu Sĩ",
        "description": "Thiêu đốt thọ mệnh và tinh huyết để đổi lấy sức mạnh chẻ trời, tác dụng phụ có thể rớt đại cảnh giới.",
    },
    {
        "id": 50,
        "key": "khong_tam_dan",
        "name": "Khống Tâm Đan",
        "aliases": ["Phệ Tâm Đan"],
        "group_id": "V",
        "group_name": "Nhóm Tà Đạo, Độc Dược & Khống Yêu",
        "subgroup": "Khống Chế & Cổ Độc",
        "target_realm": "Nô Dịch Đối Phương",
        "description": "Cấy cổ độc vào tim đối phương; không có thuốc giải định kỳ sẽ vạn tiễn xuyên tâm.",
    },
    {
        "id": 51,
        "key": "nhuyen_can_tan",
        "name": "Nhuyễn Cân Tán",
        "aliases": [],
        "group_id": "V",
        "group_name": "Nhóm Tà Đạo, Độc Dược & Khống Yêu",
        "subgroup": "Phong Bế Tu Vi",
        "target_realm": "Vô Khí Lực",
        "description": "Vô sắc vô vị, phong bế kinh mạch khiến tu sĩ không thể thi triển pháp thuật.",
    },
    {
        "id": 52,
        "key": "phe_hon_dan",
        "name": "Phệ Hồn Đan",
        "aliases": [],
        "group_id": "V",
        "group_name": "Nhóm Tà Đạo, Độc Dược & Khống Yêu",
        "subgroup": "Diệt Tuyệt Thần Hồn",
        "target_realm": "Hủy Diệt Nguyên Thần",
        "description": "Tiêu diệt trực tiếp nguyên thần, khiến mục tiêu vĩnh bất siêu sinh, triệt để bay màu khỏi luân hồi.",
    },
    {
        "id": 53,
        "key": "hoa_cot_dan",
        "name": "Hóa Cốt Đan",
        "aliases": [],
        "group_id": "V",
        "group_name": "Nhóm Tà Đạo, Độc Dược & Khống Yêu",
        "subgroup": "Xóa Dấu Vết",
        "target_realm": "Phân Hủy Thi Thể",
        "description": "Đổ lên xác chết lập tức tan thành bãi nước vàng, tuyệt kỹ xóa dấu vết giết người cướp của.",
    },
    {
        "id": 54,
        "key": "hoa_hinh_dan",
        "name": "Hóa Hình Đan",
        "aliases": [],
        "group_id": "V",
        "group_name": "Nhóm Tà Đạo, Độc Dược & Khống Yêu",
        "subgroup": "Yêu Thú Biến Hình",
        "target_realm": "Yêu Thú / Linh Thú",
        "description": "Ép yêu thú lột xác hóa thành hình người sớm hơn cảnh giới quy định.",
    },
    {
        "id": 55,
        "key": "duc_thu_dan",
        "name": "Dục Thú Đan",
        "aliases": [],
        "group_id": "V",
        "group_name": "Nhóm Tà Đạo, Độc Dược & Khống Yêu",
        "subgroup": "Kích Động Yêu Thú",
        "target_realm": "Yêu Thú",
        "description": "Chứa năng lượng bạo loạn ép yêu thú tiến hóa và phát điên.",
    },
    {
        "id": 56,
        "key": "ngu_thu_dan",
        "name": "Ngự Thú Đan",
        "aliases": [],
        "group_id": "V",
        "group_name": "Nhóm Tà Đạo, Độc Dược & Khống Yêu",
        "subgroup": "Huyết Khế Nô Dịch",
        "target_realm": "Yêu Linh / Yêu Thú",
        "description": "Thiết lập huyết khế, tước đoạt linh hồn ép yêu linh vĩnh viễn làm nô bộc.",
    },
]

# =============================================================================
# DANH MỤC NHÓM ĐAN DƯỢC
# =============================================================================
DAN_DUOC_GROUPS: Dict[str, Dict[str, Any]] = {
    "I": {
        "id": "I",
        "name": "Nhóm Đột Phá Cảnh Giới (Từ Ngưng Khí đến Vô Cảnh)",
        "count": 20,
        "subgroups": [
            "1. Nhất Bộ Cảnh (Tung Hoành Cảnh)",
            "2. Nhị Bộ Cảnh (Phi Thiên Cảnh)",
            "3. Tam Bộ Cảnh (Vô Biên Cảnh - Không Chi Cảnh)",
            "4. Tứ Bộ Cảnh (Đạp Thiên - Không Diệt - Siêu Thoát)",
            "5. Ngũ Bộ Cảnh (Vĩnh Hằng Cảnh)",
            "6. Lục Bộ Cảnh (Vô Cảnh - Cảnh Giới Tối Cao)",
        ],
    },
    "II": {
        "id": "II",
        "name": "Nhóm Đan Dược Nền Tảng & Tu Thân (Cơ Sở Luyện Khí)",
        "count": 9,
        "subgroups": ["Cơ Sở Luyện Khí"],
    },
    "III": {
        "id": "III",
        "name": "Nhóm Y Tế, Trị Thương & Khôi Phục Sinh Cơ",
        "count": 11,
        "subgroups": ["Y Tế & Trị Thương"],
    },
    "IV": {
        "id": "IV",
        "name": "Nhóm Phụ Trợ Đặc Biệt & Tranh Đấu Khốc Liệt",
        "count": 8,
        "subgroups": ["Phụ Trợ & Tranh Đấu"],
    },
    "V": {
        "id": "V",
        "name": "Nhóm Tà Đạo, Độc Dược & Khống Yêu (Đậm Chất Phản Diện)",
        "count": 8,
        "subgroups": ["Tà Đạo & Khống Yêu"],
    },
}

# =============================================================================
# BẢNG BĂM TRA CỨU
# =============================================================================
DAN_DUOC_LIST: List[Dict[str, Any]] = DAN_DUOC_DATA
TOTAL_DAN_DUOC: int = len(DAN_DUOC_LIST)

# Bảng tra theo ID
DAN_DUOC_BY_ID: Dict[int, Dict[str, Any]] = {d["id"]: d for d in DAN_DUOC_LIST}

# Bảng tra theo Key
DAN_DUOC_BY_KEY: Dict[str, Dict[str, Any]] = {d["key"]: d for d in DAN_DUOC_LIST}

# Bảng tra theo Tên và Alias (hỗ trợ tra cứu nhanh)
DAN_DUOC_BY_NAME: Dict[str, Dict[str, Any]] = {}
for d in DAN_DUOC_LIST:
    DAN_DUOC_BY_NAME[_normalize_str(d["name"])] = d
    for alias in d["aliases"]:
        DAN_DUOC_BY_NAME[_normalize_str(alias)] = d

# Phân loại theo Group ID
DAN_DUOC_BY_GROUP: Dict[str, List[Dict[str, Any]]] = {}
for d in DAN_DUOC_LIST:
    gid = d["group_id"]
    if gid not in DAN_DUOC_BY_GROUP:
        DAN_DUOC_BY_GROUP[gid] = []
    DAN_DUOC_BY_GROUP[gid].append(d)


# =============================================================================
# CÁC HÀM TIỆN ÍCH TRA CỨU
# =============================================================================
def get_all_dan_duoc() -> List[Dict[str, Any]]:
    """Trả về toàn bộ danh sách đan dược."""
    return DAN_DUOC_LIST


def get_dan_duoc_by_id(pill_id: int) -> Optional[Dict[str, Any]]:
    """Tra cứu đan dược theo ID (1 - 56)."""
    return DAN_DUOC_BY_ID.get(pill_id)


def get_dan_duoc_by_key(key: str) -> Optional[Dict[str, Any]]:
    """Tra cứu đan dược theo key slug (ví dụ: 'truc_co_dan')."""
    return DAN_DUOC_BY_KEY.get(key.strip().lower())


def get_dan_duoc_by_name(name: str) -> Optional[Dict[str, Any]]:
    """
    Tra cứu đan dược theo tên chính thức hoặc tên biệt hiệu (alias).
    Không phân biệt hoa thường.
    """
    if not name:
        return None
    normalized = _normalize_str(name)
    return DAN_DUOC_BY_NAME.get(normalized)


def get_dan_duoc_by_group(group_id: str) -> List[Dict[str, Any]]:
    """
    Lấy danh sách đan dược theo nhóm:
    - 'I': Đột Phá Cảnh Giới (Từ Ngưng Khí đến Vô Cảnh)
    - 'II': Nền Tảng & Tu Thân
    - 'III': Y Tế & Trị Thương
    - 'IV': Phụ Trợ Đặc Biệt
    - 'V': Tà Đạo, Độc Dược & Khống Yêu
    """
    clean_id = group_id.strip().upper()
    return DAN_DUOC_BY_GROUP.get(clean_id, [])


def search_dan_duoc(keyword: str) -> List[Dict[str, Any]]:
    """
    Tìm kiếm đan dược theo từ khóa xuất hiện trong tên, biệt hiệu hoặc mô tả công dụng.
    """
    if not keyword:
        return []
    kw = _normalize_str(keyword)
    results = []
    for d in DAN_DUOC_LIST:
        name_norm = _normalize_str(d["name"])
        aliases_norm = [_normalize_str(a) for a in d["aliases"]]
        desc_norm = _normalize_str(d["description"])
        subgroup_norm = _normalize_str(d["subgroup"])
        target_norm = _normalize_str(d.get("target_realm", ""))
        
        if (kw in name_norm or 
            any(kw in a for a in aliases_norm) or 
            kw in desc_norm or 
            kw in subgroup_norm or
            kw in target_norm):
            results.append(d)
    return results
