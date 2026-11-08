from langchain_core.prompts import PromptTemplate, FewShotPromptTemplate, ChatPromptTemplate

template = PromptTemplate.from_template("我的邻居是: {lastname}, 最喜欢: {hobby}")
res = template.format(lastname="iverson", hobby="打篮球")
print(res, type(res))

res2 = template.invoke({"lastname": "iverson", "hobby": "打篮球"})
print(res2, type(res2))