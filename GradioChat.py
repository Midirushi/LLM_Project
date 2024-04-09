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