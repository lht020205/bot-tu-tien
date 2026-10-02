# -*- coding: utf-8 -*-
"""
Package nguoi_tu_tien
=====================
Chứa các thành phần định hình bản thể và thuộc tính của Người Tu Tiên:
1. toc: Hệ thống 8 Chủng Tộc (4 tộc Chính Đạo, 4 tộc Ma Đạo).
2. linh_can: Hệ thống 10 loại Linh Căn (5 linh căn Chính Đạo, 5 linh căn Ma Đạo).
3. tui_tru_vat: Hệ thống Túi Trữ Vật (quản lý ô chứa đồ, phân loại vật phẩm tu tiên).
4. chi_so: Hệ thống 14 Chỉ Số toàn diện (Cơ bản, Chiến đấu, Chỉ số ẩn).
"""
from .toc import (
    TOC_DATA,
    TOC_LIST,
    TOTAL_TOC,
    TOC_BY_ID,
    TOC_BY_KEY,
    TOC_BY_NAME,
    TOC_BY_FACTION,
    get_all_toc,
    get_toc_by_id,
    get_toc_by_key,
    get_toc_by_name,
    get_toc_by_faction,
    search_toc,
)

from .linh_can import (
    LINH_CAN_DATA,
    LINH_CAN_LIST,
    TOTAL_LINH_CAN,
    LINH_CAN_BY_ID,
    LINH_CAN_BY_KEY,
    LINH_CAN_BY_NAME,
    LINH_CAN_BY_FACTION,
    get_all_linh_can,
    get_linh_can_by_id,
    get_linh_can_by_key,
    get_linh_can_by_name,
    get_linh_can_by_faction,
    search_linh_can,
)

from .tui_tru_vat import (
    ITEM_CATEGORIES,
    TUI_TRU_VAT_TIERS,
    TIER_BY_LEVEL,
    TIER_BY_KEY,
    TuiTruVat,
    get_all_tiers,
    get_tier_by_level,
    get_tier_by_key,
    get_max_slots,
    check_can_add_item,
    detect_item_category,
)

from .chi_so import (
    CHI_SO_DATA,
    CHI_SO_LIST,
    TOTAL_CHI_SO,
    CHI_SO_GROUPS,
    CHI_SO_BY_ID,
    CHI_SO_BY_KEY,
    CHI_SO_BY_CODE,
    CHI_SO_BY_NAME,
    CHI_SO_BY_GROUP,
    BangChiSoTuSi,
    get_all_chi_so,
    get_chi_so_by_id,
    get_chi_so_by_key,
    get_chi_so_by_code,
    get_chi_so_by_name,
    get_chi_so_by_group,
    search_chi_so,
)

__all__ = [
    # toc
    "TOC_DATA",
    "TOC_LIST",
    "TOTAL_TOC",
    "TOC_BY_ID",
    "TOC_BY_KEY",
    "TOC_BY_NAME",
    "TOC_BY_FACTION",
    "get_all_toc",
    "get_toc_by_id",
    "get_toc_by_key",
    "get_toc_by_name",
    "get_toc_by_faction",
    "search_toc",
    # linh_can
    "LINH_CAN_DATA",
    "LINH_CAN_LIST",
    "TOTAL_LINH_CAN",
    "LINH_CAN_BY_ID",
    "LINH_CAN_BY_KEY",
    "LINH_CAN_BY_NAME",
    "LINH_CAN_BY_FACTION",
    "get_all_linh_can",
    "get_linh_can_by_id",
    "get_linh_can_by_key",
    "get_linh_can_by_name",
    "get_linh_can_by_faction",
    "search_linh_can",
    # tui_tru_vat
    "ITEM_CATEGORIES",
    "TUI_TRU_VAT_TIERS",
    "TIER_BY_LEVEL",
    "TIER_BY_KEY",
    "TuiTruVat",
    "get_all_tiers",
    "get_tier_by_level",
    "get_tier_by_key",
    "get_max_slots",
    "check_can_add_item",
    "detect_item_category",
    # chi_so
    "CHI_SO_DATA",
    "CHI_SO_LIST",
    "TOTAL_CHI_SO",
    "CHI_SO_GROUPS",
    "CHI_SO_BY_ID",
    "CHI_SO_BY_KEY",
    "CHI_SO_BY_CODE",
    "CHI_SO_BY_NAME",
    "CHI_SO_BY_GROUP",
    "BangChiSoTuSi",
    "get_all_chi_so",
    "get_chi_so_by_id",
    "get_chi_so_by_key",
    "get_chi_so_by_code",
    "get_chi_so_by_name",
    "get_chi_so_by_group",
    "search_chi_so",
]
