import streamlit as st
import json
import os
from prompt import (
    generate_post, 
    generate_reel, 
    generate_blog, 
    generate_shooting, 
    load_brand_rule, 
    save_brand_rule
)

st.set_page_config(page_title="中美建設 AI広報部", layout="wide")

# カスタムCSS（カードデザイン、タグ風表示、レイアウト調整）
st.markdown("""
<style>
    .main { background-color: #f8f9fa; }
    div[data-testid="stSidebar"] { background-color: #ffffff; border-right: 1px solid #e9ecef; }
    .header-title { font-size: 24px; font-weight: bold; color: #17a2b8; margin-bottom: 5px; }
    .card-box { background-color: #ffffff; border-radius: 12px; padding: 24px; border: 1px solid #e9ecef; box-shadow: 0 2px 4px rgba(0,0,0,0.02); margin-bottom: 20px; }
    .hashtag-chip { background-color: #e6f7f7; color: #17a2b8; padding: 6px 14px; border-radius: 20px; font-size: 14px; font-weight: 500; display: inline-block; margin-right: 6px; margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

# 履歴データの初期化
if "history" not in st.session_state:
    st.session_state.history = []

# --- サイドバー ---
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
st.sidebar.caption("© 中美建設")

# --- 1. Instagram投稿作成 ---
if page == "📷 Instagram投稿作成":
    st.markdown("<div class='header-title'>📷 Instagram投稿作成</div>", unsafe_allow_html=True)
    st.caption("ターゲットと目的に合わせたInstagramの投稿内容、キャプション、ハッシュタグを自動生成します。")

    with st.form("input_form"):
        st.markdown("#### │ 投稿条件入力")
        genre = st.text_input("投稿ジャンル", placeholder="例：施工事例・新築・リフォーム")
        target = st.text_input("ターゲット", placeholder="例：家を建てたい30代夫婦")
        purpose = st.text_input("投稿目的", placeholder="例：信頼感の醸成・フォロワー獲得")
        details = st.text_area("伝えたい内容", placeholder="例：木の温もりある家づくり、職人の技術について", height=100)
        submitted = st.form_submit_button("投稿文を生成する", use_container_width=True)

    if submitted:
        if not genre or not details:
            st.warning("「投稿ジャンル」と「伝えたい内容」を入力してください。")
        else:
            with st.spinner("投稿案を作成中..."):
                try:
                    data = generate_post(genre, target, purpose, details)
                    st.success("作成が完了しました！")
                    
                    st.markdown("### 📝 キャプション文章")
                    st.text_area("コピーして使用できます", value=data.get("caption", ""), height=200)
                    
                    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
                    st.markdown("### 🏷️ ハッシュタグ")
                    hashtags = data.get("hashtags", [])
                    tags_html = "".join([f"<span class='hashtag-chip'>{tag}</span>" for tag in hashtags])
                    st.markdown(f"<div>{tags_html}</div>", unsafe_allow_html=True)
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
                    st.markdown("### 🕒 推奨投稿時間")
                    st.write(data.get("best_time", ""))
                    st.markdown("</div>", unsafe_allow_html=True)

                    # 履歴保存
                    st.session_state.history.append({"type": "Instagram", "title": genre, "content": data.get("caption", "")})
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

# --- 2. リール企画 ---
elif page == "🎬 リール企画":
    st.markdown("<div class='header-title'>🎬 リール企画案作成</div>", unsafe_allow_html=True)
    st.caption("短尺動画（Reels）のフック、構成案、テロップ、音源イメージを自動生成します。")

    with st.form("reel_form"):
        st.markdown("#### │ リール企画入力")
        theme = st.text_input("動画テーマ", placeholder="例：ルームツアー、失敗しない間取りの選び方")
        target = st.text_input("ターゲット", placeholder="例：子育て世代の夫婦")
        submitted = st.form_submit_button("リール企画を生成する", use_container_width=True)

    if submitted:
        if not theme:
            st.warning("「動画テーマ」を入力してください。")
        else:
            with st.spinner("リール企画を作成中..."):
                try:
                    res = generate_reel(theme, target)
                    st.success("作成が完了しました！")
                    
                    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
                    st.markdown("### 🪝 フック（最初の3秒）")
                    st.write(res.get("hook", ""))
                    st.markdown("</div>", unsafe_allow_html=True)
                    
                    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
                    st.markdown("### 🎬 動画構成案 & テロップ")
                    st.text_area("構成案", value=res.get("script", ""), height=200)
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.markdown("<div class='card-box'>", unsafe_allow_html=True)
                    st.markdown("### 🎵 推奨BGM / 音源イメージ")
                    st.write(res.get("music", ""))
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.session_state.history.append({"type": "リール企画", "title": theme, "content": res.get("script", "")})
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

# --- 3. ブログ作成 ---
elif page == "✍️ ブログ作成":
    st.markdown("<div class='header-title'>✍️ ブログ・Web記事作成</div>", unsafe_allow_html=True)
    st.caption("SEOを意識したブログ記事のタイトル、見出し構成、本文を生成します。")

    with st.form("blog_form"):
        st.markdown("#### │ ブログ条件入力")
        title_keyword = st.text_input("キーワード / テーマ", placeholder="例：注文住宅 高気密高断熱 三重県")
        target = st.text_input("想定読者", placeholder="例：冬暖かい家を建てたいファミリー")
        submitted = st.form_submit_button("ブログ記事を生成する", use_container_width=True)

    if submitted:
        if not title_keyword:
            st.warning("「キーワード / テーマ」を入力してください。")
        else:
            with st.spinner("ブログ記事を生成中..."):
                try:
                    res = generate_blog(title_keyword, target)
                    st.success("作成が完了しました！")
                    
                    st.markdown("### 📰 生成されたブログ記事")
                    st.text_area("本文（Markdown形式）", value=res, height=350)
                    
                    st.session_state.history.append({"type": "ブログ", "title": title_keyword, "content": res})
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

# --- 4. 撮影指示 ---
elif page == "📸 撮影指示":
    st.markdown("<div class='header-title'>📸 現場・物件 撮影指示書作成</div>", unsafe_allow_html=True)
    st.caption("ルームツアーや施工事例撮影の際に撮影スタッフへ渡す撮影カットリストを作成します。")

    with st.form("shooting_form"):
        st.markdown("#### │ 物件情報入力")
        house_type = st.text_input("物件特徴", placeholder="例：開放感のある吹抜けリビングと平屋風動線")
        highlights = st.text_area("特に見せたいポイント", placeholder="例：造作キッチン、無垢材の床、玄関手洗い")
        submitted = st.form_submit_button("撮影指示書を生成する", use_container_width=True)

    if submitted:
        if not house_type:
            st.warning("「物件特徴」を入力してください。")
        else:
            with st.spinner("撮影指示書を作成中..."):
                try:
                    res = generate_shooting(house_type, highlights)
                    st.success("作成が完了しました！")
                    
                    st.markdown("### 📋 撮影カットリスト・指示内容")
                    st.text_area("指示書テキスト", value=res, height=300)

                    st.session_state.history.append({"type": "撮影指示", "title": house_type, "content": res})
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")

# --- 5. ブランドガイドライン ---
elif page == "🎨 ブランドガイドライン":
    st.markdown("<div class='header-title'>🎨 ブランドガイドライン設定</div>", unsafe_allow_html=True)
    st.caption("AIが文章生成の際に参照する中美建設の強みや文章トーン＆マナーを設定・保存できます。")

    current_rule = load_brand_rule()
    
    with st.form("brand_form"):
        st.markdown("#### │ ブランドルールの編集")
        new_rule = st.text_area("ルール内容（brand_rule.txt）", value=current_rule, height=300)
        saved = st.form_submit_button("ガイドラインを保存する", use_container_width=True)

    if saved:
        save_brand_rule(new_rule)
        st.success("ブランドガイドラインを保存しました！今後の生成に反映されます。")

# --- 6. 投稿履歴 ---
elif page == "📜 投稿履歴":
    st.markdown("<div class='header-title'>📜 投稿履歴</div>", unsafe_allow_html=True)
    st.caption("このセッションで作成された各種コンテンツの履歴一覧です。")

    if not st.session_state.history:
        st.info("まだ作成されたコンテンツの履歴はありません。")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"【{item['type']}】 {item['title']}"):
                st.text_area(f"内容-{idx}", value=item["content"], height=150)
