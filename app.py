import os
from contextlib import contextmanager

import streamlit as st
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# --- ページ基本設定 ---
st.set_page_config(
    page_title="AI広報部",
    page_icon="🏠",
    layout="wide"
)

# --- prompt.py から関数を呼び出し ---
from prompt import (
    generate_instagram_post,
    generate_reel,
    generate_blog,
    generate_shooting,
    load_brand_rules,
    save_brand_rules
)

# --- カスタムCSS ---
st.markdown("""
<style>
    .stApp {
        background-color: #F8FAFC;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    }
    .custom-card {
        background-color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05), 0 2px 4px -1px rgba(0, 0, 0, 0.03);
        border: 1px solid #E2E8F0;
        margin-bottom: 20px;
    }
    .main-title {
        color: #2D3748;
        font-size: 24px;
        font-weight: 700;
        border-left: 6px solid #5EB0B1;
        padding-left: 12px;
        margin-bottom: 20px;
    }
    .sub-title {
        color: #4A5568;
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .highlight-box {
        background-color: #FFFDF0;
        border: 1px solid #FEEBC8;
        border-left: 5px solid #EEC600;
        padding: 16px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .stButton>button {
        background-color: #5EB0B1 !important;
        color: white !important;
        font-weight: 600 !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 10px 20px !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        background-color: #4A9798 !important;
        box-shadow: 0 4px 12px rgba(94, 176, 177, 0.3) !important;
    }
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

if "history" not in st.session_state:
    st.session_state.history = []


# --- 共通ヘルパー ---

@contextmanager
def card():
    """custom-card の開始/終了タグの重複を避けるためのコンテキストマネージャー。
    使い方: with card(): st.write(...)
    """
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    try:
        yield
    finally:
        st.markdown("</div>", unsafe_allow_html=True)


def g(res: dict, key: str, default=""):
    """res.get(key) の結果が None でもデフォルト値を返す安全版get。
    （キーが存在してもGeminiがnullを返すケースがあるため、通常のdict.getのdefault引数だけでは防げない）
    """
    value = res.get(key)
    return value if value is not None else default


def add_history(item_type: str, title: str, content: str):
    st.session_state.history.append({"type": item_type, "title": title, "content": content})


API_KEY_SET = bool(os.getenv("GEMINI_API_KEY"))


# --- サイドバー ---
st.sidebar.markdown("<h2 style='color: #5EB0B1; font-weight: bold;'>🏠 AI広報部</h2>", unsafe_allow_html=True)

menu = st.sidebar.radio(
    "メニューを選択",
    [
        "Instagram投稿作成",
        "リール企画",
        "ブログ作成",
        "撮影指示",
        "ブランドガイドライン",
        "投稿履歴"
    ]
)

st.sidebar.markdown("---")

# 生成系メニュー全てで共通してAPIキーが必要なため、ここで一括チェック
GENERATION_MENUS = {"Instagram投稿作成", "リール企画", "ブログ作成", "撮影指示"}
if menu in GENERATION_MENUS and not API_KEY_SET:
    st.error("⚠️ 環境変数 GEMINI_API_KEY が設定されていません。.env を確認してください。")

# --- メインコンテンツ ---

# 1. Instagram投稿作成
if menu == "Instagram投稿作成":
    st.markdown("<div class='main-title'>Instagram投稿作成</div>", unsafe_allow_html=True)

    col_input, col_result = st.columns([1, 1])

    with col_input:
        with card():
            st.markdown("<div class='sub-title'>📋 投稿条件を入力</div>", unsafe_allow_html=True)

            st.write("💡 クイックジャンル選択:")
            q_col1, q_col2, q_col3 = st.columns(3)
            if q_col1.button("🏡 完成見学会"):
                st.session_state["genre"] = "完成見学会"
            if q_col2.button("✨ 施工事例"):
                st.session_state["genre"] = "施工事例・実例紹介"
            if q_col3.button("🏗️ 構造見学会"):
                st.session_state["genre"] = "構造見学会・現場レポ"

            q_col4, q_col5, q_col6 = st.columns(3)
            if q_col4.button("📹 ルームツアー"):
                st.session_state["genre"] = "ルームツアー・Web内覧会"
            if q_col5.button("👥 スタッフ日常"):
                st.session_state["genre"] = "スタッフ・会社・現場の日常"
            if q_col6.button("💬 お客様の声"):
                st.session_state["genre"] = "オーナー様インタビュー・お客様の声"

            st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)

            genre = st.text_input("投稿ジャンル", value=st.session_state.get("genre", ""), placeholder="例: 完成見学会 / 施工事例 / 木の家")
            target = st.text_input("ターゲット", value=st.session_state.get("target", ""), placeholder="例: 自然素材の家に憧れる30代夫婦")
            purpose = st.text_input("投稿目的", value=st.session_state.get("purpose", ""), placeholder="例: 見学会予約の獲得 / ファン化")
            content = st.text_area("伝えたい内容", value=st.session_state.get("content", ""), placeholder="例: 吹抜けLDK、無垢床、造作洗面台", height=100)
            char_count = st.slider("文字数目安", min_value=200, max_value=1200, value=600, step=50)

            submit_btn = st.button("✨ 投稿案を生成する", use_container_width=True, disabled=not API_KEY_SET)

    with col_result:
        with card():
            st.markdown("<div class='sub-title'>📄 生成結果</div>", unsafe_allow_html=True)

            if submit_btn:
                if not genre or not target or not purpose or not content:
                    st.warning("すべての入力項目を入力してください。")
                else:
                    st.session_state["genre"] = genre
                    st.session_state["target"] = target
                    st.session_state["purpose"] = purpose
                    st.session_state["content"] = content

                    with st.spinner("生成中..."):
                        try:
                            res = generate_instagram_post(genre, target, purpose, content, char_count)
                            st.session_state["latest_res"] = res
                            add_history("Instagram", g(res, "title", "(無題)"), g(res, "caption"))
                        except Exception as e:
                            st.error(f"エラーが発生しました: {e}")

            if "latest_res" in st.session_state and st.session_state["latest_res"]:
                res = st.session_state["latest_res"]

                tab1, tab2, tab3 = st.tabs(["📝 キャプション・ハッシュタグ", "🖼️ カルーセル・デザイン", "💡 撮影・分析"])

                with tab1:
                    st.markdown(f"**タイトル:** {g(res, 'title')}")
                    st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
                    st.markdown(f"**キャッチコピー:**\n{g(res, 'catchphrase')}")
                    st.markdown("</div>", unsafe_allow_html=True)

                    st.write("▼ キャプション")
                    st.code(g(res, "caption"), language=None)

                    st.write("▼ ハッシュタグ")
                    st.code(g(res, "hashtags"), language=None)

                with tab2:
                    st.markdown("### 🖼️ カルーセル構成案")
                    for slide in (g(res, "carousel", []) or []):
                        st.info(slide)

                    st.markdown("### 🎨 Canvaレイアウト指示")
                    st.write(g(res, "canva_layout"))

                with tab3:
                    st.markdown("### 📷 撮影指示")
                    st.warning(g(res, "photo_instructions"))

                    st.markdown("### ⏰ 推奨投稿時間")
                    st.write(g(res, "posting_time"))

                    st.markdown("### 📈 ポイント")
                    st.success(g(res, "growth_reason"))
            else:
                st.info("左側のフォームに入力し、「投稿案を生成する」を押してください。")

# 2. リール企画
elif menu == "リール企画":
    st.markdown("<div class='main-title'>リール企画案作成</div>", unsafe_allow_html=True)

    with card():
        theme = st.text_input("動画テーマ", placeholder="例：ルームツアー、平屋のメリット3選")
        target = st.text_input("ターゲット", placeholder="例：子育て世代の夫婦")
        btn = st.button("リール企画を生成", use_container_width=True, disabled=not API_KEY_SET)

    if btn:
        if theme and target:
            with st.spinner("生成中..."):
                try:
                    res = generate_reel(theme, target)
                    with card():
                        st.markdown(f"### 🪝 フック（冒頭3秒）\n**{g(res, 'hook')}**")
                        st.markdown("### 🎬 構成・テロップ案")
                        st.code(g(res, "script"), language=None)
                        st.markdown(f"### 🎵 BGMイメージ\n{g(res, 'music')}")
                    add_history("リール", theme, f"フック: {g(res, 'hook')}\n\n構成:\n{g(res, 'script')}")
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("動画テーマとターゲットを入力してください。")

# 3. ブログ作成
elif menu == "ブログ作成":
    st.markdown("<div class='main-title'>ブログ・Web記事作成</div>", unsafe_allow_html=True)

    with card():
        title_kw = st.text_input("キーワード / テーマ", placeholder="例：注文住宅 高気密高断熱")
        target = st.text_input("想定読者", placeholder="例：冬暖かい家を建てたいファミリー")
        btn = st.button("ブログ記事を生成", use_container_width=True, disabled=not API_KEY_SET)

    if btn:
        if title_kw and target:
            with st.spinner("生成中..."):
                try:
                    res = generate_blog(title_kw, target)
                    with card():
                        st.markdown("### 📄 生成されたブログ文章")
                        st.code(res, language=None)
                    add_history("ブログ", title_kw, res)
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("キーワードと想定読者を入力してください。")

# 4. 撮影指示
elif menu == "撮影指示":
    st.markdown("<div class='main-title'>現場・物件 撮影指示書作成</div>", unsafe_allow_html=True)

    with card():
        house_type = st.text_input("物件特徴", placeholder="例：開放感のある吹抜けリビングと平屋風動線")
        highlights = st.text_area("特に見せたいポイント", placeholder="例：造作キッチン、無垢材の床、玄関手洗い")
        btn = st.button("撮影指示書を生成", use_container_width=True, disabled=not API_KEY_SET)

    if btn:
        if house_type and highlights:
            with st.spinner("生成中..."):
                try:
                    res = generate_shooting(house_type, highlights)
                    with card():
                        st.markdown("### 📷 撮影カットリスト")
                        st.code(res, language=None)
                    add_history("撮影指示", house_type, res)
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("物件特徴と見せたいポイントを入力してください。")

# 5. ブランドガイドライン
elif menu == "ブランドガイドライン":
    st.markdown("<div class='main-title'>ブランドガイドライン管理</div>", unsafe_allow_html=True)

    with card():
        current_rule = load_brand_rules()
        new_rule = st.text_area("brand/brand_rule.txt の内容", current_rule, height=350)
        if st.button("ガイドラインを更新・保存", use_container_width=True):
            try:
                save_brand_rules(new_rule)
                st.success("ガイドラインを保存しました！")
            except Exception as e:
                st.error(f"保存に失敗しました: {e}")

# 6. 投稿履歴
elif menu == "投稿履歴":
    st.markdown("<div class='main-title'>投稿履歴</div>", unsafe_allow_html=True)

    if not st.session_state.history:
        st.info("まだ生成履歴はありません。")
    else:
        if st.button("履歴をすべてクリア"):
            st.session_state.history = []
            st.rerun()

        for item in reversed(st.session_state.history):
            with card():
                st.markdown(f"**【{item['type']}】 {item['title']}**")
                st.code(item["content"], language=None)
