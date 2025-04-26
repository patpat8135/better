import streamlit as st
import random
import datetime

# 初始化 session_state 保存改写后的内容
if "rewritten_a" not in st.session_state:
    st.session_state["rewritten_a"] = []
if "rewritten_b" not in st.session_state:
    st.session_state["rewritten_b"] = []

# 页面标题
st.title("内容传播效果预测工具 (完整版 CrowdTest)")

# 输入两个内容
st.header("输入你的两个内容版本")
content_a = st.text_area("内容 A", "请输入第一个内容...")
content_b = st.text_area("内容 B", "请输入第二个内容...")

# 黄金加分关键词列表
power_keywords = [
    "限量", "爆款", "立即", "免费", "售罄", "倒计时", "排行榜",
    "超万人", "体验装", "官方认证", "明星代言", "退款保证", "超值", "必抢"
]

# 模拟用户反应
def simulate_reactions(content):
    base = random.randint(400, 600)
    boost = 0
    if any(keyword in content for keyword in power_keywords):
        boost += random.randint(100, 300)
    likes = base + boost
    comments = int(likes * random.uniform(0.05, 0.2))
    shares = int(likes * random.uniform(0.03, 0.1))
    return likes, comments, shares

# 计算传播得分
def calculate_score(likes, comments, shares):
    score = (likes * 1 + comments * 2 + shares * 3) / 10
    return min(100, round(score))

# 计算文案传播潜力指数
def calculate_power_score(content):
    count = sum(keyword in content for keyword in power_keywords)
    max_possible = len(power_keywords)
    score = int((count / max_possible) * 100)
    return score

# 简单改写内容函数（支持多版本）
def rewrite_content(content, n_versions=3):
    extra_phrases = [
        "马上抢购！", "99%用户推荐！", "限时特惠！", "不可错过的体验！",
        "爆款来袭！", "售罄倒计时！", "官方正品！", "立即拥有！"
    ]
    rewrites = []
    for _ in range(n_versions):
        if not content:
            rewrites.append("")
            continue
        rewritten = content
        if len(content) < 80:
            rewritten += " " + random.choice(extra_phrases)
        else:
            words = content.split()
            insert_position = random.randint(0, len(words) - 1)
            words.insert(insert_position, random.choice(extra_phrases))
            rewritten = " ".join(words)
        rewrites.append(rewritten)
    return rewrites

# 开始测试
if st.button("开始测试"):
    if content_a.strip() == "" or content_b.strip() == "":
        st.warning("请先填写完整两个内容版本！")
    else:
        likes_a, comments_a, shares_a = simulate_reactions(content_a)
        likes_b, comments_b, shares_b = simulate_reactions(content_b)

        score_a = calculate_score(likes_a, comments_a, shares_a)
        score_b = calculate_score(likes_b, comments_b, shares_b)

        power_score_a = calculate_power_score(content_a)
        power_score_b = calculate_power_score(content_b)

        st.subheader("测试结果")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 内容 A")
            st.write(f"点赞数：{likes_a}")
            st.write(f"评论数：{comments_a}")
            st.write(f"分享数：{shares_a}")
            st.write(f"传播得分：{score_a}/100")
            st.write(f"传播潜力指数：{power_score_a}/100")

            if st.button("一键改写内容 A (生成3版)"):
                st.session_state["rewritten_a"] = rewrite_content(content_a)

            if st.session_state["rewritten_a"]:
                st.info("改写后的内容 A：")
                for idx, version in enumerate(st.session_state["rewritten_a"], 1):
                    st.success(f"版本 {idx}: {version}")

        with col2:
            st.markdown("### 内容 B")
            st.write(f"点赞数：{likes_b}")
            st.write(f"评论数：{comments_b}")
            st.write(f"分享数：{shares_b}")
            st.write(f"传播得分：{score_b}/100")
            st.write(f"传播潜力指数：{power_score_b}/100")

            if st.button("一键改写内容 B (生成3版)"):
                st.session_state["rewritten_b"] = rewrite_content(content_b)

            if st.session_state["rewritten_b"]:
                st.info("改写后的内容 B：")
                for idx, version in enumerate(st.session_state["rewritten_b"], 1):
                    st.success(f"版本 {idx}: {version}")

        # 推荐
        if score_a > score_b:
            st.success("推荐使用 内容 A！")
        elif score_b > score_a:
            st.success("推荐使用 内容 B！")
        else:
            st.success("两个内容得分相同，均可使用。")

# 页脚
st.markdown("---")
st.caption("版本：MVP 超级完整版 🚀 | 功能：传播模拟 + AI改写 + 潜力分析")
