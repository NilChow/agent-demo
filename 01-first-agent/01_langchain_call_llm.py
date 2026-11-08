from langchain_qwq import ChatQwen
import config as cfg

model = ChatQwen(
    model="qwen-max",
    api_base=cfg.CONFIG_BASE_URL_QWEN,
)

res = model.invoke(input="你是谁呀？能做什么？")
print(res)