# -*- coding: utf-8 -*-
"""
cogs/tra_cuu.py
===============
Các lệnh tra cứu thông tin hệ thống cảnh giới chuẩn:
- /tra_cuu: Tra cứu chi tiết từng cảnh giới hoặc tổng quan từng hệ thống
  (Tu Vi, Pháp Bảo, Đan Dược, Phù Triện, Linh Thú)
"""
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

from phan_dau import canh_gioi_chung as cgc
from phan_dau import dan_duoc
import config


class TraCuuCog(commands.Cog, name="Tra Cứu"):
    """Lệnh tra cứu từ điển cảnh giới tu tiên."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(
        name="tra_cuu",
        description="Tra cứu danh bạ cảnh giới Tu Vi, Pháp Bảo, Đan Dược, Phù Triện, Linh Thú"
    )
    @app_commands.describe(
        he_thong="Hệ thống cảnh giới cần tra cứu",
        tu_khoa="Tên cảnh giới hoặc ID cần tra cứu (ví dụ: 'Nguyên Anh', '10', 'Thượng Phẩm')"
    )
    @app_commands.choices(he_thong=[
        app_commands.Choice(name="🌀 Tu Vi (106 bậc Tiên Nghịch)", value="tu_vi"),
        app_commands.Choice(name="⚔️ Pháp Bảo (13 bậc)", value="phap_bao"),
        app_commands.Choice(name="💊 Đan Dược (92 cấp)", value="dan_duoc"),
        app_commands.Choice(name="📜 Phù Triện (8 bậc)", value="phu_trien"),
        app_commands.Choice(name="🐉 Linh Thú (9 cấp)", value="linh_thu"),
    ])
    async def tra_cuu(
        self,
        interaction: discord.Interaction,
        he_thong: app_commands.Choice[str],
        tu_khoa: Optional[str] = None
    ):
        """Tra cứu thông tin cảnh giới."""
        choice_val = he_thong.value
        tu_khoa = tu_khoa.strip() if tu_khoa else ""

        # Mapping tương ứng theo hệ thống
        if choice_val == "tu_vi":
            all_realms = cgc.get_all_tu_vi_realms()
            get_by_id = cgc.get_tu_vi_realm_by_id
            get_by_name = cgc.get_tu_vi_realm_by_name
            get_next = cgc.get_next_tu_vi_realm
            is_max = cgc.is_max_tu_vi_realm
            title_name = "Tu Vi (Tiên Nghịch)"
            color = config.COLOR_CYAN
            total_count = cgc.TOTAL_TU_VI_REALMS
        elif choice_val == "phap_bao":
            all_realms = cgc.get_all_phap_bao_realms()
            get_by_id = cgc.get_phap_bao_realm_by_id
            get_by_name = cgc.get_phap_bao_realm_by_name
            get_next = cgc.get_next_phap_bao_realm
            is_max = cgc.is_max_phap_bao_realm
            title_name = "Pháp Bảo"
            color = config.COLOR_GOLD
            total_count = cgc.TOTAL_PHAP_BAO_REALMS
        elif choice_val == "dan_duoc":
            all_realms = cgc.get_all_dan_duoc_realms()
            get_by_id = cgc.get_dan_duoc_realm_by_id
            get_by_name = cgc.get_dan_duoc_realm_by_name
            get_next = cgc.get_next_dan_duoc_realm
            is_max = cgc.is_max_dan_duoc_realm
            title_name = "Đan Dược"
            color = config.COLOR_SUCCESS
            total_count = cgc.TOTAL_DAN_DUOC_REALMS
        elif choice_val == "phu_trien":
            all_realms = cgc.get_all_phu_trien_realms()
            get_by_id = cgc.get_phu_trien_realm_by_id
            get_by_name = cgc.get_phu_trien_realm_by_name
            get_next = cgc.get_next_phu_trien_realm
            is_max = cgc.is_max_phu_trien_realm
            title_name = "Phù Triện"
            color = config.COLOR_PURPLE
            total_count = cgc.TOTAL_PHU_TRIEN_REALMS
        else:  # linh_thu
            all_realms = cgc.get_all_linh_thu_realms()
            get_by_id = cgc.get_linh_thu_realm_by_id
            get_by_name = cgc.get_linh_thu_realm_by_name
            get_next = cgc.get_next_linh_thu_realm
            is_max = cgc.is_max_linh_thu_realm
            title_name = "Linh Thú"
            color = config.COLOR_FAIL
            total_count = cgc.TOTAL_LINH_THU_REALMS

        # Trường hợp 1: Không nhập từ khóa -> Xem tổng quan hệ thống
        if not tu_khoa:
            embed = discord.Embed(
                title=f"📖 TỔNG QUAN HỆ THỐNG CẢNH GIỚI: {title_name.upper()}",
                description=f"Hệ thống bao gồm tổng cộng **{total_count}** thứ bậc/phẩm cấp từ sơ khai đến cực hạn.",
                color=color
            )

            # Gom nhóm theo major_realm
            groups = {}
            for r in all_realms:
                groups.setdefault(r["major_realm"], []).append(r["name"])

            for major, items in list(groups.items())[:6]:  # Giới hạn field Discord
                sample_text = ", ".join(items[:5])
                if len(items) > 5:
                    sample_text += f", ... (+{len(items)-5} cấp)"
                embed.add_field(name=f"🌌 {major} ({len(items)} cấp)", value=sample_text, inline=False)

            embed.set_footer(text=f"Nhập thêm từ khóa vào lệnh /tra_cuu để xem chi tiết từng bậc!")
            await interaction.response.send_message(embed=embed)
            return

        # Trường hợp 2: Có từ khóa -> Tìm theo ID hoặc theo Tên
        found = None
        if tu_khoa.isdigit():
            found = get_by_id(int(tu_khoa))

        if not found:
            found = get_by_name(tu_khoa)

        # Nếu vẫn chưa tìm thấy chính xác, thử tìm kiếm chứa chuỗi (fuzzy-like search)
        if not found:
            lowered = tu_khoa.lower()
            matches = [r for r in all_realms if lowered in r["name"].lower() or lowered in r["minor_realm"].lower()]
            if len(matches) == 1:
                found = matches[0]
            elif len(matches) > 1:
                # Hiển thị danh sách các kết quả tương đồng
                embed = discord.Embed(
                    title=f"🔍 KẾT QUẢ TÌM KIẾM: '{tu_khoa}'",
                    description=f"Tìm thấy **{len(matches)}** cảnh giới phù hợp trong hệ thống {title_name}:",
                    color=color
                )
                lines = [f"• ID `{r['id']}`: **{r['name']}**" for r in matches[:15]]
                if len(matches) > 15:
                    lines.append(f"... và còn {len(matches) - 15} kết quả khác.")
                embed.description += "\n\n" + "\n".join(lines)
                embed.set_footer(text="Dùng ID chính xác để xem chi tiết từng cảnh giới!")
                await interaction.response.send_message(embed=embed)
                return

        if not found:
            await interaction.response.send_message(
                f"❌ Không tìm thấy cảnh giới nào có tên hoặc ID là '**{tu_khoa}**' trong hệ thống {title_name}!",
                ephemeral=True
            )
            return

        # Đã tìm thấy cảnh giới
        rid = found["id"]
        next_r = get_next(rid)
        is_peak = is_max(rid)

        embed = discord.Embed(
            title=f"📜 CHI TIẾT CẢNH GIỚI: {found['name']}",
            color=color
        )
        embed.add_field(name="🆔 Thứ Bậc ID", value=f"`#{found['id']}` / `{total_count}`", inline=True)
        embed.add_field(name="🌌 Đại Cảnh Giới", value=found["major_realm"], inline=True)
        embed.add_field(name="🌀 Phân Loại / Kỳ", value=found["minor_realm"], inline=True)

        if found.get("stage"):
            embed.add_field(name="✨ Giai Đoạn / Phẩm", value=found["stage"], inline=True)

        if is_peak:
            embed.add_field(name="👑 Cảnh Giới Kế Tiếp", value="**Đã là Đỉnh Phong Cực Hạn!**", inline=False)
        elif next_r:
            embed.add_field(name="⚡ Cảnh Giới Kế Tiếp", value=f"ID `{next_r['id']}`: **{next_r['name']}**", inline=False)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(TraCuuCog(bot))
