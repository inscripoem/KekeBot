from bilibili_api import video
from nonebot import get_driver
from nonebot import on_command
from nonebot.adapters import Event, Message
from nonebot.params import CommandArg
from .config import Config

from .data_source import get_stat_by_bvid, cal_favcoin, limit_fix

global_config = get_driver().config
config = Config.parse_obj(global_config)

SVcal = on_command("周刊算分", aliases={"算分"}, block=True)


@SVcal.handle()
async def _(event: Event, msg: Message = CommandArg()):
    bvid = msg.extract_plain_text().strip()
    if not bvid.isalnum():
        await SVcal.finish("请输入BV号！")
    video_set = video.Video(bvid=bvid)
    info = await video_set.get_info()
    stats = info['stat']
    view = stats['view']
    danmaku = stats['danmaku']
    reply = stats['reply']
    favorite = stats['favorite']
    coin = stats['coin']
    share = stats['share']
    like = stats['like']

    favcoin = cal_favcoin(favorite, coin)

    fixb = favcoin / view * 200
    fixb = limit_fix(fixb, 0.000, 100.000)
    if favorite >= view or coin >= view:
        fixb = 0.000
    fixa = (favcoin + danmaku*5 + reply*5) / (view + favcoin + share + like + danmaku + reply) + fixb*0.01
    # 修正A的时间因素暂时没写，摆烂了
    fixa = limit_fix(fixa, 0.000, 1.500)
    if share >= view or like >= view:
        fixb = 0.000
    fixc = (view + favcoin) / (view + favcoin + reply*10 + danmaku*25)
    fixc = float(format(fixc, '.3f'))
    score = round((view + share*50 + like*30)*fixa + favcoin*fixb + (reply*10 + danmaku*25)*fixc)
    result = f"计算完成，总分为{score}，其中修正A为{fixa}，修正B为{fixb}，修正C为{fixc}\n此结果不一定准确，请以周刊实际为准"
    await SVcal.finish(result)














# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass
