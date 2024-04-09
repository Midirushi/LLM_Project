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
    title="Chat Robot",  # 界面标题
    description="Local Knowledge Base Q&A with llm",  # 界面描述
    # allow_flagging="never",
)

# 关闭可能已经启动的任何先前的 gradio 实例
gr.close_all()

# 启动 Web 界面
# 使用环境变量 PORT1 作为服务器的端口号
# demo.launch(share=True, server_port=int(os.environ['PORT1']))
demo.launch() # 直接启动页面


# 定义一个函数，用于格式化聊天 prompt。
def format_chat_prompt(message, chat_history):
    """
    该函数用于格式化聊天 prompt。

    参数:
    message: 当前的用户消息。
    chat_history: 聊天历史记录。

    返回:
    prompt: 格式化后的 prompt。
    """
    # 初始化一个空字符串，用于存放格式化后的聊天 prompt。
    prompt = ""
    # 遍历聊天历史记录。
    for turn in chat_history:
        # 从聊天记录中提取用户和机器人的消息。
        user_message, bot_message = turn
        # 更新 prompt，加入用户和机器人的消息。
        prompt = f"{prompt}\nUser: {user_message}\nAssistant: {bot_message}"
    # 将当前的用户消息也加入到 prompt中，并预留一个位置给机器人的回复。
    prompt = f"{prompt}\nUser: {message}\nAssistant:"
    # 返回格式化后的 prompt。
    return prompt

# 定义一个函数，用于生成机器人的回复。
def respond(message, chat_history):
    """
    该函数用于生成机器人的回复。

    参数:
    message: 当前的用户消息。
    chat_history: 聊天历史记录。

    返回:
    "": 空字符串表示没有内容需要显示在界面上，可以替换为真正的机器人回复。
    chat_history: 更新后的聊天历史记录
    """
    # 调用上面的函数，将用户的消息和聊天历史记录格式化为一个 prompt。
    formatted_prompt = format_chat_prompt(message, chat_history)
    # 使用llm对象的predict方法生成机器人的回复（注意：llm对象在此代码中并未定义）。
    bot_message = llm.predict(formatted_prompt,
                                max_new_tokens=1024,
                                stop_sequences=["\nUser:", ""])
    # 将用户的消息和机器人的回复加入到聊天历史记录中。
    chat_history.append((message, bot_message))
    # 返回一个空字符串和更新后的聊天历史记录（这里的空字符串可以替换为真正的机器人回复，如果需要显示在界面上）。
    return "", chat_history

# 下面的代码是设置Gradio界面的部分。

# 使用Gradio的Blocks功能定义一个代码块。
with gr.Blocks() as demo:
    # 创建一个Gradio聊天机器人组件，设置其高度为240。
    chatbot = gr.Chatbot(height=240)
    # 创建一个文本框组件，用于输入  prompt。
    msg = gr.Textbox(label="Prompt")
    # 创建一个提交按钮。
    btn = gr.Button("Submit")
    # 创建一个清除按钮，用于清除文本框和聊天机器人组件的内容。
    clear = gr.ClearButton(components=[msg, chatbot], value="Clear console")

    # 设置按钮的点击事件。当点击时，调用上面定义的respond函数，并传入用户的消息和聊天历史记录，然后更新文本框和聊天机器人组件。
    btn.click(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])
    # 设置文本框的提交事件（即按下Enter键时）。功能与上面的按钮点击事件相同。
    msg.submit(respond, inputs=[msg, chatbot], outputs=[msg, chatbot])

# 关闭所有已经存在的 Gradio 实例。
gr.close_all()
# 启动新的 Gradio 应用，设置分享功能为 True，并使用环境变量 PORT1 指定服务器端口。
# demo.launch(share=True, server_port=int(os.environ['PORT1']))
demo.launch()
