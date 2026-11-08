from langchain_core.output_parsers import StrOutputParser
from langchain_qwq import ChatQwen
from langchain_core.prompts import PromptTemplate
import config as cfg

prompt_text = PromptTemplate.from_template(
    "我的邻居姓{lastName}，刚生了个{gender}，请你根据生肖、属性，帮他起一个{count}个字的名字，仅回答名字即可不需要其他内容"
)

model = ChatQwen(
    model="qwen-max",
    api_key=cfg.CONFIG_API_KEY_OS,
    api_base=cfg.CONFIG_BASE_URL_QWEN,
)

parser = StrOutputParser()

chain = prompt_text | model | parser | model
print(chain.invoke({"lastName": "周", "gender": "女儿", "count": "三"}).content)