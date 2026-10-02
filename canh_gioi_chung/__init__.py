# -*- coding: utf-8 -*-
"""
Package canh_gioi_chung
=======================
Cung cấp toàn bộ hệ thống cảnh giới dùng chung cho bot tu tiên:
1. Cảnh giới tu vi (canh_gioi_tu_vi)
2. Cảnh giới binh khí (canh_gioi_binh_khi)
3. Cảnh giới pháp bảo (canh_gioi_phap_bao)
4. Cảnh giới công pháp (canh_gioi_cong_phap)
5. Cảnh giới đan dược (canh_gioi_dan_duoc)
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

# Cảnh giới pháp bảo
from .canh_gioi_phap_bao import (
    REALMS as PHAP_BAO_REALMS,
    TREASURE_REALMS,
    TOTAL_REALMS as TOTAL_PHAP_BAO_REALMS,
    TOTAL_TREASURE_REALMS,
    get_all_realms as get_all_phap_bao_realms,
    get_realm_by_id as get_phap_bao_realm_by_id,
    get_realm_by_name as get_phap_bao_realm_by_name,
    get_next_realm as get_next_phap_bao_realm,
    is_max_realm as is_max_phap_bao_realm,
    get_all_treasure_realms,
    get_treasure_realm_by_id,
    get_treasure_realm_by_name,
    get_next_treasure_realm,
    is_max_treasure_realm,
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

# Cảnh giới đan dược
from .canh_gioi_dan_duoc import (
    REALMS as DAN_DUOC_REALMS,
    PILL_REALMS,
    ELIXIR_REALMS,
    TOTAL_REALMS as TOTAL_DAN_DUOC_REALMS,
    TOTAL_DAN_DUOC_REALMS as TOTAL_PILL_REALMS,
    get_all_realms as get_all_dan_duoc_realms,
    get_realm_by_id as get_dan_duoc_realm_by_id,
    get_realm_by_name as get_dan_duoc_realm_by_name,
    get_next_realm as get_next_dan_duoc_realm,
    is_max_realm as is_max_dan_duoc_realm,
    get_all_dan_duoc_realms as get_all_pill_realms,
    get_dan_duoc_realm_by_id as get_pill_realm_by_id,
    get_dan_duoc_realm_by_name as get_pill_realm_by_name,
    get_next_dan_duoc_realm as get_next_pill_realm,
    is_max_dan_duoc_realm as is_max_pill_realm,
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
    # Pháp bảo
    "PHAP_BAO_REALMS",
    "TREASURE_REALMS",
    "TOTAL_PHAP_BAO_REALMS",
    "TOTAL_TREASURE_REALMS",
    "get_all_phap_bao_realms",
    "get_phap_bao_realm_by_id",
    "get_phap_bao_realm_by_name",
    "get_next_phap_bao_realm",
    "is_max_phap_bao_realm",
    "get_all_treasure_realms",
    "get_treasure_realm_by_id",
    "get_treasure_realm_by_name",
    "get_next_treasure_realm",
    "is_max_treasure_realm",
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
    # Đan dược
    "DAN_DUOC_REALMS",
    "PILL_REALMS",
    "ELIXIR_REALMS",
    "TOTAL_DAN_DUOC_REALMS",
    "TOTAL_PILL_REALMS",
    "get_all_dan_duoc_realms",
    "get_dan_duoc_realm_by_id",
    "get_dan_duoc_realm_by_name",
    "get_next_dan_duoc_realm",
    "is_max_dan_duoc_realm",
    "get_all_pill_realms",
    "get_pill_realm_by_id",
    "get_pill_realm_by_name",
    "get_next_pill_realm",
    "is_max_pill_realm",
]
