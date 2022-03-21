from nonebot import on_command, logger
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import MessageSegment, Message
from nonebot.adapters.onebot.v11.event import Event
from .data_source import get_cat, get_dog, get_fox

miao = on_command("来个", block=True)


@miao.handle()
async def hf(bot: Bot, event: Event, msg: Message = CommandArg()):
    cat = msg.extract_plain_text().strip()
    if cat == "猫猫":
        await miao.send(message=Message(f'稍等一下哦，正在搜罗{cat}图……'))
        pic = await get_cat()
    elif cat == "狗狗":
        await miao.send(message=Message(f'稍等一下哦，正在搜罗{cat}图……'))
        pic = await get_dog()
    elif cat == "狐狸":
        await miao.send(message=Message(f'稍等一下哦，正在搜罗{cat}图……'))
        pic = await get_fox()
    else:
        pic = [False, '', '', '']
        await miao.finish("请发送来个猫猫/狗狗/狐狸中的一个！")
    if pic[0]:
        try:
            await miao.send(message=Message(pic[2]))
            await miao.send(
                message=Message(f"啊哈哈哈哈哈，{cat}来咯"),
            )
        except Exception as e:
            logger.warning(e)
            await miao.finish(
                message=Message(f"消息被风控，图发不出来\n{pic[1]}\n这是链接\n{pic[3]}"),
            )
    else:
        await miao.finish(f"出错：{pic[1]}")
