from langchain_core.prompts import PromptTemplate
from langchain_qwq import ChatQwen
from langchain_core.runnables import RunnableLambda
import os
import config as cfg

api_key = os.getenv("DASHSCOPE_API_KEY")

mock_data = [
    {"year": "1984", "name": "Jordan", "score": 35600},
    {"year": "1984", "name": "Stokton", "score": 19800},
    {"year": "1992", "name": "Oneal", "score": 28000},
    {"year": "1996", "name": "Iverson", "score": 26500},
    {"year": "1996", "name": "Kobe", "score": 38000},
    {"year": "1996", "name": "Nash", "score": 19000},
    {"year": "1995", "name": "Garnett", "score": 23000},
    {"year": "1997", "name": "Duncan", "score": 29000},
    {"year": "1998", "name": "Pierce", "score": 27000},
    {"year": "1998", "name": "McGrady", "score": 22000},
    {"year": "2003", "name": "James", "score": 43000},
    {"year": "2003", "name": "Wade", "score": 27500},
    {"year": "2003", "name": "Anthony", "score": 30000},
]

def get_origin_data(_=None):
    return mock_data

def get_group_data(origin_data):
    group_res = {}
    for data in origin_data:
        year = data["year"]
        if year not in group_res:
            group_res[year] = []
        group_res[year].append(data)
    return group_res

def get_score_king(group_datas):
    score_king = {}
    for year, datas in group_datas.items():
        max_score = 0
        for data in datas:
            if data["score"] > max_score:
                max_score = data["score"]
                score_king[year] = data
    return score_king

def format_score_info(score_king):
    lines = []
    for year, data in sorted(score_king.items()):
        lines.append(f"{year}年: {data['name']} ({data['score']}分)")
    return {"score_info": "\n".join(lines)}

get_origin_data_runnable = RunnableLambda(get_origin_data)
get_group_data_runnable = RunnableLambda(get_group_data)
get_score_king_runnable = RunnableLambda(get_score_king)
format_score_info_runnable = RunnableLambda(format_score_info)
 
prompt_template = PromptTemplate.from_template(
    "每年NBA的得分王如下：{score_info}。请从这个信息中告诉我，最终的得分王是谁"
)

model = ChatQwen(
    model="qwen-max",
    api_key=api_key,
    api_base=cfg.CONFIG_BASE_URL_QWEN,
)

chain = (
    get_origin_data_runnable
    | get_group_data_runnable
    | get_score_king_runnable
    | format_score_info_runnable
    | prompt_template
    | model
)

res = chain.invoke(None)
print(res)