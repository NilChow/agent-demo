from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_qwq import ChatQwen
from langchain_core.prompts import PromptTemplate
import config as cfg

first_prompt = PromptTemplate.from_template(
    "我的邻居姓{lastName}，刚生了个{gender}，请你根据生肖、属性，帮他起一个{count}个字的名字，仅回答名字即可不需要其他内容。"
    "要求回复用json格式，第一个key是name，value就是你起的名字，第二个key是gender，value是{gender}请严格遵守格式要求"
)

second_prompt = PromptTemplate.from_template(
    "朋友的{gender}名字叫{name}，请给这个名字评分，并给出一段评价，还要分析下这个名字和性别是否匹配"
)

model = ChatQwen(
    model="qwen-max",
    api_key=cfg.CONFIG_API_KEY_OS,
    api_base=cfg.CONFIG_BASE_URL_QWEN,
)

parser = StrOutputParser()
json_parser = JsonOutputParser()

chain = first_prompt | model | json_parser | second_prompt
print(chain.invoke({"lastName": "王", "gender": "儿子", "count": "三"}))