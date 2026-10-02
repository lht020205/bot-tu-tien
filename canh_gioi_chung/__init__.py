# -*- coding: utf-8 -*-
"""
Package canh_gioi_chung
=======================
Cung cấp toàn bộ hệ thống cảnh giới dùng chung cho bot tu tiên:
1. Cảnh giới tu vi (canh_gioi_tu_vi)
2. Cảnh giới binh khí (canh_gioi_binh_khi)
3. Cảnh giới công pháp (canh_gioi_cong_phap)
4. Cảnh giới di tích (canh_gioi_di_tich)
"""

# Cảnh giới tu vi (Mặc định cho các hàm không tiền tố để tương thích)
from .canh_gioi_tu_vi import (
    REALMS,
    TOTAL_REALMS,
    REALM_BLUEPRINT,
    REALM_BY_ID,
    REALM_BY_NAME,
    get_all_realms,
    get_realm_by_id,
    get_realm_by_name,
    get_next_realm,
    is_max_realm,
    # Alias rõ nghĩa
    REALMS as TU_VI_REALMS,
    TOTAL_REALMS as TOTAL_TU_VI_REALMS,
    get_all_realms as get_all_tu_vi_realms,
    get_realm_by_id as get_tu_vi_realm_by_id,
    get_realm_by_name as get_tu_vi_realm_by_name,
    get_next_realm as get_next_tu_vi_realm,
    is_max_realm as is_max_tu_vi_realm,
)

# Cảnh giới binh khí
from .canh_gioi_binh_khi import (
    REALMS as BINH_KHI_REALMS,
    WEAPON_REALMS,
    TOTAL_REALMS as TOTAL_BINH_KHI_REALMS,
    TOTAL_WEAPON_REALMS,
    get_all_realms as get_all_binh_khi_realms,
    get_realm_by_id as get_binh_khi_realm_by_id,
    get_realm_by_name as get_binh_khi_realm_by_name,
    get_next_realm as get_next_binh_khi_realm,
    is_max_realm as is_max_binh_khi_realm,
    get_all_weapon_realms,
    get_weapon_realm_by_id,
    get_weapon_realm_by_name,
    get_next_weapon_realm,
    is_max_weapon_realm,
)

# Cảnh giới công pháp
from .canh_gioi_cong_phap import (
    REALMS as CONG_PHAP_REALMS,
    SKILL_REALMS,
    TOTAL_REALMS as TOTAL_CONG_PHAP_REALMS,
    TOTAL_CONG_PHAP_REALMS as TOTAL_SKILL_REALMS,
    get_all_realms as get_all_cong_phap_realms,
    get_realm_by_id as get_cong_phap_realm_by_id,
    get_realm_by_name as get_cong_phap_realm_by_name,
    get_next_realm as get_next_cong_phap_realm,
    is_max_realm as is_max_cong_phap_realm,
    get_all_cong_phap_realms as get_all_skill_realms,
    get_cong_phap_realm_by_id as get_skill_realm_by_id,
    get_cong_phap_realm_by_name as get_skill_realm_by_name,
    get_next_cong_phap_realm as get_next_skill_realm,
    is_max_cong_phap_realm as is_max_skill_realm,
)

# Cảnh giới di tích
from .canh_gioi_di_tich import (
    REALMS as DI_TICH_REALMS,
    RELIC_REALMS,
    RUINS_REALMS,
    TOTAL_REALMS as TOTAL_DI_TICH_REALMS,
    TOTAL_DI_TICH_REALMS as TOTAL_RELIC_REALMS,
    get_all_realms as get_all_di_tich_realms,
    get_realm_by_id as get_di_tich_realm_by_id,
    get_realm_by_name as get_di_tich_realm_by_name,
    get_next_realm as get_next_di_tich_realm,
    is_max_realm as is_max_di_tich_realm,
    get_all_relic_realms,
    get_relic_realm_by_id,
    get_relic_realm_by_name,
    get_next_relic_realm,
    is_max_relic_realm,
)

__all__ = [
    # Tu vi
    "REALMS",
    "TOTAL_REALMS",
    "REALM_BLUEPRINT",
    "REALM_BY_ID",
    "REALM_BY_NAME",
    "get_all_realms",
    "get_realm_by_id",
    "get_realm_by_name",
    "get_next_realm",
    "is_max_realm",
    "TU_VI_REALMS",
    "TOTAL_TU_VI_REALMS",
    "get_all_tu_vi_realms",
    "get_tu_vi_realm_by_id",
    "get_tu_vi_realm_by_name",
    "get_next_tu_vi_realm",
    "is_max_tu_vi_realm",
    # Binh khí
    "BINH_KHI_REALMS",
    "WEAPON_REALMS",
    "TOTAL_BINH_KHI_REALMS",
    "TOTAL_WEAPON_REALMS",
    "get_all_binh_khi_realms",
    "get_binh_khi_realm_by_id",
    "get_binh_khi_realm_by_name",
    "get_next_binh_khi_realm",
    "is_max_binh_khi_realm",
    "get_all_weapon_realms",
    "get_weapon_realm_by_id",
    "get_weapon_realm_by_name",
    "get_next_weapon_realm",
    "is_max_weapon_realm",
    # Công pháp
    "CONG_PHAP_REALMS",
    "SKILL_REALMS",
    "TOTAL_CONG_PHAP_REALMS",
    "TOTAL_SKILL_REALMS",
    "get_all_cong_phap_realms",
    "get_cong_phap_realm_by_id",
    "get_cong_phap_realm_by_name",
    "get_next_cong_phap_realm",
    "is_max_cong_phap_realm",
    "get_all_skill_realms",
    "get_skill_realm_by_id",
    "get_skill_realm_by_name",
    "get_next_skill_realm",
    "is_max_skill_realm",
    # Di tích
    "DI_TICH_REALMS",
    "RELIC_REALMS",
    "RUINS_REALMS",
    "TOTAL_DI_TICH_REALMS",
    "TOTAL_RELIC_REALMS",
    "get_all_di_tich_realms",
    "get_di_tich_realm_by_id",
    "get_di_tich_realm_by_name",
    "get_next_di_tich_realm",
    "is_max_di_tich_realm",
    "get_all_relic_realms",
    "get_relic_realm_by_id",
    "get_relic_realm_by_name",
    "get_next_relic_realm",
    "is_max_relic_realm",
]
