import base64
from re import findall
from sys import exc_info
import httpx
from httpx import AsyncClient
from nonebot import logger


async def get_cat():
    async with AsyncClient() as client:
        req_url = "https://api.thecatapi.com/v1/images/search"
        params = {'mime_types': 'gif'}
        try:
            res = await client.get(req_url, params=params, timeout=120)
            logger.info(res.json())
        except httpx.HTTPError as e:
            logger.warning(e)
            return [False, f"API异常{e}", '', '']
        try:
            img_url = res.json()[0]['url']
            content = await down_pic(img_url)
            img_base64 = convert_b64(content)
            if type(img_base64) == str:
                pic_cq = "[CQ:image,file=base64://" + img_base64 + "]"
            return [True, '', pic_cq, img_url]
        except:
            logger.warning(f"{exc_info()[0]}, {exc_info()[1]}")
            return [False, f"{exc_info()[0]} {exc_info()[1]}。", '', '']


async def get_dog():
    async with AsyncClient() as client:
        req_url = "https://dog.ceo/api/breeds/image/random"
        try:
            res = await client.get(req_url, timeout=120)
            logger.info(res.json())
        except httpx.HTTPError as e:
            logger.warning(e)
            return [False, f"API异常{e}", '', '']
        try:
            img_url = res.json()['message']
            content = await down_pic(img_url.replace("\\", ''))
            img_base64 = convert_b64(content)
            if type(img_base64) == str:
                pic_cq = "[CQ:image,file=base64://" + img_base64 + "]"
            return [True, '', pic_cq, img_url]
        except:
            logger.warning(f"{exc_info()[0]}, {exc_info()[1]}")
            return [False, f"{exc_info()[0]} {exc_info()[1]}。", '', '']


async def get_fox():
    async with AsyncClient() as client:
        req_url = "https://randomfox.ca/floof/"
        try:
            res = await client.get(req_url, timeout=120)
            logger.info(res.json())
        except httpx.HTTPError as e:
            logger.warning(e)
            return [False, f"API异常{e}", '', '']
        try:
            img_url = res.json()['image']
            content = await down_pic(img_url)
            img_base64 = convert_b64(content)
            if type(img_base64) == str:
                pic_cq = "[CQ:image,file=base64://" + img_base64 + "]"
            return [True, '', pic_cq, img_url]
        except:
            logger.warning(f"{exc_info()[0]}, {exc_info()[1]}")
            return [False, f"{exc_info()[0]} {exc_info()[1]}。", '', '']


async def down_pic(url):
    async with AsyncClient() as client:
        headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        }
        re = await client.get(url=url, headers=headers, timeout=120)
        if re.status_code == 200:
            logger.success("成功获取图片")
            return re.content
        else:
            logger.error(f"获取图片失败: {re.status_code}")
            return re.status_code


def convert_b64(content) -> str:
    ba = str(base64.b64encode(content))
    pic = findall(r"\'([^\"]*)\'", ba)[0].replace("'", "")
    return pic

