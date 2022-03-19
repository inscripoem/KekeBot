from typing import Any

import httpx
from nonebot.log import logger


async def get_stat_by_bvid(bvid: str) -> dict:
    try:
        url = "https://api.bilibili.com/x/web-interface/view"
        params = {"bvid": bvid}
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, params=params)
            result = resp.json()
        if not result or result["code"] != 0:
            return {}
        return result["data"]["stat"]
    except Exception as e:
        logger.warning(f"Error in get_uid_by_name({bvid}): {e}")
        return {}


def cal_favcoin(favorite, coin):
    favcoin = favorite + coin
    if favcoin > favorite * 3 and favcoin > coin * 3:
        favcoin = min([favorite * 3, coin * 3])
    elif favorite * 3 < favcoin <= coin * 3:
        favcoin = favorite * 3
    else:
        favcoin = coin * 3
    return favcoin


def limit_fix(fix, floor, ceiling):
    if fix < floor:
        fix = floor
    elif fix > ceiling:
        fix = ceiling
    return float(format(fix, '.3f'))


