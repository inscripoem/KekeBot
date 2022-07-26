from nonebot import get_driver, on_command, logger
from nonebot.adapters.onebot.v11 import Message

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)


swindle = on_command('诈骗', block=True)




# Export something for other plugin
# export = nonebot.export()
# export.foo = "bar"

# @export.xxx
# def some_function():
#     pass

