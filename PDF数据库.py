import langchain
from langchain.document_loaders import PyMuPDFLoader
from langchain.document_loaders import UnstructuredMarkdownLoader



# 创建一个 PyMuPDFLoader Class 实例，输入为待加载的 pdf 文档路径
loader = PyMuPDFLoader("C:\\Users\YQ\Desktop\测试用.pdf")

# 调用 PyMuPDFLoader Class 的函数 load 对 pdf 文件进行加载
pages = loader.load()
print(f"载入后的变量类型为：{type(pages)}，",  f"该 PDF 一共包含 {len(pages)} 页")
page = pages[0]
print(f"每一个元素的类型：{type(page)}.",
    f"该文档的描述性数据：{page.metadata}",
    f"查看该文档的内容:\n{page.page_content[0:1000]}",
    sep="\n------\n")


