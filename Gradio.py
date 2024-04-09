# 导入所需的库
import gradio as gr  # 用于创建 Web 界面
import os  # 用于与操作系统交互，如读取环境变量

# 定义一个函数来根据输入生成文本
def generate(input, temperature):
    """
    该函数用于根据输入生成文本。

    参数:
    input: 输入内容。
    temperature: LLM 的温度系数。

    返回:
    output: 生成的文本。
    """
    # 使用预定义的 client 对象的 predict 方法，从输入生成文本
    # slider 的值限制生成的token的数量
    output = llm.predict(input, temperature=temperature)
    return output  # 返回生成的文本

# 创建一个 Web 界面
# 输入：一个文本框和一个滑块
# 输出：一个文本框显示生成的文本
demo = gr.Interface(
    fn=generate,
    inputs=[
        gr.Textbox(label="Prompt"),  # 文本输入框
        gr.Slider(label="Temperature", value=0,  maximum=1, minimum=0)  # 滑块用于选择模型的 temperature
    ],
    outputs=[gr.Textbox(label="Completion")],  # 显示生成文本的文本框
    title="问答助手",  # 界面标题
    description="LLM本地知识库问答助手",  # 界面描述
    # allow_flagging="never",
)

# 关闭可能已经启动的任何先前的 gradio 实例
gr.close_all()

# 启动 Web 界面
# 使用环境变量 PORT1 作为服务器的端口号
# demo.launch(share=True, server_port=int(os.environ['PORT1']))
demo.launch() # 直接启动页面