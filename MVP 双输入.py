import streamlit as st
import random

# 初始化 session_state
if "rewritten_a" not in st.session_state:
    st.session_state["rewritten_a"] = []
if "rewritten_b" not in st.session_state:
    st.session_state["rewritten_b"] = []

# 页面标题
st.title("内容传播测试 + A/B对比 + AI改写（最终极版）")

# 输入内容
st.header("请输入你的两个内容版本")
content_a = st.text_area("内容 A", "例：新品巧克力上线啦，快来试吃吧！")
content_b = st.text_area("内容 B", "例：首发限量版，错过不再有！")

# 用户选择想要生成几个改写版本
n_rewrites = st.selectbox(
    "想生成几个改写版本？",
    options=[3, 5, 7, 10],
    index=0
)

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

# 传播得分
def calculate_score(likes, comments, shares):
    score = (likes * 1 + comments * 2 + shares * 3) / 10
    return min(100, round(score))

# 传播潜力指数
def calculate_power_score(content):
    count = sum(keyword in content for keyword in power_keywords)
    max_possible = len(power_keywords)
    return int((count / max_possible) * 100)

# 简单改写函数（多版本）
def rewrite_content(content, n_versions=3):
    extra_phrases = [
        "马上抢购！", "99%用户推荐！", "限时特惠！", "不可错过的体验！",
        "爆款来袭！", "售罄倒计时！", "官方正品！", "立即拥有！"
    ]
    rewrites = []
    for _ in range(n_versions):
        if not content:
            rewrites.append("")
        else:
            words = content.split()
            insert_position = random.randint(0, len(words) - 1)
            words.insert(insert_position, random.choice(extra_phrases))
            rewritten = " ".join(words)
            rewrites.append(rewritten)
    return rewrites

# 测试按钮
if st.button("开始测试", key="start_test"):
    if content_a.strip() == "" or content_b.strip() == "":
        st.warning("请填写完整两个内容版本！")
    else:
        likes_a, comments_a, shares_a = simulate_reactions(content_a)
        likes_b, comments_b, shares_b = simulate_reactions(content_b)

        score_a = calculate_score(likes_a, comments_a, shares_a)
        score_b = calculate_score(likes_b, comments_b, shares_b)

        power_score_a = calculate_power_score(content_a)
        power_score_b = calculate_power_score(content_b)

        st.subheader("原始内容测试结果")
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 内容 A 测试")
            st.write(f"点赞数：{likes_a}")
            st.write(f"评论数：{comments_a}")
            st.write(f"分享数：{shares_a}")
            st.write(f"传播得分：{score_a}/100")
            st.write(f"传播潜力指数：{power_score_a}/100")

        with col2:
            st.markdown("### 内容 B 测试")
            st.write(f"点赞数：{likes_b}")
            st.write(f"评论数：{comments_b}")
            st.write(f"分享数：{shares_b}")
            st.write(f"传播得分：{score_b}/100")
            st.write(f"传播潜力指数：{power_score_b}/100")

        # 综合推荐
        if score_a > score_b:
            st.success("✅ 推荐使用 内容 A！")
        elif score_b > score_a:
            st.success("✅ 推荐使用 内容 B！")
        else:
            st.success("✅ 内容 A 和 B 得分相同，均可使用。")

# 改写按钮和改写展示
st.markdown("---")
st.subheader("一键AI改写（提高传播潜力）")

col1, col2 = st.columns(2)

with col1:
    if st.button(f"一键改写内容 A (生成{n_rewrites}版)", key="rewrite_a"):
        st.session_state["rewritten_a"] = rewrite_content(content_a, n_versions=n_rewrites)

    if st.session_state["rewritten_a"]:
        st.info(f"改写后的内容 A（共{n_rewrites}版）：")
        best_score_a = -1
        best_version_a = ""
        for idx, version in enumerate(st.session_state["rewritten_a"], 1):
            score = calculate_power_score(version)
            st.success(f"版本 {idx}: {version}\n\n传播潜力指数：{score}/100")
            if score > best_score_a:
                best_score_a = score
                best_version_a = version
        if best_version_a:
            st.warning(f"⭐ 推荐最佳改写版 A（传播潜力最高 {best_score_a}/100）👇")
            st.code(best_version_a)

with col2:
    if st.button(f"一键改写内容 B (生成{n_rewrites}版)", key="rewrite_b"):
        st.session_state["rewritten_b"] = rewrite_content(content_b, n_versions=n_rewrites)

    if st.session_state["rewritten_b"]:
        st.info(f"改写后的内容 B（共{n_rewrites}版）：")
        best_score_b = -1
        best_version_b = ""
        for idx, version in enumerate(st.session_state["rewritten_b"], 1):
            score = calculate_power_score(version)
            st.success(f"版本 {idx}: {version}\n\n传播潜力指数：{score}/100")
            if score > best_score_b:
                best_score_b = score
                best_version_b = version
        if best_version_b:
            st.warning(f"⭐ 推荐最佳改写版 B（传播潜力最高 {best_score_b}/100）👇")
            st.code(best_version_b)

# 页脚
st.markdown("---")
st.caption("版本：MVP 双输入对比最终极版 🚀 | 功能：传播模拟 + AI改写 + 潜力分析 + 智能推荐")
