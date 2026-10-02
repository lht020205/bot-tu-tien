# -*- coding: utf-8 -*-
"""
cogs/van_bao_cac.py
===================
Hệ thống Vạn Bảo Các (Cửa Hàng) & Túi Trữ Vật (Inventory):
- /van_bao_cac: Xem các loại Đan Dược, Pháp Bảo, Linh Thú bày bán
- /mua: Mua vật phẩm bằng Linh Thạch
- /tui_do: Xem túi trữ vật của bản thân
- /su_dung: Dùng đan dược hồi phục, tăng EXP hoặc tăng tỷ lệ đột phá
- /trang_bi: Trang bị Pháp Bảo / Linh Thú hộ thân
- /thao_trang_bi: Tháo trang bị
"""
from typing import Optional, List
import discord
from discord import app_commands
from discord.ext import commands

import database as db
import config


class VanBaoCacCog(commands.Cog, name="Vạn Bảo Các"):
    """Quản lý giao dịch mua sắm và túi trữ vật của tu sĩ."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="van_bao_cac", description="Ghé thăm Vạn Bảo Các - Thiên hạ kỳ trân dị bảo")
    async def van_bao_cac(self, interaction: discord.Interaction):
        """Hiển thị danh mục cửa hàng."""
        embed = discord.Embed(
            title=f"{config.EMOJI_SHOP} VẠN BẢO CÁC - THIÊN HẠ BẢO VẬT {config.EMOJI_SHOP}",
            description="Chào mừng chư vị đạo hữu ghé thăm Vạn Bảo Các! Dưới đây là các loại đan dược và kỳ trân dị bảo:",
            color=config.COLOR_GOLD
        )

        pills = []
        equipments = []
        pets = []

        for key, item in config.SHOP_ITEMS.items():
            line = f"• **{item['name']}** - 💎 `{item['price']:,}` Linh Thạch\n  *{item['description']}* (Mã: `{key}`)"
            cat = item.get("category")
            if cat == "consumable":
                pills.append(line)
            elif cat == "equipment":
                equipments.append(line)
            elif cat == "pet":
                pets.append(line)

        embed.add_field(name="💊 Đan Dược Thần Hiệu", value="\n".join(pills), inline=False)
        embed.add_field(name="⚔️ Pháp Bảo Trấn Phái", value="\n".join(equipments), inline=False)
        embed.add_field(name="🐉 Linh Thú Hộ Thể", value="\n".join(pets), inline=False)

        embed.set_footer(text="Dùng lệnh /mua <mã_vật_phẩm> để sở hữu | Dùng /tui_do để kiểm tra túi")
        await interaction.response.send_message(embed=embed)

    async def item_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> List[app_commands.Choice[str]]:
        """Hỗ trợ tự động gợi ý tên vật phẩm khi gõ lệnh mua."""
        choices = []
        for key, item in config.SHOP_ITEMS.items():
            if current.lower() in item["name"].lower() or current.lower() in key:
                choices.append(app_commands.Choice(name=f"{item['name']} ({item['price']} viên)", value=key))
            if len(choices) >= 20:
                break
        return choices

    @app_commands.command(name="mua", description="Mua vật phẩm từ Vạn Bảo Các bằng Linh Thạch")
    @app_commands.describe(
        vat_pham="Chọn vật phẩm cần mua",
        so_luong="Số lượng muốn mua (mặc định là 1)"
    )
    @app_commands.autocomplete(vat_pham=item_autocomplete)
    async def mua(self, interaction: discord.Interaction, vat_pham: str, so_luong: Optional[int] = 1):
        """Mua vật phẩm."""
        user_id = interaction.user.id
        player = await db.get_player(user_id)

        if not player:
            await interaction.response.send_message("⚠️ Đạo hữu chưa nhập môn tu tiên! Hãy dùng `/khoi_dau` trước.", ephemeral=True)
            return

        if so_luong is None or so_luong <= 0:
            await interaction.response.send_message("⚠️ Số lượng mua tối thiểu là 1!", ephemeral=True)
            return

        item = config.SHOP_ITEMS.get(vat_pham)
        if not item:
            await interaction.response.send_message("❌ Vật phẩm này không tồn tại trong Vạn Bảo Các!", ephemeral=True)
            return

        total_price = item["price"] * so_luong
        if player["linh_thach"] < total_price:
            missing = total_price - player["linh_thach"]
            await interaction.response.send_message(
                f"❌ Đạo hữu không đủ Linh Thạch! Cần **{total_price:,}**, hiện có **{player['linh_thach']:,}** (còn thiếu **{missing:,}** viên).",
                ephemeral=True
            )
            return

        # Trừ tiền và thêm đồ
        await db.modify_player_stones(user_id, -total_price)
        await db.add_item(user_id, vat_pham, so_luong)

        embed = discord.Embed(
            title="🛒 GIAO DỊCH THÀNH CÔNG",
            description=f"Đạo hữu đã mua thành công **{so_luong}x {item['name']}**!",
            color=config.COLOR_SUCCESS
        )
        embed.add_field(name="💎 Tiêu Hao", value=f"-**{total_price:,}** Linh Thạch", inline=True)
        rem_stones = player["linh_thach"] - total_price
        embed.add_field(name="💎 Số Dư Còn Lại", value=f"**{rem_stones:,}** Linh Thạch", inline=True)
        embed.set_footer(text="Dùng /tui_do để kiểm tra túi trữ vật | Dùng /su_dung để dùng đan dược")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="tui_do", description="Mở túi trữ vật, kiểm tra các bảo vật đang sở hữu")
    async def tui_do(self, interaction: discord.Interaction):
        """Xem danh sách túi trữ vật."""
        user_id = interaction.user.id
        player = await db.get_player(user_id)

        if not player:
            await interaction.response.send_message("⚠️ Đạo hữu chưa nhập môn tu tiên! Hãy dùng `/khoi_dau` trước.", ephemeral=True)
            return

        inv = await db.get_inventory(user_id)
        if not inv:
            await interaction.response.send_message(
                f"🎒 Túi trữ vật của đạo hữu trống không! Hiện chỉ có **{player['linh_thach']:,}** Linh Thạch. Hãy ghé `/van_bao_cac` mua sắm hoặc đi `/lich_luyen` săn bảo.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title=f"🎒 TÚI TRỮ VẬT: {player['dao_hieu']}",
            color=config.COLOR_CYAN
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="💎 Linh Thạch", value=f"**{player['linh_thach']:,}** Viên", inline=False)

        lines = []
        for row in inv:
            item_key = row["item_key"]
            qty = row["quantity"]
            item_info = config.SHOP_ITEMS.get(item_key, {"name": item_key, "description": "Bảo vật chưa rõ"})
            lines.append(f"• **{item_info['name']}** x`{qty}` *(Mã: `{item_key}`)*\n  └ *{item_info['description']}*")

        embed.description = "\n".join(lines)
        embed.set_footer(text="Dùng /su_dung <mã> cho đan dược | Dùng /trang_bi <mã> cho pháp bảo/linh thú")
        await interaction.response.send_message(embed=embed)

    async def owned_consumables_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> List[app_commands.Choice[str]]:
        """Gợi ý các đan dược người chơi đang có trong túi."""
        user_id = interaction.user.id
        inv = await db.get_inventory(user_id)
        choices = []
        for row in inv:
            key = row["item_key"]
            item = config.SHOP_ITEMS.get(key)
            if item and item.get("category") == "consumable":
                if current.lower() in item["name"].lower() or current.lower() in key:
                    choices.append(app_commands.Choice(name=f"{item['name']} (Còn x{row['quantity']})", value=key))
        return choices

    @app_commands.command(name="su_dung", description="Sử dụng đan dược trong túi trữ vật")
    @app_commands.describe(dan_duoc="Chọn đan dược cần dùng")
    @app_commands.autocomplete(dan_duoc=owned_consumables_autocomplete)
    async def su_dung(self, interaction: discord.Interaction, dan_duoc: str):
        """Dùng đan dược."""
        user_id = interaction.user.id
        player = await db.get_player(user_id)

        if not player:
            await interaction.response.send_message("⚠️ Đạo hữu chưa nhập môn tu tiên!", ephemeral=True)
            return

        item = config.SHOP_ITEMS.get(dan_duoc)
        if not item or item.get("category") != "consumable":
            await interaction.response.send_message("❌ Vật phẩm này không thể sử dụng trực tiếp!", ephemeral=True)
            return

        # Tiêu hao 1 viên
        success = await db.remove_item(user_id, dan_duoc, 1)
        if not success:
            await interaction.response.send_message("❌ Đạo hữu không có đan dược này trong túi trữ vật!", ephemeral=True)
            return

        eff = item.get("effect", {})
        eff_type = eff.get("type")
        result_desc = ""

        if eff_type == "add_exp":
            exp_val = eff["value"]
            await db.update_player_cultivate(user_id, exp_val, 0, player["last_cultivate_time"])
            result_desc = f"✨ Dược lực tan trong kinh mạch! Đạo hữu lập tức hấp thu được **+{exp_val:,} EXP** tu vi!"

        elif eff_type == "breakthrough_buff":
            buff_val = eff["value"]
            await db.add_breakthrough_buff(user_id, buff_val)
            result_desc = f"🪷 Tẩy tủy hoàn tất! Tỷ lệ đột phá cho lần tiếp theo được tăng thêm **+{int(buff_val*100)}%**!"

        elif eff_type == "add_exp_and_buff":
            exp_val = eff["exp"]
            buff_val = eff["buff"]
            await db.update_player_cultivate(user_id, exp_val, 0, player["last_cultivate_time"])
            await db.add_breakthrough_buff(user_id, buff_val)
            result_desc = f"⚡ Kim quang bao phủ! Nhận ngay **+{exp_val:,} EXP** và **+{int(buff_val*100)}%** tỷ lệ đột phá kế tiếp!"

        elif eff_type == "heal_full":
            stats = config.get_combat_stats(player["realm_id"])
            await db.update_player_hp(user_id, stats["max_hp"])
            result_desc = f"💖 Khí huyết khôi phục toàn diện! Sinh lực đã trở về trạng thái đỉnh phong (**{stats['max_hp']:,} HP**)!"

        embed = discord.Embed(
            title=f"💊 SỬ DỤNG THÀNH CÔNG: {item['name']}",
            description=result_desc,
            color=config.COLOR_SUCCESS
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

    async def owned_equipment_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str
    ) -> List[app_commands.Choice[str]]:
        """Gợi ý các trang bị người chơi đang có trong túi."""
        user_id = interaction.user.id
        inv = await db.get_inventory(user_id)
        choices = []
        for row in inv:
            key = row["item_key"]
            item = config.SHOP_ITEMS.get(key)
            if item and item.get("category") in ("equipment", "pet"):
                if current.lower() in item["name"].lower() or current.lower() in key:
                    choices.append(app_commands.Choice(name=f"{item['name']}", value=key))
        return choices

    @app_commands.command(name="trang_bi", description="Trang bị Pháp Bảo hoặc Linh Thú hộ thân")
    @app_commands.describe(vat_pham="Chọn bảo vật cần trang bị")
    @app_commands.autocomplete(vat_pham=owned_equipment_autocomplete)
    async def trang_bi(self, interaction: discord.Interaction, vat_pham: str):
        """Trang bị vật phẩm."""
        user_id = interaction.user.id
        player = await db.get_player(user_id)

        if not player:
            await interaction.response.send_message("⚠️ Đạo hữu chưa nhập môn tu tiên!", ephemeral=True)
            return

        item = config.SHOP_ITEMS.get(vat_pham)
        if not item or item.get("category") not in ("equipment", "pet"):
            await interaction.response.send_message("❌ Vật phẩm này không thể trang bị!", ephemeral=True)
            return

        # Kiểm tra xem có trong túi không
        inv = await db.get_inventory(user_id)
        has_item = any(r["item_key"] == vat_pham and r["quantity"] > 0 for r in inv)
        if not has_item:
            await interaction.response.send_message("❌ Đạo hữu chưa sở hữu bảo vật này trong túi trữ vật!", ephemeral=True)
            return

        cat = item.get("category")
        item_type = "phap_bao" if cat == "equipment" else "linh_thu"
        await db.set_equipment(user_id, item_type, vat_pham)

        embed = discord.Embed(
            title="🛡️ TRANG BỊ THÀNH CÔNG",
            description=f"Đạo hữu đã trang bị **{item['name']}**!\nChiến lực bản thân đã được tăng cường đáng kể. Dùng `/ho_so` để xem thuộc tính mới.",
            color=config.COLOR_GOLD
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(VanBaoCacCog(bot))
