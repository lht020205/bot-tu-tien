# -*- coding: utf-8 -*-
"""
bot.py
======
File chạy chính của Bot Discord Tu Tiên:
- Khởi tạo Discord Bot với discord.py (v2.x)
- Tải cơ sở dữ liệu và các Cogs chức năng (/khoi_dau, /ho_so, /tu_luyen, /dot_pha, /tra_cuu...)
- Tự động đồng bộ Slash Commands
"""
import sys
import asyncio
import logging
import discord
from discord.ext import commands

import config
import database as db

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("BotTuTien")


class TuTienBot(commands.Bot):
    """Lớp Bot Tu Tiên kế thừa commands.Bot."""

    def __init__(self):
        intents = discord.Intents.default()
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )
        self.add_command(sync_command)

    async def setup_hook(self) -> None:
        """Khởi tạo database và nạp các Cogs khi bot khởi động."""
        logger.info("Đang khởi tạo cơ sở dữ liệu SQLite...")
        await db.init_db()

        # Nạp các cogs
        cogs_to_load = [
            "cogs.menu",
            "cogs.tu_tien",
            "cogs.tra_cuu",
            "cogs.van_bao_cac",
            "cogs.lich_luyen",
        ]
        for cog in cogs_to_load:
            try:
                await self.load_extension(cog)
                logger.info(f"Đã nạp thành công module: {cog}")
            except Exception as e:
                logger.error(f"Lỗi khi nạp module {cog}: {e}", exc_info=True)

        # Đồng bộ Slash Commands
        try:
            if config.GUILD_ID:
                guild_obj = discord.Object(id=int(config.GUILD_ID))
                self.tree.copy_global_to(guild=guild_obj)
                synced = await self.tree.sync(guild=guild_obj)
                logger.info(f"Đã đồng bộ {len(synced)} lệnh Slash vào Guild ID: {config.GUILD_ID}")
            else:
                synced = await self.tree.sync()
                logger.info(f"Đã đồng bộ toàn cầu (global) {len(synced)} lệnh Slash.")
        except Exception as e:
            logger.error(f"Lỗi khi đồng bộ Slash Commands: {e}")

    async def on_ready(self):
        """Sự kiện khi bot đã đăng nhập và sẵn sàng hoạt động."""
        logger.info(f"==================================================")
        logger.info(f"  Bot Tu Tiên đã sẵn sàng: {self.user} (ID: {self.user.id})")
        logger.info(f"  Đang phục vụ {len(self.guilds)} máy chủ Discord.")
        logger.info(f"==================================================")

        # Tự động đồng bộ tức thì (Instant Sync) vào toàn bộ server bot đang tham gia
        for guild in self.guilds:
            try:
                self.tree.copy_global_to(guild=guild)
                synced = await self.tree.sync(guild=guild)
                logger.info(f"⚡ ĐÃ ĐỒNG BỘ TỨC THÌ {len(synced)} LỆNH VÀO SERVER: {guild.name} (ID: {guild.id})")
            except Exception as e:
                logger.error(f"Lỗi khi đồng bộ server {guild.name}: {e}")

        # Đặt trạng thái hoạt động
        activity = discord.Activity(
            type=discord.ActivityType.custom,
            name="⛩️ /menu để mở Bảng Tu Tiên"
        )
        await self.change_presence(status=discord.Status.online, activity=activity)


# Lệnh dự phòng: Gõ !sync trong kênh chat bất kỳ để ép Discord cập nhật lệnh ngay
@commands.command(name="sync")
async def sync_command(ctx: commands.Context):
    async with ctx.typing():
        for guild in ctx.bot.guilds:
            ctx.bot.tree.copy_global_to(guild=guild)
            await ctx.bot.tree.sync(guild=guild)
        synced_global = await ctx.bot.tree.sync()
        await ctx.send(f"⚡ **Đã đồng bộ tức thì {len(synced_global)} lệnh Slash vào server!** Bạn có thể gõ ngay `/menu`.")


async def main():
    if not config.DISCORD_TOKEN:
        logger.error(
            "\n" + "=" * 60 + "\n"
            "CHƯA CẤU HÌNH DISCORD BOT TOKEN!\n"
            "Vui lòng mở file .env và điền DISCORD_TOKEN=<token_cua_ban>\n"
            "Cách lấy token: Truy cập https://discord.com/developers/applications\n"
            "Tạo bot -> Chọn tab Bot -> Nhấn Reset Token -> Copy dán vào .env\n"
            + "=" * 60
        )
        sys.exit(1)

    bot = TuTienBot()
    async with bot:
        await bot.start(config.DISCORD_TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot đã dừng bởi người dùng.")
