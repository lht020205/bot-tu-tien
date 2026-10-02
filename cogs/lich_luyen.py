# -*- coding: utf-8 -*-
"""
cogs/lich_luyen.py
==================
Hệ thống Thám Hiểm Bí Cảnh, Đấu Pháp PvP và Song Tu Đạo Lữ:
- /lich_luyen: Bước vào bí cảnh cổ đại, trảm yêu đoạt bảo
- /dau_phap: Tỷ thí so tài đạo hạnh giữa 2 tu sĩ
- /song_tu: Mời đạo hữu cùng nhau vận chuyển chu thiên, tăng tốc tu vi
"""
import time
import random
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

import canh_gioi_chung as cgc
import database as db
import config


class LichLuyenCog(commands.Cog, name="Lịch Luyện & Đấu Pháp"):
    """Các hoạt động viễn chinh bí cảnh, giao chiến PvP và song tu."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="lich_luyen", description="Bước vào bí cảnh thám hiểm, trảm sát yêu ma, tìm kiếm cơ duyên")
    @app_commands.describe(bi_canh="Chọn bí cảnh muốn tiến vào")
    @app_commands.choices(bi_canh=[
        app_commands.Choice(name="🌲 U Minh Sơn Mạch (Yêu cầu: Ngưng Khí)", value="u_minh"),
        app_commands.Choice(name="⚔️ Vạn Kiếm Cổ Trủng (Yêu cầu: Trúc Cơ)", value="van_kiem"),
        app_commands.Choice(name="🩸 Hóa Thần Cấm Địa (Yêu cầu: Hóa Thần)", value="hoa_than"),
        app_commands.Choice(name="🌌 Cổ Thần Chi Địa (Yêu cầu: Khuy Niết)", value="co_than"),
    ])
    async def lich_luyen(self, interaction: discord.Interaction, bi_canh: app_commands.Choice[str]):
        """Thám hiểm bí cảnh."""
        user_id = interaction.user.id
        player = await db.get_player(user_id)

        if not player:
            await interaction.response.send_message("⚠️ Đạo hữu chưa nhập môn tu tiên! Hãy dùng `/khoi_dau` trước.", ephemeral=True)
            return

        now = time.time()
        last_time = player.get("last_explore_time", 0)
        diff = now - last_time

        if diff < config.EXPLORE_COOLDOWN_SECONDS:
            remain = int(config.EXPLORE_COOLDOWN_SECONDS - diff)
            await interaction.response.send_message(
                f"⏳ Chân khí sau chuyến lịch luyện trước chưa bình ổn. Hãy chờ thêm **{remain} giây** trước khi tiếp tục xuất hành!",
                ephemeral=True
            )
            return

        # Tìm dữ liệu bí cảnh
        dungeon = next((d for d in config.BI_CANH_LIST if d["id"] == bi_canh.value), None)
        if not dungeon:
            await interaction.response.send_message("❌ Bí cảnh không tồn tại!", ephemeral=True)
            return

        realm_id = player["realm_id"]
        if realm_id < dungeon["min_realm"]:
            req_info = cgc.get_tu_vi_realm_by_id(dungeon["min_realm"])
            req_name = req_info["name"] if req_info else f"Bậc {dungeon['min_realm']}"
            await interaction.response.send_message(
                f"🚫 Tu vi chưa đủ! Bí cảnh **{dungeon['name']}** vô cùng hiểm trở, đòi hỏi tu vi tối thiểu **{req_name}**.",
                ephemeral=True
            )
            return

        # Kiểm tra khí huyết
        pb_key = player.get("equipped_phap_bao")
        pb_id = config.SHOP_ITEMS.get(pb_key, {}).get("item_id") if pb_key else None
        lt_key = player.get("equipped_linh_thu")
        lt_id = config.SHOP_ITEMS.get(lt_key, {}).get("item_id") if lt_key else None

        stats = config.get_combat_stats(realm_id, pb_id, lt_id)
        current_hp = player.get("current_hp", stats["max_hp"])

        if current_hp <= 30:
            await interaction.response.send_message(
                f"⚠️ Khí huyết của đạo hữu quá suy yếu (`{current_hp}/{stats['max_hp']} HP`)! Không thể mạo hiểm vào bí cảnh. Hãy dùng **Cửu Chuyển Hoàn Hồn Đan** tại `/van_bao_cac`.",
                ephemeral=True
            )
            return

        # Diễn biến lịch luyện
        exp_gain = random.randint(*dungeon["exp_range"])
        stone_gain = random.randint(*dungeon["stone_range"])
        hp_loss = random.randint(15, 45)
        new_hp = max(10, current_hp - hp_loss)

        # Cơ hội rơi đồ (25% nhặt được đan dược)
        drop_item = None
        if random.random() < 0.25:
            consumables = [k for k, v in config.SHOP_ITEMS.items() if v.get("category") == "consumable"]
            drop_item = random.choice(consumables)
            await db.add_item(user_id, drop_item, 1)

        await db.update_player_explore(user_id, exp_gain, stone_gain, now, new_hp)

        drop_text = f"\n🎁 **Cơ duyên đoạt bảo:** Nhặt được **1x {config.SHOP_ITEMS[drop_item]['name']}**!" if drop_item else ""

        embed = discord.Embed(
            title=f"🗺️ LỊCH LUYỆN BÍ CẢNH: {dungeon['name'].upper()}",
            description=(
                f"Đạo hữu bước vào {dungeon['name']}, đụng độ hung thú **{dungeon['monster_name']}** hung tàn!\n"
                f"Trải qua 30 hiệp kịch chiến thi triển thần thông, đạo hữu đã trảm sát yêu vật, thu hoạch phong phú!"
                f"{drop_text}"
            ),
            color=config.COLOR_ORANGE
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="✨ Tu Vi Đoạt Được", value=f"+**{exp_gain:,}** EXP", inline=True)
        embed.add_field(name="💎 Linh Thạch Thu Lượm", value=f"+**{stone_gain:,}** Viên", inline=True)
        embed.add_field(name="💔 Khí Huyết Tổn Hao", value=f"-{hp_loss} HP (Còn **{new_hp}/{stats['max_hp']}**)", inline=True)
        embed.set_footer(text=f"Thời gian hồi: {config.EXPLORE_COOLDOWN_SECONDS}s | Dùng /tui_do để kiểm tra đồ nhặt được")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dau_phap", description="Tỷ thí luận đạo, so tài tu vi và pháp bảo với đạo hữu khác")
    @app_commands.describe(doi_thu="Đạo hữu muốn khiêu chiến")
    async def dau_phap(self, interaction: discord.Interaction, doi_thu: discord.Member):
        """Đấu pháp PvP giữa hai tu sĩ."""
        user1_id = interaction.user.id
        user2_id = doi_thu.id

        if user1_id == user2_id:
            await interaction.response.send_message("❌ Đạo hữu không thể tự đấu pháp với chính mình!", ephemeral=True)
            return

        if doi_thu.bot:
            await interaction.response.send_message("❌ Khôi lỗi (Bot) không có linh trí để đấu pháp cùng đạo hữu!", ephemeral=True)
            return

        p1 = await db.get_player(user1_id)
        if not p1:
            await interaction.response.send_message("⚠️ Đạo hữu chưa nhập môn tu tiên! Hãy dùng `/khoi_dau` trước.", ephemeral=True)
            return

        p2 = await db.get_player(user2_id)
        if not p2:
            await interaction.response.send_message(f"❌ Đối phương {doi_thu.mention} chưa bước chân vào giới tu tiên!", ephemeral=True)
            return

        now = time.time()
        diff = now - p1.get("last_duel_time", 0)
        if diff < config.DUEL_COOLDOWN_SECONDS:
            remain = int(config.DUEL_COOLDOWN_SECONDS - diff)
            await interaction.response.send_message(f"⏳ Khí tức chưa điều hòa xong sau trận đấu trước. Hãy chờ **{remain} giây**!", ephemeral=True)
            return

        # Tính chỉ số 2 bên
        pb1 = config.SHOP_ITEMS.get(p1.get("equipped_phap_bao"), {}).get("item_id")
        lt1 = config.SHOP_ITEMS.get(p1.get("equipped_linh_thu"), {}).get("item_id")
        s1 = config.get_combat_stats(p1["realm_id"], pb1, lt1)

        pb2 = config.SHOP_ITEMS.get(p2.get("equipped_phap_bao"), {}).get("item_id")
        lt2 = config.SHOP_ITEMS.get(p2.get("equipped_linh_thu"), {}).get("item_id")
        s2 = config.get_combat_stats(p2["realm_id"], pb2, lt2)

        # Mô phỏng trận đấu 3 hiệp
        hp1, hp2 = s1["max_hp"], s2["max_hp"]
        rounds_log = []

        for r in range(1, 4):
            # Lượt 1 tấn công 2
            dmg1 = max(15, int(s1["atk"] * random.uniform(0.8, 1.2) - s2["def"] * 0.4))
            hp2 -= dmg1
            # Lượt 2 phản công 1
            dmg2 = max(15, int(s2["atk"] * random.uniform(0.8, 1.2) - s1["def"] * 0.4))
            hp1 -= dmg2

            rounds_log.append(f"• **Hiệp {r}:** {p1['dao_hieu']} đánh gây `{dmg1}` sát thương ⚔️ | {p2['dao_hieu']} phản kích trả lại `{dmg2}` sát thương 🛡️")

            if hp1 <= 0 or hp2 <= 0:
                break

        # Xác định người thắng
        if hp1 >= hp2:
            winner, loser = p1, p2
            winner_user, loser_user = interaction.user, doi_thu
        else:
            winner, loser = p2, p1
            winner_user, loser_user = doi_thu, interaction.user

        reward_stones = 50
        await db.update_player_duel(winner["user_id"], loser["user_id"], now, reward_stones)

        embed = discord.Embed(
            title="⚔️ TRẬN ĐẤU PHÁP PHÂN TRANH CAO THẤP ⚔️",
            description=(
                f"Trận kịch chiến long trời lở đất giữa **{p1['dao_hieu']}** và **{p2['dao_hieu']}** tại Luận Đạo Đài!\n\n"
                + "\n".join(rounds_log)
                + f"\n\n🏆 **KẾT QUẢ:** **{winner['dao_hieu']}** ({winner_user.mention}) xuất thủ áp đảo giành chiến thắng vẻ vang!"
            ),
            color=config.COLOR_PURPLE
        )
        embed.add_field(name="💎 Phần Thưởng Người Thắng", value=f"+**{reward_stones}** Linh Thạch", inline=True)
        embed.set_footer(text="Luận đạo kết thúc hữu hảo, dĩ hòa vi quý!")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="song_tu", description="Mời một đạo hữu cùng nhau song tu đả tọa, tăng gấp bội hiệu suất tu hành")
    @app_commands.describe(dao_huu="Đạo hữu muốn mời cùng song tu")
    async def song_tu(self, interaction: discord.Interaction, dao_huu: discord.Member):
        """Lệnh song tu cùng đạo hữu."""
        user1_id = interaction.user.id
        user2_id = dao_huu.id

        if user1_id == user2_id:
            await interaction.response.send_message("❌ Đạo hữu không thể tự song tu với bản thân!", ephemeral=True)
            return

        if dao_huu.bot:
            await interaction.response.send_message("❌ Khôi lỗi không có kinh mạch khí huyết để song tu!", ephemeral=True)
            return

        p1 = await db.get_player(user1_id)
        p2 = await db.get_player(user2_id)

        if not p1:
            await interaction.response.send_message("⚠️ Đạo hữu chưa nhập môn tu tiên! Hãy dùng `/khoi_dau` trước.", ephemeral=True)
            return
        if not p2:
            await interaction.response.send_message(f"❌ {dao_huu.mention} chưa bước vào giới tu tiên!", ephemeral=True)
            return

        now = time.time()
        diff = now - p1.get("last_song_tu_time", 0)
        if diff < config.SONG_TU_COOLDOWN_SECONDS:
            remain = int((config.SONG_TU_COOLDOWN_SECONDS - diff) // 60)
            await interaction.response.send_message(
                f"⏳ Âm dương hòa hợp cần thời gian ngưng tụ. Hãy chờ **{remain} phút** nữa trước khi song tu tiếp!",
                ephemeral=True
            )
            return

        # Tính toán phần thưởng song tu (gấp 1.8 lần so với tọa thiền đơn độc)
        avg_realm = (p1["realm_id"] + p2["realm_id"]) // 2
        exp1, stone1 = config.get_cultivate_reward(avg_realm)
        exp_gain = int(exp1 * 1.8)
        stone_gain = int(stone1 * 1.8)

        await db.update_player_song_tu(user1_id, user2_id, exp_gain, stone_gain, now)

        embed = discord.Embed(
            title="🪷 ÂM DƯƠNG HÒA HỢP - SONG TU ĐẠO THÀNH 🪷",
            description=(
                f"**{p1['dao_hieu']}** và **{p2['dao_hieu']}** tương hỗ khí tức, cùng nhau vận chuyển đại chu thiên!\n"
                f"Thiên địa linh khí kết thành đóa sen tuyết ngưng tụ trên đỉnh đầu cả hai vị đạo hữu."
            ),
            color=config.COLOR_CYAN
        )
        embed.add_field(name="✨ Tu Vi Đôi Bên Nhận Được", value=f"+**{exp_gain:,}** EXP", inline=True)
        embed.add_field(name="💎 Linh Thạch Thu Hoạch", value=f"+**{stone_gain:,}** Viên", inline=True)
        embed.set_footer(text=f"Thời gian hồi song tu: {config.SONG_TU_COOLDOWN_SECONDS // 60} phút")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(LichLuyenCog(bot))
