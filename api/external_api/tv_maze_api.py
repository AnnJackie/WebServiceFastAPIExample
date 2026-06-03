from typing import Optional
import httpx
from model.tv_maze_show_response import TvMazeShowResponse
from repository.database import config

async def get_show_by_id(show_id: int) -> Optional[TvMazeShowResponse]:
    url = f"{config.TV_MAZE_API_BASE_URL}/shows/{show_id}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            tv_show = TvMazeShowResponse(
                tv_show_id=data.get("id"),
                tv_show_name=data.get("name"),
                tv_show_url=data.get("url"),
                tv_show_image_original_url=data.get("image", {}).get("original"),
            )
            return tv_show
        except httpx.HTTPStatusError as exc:
            print(f"Cannot fetch TV show with id {show_id}: {exc}")
            return None
