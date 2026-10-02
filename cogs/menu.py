# -*- coding: utf-8 -*-
"""
cogs/menu.py
============
Trung tâm điều khiển Tu Tiên (HUB tương tác giao diện Buttons & Modals):
- Lệnh chính: /menu
- Giao diện chống xé hình (Anti-Tearing UI) chuẩn form trên cả Mobile & PC
- Tạo nhân vật bằng Discord Modal Popup
- Tính năng Tán Tu / Xóa Nhân Vật để test lại từ đầu
- Bảng Hub tương tác đầy đủ các nút bấm:
  + [🧘 Tọa Thiền] [⚡ Trùng Kích] [🎒 Túi Đồ] [🏪 Vạn Bảo Các]
  + [🗺️ Lịch Luyện] [🏅 Thiên Kiêu Bảng] [🔄 Làm Mới] [💀 Tán Tu / Xóa]
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


# =============================================================================
# HELPER TẠO THANH TIẾN ĐỘ CHỐNG XÉ HÌNH (ANTI-TEARING PROGRESS BAR)
# =============================================================================

def render_smooth_bar(current: int, total: int, length: int = 10) -> str:
    """Tạo thanh tiến trình đơn khối monospaced không bao giờ bị xé hình trên mobile."""
    if total <= 0:
        return f"`[{'░' * length}]` 0%"
    ratio = min(1.0, max(0.0, current / total))
    filled = int(round(length * ratio))
    empty = length - filled
    percent = int(ratio * 100)
    return f"`[{'█' * filled}{'░' * empty}]` {percent}%"


async def create_hub_embed(user: discord.User, player: dict) -> discord.Embed:
    """Tạo Embed giao diện Trung Tâm Tu Tiên mượt mà, chống vỡ khung trên mọi thiết bị."""
    realm_id = player["realm_id"]
    realm_info = cgc.get_tu_vi_realm_by_id(realm_id) or {"name": f"Bậc {realm_id}", "major_realm": "Chưa rõ"}

    # Trang bị
    eq_pb_key = player.get("equipped_phap_bao")
    eq_pb = config.SHOP_ITEMS.get(eq_pb_key, {}) if eq_pb_key else {}
    pb_name = eq_pb.get("name", "Bàn tay trần")

    eq_lt_key = player.get("equipped_linh_thu")
    eq_lt = config.SHOP_ITEMS.get(eq_lt_key, {}) if eq_lt_key else {}
    lt_name = eq_lt.get("name", "Chưa có")

    # Chỉ số chiến lực
    stats = config.get_combat_stats(realm_id, eq_pb.get("item_id"), eq_lt.get("item_id"))
    max_hp = stats["max_hp"]
    cur_hp = min(max_hp, player.get("current_hp", max_hp))
    hp_bar = render_smooth_bar(cur_hp, max_hp, length=10)

    # Tu vi
    req_exp = config.get_required_exp(realm_id)
    cur_exp = player["current_exp"]
    exp_bar = render_smooth_bar(cur_exp, req_exp, length=10)

    # Tỷ lệ đột phá
    base_rate = config.get_breakthrough_rate(realm_id)
    buff = player.get("breakthrough_buff", 0.0) or 0.0
    total_rate = min(1.0, base_rate + buff)
    buff_str = f" *(+{int(buff*100)}% đan dược)*" if buff > 0 else ""

    is_max = cgc.is_max_tu_vi_realm(realm_id)
    breakthrough_info = "👑 Đã đạt Đỉnh Phong Siêu Thoát" if is_max else f"{int(total_rate*100)}%{buff_str}"

    color = config.COLOR_PURPLE if realm_id > 50 else (config.COLOR_GOLD if realm_id > 20 else config.COLOR_CYAN)

    embed = discord.Embed(
        title=f"⛩️ TIÊN PHỦ ĐẠO TRÀNG ⛩️",
        color=color
    )
    embed.set_author(name=f"Tu Sĩ: {player['dao_hieu']}", icon_url=user.display_avatar.url)
    embed.set_thumbnail(url=user.display_avatar.url)

    # Định dạng khung nguyên khối bằng Markdown Box không thể bị xé hình
    dashboard_text = (
        f"```yaml\n"
        f"【ĐẠO HIỆU】: {player['dao_hieu']}\n"
        f"【CẢNH GIỚI】: {realm_info['name']} (Bậc {realm_id}/{cgc.TOTAL_TU_VI_REALMS})\n"
        f"【ĐẠI CẢNH】: {realm_info.get('major_realm', 'Vô Biên')}\n"
        f"```\n"
        f"**📊 TRẠNG THÁI KHÍ TỨC**\n"
        f"❤️ Khí Huyết: {hp_bar} `({cur_hp:,}/{max_hp:,} HP)`\n"
        f"✨ Tiến Trình: {exp_bar} `({cur_exp:,}/{req_exp:,} EXP)`\n"
        f"⚡ Bình Cảnh: Tỷ lệ đột phá **{breakthrough_info}**\n\n"
        f"**⚔️ CHIẾN LỰC & HỘ THÂN**\n"
        f"🗡️ Công: **{stats['atk']}** │ 🛡️ Thủ: **{stats['def']}** │ ⚡ Tốc: **{stats['speed']}**\n"
        f"🔮 Pháp Bảo: *{pb_name}*\n"
        f"🐉 Linh Thú: *{lt_name}*\n\n"
        f"**💎 TÀI BẢO & ĐẠO HẠNH**\n"
        f"💰 Linh Thạch: **{player['linh_thach']:,}** viên\n"
        f"🧘 Tọa Thiền: **{player['total_cultivations']}** lần │ ⚡ Độ Kiếp: **{player['total_breakthroughs']}** lần"
    )

    embed.description = dashboard_text
    embed.set_footer(text="Nhấn các nút bên dưới để thao tác trực tiếp mượt mà!")
    return embed


# =============================================================================
# MODAL NHẬP ĐẠO HIỆU KHI TẠO NHÂN VẬT
# =============================================================================

class TaoNhanVatModal(discord.ui.Modal, title="Khai Mở Tiên Lộ - Tạo Đạo Hiệu"):
    dao_hieu_input = discord.ui.TextInput(
        label="Nhập Đạo Hiệu Tu Tiên Của Bạn",
        placeholder="Ví dụ: Hàn Lập, Vương Lâm, Tiêu Viêm, Bạch Tiểu Thuần...",
        min_length=2,
        max_length=32,
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        dao_hieu = self.dao_hieu_input.value.strip()
        user_id = interaction.user.id

        player = await db.get_player(user_id)
        if player:
            await interaction.response.send_message(
                f"⚠️ Đạo hữu đã đăng ký với đạo hiệu **{player['dao_hieu']}** rồi!",
                ephemeral=True
            )
            return

        new_player = await db.create_player(user_id, dao_hieu)
        embed = await create_hub_embed(interaction.user, new_player)
        view = MainHubView(user_id)

        await interaction.response.edit_message(
            content=f"🎉 **Chúc mừng đạo hữu `{dao_hieu}` đã nhập môn thành công!** Bắt đầu hành trình tu tiên dưới đây:",
            embed=embed,
            view=view
        )


# =============================================================================
# VIEW KHI CHƯA ĐĂNG KÝ
# =============================================================================

class UnregisteredView(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=300)
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "⚠️ Vui lòng gõ `/menu` để mở bảng tạo nhân vật của riêng bạn!",
                ephemeral=True
            )
            return False
        return True

    @discord.ui.button(label="✨ Khai Mở Tiên Lộ (Tạo Nhân Vật)", style=discord.ButtonStyle.success, emoji="🪷")
    async def btn_create_char(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(TaoNhanVatModal())


# =============================================================================
# VIEW XÁC NHẬN XÓA NHÂN VẬT (CHUYỂN SINH)
# =============================================================================

class ConfirmDeleteView(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=120)
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message("⚠️ Bạn không thể thao tác trên bảng này!", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="✅ Đồng Ý Xóa (Chuyển Sinh Phàm Nhân)", style=discord.ButtonStyle.danger, emoji="💀")
    async def btn_confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        await db.delete_player(user_id)

        embed = discord.Embed(
            title="⛩️ TÁN KHÍ TIÊU BIẾN - CHUYỂN SINH HOÀN TẤT ⛩️",
            description=(
                f"Đạo hữu đã rũ bỏ toàn bộ tu vi, tán đi chân khí, chuyển sinh trở lại làm một phàm nhân!\n\n"
                f"👉 **Bây giờ bạn có thể nhấn nút xanh bên dưới để tạo lại nhân vật và test từ đầu:**"
            ),
            color=config.COLOR_GOLD
        )
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        view = UnregisteredView(user_id)
        await interaction.response.edit_message(content=None, embed=embed, view=view)

    @discord.ui.button(label="❌ Hủy Bỏ (Quay Lại)", style=discord.ButtonStyle.secondary, emoji="↩️")
    async def btn_cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = await db.get_player(interaction.user.id)
        if player:
            embed = await create_hub_embed(interaction.user, player)
            view = MainHubView(interaction.user.id)
            await interaction.response.edit_message(content="Đã hủy bỏ tán tu!", embed=embed, view=view)
        else:
            await interaction.response.send_message("Đã hủy bỏ!", ephemeral=True)


# =============================================================================
# VIEW TRUNG TÂM ĐIỀU KHIỂN (MAIN HUB VIEW)
# =============================================================================

class MainHubView(discord.ui.View):
    def __init__(self, author_id: int):
        super().__init__(timeout=600)
        self.author_id = author_id

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id != self.author_id:
            await interaction.response.send_message(
                "⚠️ Đây là Tiên Phủ của đạo hữu khác! Hãy dùng lệnh `/menu` để mở Tiên Phủ của riêng bạn.",
                ephemeral=True
            )
            return False
        return True

    # ROW 0: TU HÀNH & KHO HÀNG
    @discord.ui.button(label="Tọa Thiền", style=discord.ButtonStyle.primary, emoji="🧘", row=0)
    async def btn_cultivate(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        player = await db.get_player(user_id)
        if not player:
            await interaction.response.send_message("Vui lòng tạo nhân vật trước!", ephemeral=True)
            return

        now = time.time()
        diff = now - player["last_cultivate_time"]
        if diff < config.CULTIVATE_COOLDOWN_SECONDS:
            remain = int(config.CULTIVATE_COOLDOWN_SECONDS - diff)
            mins, secs = divmod(remain, 60)
            t_str = f"{mins}p {secs}s" if mins > 0 else f"{secs}s"
            await interaction.response.send_message(
                f"⏳ Kinh mạch còn bão hòa chân khí. Hãy tĩnh dưỡng thêm **{t_str}**!",
                ephemeral=True
            )
            return

        realm_id = player["realm_id"]
        base_exp, base_stone = config.get_cultivate_reward(realm_id)

        roll = random.random()
        msg_extra = ""
        if roll < 0.05:
            base_exp = int(base_exp * 2.2)
            base_stone = int(base_stone * 2)
            msg_extra = " ⚡ **(Đại Ngộ Đạo x2.2 EXP!)**"
        elif roll < 0.18:
            base_exp = int(base_exp * 1.5)
            msg_extra = " 🪷 **(Tiểu Ngộ Đạo x1.5 EXP!)**"

        await db.update_player_cultivate(user_id, base_exp, base_stone, now)
        updated_player = await db.get_player(user_id)
        new_embed = await create_hub_embed(interaction.user, updated_player)

        await interaction.response.edit_message(
            content=f"🧘 Tọa thiền xong: +**{base_exp:,} EXP** │ +**{base_stone} Linh Thạch**{msg_extra}",
            embed=new_embed,
            view=self
        )

    @discord.ui.button(label="Trùng Kích", style=discord.ButtonStyle.danger, emoji="⚡", row=0)
    async def btn_breakthrough(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        player = await db.get_player(user_id)
        if not player:
            return

        realm_id = player["realm_id"]
        cur_exp = player["current_exp"]

        if cgc.is_max_tu_vi_realm(realm_id):
            await interaction.response.send_message("👑 Đạo hữu đã đạt cảnh giới Đỉnh Phong Siêu Thoát cực hạn!", ephemeral=True)
            return

        req_exp = config.get_required_exp(realm_id)
        if cur_exp < req_exp:
            missing = req_exp - cur_exp
            await interaction.response.send_message(
                f"⚠️ Chưa đủ tu vi để đột phá!\n• Cần: **{req_exp:,}** EXP\n• Hiện có: **{cur_exp:,}** EXP (Còn thiếu **{missing:,}** EXP). Hãy bấm [🧘 Tọa Thiền] tiếp.",
                ephemeral=True
            )
            return

        base_rate = config.get_breakthrough_rate(realm_id)
        buff = player.get("breakthrough_buff", 0.0) or 0.0
        final_rate = min(1.0, base_rate + buff)

        success = random.random() < final_rate
        next_realm = cgc.get_next_tu_vi_realm(realm_id)

        if success and next_realm:
            new_id = next_realm["id"]
            rem_exp = cur_exp - req_exp
            await db.update_player_breakthrough_success(user_id, new_id, rem_exp)
            stats = config.get_combat_stats(new_id)
            await db.update_player_hp(user_id, stats["max_hp"])

            updated_player = await db.get_player(user_id)
            new_embed = await create_hub_embed(interaction.user, updated_player)
            await interaction.response.edit_message(
                content=f"🎉 **ĐỘT PHÁ THÀNH CÔNG!** Đạo hữu đã bước lên cảnh giới: **{next_realm['name']}**!",
                embed=new_embed,
                view=self
            )
        else:
            loss = int(cur_exp * random.uniform(0.10, 0.20))
            await db.update_player_breakthrough_failure(user_id, loss)
            updated_player = await db.get_player(user_id)
            new_embed = await create_hub_embed(interaction.user, updated_player)
            await interaction.response.edit_message(
                content=f"🔥 **Đột phá thất bại!** Tẩu hỏa nhập ma tổn thất -**{loss:,} EXP**. Hãy tẩm bổ đan dược rồi thử lại.",
                embed=new_embed,
                view=self
            )

    @discord.ui.button(label="Túi Đồ", style=discord.ButtonStyle.secondary, emoji="🎒", row=0)
    async def btn_inventory(self, interaction: discord.Interaction, button: discord.ui.Button):
        user_id = interaction.user.id
        player = await db.get_player(user_id)
        inv = await db.get_inventory(user_id)

        if not inv:
            await interaction.response.send_message(
                f"🎒 Túi trữ vật đang trống! Hiện có **{player['linh_thach']:,}** Linh Thạch. Bấm [🏪 Vạn Bảo Các] để mua đồ.",
                ephemeral=True
            )
            return

        lines = []
        for r in inv:
            item_info = config.SHOP_ITEMS.get(r["item_key"], {"name": r["item_key"]})
            lines.append(f"• **{item_info['name']}** x`{r['quantity']}` (Dùng: `/su_dung dan_duoc:{r['item_key']}`)")

        embed = discord.Embed(
            title=f"🎒 TÚI TRỮ VẬT: {player['dao_hieu']}",
            description="\n".join(lines),
            color=config.COLOR_CYAN
        )
        embed.set_footer(text="Dùng lệnh /su_dung cho đan dược | Dùng /trang_bi cho vũ khí")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Vạn Bảo Các", style=discord.ButtonStyle.success, emoji="🏪", row=0)
    async def btn_shop(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title=f"{config.EMOJI_SHOP} VẠN BẢO CÁC - THIÊN HẠ BẢO VẬT {config.EMOJI_SHOP}",
            description="Bảng giá hôm nay:",
            color=config.COLOR_GOLD
        )
        pills, equips = [], []
        for k, v in config.SHOP_ITEMS.items():
            line = f"• **{v['name']}** - 💎 `{v['price']:,}` Linh Thạch (Mã: `{k}`)"
            if v.get("category") == "consumable":
                pills.append(line)
            else:
                equips.append(line)

        embed.add_field(name="💊 Đan Dược", value="\n".join(pills), inline=False)
        embed.add_field(name="⚔️ Pháp Bảo & Linh Thú", value="\n".join(equips), inline=False)
        embed.set_footer(text="Gõ lệnh /mua vat_pham:<mã> để mua sắm!")
        await interaction.response.send_message(embed=embed, ephemeral=True)

    # ROW 1: HOẠT ĐỘNG, CẬP NHẬT & TÁN TU XÓA NHÂN VẬT
    @discord.ui.button(label="Lịch Luyện", style=discord.ButtonStyle.secondary, emoji="🗺️", row=1)
    async def btn_explore(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="🗺️ DANH SÁCH BÍ CẢNH CỔ ĐẠI",
            description="Dùng lệnh `/lich_luyen bi_canh:<mã>` để tiến vào:",
            color=config.COLOR_ORANGE
        )
        for bc in config.BI_CANH_LIST:
            req_info = cgc.get_tu_vi_realm_by_id(bc["min_realm"])
            req_name = req_info["name"] if req_info else f"Bậc {bc['min_realm']}"
            embed.add_field(
                name=f"🌲 {bc['name']} (Mã: `{bc['id']}`)",
                value=f"• Yêu cầu: **{req_name}**\n• {bc['description']}",
                inline=False
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Thiên Kiêu Bảng", style=discord.ButtonStyle.secondary, emoji="🏅", row=1)
    async def btn_leaderboard(self, interaction: discord.Interaction, button: discord.ui.Button):
        top_players = await db.get_top_players(limit=10)
        medals = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        lines = []
        for i, p in enumerate(top_players):
            m = medals[i] if i < len(medals) else f"#{i+1}"
            r_info = cgc.get_tu_vi_realm_by_id(p["realm_id"])
            r_name = r_info["name"] if r_info else f"Bậc {p['realm_id']}"
            lines.append(f"{m} **{p['dao_hieu']}** • `{r_name}` • *{p['current_exp']:,} EXP*")

        embed = discord.Embed(
            title="🏅 THIÊN KIÊU BẢNG - TOP ĐẠI NĂNG",
            description="\n".join(lines) if lines else "Chưa có tu sĩ nào ghi danh.",
            color=config.COLOR_GOLD
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="Làm Mới", style=discord.ButtonStyle.secondary, emoji="🔄", row=1)
    async def btn_refresh(self, interaction: discord.Interaction, button: discord.ui.Button):
        player = await db.get_player(interaction.user.id)
        if player:
            new_embed = await create_hub_embed(interaction.user, player)
            await interaction.response.edit_message(content=None, embed=new_embed, view=self)

    @discord.ui.button(label="Tán Tu (Xóa)", style=discord.ButtonStyle.danger, emoji="💀", row=1)
    async def btn_delete_character(self, interaction: discord.Interaction, button: discord.ui.Button):
        """Bấm nút xóa nhân vật / tán tu."""
        player = await db.get_player(interaction.user.id)
        if not player:
            return

        embed = discord.Embed(
            title="⚠️ CẢNH BÁO TÁN TU CHUYỂN SINH (XÓA NHÂN VẬT) ⚠️",
            description=(
                f"Đạo hữu **{player['dao_hieu']}** có chắc chắn muốn **TÁN TU CHUYỂN SINH** không?\n\n"
                f"🚨 **Hành động này sẽ xóa vĩnh viễn:**\n"
                f"• Cảnh giới tu vi và toàn bộ EXP đã tích lũy\n"
                f"• Toàn bộ **{player['linh_thach']:,}** Linh Thạch và túi đồ\n"
                f"• Bạn sẽ trở lại làm Phàm Nhân và có thể tạo lại nhân vật mới từ đầu!"
            ),
            color=config.COLOR_FAIL
        )
        embed.set_footer(text="Hành động này không thể hoàn tác!")
        view = ConfirmDeleteView(interaction.user.id)
        await interaction.response.edit_message(content=None, embed=embed, view=view)


# =============================================================================
# COG MENU CHÍNH
# =============================================================================

class MenuCog(commands.Cog, name="Menu Tu Tiên"):
    """Lệnh bảng điều khiển Menu Hub tương tác."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="menu", description="Mở Bảng Điều Khiển Tu Tiên (HUB) tương tác nút bấm, quản lý toàn diện")
    async def menu(self, interaction: discord.Interaction):
        """Mở menu tương tác chính."""
        user = interaction.user
        player = await db.get_player(user.id)

        # Trường hợp 1: Người chơi mới chưa đăng ký nhân vật
        if not player:
            embed = discord.Embed(
                title="⛩️ BƯỚC VÀO TIÊN ĐẠO - KHAI MỞ TIÊN LỘ ⛩️",
                description=(
                    f"Chào mừng đạo hữu **{user.display_name}** đã giáng lâm Tu Tiên Giới!\n\n"
                    f"Trời đất vô tình coi vạn vật như cỏ rác. Muốn nghịch thiên đoạt mệnh, "
                    f"chỉ có con đường duy nhất là **Tu Hành Chứng Đạo**!\n\n"
                    f"👉 **Hãy nhấn nút màu xanh bên dưới để định danh Đạo Hiệu và bước vào tiên lộ:**"
                ),
                color=config.COLOR_GOLD
            )
            embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
            embed.set_thumbnail(url=user.display_avatar.url)
            embed.add_field(
                name="🎁 Cơ Duyên Nhập Môn",
                value=f"• Cảnh giới ban đầu: **Ngưng Khí Kỳ - Sơ Kỳ**\n• Ngân lượng khởi nghiệp: **100 Linh Thạch**\n• Mở khóa trọn bộ {cgc.TOTAL_TU_VI_REALMS} cảnh giới Tiên Nghịch",
                inline=False
            )
            embed.set_footer(text="Nhấn nút 'Khai Mở Tiên Lộ' để bắt đầu ngay!")

            view = UnregisteredView(user.id)
            await interaction.response.send_message(embed=embed, view=view)
            return

        # Trường hợp 2: Đã có nhân vật -> Hiển thị Trung Tâm Điều Khiển (HUB)
        embed = await create_hub_embed(user, player)
        view = MainHubView(user.id)
        await interaction.response.send_message(embed=embed, view=view)

    @app_commands.command(name="xoa_nhan_vat", description="Tán tu chuyển sinh, xóa sạch nhân vật cũ để tạo lại từ đầu")
    async def xoa_nhan_vat(self, interaction: discord.Interaction):
        """Lệnh tắt để xóa nhân vật."""
        user = interaction.user
        player = await db.get_player(user.id)

        if not player:
            await interaction.response.send_message("Đạo hữu chưa có nhân vật nào để xóa!", ephemeral=True)
            return

        embed = discord.Embed(
            title="⚠️ XÁC NHẬN TÁN TU (XÓA NHÂN VẬT) ⚠️",
            description=f"Đạo hữu **{player['dao_hieu']}** có chắc chắn muốn xóa toàn bộ tu vi, linh thạch và túi đồ để tạo lại nhân vật từ đầu không?",
            color=config.COLOR_FAIL
        )
        view = ConfirmDeleteView(user.id)
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(MenuCog(bot))
