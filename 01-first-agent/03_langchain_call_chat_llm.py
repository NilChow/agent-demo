from langchain_qwq.chat_models import ChatQwen
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
import config as cfg

chat = ChatQwen(
    model="qwen-max",
    api_base=cfg.CONFIG_BASE_URL_QWEN,
)

messages = [
    SystemMessage(content="你是一个来自边塞的诗人"),
    HumanMessage(content="给我写一首唐诗"),
    AIMessage(content="风急天高猿啸哀，渚清沙白鸟飞回。无边落木萧萧下，不尽长江滚滚来。万里悲秋常作客，百年多病独登台。艰难苦恨繁霜鬓，潦倒新停浊酒杯。"),
    HumanMessage(content="请你仿照上一首诗的格式，再来一首")
]

for chunk in chat.stream(input=messages):
    print(chunk.content, end="", flush=True)