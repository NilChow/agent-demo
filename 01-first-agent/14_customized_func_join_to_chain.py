from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableLambda
from langchain_core.prompts import PromptTemplate
from langchain_qwq import ChatQwen
import config as cfg

first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastName}，刚生了个{gender}，请你根据生肖、属性，帮他起一个{count}个字的名字，仅回答名字即可不需要其他内容。"
)

second_prompt = PromptTemplate.from_template(
    "朋友的小孩名字叫{name}，请给这个名字评分，并给出一段评价，还要分析下这个名字和性别是否匹配"
)

model = ChatQwen(
    model="qwen-max",
    api_key=cfg.CONFIG_API_KEY_OS,
    api_base=cfg.CONFIG_BASE_URL_QWEN,
)

parser = StrOutputParser()
my_func = RunnableLambda(lambda ai_msg: {"name": ai_msg.content})

chain = first_prompt | model | my_func
print(chain.invoke({"lastName": "王", "gender": "儿子", "count": "四"}))