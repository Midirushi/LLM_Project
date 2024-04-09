# 使用前配置自己的 api 到环境变量中如
import os
import openai
import zhipuai
import sys
sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv()) # read local .env fileopenai.api_key  = os.environ['OPENAI_API_KEY']
openai.api_key  = os.environ['OPENAI_API_KEY']
zhipuai.api_key = os.environ['ZHIPUAI_API_KEY']
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from zhipuai_embedding import ZhipuAIEmbeddings

# embedding = OpenAIEmbeddings()
# embedding = HuggingFaceEmbeddings(model_name="moka-ai/m3e-base")
embedding = ZhipuAIEmbeddings()

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
query1 = "机器学习"
query2 = "强化学习"
query3 = "大语言模型"

# 通过对应的 embedding 类生成 query 的 embedding。
emb1 = embedding.embed_query(query1)
emb2 = embedding.embed_query(query2)
emb3 = embedding.embed_query(query3)

# 将返回结果转成 numpy 的格式，便于后续计算
emb1 = np.array(emb1)
emb2 = np.array(emb2)
emb3 = np.array(emb3)
print(f"{query1} 生成的为长度 {len(emb1)} 的 embedding , 其前 30 个值为： {emb1[:30]}")

print(f"{query1} 和 {query2} 向量之间的点积为：{np.dot(emb1, emb2)}")
print(f"{query1} 和 {query3} 向量之间的点积为：{np.dot(emb1, emb3)}")
print(f"{query2} 和 {query3} 向量之间的点积为：{np.dot(emb2, emb3)}")

print(f"{query1} 和 {query2} 向量之间的余弦相似度为：{cosine_similarity(emb1.reshape(1, -1) , emb2.reshape(1, -1) )}")
print(f"{query1} 和 {query3} 向量之间的余弦相似度为：{cosine_similarity(emb1.reshape(1, -1) , emb3.reshape(1, -1) )}")
print(f"{query2} 和 {query3} 向量之间的余弦相似度为：{cosine_similarity(emb2.reshape(1, -1) , emb3.reshape(1, -1) )}")

