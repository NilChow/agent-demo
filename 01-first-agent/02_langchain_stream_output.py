from langchain_qwq import ChatQwen
import config as cfg

model = ChatQwen(
    model="qwen-max",
    api_base=cfg.CONFIG_BASE_URL_QWEN,
)

res = model.stream(input="你是谁呀？能做什么？")

for chunk in res:
    print(chunk.content, end="", flush=True)