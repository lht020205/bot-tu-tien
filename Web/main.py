import random
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

import canh_gioi  # cần có get_realm_info() và get_next_realm()

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="Tu Tiên - Test Tu Luyện & Đột Phá")

# ----------------------------------------------------------------------------
# Cấu hình
# ----------------------------------------------------------------------------
EXP_MIN, EXP_MAX = 10, 50       # EXP nhận được mỗi lần bế quan
FAIL_LOSS_RATIO = 0.5           # Đột phá thất bại: mất 50% EXP đã dùng (đặt 1.0 để mất toàn bộ)

# Dữ liệu người chơi giả lập (reset mỗi khi khởi động lại server)
player = {"realm_id": 1, "exp": 0}


def build_state() -> dict:
    """Gom thông tin người chơi + cảnh giới hiện tại + cảnh giới tiếp theo."""
    current = canh_gioi.get_realm_info(player["realm_id"])
    next_realm = canh_gioi.get_next_realm(player["realm_id"])

    exp_needed = None
    if next_realm is not None:
        exp_needed = max(0, next_realm["required_exp"] - player["exp"])

    return {
        "player": dict(player),
        "current_realm": current,
        "next_realm": next_realm,   # None nếu đã ở cảnh giới cao nhất
        "exp_needed": exp_needed,   # EXP còn thiếu để được đột phá
    }


# Các endpoint dùng `async def` (không có await) nên chạy tuần tự trên event loop,
# tránh xung đột khi nhiều request cùng sửa biến global `player`.

@app.get("/api/player")
async def get_player():
    return build_state()


@app.post("/api/tu-luyen")
async def tu_luyen():
    gained = random.randint(EXP_MIN, EXP_MAX)
    player["exp"] += gained
    return {
        "message": f"Bế quan tu luyện, tu vi tăng thêm {gained} EXP.",
        "gained_exp": gained,
        **build_state(),
    }


@app.post("/api/dot-pha")
async def dot_pha():
    next_realm = canh_gioi.get_next_realm(player["realm_id"])
    if next_realm is None:
        raise HTTPException(status_code=400, detail="Bạn đã đạt cảnh giới cao nhất, không thể đột phá thêm.")

    cost = next_realm["required_exp"]
    if player["exp"] < cost:
        raise HTTPException(
            status_code=400,
            detail=f"Chưa đủ tu vi để đột phá lên {next_realm['name']}: còn thiếu {cost - player['exp']:,} EXP.",
        )

    success = random.random() < next_realm["success_rate"]

    if success:
        player["exp"] -= cost
        player["realm_id"] += 1
        exp_lost = cost
        message = f"Đột phá thành công! Bạn đã đạt {next_realm['name']}."
    else:
        exp_lost = int(cost * FAIL_LOSS_RATIO)
        player["exp"] -= exp_lost
        message = f"Đột phá thất bại! Bạn mất {exp_lost:,} EXP, hãy tu luyện thêm rồi thử lại."

    return {"success": success, "exp_lost": exp_lost, "message": message, **build_state()}


@app.get("/", include_in_schema=False)
async def index():
    return FileResponse(BASE_DIR / "index.html")