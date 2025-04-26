import streamlit as st
import random

# 初始化 session_state
if "rewritten_versions" not in st.session_state:
    st.session_state["rewritten_versions"] = []

# 页面标题
st.title("内容传播测试 + 一键AI改写（稳定版）")

# 用户输入原内容
content = st.text_area("请输入原文案内容", "例：新品巧克力上线啦，快来试吃吧！")

# 选择想要生成几版改写
n_rewrites = st.selectbox(
    "想生成几版改写？",
    options=[3, 5, 7, 10],
    index=0
)

# 黄金加分关键词列表（提升传播潜力）
power_keywords = [
    "限量", "爆款", "立即", "免费", "售罄", "倒计时",
    "排行榜", "超万人", "体验装", "官方认证", "明星代言",
    "退款保证", "超值", "必抢"
]

# 改写函数
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

# 传播潜力指数函数
def calculate_power_score(content):
    count = sum(keyword in content for keyword in power_keywords)
    max_possible = len(power_keywords)
    return int((count / max_possible) * 100)

# 按钮，点击后生成改写并保存
if st.button("一键AI改写", key="rewrite_button"):
    st.session_state["rewritten_versions"] = rewrite_content(content, n_versions=n_rewrites)

# 页面刷新后也能正确显示改写版本
if st.session_state["rewritten_versions"]:
    st.subheader(f"改写后的 {n_rewrites} 个版本：")

    # 找到最高潜力版本
    best_score = -1
    best_version = ""
    
    for idx, version in enumerate(st.session_state["rewritten_versions"], 1):
        score = calculate_power_score(version)
        st.success(f"版本 {idx}: {version}\n\n传播潜力指数：{score}/100")
        
        if score > best_score:
            best_score = score
            best_version = version

    if best_version:
        st.warning(f"⭐ 推荐最佳改写版（传播潜力最高 {best_score}/100）👇")
        st.code(best_version)

# 页脚
st.markdown("---")
st.caption("版本：最精简稳定版 ✅  |  作者：ChatGPT + 用户")
