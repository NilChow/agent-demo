# from dashscope import TextEmbedding
# import config as cfg
#
# res = TextEmbedding.call(
#     model="text-embedding-v3",
#     input="我喜欢你",
#     dimension=1024
# )
#
# print(res.output["embeddings"][0]["embedding"])


from langchain_community.embeddings import DashScopeEmbeddings
# from langchain_dashscope import DashScopeEmbeddings
import config as cfg

embeddings = DashScopeEmbeddings(
    model="text-embedding-v3",
    dashscope_api_key=cfg.CONFIG_API_KEY_DASHSCOPE,
    # dimensions=1024,
)

vec_q = embeddings.embed_query("我喜欢你")
print(f"query向量长度：{len(vec_q)}")

vec_docs = embeddings.embed_documents(["我喜欢你", "我稀饭你", "晚上吃啥"])
for idx, vec in enumerate(vec_docs):
    print(f"doc{idx}向量长度：{len(vec)}")