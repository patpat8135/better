import streamlit as st
import random
import datetime

# 页面标题
st.title("内容传播效果预测工具 (简版 CrowdTest)")

# 模拟用户反应函数
def simulate_reactions(content):
    base = random.randint(400, 600)
    boost = 0
    if any(keyword in content for keyword in ["限量", "爆款", "立即", "免费"]):
        boost += random.randint(100, 300)
    if any(number in content for number in ["90%", "99%", "100%"]):
        boost += random.randint(50, 150)
    likes = base + boost
    comments = int(likes * random.uniform(0.05, 0.2))
    shares = int(likes * random.uniform(0.03, 0.1))
    return likes, comments, shares

# 优化建议函数
def generate_optimization_suggestions(content):
    suggestions = []
    if not any(word in content for word in ["立即", "限时", "马上", "现在"]):
        suggestions.append("增加紧迫感词汇，例如 '立即'、'限时'。")
    if not any(percent in content for percent in ["90%", "99%", "100%"]):
        suggestions.append("添加具体数字或百分比提升说服力。")
    if len(content) < 50:
        suggestions.append("内容偏短，可增加更多细节或情绪词。")
    return suggestions

# 传播得分计算函数
def calculate_score(likes, comments, shares):
    score = (likes * 1 + comments * 2 + shares * 3) / 10
    return min(100, round(score))

# 简易AI改写内容函数
def rewrite_content(content):
    extra_phrases = ["马上抢购！", "99%用户推荐！", "限时特惠！", "不可错过的体验！"]
    if not content:
        return ""
    rewritten = content
    if len(content) < 80:
        rewritten += " " + random.choice(extra_phrases)
    else:
        words = content.split()
        insert_position = random.randint(0, len(words) - 1)
        words.insert(insert_position, random.choice(extra_phrases))
        rewritten = " ".join(words)
    return rewritten

# 测试记录列表
if "history" not in st.session_state:
    st.session_state.history = []

# 选择模式
mode = st.radio("选择测试模式", ["单个对比测试", "批量测试"])

if mode == "单个对比测试":
    st.header("输入你的两个内容版本")
    content_a = st.text_area("内容 A", "请输入第一个内容...")
    content_b = st.text_area("内容 B", "请输入第二个内容...")

    if st.button("开始测试"):
        if content_a.strip() == "" or content_b.strip() == "":
            st.warning("请先填写完整两个内容版本！")
        else:
            likes_a, comments_a, shares_a = simulate_reactions(content_a)
            likes_b, comments_b, shares_b = simulate_reactions(content_b)

            score_a = calculate_score(likes_a, comments_a, shares_a)
            score_b = calculate_score(likes_b, comments_b, shares_b)

            st.subheader("测试结果")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("### 内容 A")
                st.write(f"点赞数：{likes_a}")
                st.write(f"评论数：{comments_a}")
                st.write(f"分享数：{shares_a}")
                st.write(f"传播得分：{score_a}/100")
                suggestions_a = generate_optimization_suggestions(content_a)
                if suggestions_a:
                    st.info("优化建议：" + " ".join(suggestions_a))
                if st.button("一键改写内容 A"):
                    st.write(rewrite_content(content_a))
            with col2:
                st.markdown("### 内容 B")
                st.write(f"点赞数：{likes_b}")
                st.write(f"评论数：{comments_b}")
                st.write(f"分享数：{shares_b}")
                st.write(f"传播得分：{score_b}/100")
                suggestions_b = generate_optimization_suggestions(content_b)
                if suggestions_b:
                    st.info("优化建议：" + " ".join(suggestions_b))
                if st.button("一键改写内容 B"):
                    st.write(rewrite_content(content_b))

            if score_a > score_b:
                recommendation = "推荐使用 内容 A！"
            elif score_b > score_a:
                recommendation = "推荐使用 内容 B！"
            else:
                recommendation = "内容 A 和 内容 B 得分相同，均可使用。"

            st.success(recommendation)

            st.session_state.history.append({
                "时间": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "内容 A": content_a,
                "内容 B": content_b,
                "结果": recommendation
            })

elif mode == "批量测试":
    st.header("批量输入内容，每行一个版本（最多10个）")
    batch_input = st.text_area("批量内容输入", "请输入每行一个不同内容...")

    if st.button("开始批量测试"):
        contents = batch_input.strip().split("\n")
        if len(contents) < 2:
            st.warning("请至少输入两个内容进行比较！")
        else:
            st.subheader("批量测试结果")
            scores = []
            for idx, content in enumerate(contents):
                likes, comments, shares = simulate_reactions(content)
                score = calculate_score(likes, comments, shares)
                scores.append((idx+1, content, score))

            scores = sorted(scores, key=lambda x: x[2], reverse=True)

            for rank, (idx, content, score) in enumerate(scores, start=1):
                st.markdown(f"**第{rank}名：内容{idx}**")
                st.write(f"内容：{content}")
                st.write(f"传播得分：{score}/100")
                st.markdown("---")

# 显示测试记录
if st.session_state.history:
    st.markdown("---")
    st.header("历史测试记录")
    for record in st.session_state.history:
        st.write(record)

st.markdown("---")
st.caption("版本：MVP 0.5 | 作者：ChatGPT + 用户 | 功能：内容预测、优化建议、测试记录保存、传播得分系统、一键改写、批量测试")