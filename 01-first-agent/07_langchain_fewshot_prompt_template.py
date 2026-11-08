from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_qwq import ChatQwen
import config as cfg

example_template = PromptTemplate.from_template("单词: {word}, 反义词: {antonym}")

example_data = [
    {"word": "大", "antonym": "小"},
    {"word": "上", "antonym": "下"},
    {"word": "美", "antonym": "丑"},
]

few_shot_prompt = FewShotPromptTemplate(
    example_prompt=example_template,
    examples=example_data,
    # prefix="回答给定词的反义词，有如下提示",
    prefix="回答给定词的{input_word_0}，有如下提示",
    suffix="基于示例告诉我: {input_word_1}和{input_word_2}的{input_word_0}是？",
    input_variables=['input_word_0', 'input_word_1', 'input_word_2'],
)

prompt_text = few_shot_prompt.invoke(input={"input_word_0": "反义词", "input_word_1": "左", "input_word_2": "old"}).to_string()
print(prompt_text)

model = ChatQwen(
    model="qwen-max",
    api_key=cfg.CONFIG_API_KEY_OS,
    api_base=cfg.CONFIG_BASE_URL_QWEN,
)

print(model.invoke(input=prompt_text).content)