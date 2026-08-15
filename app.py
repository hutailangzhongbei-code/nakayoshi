import streamlit as st
import json
from prompt import generate_post

st.set_page_config(page_title="中美建設 AI広報部", layout="wide")

# CSSでReplitのサイドバーとヘッダー風デザインを再現
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    div[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e9ecef;
    }
    .header-title {
        font-size: 24px;
        font-weight: bold;
        color: #17a2b8;
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 5px;
    }
    .card-box {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 24px;
        border: 1px solid #e9ecef;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        margin-bottom: 20px;
    }
    .hashtag-chip {
        background-color: #e6f7f7;
        color: #17a2b8;
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 14px;
        font-weight: 500;
        display: inline-block;
        margin-right: 6px;
        margin-bottom: 8px;
    }
</style>
""", unsafe_allow_html=True)

# --- サイドバーメニュー ---
st.sidebar.markdown("### 🏠 中美建設 AI広報部")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "メニューを選択",
    [
        "📷 Instagram投稿作成",
        "🎬 リール企画",
        "✍️ ブログ作成",
        "📸 撮影指示",
        "🎨 ブランドガイドライン",
        "📜 投稿履歴"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("© Nakabi Construction")

# --- メインコンテンツ領域 ---

if page == "📷 Instagram投稿作成":
    st.markdown("<div class='header-title'>📷 Instagram投稿作成</div>", unsafe_allow_html=True)
    st.caption("ターゲットと目的に合わせたInstagramの投稿内容、キャプション、ハッシュタグを自動生成します。")
    st.write("")

    with st.form("input_form"):
        st.markdown("#### │ 投稿条件入力")
        
        genre = st.text_input("投稿ジャンル", placeholder="例：施工事例・新築・リフォーム")
        target = st.text_input("ターゲット", placeholder="例：家を建てたい30代夫婦")
        purpose = st.text_input("投稿目的", placeholder="例：信頼感の醸成・フォロワー獲得")
        details = st.text_area("伝えたい内容", placeholder="例：木の温もりある家づくり、職人の技術について", height=120)
        
        submitted = st.form_submit_button("投稿文を生成する", use_container_width=True)

    if submitted:
        if not genre or not details:
            st.warning("「投稿ジャンル」と「伝えたい内容」を入力してください。")
        else:
            with st.spinner("投稿案を作成中..."):
                try:
                    data = generate_post(genre, target, purpose, details)
                    st.success("作成が完了しました！")
                    
                    # 1. キャプション
                    st.markdown("### 📝 キャプション文章")
                    st.text_area("コピーして使用できます", value=data.get("caption", ""), height=250)
                    
                    # 2. ハッシュタグ（チップデザイン）
                    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
                    st.markdown("### 🏷️ ハッシュタグ")
                    hashtags = data.get("hashtags", [])
                    tags_html = "".join([f"<span class='hashtag-chip'>{tag}</span>" for tag in hashtags])
                    st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    # 3. 推奨投稿時間
                    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
                    st.markdown("### 🕒 推奨投稿時間")
                    st.write(data.get("best_time", ""))
                    st.markdown("</div>", unsafe_allow_html=True)

                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

else:
    # 準備中のページ表示
    st.markdown(f"<div class='header-title'>{page}</div>", unsafe_allow_html=True)
    st.info("この機能は現在準備中です。順次追加していきます！")
