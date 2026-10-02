# -*- coding: utf-8 -*-
"""
Package phan_dau
================
Chứa các thành phần hệ thống cơ sở (Phần Đầu) của Bot Tu Tiên:
1. canh_gioi_chung: Thư viện các hệ thống cảnh giới chuẩn Tiên Nghịch:
   - Tu Vi (83 cảnh giới từ Ngưng Khí đến Vô Cảnh)
   - Đan Dược (Phẩm cấp chất lượng đan dược: Phàm Đan, Linh Đan, Tiên Đan)
   - Pháp Bảo (Phẩm giai: Phàm Khí, Linh Khí, Tiên Khí, Thần Khí, Bản Nguyên Thánh Khí)
   - Linh Thú (Phẩm giai yêu thú)
   - Phù Triện (Đẳng cấp bùa chú)
2. dan_duoc: Danh mục chi tiết toàn bộ 56 loại đan dược trong thế giới Tu Tiên.
"""
import sys
from pathlib import Path

# Đảm bảo đường dẫn của phan_dau có trong sys.path để hỗ trợ tương thích ngược
_current_dir = Path(__file__).resolve().parent
if str(_current_dir) not in sys.path:
    sys.path.insert(0, str(_current_dir))

from . import canh_gioi_chung
from . import dan_duoc
from . import nguoi_tu_tien
from . import tai_nguyen
from . import cong_phap

# Hỗ trợ tương thích ngược cho các file import cũ
sys.modules.setdefault("canh_gioi_chung", canh_gioi_chung)
sys.modules.setdefault("dan_duoc", dan_duoc)
sys.modules.setdefault("nguoi_tu_tien", nguoi_tu_tien)
sys.modules.setdefault("tai_nguyen", tai_nguyen)
sys.modules.setdefault("cong_phap", cong_phap)

__all__ = [
    "canh_gioi_chung",
    "dan_duoc",
    "nguoi_tu_tien",
    "tai_nguyen",
    "cong_phap",
]
