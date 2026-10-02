# -*- coding: utf-8 -*-
"""
database.py
===========
Quản lý cơ sở dữ liệu SQLite bất đồng bộ (aiosqlite) cho Bot Tu Tiên:
- Bảng người chơi (players): Lưu thông tin cảnh giới, exp, linh thạch, trang bị, HP, PvP
- Bảng túi đồ (inventory): Lưu trữ đan dược, pháp bảo, linh thú
- Bảng tông môn (sects) & thành viên tông môn (sect_members)
- Các thao tác đọc / ghi an toàn với transaction
"""
import time
from typing import Optional, Dict, Any, List
import aiosqlite
from config import DATABASE_PATH


async def init_db() -> None:
    """Khởi tạo các bảng dữ liệu nếu chưa tồn tại, hỗ trợ migrate tự động."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Bảng players
        await db.execute("""
            CREATE TABLE IF NOT EXISTS players (
                user_id INTEGER PRIMARY KEY,
                dao_hieu TEXT NOT NULL,
                realm_id INTEGER DEFAULT 1,
                current_exp INTEGER DEFAULT 0,
                linh_thach INTEGER DEFAULT 100,
                current_hp INTEGER DEFAULT 160,
                equipped_phap_bao TEXT DEFAULT NULL,
                equipped_linh_thu TEXT DEFAULT NULL,
                breakthrough_buff REAL DEFAULT 0.0,
                last_cultivate_time REAL DEFAULT 0,
                last_explore_time REAL DEFAULT 0,
                last_duel_time REAL DEFAULT 0,
                last_song_tu_time REAL DEFAULT 0,
                pvp_wins INTEGER DEFAULT 0,
                pvp_losses INTEGER DEFAULT 0,
                total_cultivations INTEGER DEFAULT 0,
                total_breakthroughs INTEGER DEFAULT 0,
                created_at REAL DEFAULT 0
            )
        """)

        # Bảng inventory
        await db.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                item_key TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                UNIQUE(user_id, item_key),
                FOREIGN KEY (user_id) REFERENCES players(user_id) ON DELETE CASCADE
            )
        """)

        # Bảng tông môn
        await db.execute("""
            CREATE TABLE IF NOT EXISTS sects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                leader_id INTEGER NOT NULL,
                level INTEGER DEFAULT 1,
                bank_stones INTEGER DEFAULT 0,
                created_at REAL DEFAULT 0
            )
        """)

        # Tự động migrate thêm cột nếu bảng đã tồn tại từ trước
        columns_to_add = [
            ("current_hp", "INTEGER DEFAULT 160"),
            ("equipped_phap_bao", "TEXT DEFAULT NULL"),
            ("equipped_linh_thu", "TEXT DEFAULT NULL"),
            ("breakthrough_buff", "REAL DEFAULT 0.0"),
            ("last_explore_time", "REAL DEFAULT 0"),
            ("last_duel_time", "REAL DEFAULT 0"),
            ("last_song_tu_time", "REAL DEFAULT 0"),
            ("pvp_wins", "INTEGER DEFAULT 0"),
            ("pvp_losses", "INTEGER DEFAULT 0"),
        ]

        # Kiểm tra các cột hiện có trong players
        async with db.execute("PRAGMA table_info(players)") as cursor:
            existing_cols = [row[1] for row in await cursor.fetchall()]

        for col_name, col_type in columns_to_add:
            if col_name not in existing_cols:
                try:
                    await db.execute(f"ALTER TABLE players ADD COLUMN {col_name} {col_type}")
                except Exception:
                    pass

        # Kiểm tra cột trong inventory nếu còn dùng schema cũ
        async with db.execute("PRAGMA table_info(inventory)") as cursor:
            inv_cols = [row[1] for row in await cursor.fetchall()]
        if "item_key" not in inv_cols:
            try:
                await db.execute("ALTER TABLE inventory ADD COLUMN item_key TEXT DEFAULT ''")
            except Exception:
                pass

        await db.commit()


async def get_player(user_id: int) -> Optional[Dict[str, Any]]:
    """Lấy thông tin người chơi theo user_id Discord."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM players WHERE user_id = ?", (user_id,)) as cursor:
            row = await cursor.fetchone()
            if row:
                return dict(row)
    return None


async def create_player(user_id: int, dao_hieu: str) -> Dict[str, Any]:
    """Tạo mới hồ sơ tu sĩ cho người chơi."""
    now = time.time()
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO players (
                user_id, dao_hieu, realm_id, current_exp, linh_thach,
                current_hp, equipped_phap_bao, equipped_linh_thu, breakthrough_buff,
                last_cultivate_time, last_explore_time, last_duel_time, last_song_tu_time,
                pvp_wins, pvp_losses, total_cultivations, total_breakthroughs, created_at
            ) VALUES (?, ?, 1, 0, 100, 160, NULL, NULL, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, ?)
        """, (user_id, dao_hieu, now))
        await db.commit()

    return await get_player(user_id)


async def update_player_cultivate(
    user_id: int,
    exp_gain: int,
    stone_gain: int,
    cultivate_time: float
) -> None:
    """Cập nhật EXP, Linh Thạch và thời gian sau khi tu luyện."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE players
            SET current_exp = current_exp + ?,
                linh_thach = linh_thach + ?,
                last_cultivate_time = ?,
                total_cultivations = total_cultivations + 1
            WHERE user_id = ?
        """, (exp_gain, stone_gain, cultivate_time, user_id))
        await db.commit()


async def update_player_breakthrough_success(
    user_id: int,
    new_realm_id: int,
    remaining_exp: int
) -> None:
    """Cập nhật cảnh giới mới và tiêu hao buff khi đột phá thành công."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE players
            SET realm_id = ?,
                current_exp = ?,
                breakthrough_buff = 0.0,
                total_breakthroughs = total_breakthroughs + 1
            WHERE user_id = ?
        """, (new_realm_id, remaining_exp, user_id))
        await db.commit()


async def update_player_breakthrough_failure(
    user_id: int,
    exp_loss: int
) -> None:
    """Khấu trừ EXP do phản phệ khí huyết khi đột phá thất bại."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE players
            SET current_exp = MAX(0, current_exp - ?)
            WHERE user_id = ?
        """, (exp_loss, user_id))
        await db.commit()


async def add_breakthrough_buff(user_id: int, buff_value: float) -> None:
    """Cộng thêm tỷ lệ buff đột phá từ đan dược (tối đa +50%)."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE players
            SET breakthrough_buff = MIN(0.50, COALESCE(breakthrough_buff, 0.0) + ?)
            WHERE user_id = ?
        """, (buff_value, user_id))
        await db.commit()


async def update_player_hp(user_id: int, new_hp: int) -> None:
    """Cập nhật khí huyết hiện tại của người chơi."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE players SET current_hp = ? WHERE user_id = ?
        """, (new_hp, user_id))
        await db.commit()


async def modify_player_stones(user_id: int, delta: int) -> bool:
    """Cộng hoặc trừ Linh Thạch của người chơi. Trả về True nếu thành công."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        if delta < 0:
            async with db.execute("SELECT linh_thach FROM players WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                if not row or row[0] < abs(delta):
                    return False
        await db.execute("""
            UPDATE players SET linh_thach = linh_thach + ? WHERE user_id = ?
        """, (delta, user_id))
        await db.commit()
        return True


async def update_player_explore(
    user_id: int,
    exp_gain: int,
    stone_gain: int,
    explore_time: float,
    new_hp: int
) -> None:
    """Cập nhật sau khi thám hiểm lịch luyện bí cảnh."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            UPDATE players
            SET current_exp = current_exp + ?,
                linh_thach = linh_thach + ?,
                current_hp = ?,
                last_explore_time = ?
            WHERE user_id = ?
        """, (exp_gain, stone_gain, new_hp, explore_time, user_id))
        await db.commit()


async def update_player_duel(
    winner_id: int,
    loser_id: int,
    duel_time: float,
    stone_reward: int = 50
) -> None:
    """Cập nhật kết quả sau trận đấu pháp giữa hai tu sĩ."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        # Winner
        await db.execute("""
            UPDATE players
            SET pvp_wins = pvp_wins + 1,
                linh_thach = linh_thach + ?,
                last_duel_time = ?
            WHERE user_id = ?
        """, (stone_reward, duel_time, winner_id))

        # Loser
        await db.execute("""
            UPDATE players
            SET pvp_losses = pvp_losses + 1,
                last_duel_time = ?
            WHERE user_id = ?
        """, (duel_time, loser_id))

        await db.commit()


async def update_player_song_tu(
    user1_id: int,
    user2_id: int,
    exp_gain: int,
    stone_gain: int,
    song_tu_time: float
) -> None:
    """Cập nhật cả 2 người chơi sau khi song tu."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        for uid in (user1_id, user2_id):
            await db.execute("""
                UPDATE players
                SET current_exp = current_exp + ?,
                    linh_thach = linh_thach + ?,
                    last_song_tu_time = ?
                WHERE user_id = ?
            """, (exp_gain, stone_gain, song_tu_time, uid))
        await db.commit()


async def set_equipment(user_id: int, item_type: str, item_key: Optional[str]) -> None:
    """Trang bị hoặc tháo gỡ pháp bảo / linh thú."""
    col = "equipped_phap_bao" if item_type == "phap_bao" else "equipped_linh_thu"
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(f"UPDATE players SET {col} = ? WHERE user_id = ?", (item_key, user_id))
        await db.commit()


# =============================================================================
# QUẢN LÝ TÚI ĐỒ (INVENTORY)
# =============================================================================

async def add_item(user_id: int, item_key: str, quantity: int = 1) -> None:
    """Thêm vật phẩm vào túi đồ của người chơi."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            INSERT INTO inventory (user_id, item_key, quantity)
            VALUES (?, ?, ?)
            ON CONFLICT(user_id, item_key) DO UPDATE SET quantity = quantity + ?
        """, (user_id, item_key, quantity, quantity))
        await db.commit()


async def remove_item(user_id: int, item_key: str, quantity: int = 1) -> bool:
    """Tiêu hao hoặc xóa vật phẩm khỏi túi đồ."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        async with db.execute(
            "SELECT quantity FROM inventory WHERE user_id = ? AND item_key = ?",
            (user_id, item_key)
        ) as cursor:
            row = await cursor.fetchone()
            if not row or row[0] < quantity:
                return False

        new_qty = row[0] - quantity
        if new_qty > 0:
            await db.execute(
                "UPDATE inventory SET quantity = ? WHERE user_id = ? AND item_key = ?",
                (new_qty, user_id, item_key)
            )
        else:
            await db.execute(
                "DELETE FROM inventory WHERE user_id = ? AND item_key = ?",
                (user_id, item_key)
            )
        await db.commit()
        return True


async def get_inventory(user_id: int) -> List[Dict[str, Any]]:
    """Lấy danh sách toàn bộ vật phẩm trong túi đồ của người chơi."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM inventory WHERE user_id = ? AND quantity > 0",
            (user_id,)
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


async def get_top_players(limit: int = 10) -> List[Dict[str, Any]]:
    """Lấy danh sách các tu sĩ có tu vi cao nhất."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("""
            SELECT * FROM players
            ORDER BY realm_id DESC, current_exp DESC
            LIMIT ?
        """, (limit,)) as cursor:
            rows = await cursor.fetchall()
            return [dict(r) for r in rows]


async def delete_player(user_id: int) -> bool:
    """Xóa bỏ hoàn toàn nhân vật và túi đồ của người chơi (dùng khi chuyển sinh / test lại)."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("DELETE FROM inventory WHERE user_id = ?", (user_id,))
        cursor = await db.execute("DELETE FROM players WHERE user_id = ?", (user_id,))
        await db.commit()
        return cursor.rowcount > 0

