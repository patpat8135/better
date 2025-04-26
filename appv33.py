import streamlit as st
import openai
import pandas as pd
import datetime

# OpenAI API key设置（你需要替换成自己的）
openai.api_key = '你的OpenAI_API_KEY'

def simulate_reactions(content_a, content_b):
    prompt = f"""
你是一个社交媒体用户模拟器。请根据以下文案预测其社交媒体表现，包括点赞数、评论数和分享数。
内容A：{content_a}
内容B：{content_b}
请输出：
内容A - 点赞：xxx 评论：xxx 分享：xxx
内容B - 点赞：xxx 评论：xxx 分享：xxx
然后推荐哪个版本表现更好，并给出优化建议。
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    return response['choices'][0]['message']['content']

# 保存历史记录
@st.cache_data
def save_record(record):
    try:
        history = pd.read_csv("history.csv")
    except FileNotFoundError:
        history = pd.DataFrame(columns=["时间", "内容A", "内容B", "结果"])
    history = pd.concat([history, pd.DataFrame([record])], ignore_index=True)
    history.to_csv("history.csv", index=False)

# Streamlit界面
st.title("CrowdTest 简化版内容测试工具")
st.write("请输入要测试的两个内容版本：")

content_a = st.text_area("内容 A", height=150)
content_b = st.text_area("内容 B", height=150)

if st.button("提交测试"):
    if not content_a or not content_b:
        st.error("请输入两个内容！")
    else:
        with st.spinner("AI模拟中，请稍候..."):
            result = simulate_reactions(content_a, content_b)
        st.success("模拟完成！")
        st.write("### 测试结果：")
        st.text(result)

        record = {
            "时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "内容A": content_a,
            "内容B": content_b,
            "结果": result
        }
        save_record(record)

# 查看历史记录
if st.checkbox("查看历史测试记录"):
    try:
        history = pd.read_csv("history.csv")
        st.dataframe(history)
    except FileNotFoundError:
        st.info("暂无历史记录。")
