from nonebot import on_command, logger, get_driver
from nonebot.params import CommandArg
from nonebot.adapters.onebot.v11.bot import Bot
from nonebot.adapters.onebot.v11 import GroupMessageEvent, Message
from .data_source import get_cat, get_dog, get_fox, get_else


setu_ban_group = get_driver().config.setu_ban_group
miao = on_command("来个", block=True)


@miao.handle()
async def hf(bot: Bot, event: GroupMessageEvent, msg: Message = CommandArg()):
    cat = msg.extract_plain_text().strip()
    gid = str(event.group_id)
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
        if gid in setu_ban_group or not cat:
            pic = [False, '', '', '']
            await miao.finish("请发送来个猫猫/狗狗/狐狸中的一个！")
        else:
            await miao.send(message=Message(f'稍等一下哦，正在搜罗{cat}图……'))
            pic = await get_else(cat)
    if pic[0]:
        try:
            await miao.send(
                message=Message(f"啊哈哈哈哈哈，{cat}来咯"),
            )
            await miao.send(message=Message(pic[2]))
        except Exception as e:
            logger.warning(e)
            await miao.finish(
                message=Message(f"消息被风控，图发不出来\n{pic[1]}\n这是链接\n{pic[3]}"),
            )
    else:
        await miao.finish(f"出错：{pic[1]}")
