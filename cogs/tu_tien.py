# -*- coding: utf-8 -*-
"""
cogs/tu_tien.py
===============
Các lệnh cốt lõi của hệ thống Tu Tiên:
- /khoi_dau: Bắt đầu bước chân vào tiên lộ, định danh đạo hiệu
- /ho_so: Xem thông tin tu sĩ, khí huyết, công thủ, pháp bảo, linh thú, tiến trình EXP
- /tu_luyen: Tọa thiền hấp thu thiên địa linh khí
- /dot_pha: Phá vỡ bình cảnh (tính cả buff từ đan dược), trùng kích cảnh giới mới
- /bang_xep_hang: Bảng vàng Thiên Kiêu bảng
"""
import time
import random
from typing import Optional
import discord
from discord import app_commands
from discord.ext import commands

from phan_dau import canh_gioi_chung as cgc
import database as db
import config


class TuTienCog(commands.Cog, name="Tu Tiên"):
    """Các lệnh tu hành, độ kiếp và quản lý đạo hạnh tu sĩ."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="khoi_dau", description="Bắt đầu hành trình tu tiên, định danh đạo hiệu của bản thân")
    @app_commands.describe(dao_hieu="Đạo hiệu tu tiên của bạn (Ví dụ: Hàn Lập, Vương Lâm, Tiêu Viêm...)")
    async def khoi_dau(self, interaction: discord.Interaction, dao_hieu: str):
        """Khởi tạo tài khoản tu tiên."""
        user_id = interaction.user.id
        dao_hieu = dao_hieu.strip()

        if len(dao_hieu) < 2 or len(dao_hieu) > 32:
            await interaction.response.send_message(
                "⚠️ Đạo hiệu phải có độ dài từ 2 đến 32 ký tự!",
                ephemeral=True
            )
            return

        player = await db.get_player(user_id)
        if player:
            await interaction.response.send_message(
                f"⚠️ Đạo hữu đã bước vào tiên lộ với đạo hiệu **{player['dao_hieu']}** rồi! Hãy dùng `/ho_so` để xem tiến độ.",
                ephemeral=True
            )
            return

        # Tạo hồ sơ mới
        player = await db.create_player(user_id, dao_hieu)
        realm_info = cgc.get_tu_vi_realm_by_id(player["realm_id"])
        realm_name = realm_info["name"] if realm_info else "Ngưng Khí Tầng 1"

        embed = discord.Embed(
            title=f"{config.EMOJI_LOTUS} KHAI MỞ TIÊN LỘ THÀNH CÔNG {config.EMOJI_LOTUS}",
            description=(
                f"Chúc mừng đạo hữu **{dao_hieu}** đã chính thức bước vào con đường nghịch thiên tu hành!\n\n"
                f"Thiên đạo ban tặng cơ duyên nhập môn, chúc đạo hữu sớm ngày Đạp Thiên chứng đạo!"
            ),
            color=config.COLOR_SUCCESS
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="🌀 Cảnh Giới Ban Đầu", value=f"**{realm_name}**", inline=True)
        embed.add_field(name="💎 Linh Thạch Khởi Điểm", value=f"**{player['linh_thach']}** Viên", inline=True)
        embed.add_field(name="💡 Hướng Dẫn Tiếp Theo", value=(
            "• `/tu_luyen`: Tọa thiền tích lũy tu vi\n"
            "• `/dot_pha`: Trùng kích cảnh giới mới\n"
            "• `/van_bao_cac`: Ghé thăm tiệm mua đan dược & pháp bảo\n"
            "• `/lich_luyen`: Thám hiểm các bí cảnh cổ đại"
        ), inline=False)
        embed.set_footer(text="Tu tiên nghịch thiên cải mệnh | Bot Tu Tiên")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="ho_so", description="Xem hồ sơ đạo hạnh, cảnh giới, trang bị và chiến lực của bản thân hoặc đạo hữu khác")
    @app_commands.describe(dao_huu="Tu sĩ cần xem thông tin (để trống nếu muốn xem của bản thân)")
    async def ho_so(self, interaction: discord.Interaction, dao_huu: Optional[discord.Member] = None):
        """Hiển thị hồ sơ tu sĩ."""
        target_user = dao_huu or interaction.user
        player = await db.get_player(target_user.id)

        if not player:
            msg = "Đạo hữu chưa bước vào tu tiên lộ! Hãy dùng lệnh `/khoi_dau <dao_hieu>` trước." if target_user == interaction.user else f"Tu sĩ {target_user.mention} vẫn chưa bước chân vào giới tu tiên."
            await interaction.response.send_message(msg, ephemeral=True)
            return

        realm_id = player["realm_id"]
        realm_info = cgc.get_tu_vi_realm_by_id(realm_id)
        if not realm_info:
            realm_info = {"name": f"Cảnh giới vô danh (ID: {realm_id})", "major_realm": "Chưa rõ"}

        # Trang bị
        eq_pb_key = player.get("equipped_phap_bao")
        eq_pb_id = config.SHOP_ITEMS.get(eq_pb_key, {}).get("item_id") if eq_pb_key else None
        eq_pb_name = config.SHOP_ITEMS.get(eq_pb_key, {}).get("name", "Không có") if eq_pb_key else "Bàn tay trần"

        eq_lt_key = player.get("equipped_linh_thu")
        eq_lt_id = config.SHOP_ITEMS.get(eq_lt_key, {}).get("item_id") if eq_lt_key else None
        eq_lt_name = config.SHOP_ITEMS.get(eq_lt_key, {}).get("name", "Không có") if eq_lt_key else "Đơn độc độc hành"

        # Tính chiến lực
        combat_stats = config.get_combat_stats(realm_id, eq_pb_id, eq_lt_id)
        max_hp = combat_stats["max_hp"]
        cur_hp = min(max_hp, player.get("current_hp", max_hp))

        current_exp = player["current_exp"]
        req_exp = config.get_required_exp(realm_id)
        base_rate = config.get_breakthrough_rate(realm_id)
        extra_buff = player.get("breakthrough_buff", 0.0) or 0.0
        total_rate = min(1.0, base_rate + extra_buff)
        rate_percent = int(total_rate * 100)

        progress_str = config.render_progress_bar(current_exp, req_exp)
        is_max = cgc.is_max_tu_vi_realm(realm_id)

        embed = discord.Embed(
            title=f"{config.EMOJI_YANG} HỒ SƠ TU SĨ: {player['dao_hieu']} {config.EMOJI_YANG}",
            color=config.COLOR_PURPLE if realm_id > 60 else (config.COLOR_GOLD if realm_id > 20 else config.COLOR_CYAN)
        )
        embed.set_author(name=target_user.display_name, icon_url=target_user.display_avatar.url)
        embed.set_thumbnail(url=target_user.display_avatar.url)

        embed.add_field(
            name="🌌 Đại Cảnh Giới",
            value=f"**{realm_info.get('major_realm', 'Vô Biên')}**",
            inline=True
        )
        embed.add_field(
            name="🌀 Cảnh Giới Hiện Tại",
            value=f"**{realm_info['name']}** `(Bậc {realm_id}/106)`",
            inline=True
        )
        embed.add_field(
            name="💎 Linh Thạch",
            value=f"**{player['linh_thach']:,}** Viên",
            inline=True
        )

        # Thuộc tính chiến đấu
        embed.add_field(
            name="⚔️ Thuộc Tính & Chiến Lực",
            value=(
                f"• {config.EMOJI_HEART} Khí Huyết: **{cur_hp:,}** / **{max_hp:,}** HP\n"
                f"• {config.EMOJI_SWORD} Công Kích: **{combat_stats['atk']:,}**\n"
                f"• {config.EMOJI_SHIELD} Phòng Ngự: **{combat_stats['def']:,}**\n"
                f"• ⚡ Tốc Độ: **{combat_stats['speed']:,}**"
            ),
            inline=False
        )

        # Trang bị
        embed.add_field(
            name="🛡️ Trang Bị Hộ Thân",
            value=(
                f"• {config.EMOJI_SWORD} Pháp Bảo: **{eq_pb_name}**\n"
                f"• {config.EMOJI_BEAST} Linh Thú: **{eq_lt_name}**"
            ),
            inline=False
        )

        # Tiến trình tu vi
        if is_max:
            embed.add_field(
                name="✨ Tu Vi Thần Thông",
                value="👑 **Đã đạt Đỉnh Phong Siêu Thoát, cực hạn thiên địa!**",
                inline=False
            )
        else:
            buff_text = f" *(+ {int(extra_buff * 100)}% từ đan dược)*" if extra_buff > 0 else ""
            embed.add_field(
                name=f"{config.EMOJI_EXP} Tiến Độ Tu Vi",
                value=f"{progress_str}\nTu vi: **{current_exp:,}** / **{req_exp:,}** EXP\nTỷ lệ trùng kích bình cảnh: **{rate_percent}%**{buff_text}",
                inline=False
            )

        # Thống kê
        embed.add_field(
            name="📜 Đạo Hạnh & Chiến Tích",
            value=(
                f"• Tọa thiền: **{player['total_cultivations']}** lần | Đột phá thành công: **{player['total_breakthroughs']}** lần\n"
                f"• Tỷ thí PvP: **{player.get('pvp_wins', 0)}** Thắng / **{player.get('pvp_losses', 0)}** Bại"
            ),
            inline=False
        )

        embed.set_footer(text=f"ID Tu Sĩ: {target_user.id} | Dùng /tu_luyen để tăng tu vi")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="tu_luyen", description="Tọa thiền hấp thu linh khí thiên địa, tích lũy tu vi và linh thạch")
    async def tu_luyen(self, interaction: discord.Interaction):
        """Lệnh tọa thiền tu luyện."""
        user_id = interaction.user.id
        player = await db.get_player(user_id)

        if not player:
            await interaction.response.send_message(
                "⚠️ Đạo hữu chưa nhập môn tu tiên! Hãy dùng `/khoi_dau <dao_hieu>` trước.",
                ephemeral=True
            )
            return

        now = time.time()
        last_time = player["last_cultivate_time"]
        diff = now - last_time

        if diff < config.CULTIVATE_COOLDOWN_SECONDS:
            remain = int(config.CULTIVATE_COOLDOWN_SECONDS - diff)
            minutes, seconds = divmod(remain, 60)
            time_str = f"{minutes} phút {seconds} giây" if minutes > 0 else f"{seconds} giây"
            await interaction.response.send_message(
                f"⏳ Kinh mạch của đạo hữu đang bão hòa chân khí. Hãy tĩnh dưỡng tâm thần, quay lại sau **{time_str}**!",
                ephemeral=True
            )
            return

        realm_id = player["realm_id"]
        base_exp, base_stone = config.get_cultivate_reward(realm_id)

        # Cơ chế cơ duyên ngộ đạo ngẫu nhiên
        roll = random.random()
        is_critical = False

        if roll < 0.05:
            is_critical = True
            base_exp = int(base_exp * 2.2)
            base_stone = int(base_stone * 2)
            flavor_text = "⚡ **Thiên nhân hợp nhất!** Đạo hữu đột nhiên tiến vào trạng thái đốn ngộ, linh khí vạn dặm cuồn cuộn đổ vào đan điền!"
        elif roll < 0.18:
            is_critical = True
            base_exp = int(base_exp * 1.5)
            flavor_text = "🪷 **Tâm cảnh thông suốt!** Đạo hữu lĩnh ngộ được huyền bí thiên địa, tốc độ hấp thu linh khí tăng vọt."
        else:
            flavor_text = "🧘 Đạo hữu ngồi xếp bằng thổ nạp nhật nguyệt tinh hoa, chân khí vận hành chu thiên vững vàng."

        await db.update_player_cultivate(user_id, base_exp, base_stone, now)

        color = config.COLOR_GOLD if is_critical else config.COLOR_DEFAULT
        embed = discord.Embed(
            title=f"{config.EMOJI_LOTUS} TỌA THIỀN TU LUYỆN HOÀN TẤT",
            description=flavor_text,
            color=color
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        embed.add_field(name="✨ Tu Vi Thu Được", value=f"+**{base_exp:,}** EXP", inline=True)
        embed.add_field(name="💎 Linh Thạch Tích Lũy", value=f"+**{base_stone:,}** Viên", inline=True)
        embed.set_footer(text=f"Thời gian hồi: {config.CULTIVATE_COOLDOWN_SECONDS // 60} phút | Dùng /dot_pha khi đủ tu vi")

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="dot_pha", description="Trùng kích bình cảnh, phá vỡ giới hạn để thăng hoa cảnh giới mới")
    async def dot_pha(self, interaction: discord.Interaction):
        """Lệnh đột phá cảnh giới."""
        user_id = interaction.user.id
        player = await db.get_player(user_id)

        if not player:
            await interaction.response.send_message(
                "⚠️ Đạo hữu chưa nhập môn tu tiên! Hãy dùng `/khoi_dau <dao_hieu>` trước.",
                ephemeral=True
            )
            return

        realm_id = player["realm_id"]
        current_exp = player["current_exp"]

        # Kiểm tra cực hạn
        if cgc.is_max_tu_vi_realm(realm_id):
            await interaction.response.send_message(
                "👑 Đạo hữu đã đạt tới cảnh giới **Đạp Thiên Cực Hạn (Siêu Thoát)**, trên đỉnh vạn giới không còn bình cảnh nào có thể ngăn trở!",
                ephemeral=True
            )
            return

        req_exp = config.get_required_exp(realm_id)
        if current_exp < req_exp:
            missing = req_exp - current_exp
            await interaction.response.send_message(
                f"⚠️ Đạo hạnh chưa đủ để phá vỡ bình cảnh!\n"
                f"• Cần: **{req_exp:,}** EXP\n"
                f"• Hiện có: **{current_exp:,}** EXP\n"
                f"• Còn thiếu: **{missing:,}** EXP. Hãy dùng `/tu_luyen` tiếp tục tích lũy.",
                ephemeral=True
            )
            return

        # Tính toán tỷ lệ (bao gồm cả buff từ đan dược)
        base_rate = config.get_breakthrough_rate(realm_id)
        extra_buff = player.get("breakthrough_buff", 0.0) or 0.0
        final_rate = min(1.0, base_rate + extra_buff)

        success = random.random() < final_rate

        current_realm_info = cgc.get_tu_vi_realm_by_id(realm_id)
        next_realm_info = cgc.get_next_tu_vi_realm(realm_id)

        if success and next_realm_info:
            # Thành công đột phá!
            new_realm_id = next_realm_info["id"]
            remaining_exp = current_exp - req_exp
            await db.update_player_breakthrough_success(user_id, new_realm_id, remaining_exp)

            # Cập nhật máu tối đa khi thăng cấp
            stats = config.get_combat_stats(new_realm_id)
            await db.update_player_hp(user_id, stats["max_hp"])

            is_major = (current_realm_info["minor_realm"] != next_realm_info["minor_realm"])

            flavor = (
                f"💥 **THIÊN ĐỊA DỊ TƯỢNG!** Tử khí đông lai ba vạn dặm!\n"
                f"Đạo hữu đã đập tan gông cùm thiên đạo, thành công phá vỡ bình cảnh **{current_realm_info['name']}**, "
                f"chính thức bước chân vào cảnh giới **{next_realm_info['name']}**!"
                if is_major else
                f"✨ Chân khí trong đan điền cuộn trào ngưng tụ! Đạo hữu thuận lợi thăng cấp lên **{next_realm_info['name']}**!"
            )

            embed = discord.Embed(
                title="⚡ ĐỘT PHÁ THÀNH CÔNG - NGHỊCH THIÊN THĂNG CẤP ⚡",
                description=flavor,
                color=config.COLOR_SUCCESS
            )
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
            embed.add_field(name="🌀 Cảnh Giới Mới", value=f"**{next_realm_info['name']}**", inline=False)
            embed.add_field(name="✨ Tu Vi Dư Lại", value=f"**{remaining_exp:,}** EXP", inline=True)
            embed.set_footer(text="Đạo tâm kiên định, đại đạo trường sinh!")
            await interaction.response.send_message(embed=embed)

        else:
            # Thất bại đột phá
            exp_loss = int(current_exp * random.uniform(0.10, 0.20))
            await db.update_player_breakthrough_failure(user_id, exp_loss)

            embed = discord.Embed(
                title="🔥 ĐỘT PHÁ THẤT BẠI - TẨU HỎA NHẬP MA 🔥",
                description=(
                    f"Trong lúc dẫn dắt linh khí xung kích kinh mạch, đạo tâm bất ổn, tâm ma xuất hiện làm rối loạn khí huyết!\n\n"
                    f"Đột phá thất bại! May nhờ nền tảng vững vàng nên bảo toàn tính mạng, chỉ tổn thất một lượng chân khí."
                ),
                color=config.COLOR_FAIL
            )
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
            embed.add_field(name="💔 Tổn Thất Tu Vi", value=f"-**{exp_loss:,}** EXP", inline=True)
            embed.add_field(name="💡 Gợi Ý Đạo Hữu", value="Có thể ghé thăm `/van_bao_cac` mua **Trúc Cơ Đan** để tăng tỷ lệ đột phá cho lần sau!", inline=False)
            embed.set_footer(text=f"Tỷ lệ thành công vừa rồi: {int(final_rate*100)}%")
            await interaction.response.send_message(embed=embed)

    @app_commands.command(name="bang_xep_hang", description="Xem Thiên Kiêu Bảng - Top 10 đại năng tu vi cao nhất thiên địa")
    async def bang_xep_hang(self, interaction: discord.Interaction):
        """Bảng xếp hạng cao thủ."""
        top_players = await db.get_top_players(limit=10)

        if not top_players:
            await interaction.response.send_message("Hiện chưa có tu sĩ nào ghi danh trên Thiên Kiêu Bảng!", ephemeral=True)
            return

        embed = discord.Embed(
            title=f"{config.EMOJI_MEDAL} BẢNG VÀNG THIÊN KIÊU - TOP ĐẠI NĂNG {config.EMOJI_MEDAL}",
            description="Danh sách những bậc đại năng tu vi thông thiên triệt địa:",
            color=config.COLOR_GOLD
        )

        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

        lines = []
        for i, p in enumerate(top_players):
            medal = medals[i] if i < len(medals) else f"#{i+1}"
            realm_info = cgc.get_tu_vi_realm_by_id(p["realm_id"])
            realm_name = realm_info["name"] if realm_info else f"Bậc {p['realm_id']}"
            lines.append(f"{medal} **{p['dao_hieu']}** • `{realm_name}` • *{p['current_exp']:,} EXP*")

        embed.description = "\n".join(lines)
        embed.set_footer(text="Dùng /tu_luyen và /dot_pha để tranh đoạt vị trí trên bảng vàng!")

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(TuTienCog(bot))
