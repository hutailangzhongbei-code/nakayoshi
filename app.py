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
# デザインコンセプト：住宅の「設計図(ブループリント)」×「無垢材」
# 色: 図面紙の白 / ブループリント紺(見出し・構造) / 木の色(アクセント・CTA)
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Zen+Old+Mincho:wght@600;700&family=Zen+Kaku+Gothic+New:wght@400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
    :root {
        --bg: #F4F5F0;
        --surface: #FFFFFF;
        --ink: #202A22;
        --ink-soft: #667066;
        --blueprint: #2F4858;
        --wood: #A8763E;
        --line: #DAD6C8;
        --grid: rgba(47, 72, 88, 0.05);
    }

    html, body, [class*="css"] {
        font-family: 'Zen Kaku Gothic New', -apple-system, sans-serif;
        color: var(--ink);
    }

    .stApp {
        background-color: var(--bg);
        background-image:
            linear-gradient(var(--grid) 1px, transparent 1px),
            linear-gradient(90deg, var(--grid) 1px, transparent 1px);
        background-size: 28px 28px;
    }

    /* カード：図面のトンボ(レジストレーションマーク)を四隅に配置 */
    .custom-card {
        background-color: var(--surface);
        padding: 28px 26px;
        border-radius: 3px;
        border: 1px solid var(--line);
        margin-bottom: 22px;
        background-image:
            linear-gradient(var(--blueprint) 2px, transparent 2px),
            linear-gradient(var(--blueprint) 2px, transparent 2px),
            linear-gradient(90deg, var(--blueprint) 2px, transparent 2px),
            linear-gradient(90deg, var(--blueprint) 2px, transparent 2px),
            linear-gradient(var(--blueprint) 2px, transparent 2px),
            linear-gradient(var(--blueprint) 2px, transparent 2px),
            linear-gradient(90deg, var(--blueprint) 2px, transparent 2px),
            linear-gradient(90deg, var(--blueprint) 2px, transparent 2px);
        background-position: 0 0, 0 100%, 0 0, 100% 0, 100% 0, 100% 100%, 0 100%, 100% 100%;
        background-repeat: no-repeat;
        background-size: 14px 14px;
    }

    .section-heading { margin-bottom: 26px; }
    .eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: var(--wood);
        margin-bottom: 6px;
    }
    .main-title {
        font-family: 'Zen Old Mincho', serif;
        font-size: 26px;
        font-weight: 700;
        color: var(--ink);
        padding-bottom: 14px;
        position: relative;
    }
    .main-title::after {
        content: "";
        position: absolute;
        left: 0; right: 0; bottom: 0;
        height: 1px;
        background-image: repeating-linear-gradient(90deg, var(--blueprint) 0 8px, transparent 8px 14px);
    }

    .sub-title {
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        color: var(--ink-soft);
        margin-bottom: 14px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--line);
    }

    .highlight-box {
        background-color: #FBF9F3;
        border: 1px dashed var(--wood);
        border-left: 3px solid var(--wood);
        padding: 16px 18px;
        border-radius: 2px;
        margin-bottom: 16px;
    }

    .stButton>button {
        background-color: var(--blueprint) !important;
        color: #FFFFFF !important;
        font-family: 'Zen Kaku Gothic New', sans-serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.03em;
        border-radius: 2px !important;
        border: 1px solid var(--blueprint) !important;
        padding: 10px 20px !important;
        transition: all 0.15s ease !important;
    }
    .stButton>button:hover {
        background-color: var(--wood) !important;
        border-color: var(--wood) !important;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] {
        background-color: var(--surface);
        border-right: 1px solid var(--line);
    }

    .sidebar-stamp {
        padding: 18px 4px 18px;
        border-bottom: 2px solid var(--blueprint);
        margin-bottom: 14px;
    }
    .stamp-eyebrow {
        font-family: 'JetBrains Mono', monospace;
        font-size: 10px;
        letter-spacing: 0.16em;
        color: var(--wood);
        margin-bottom: 4px;
    }
    .stamp-title {
        font-family: 'Zen Old Mincho', serif;
        font-size: 22px;
        font-weight: 700;
        color: var(--ink);
    }

    .title-block {
        border: 1px solid var(--line);
        border-radius: 2px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px;
        overflow: hidden;
    }
    .title-block-row {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        padding: 7px 10px;
        border-bottom: 1px solid var(--line);
        color: var(--ink-soft);
    }
    .title-block-row:last-child { border-bottom: none; }
    .title-block-row span:first-child {
        letter-spacing: 0.08em;
        color: var(--wood);
    }

    [data-baseweb="tab-list"] {
        gap: 4px;
        border-bottom: 1px solid var(--line);
    }
    [data-baseweb="tab"] {
        font-family: 'Zen Kaku Gothic New', sans-serif;
        font-weight: 600;
        color: var(--ink-soft);
    }
    [data-baseweb="tab-highlight"] {
        background-color: var(--wood) !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 2px;
        font-family: 'Zen Kaku Gothic New', sans-serif;
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


def section_title(title: str, eyebrow: str):
    """図面の表題欄風の見出し（小さな英字ラベル＋明朝体タイトル＋寸法線）を表示する。"""
    st.markdown(
        f"""<div class="section-heading">
            <div class="eyebrow">{eyebrow}</div>
            <div class="main-title">{title}</div>
        </div>""",
        unsafe_allow_html=True,
    )


API_KEY_SET = bool(os.getenv("GEMINI_API_KEY"))


# --- サイドバー ---
st.sidebar.markdown(
    """<div class="sidebar-stamp">
        <div class="stamp-eyebrow">SNS / WEB PLANNING TOOL</div>
        <div class="stamp-title">🏠 AI広報部</div>
    </div>""",
    unsafe_allow_html=True,
)

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

# 図面の表題欄(タイトルブロック)風に、選択中のシート(メニュー)を表示
st.sidebar.markdown(
    f"""<div class="title-block">
        <div class="title-block-row"><span>PROJECT</span><span>AI広報部</span></div>
        <div class="title-block-row"><span>SHEET</span><span>{menu}</span></div>
    </div>""",
    unsafe_allow_html=True,
)

# 生成系メニュー全てで共通してAPIキーが必要なため、ここで一括チェック
GENERATION_MENUS = {"Instagram投稿作成", "リール企画", "ブログ作成", "撮影指示"}
if menu in GENERATION_MENUS and not API_KEY_SET:
    st.error("⚠️ 環境変数 GEMINI_API_KEY が設定されていません。.env を確認してください。")

# --- メインコンテンツ ---

# 1. Instagram投稿作成
if menu == "Instagram投稿作成":
    section_title("Instagram投稿作成", "SHEET 01 — INSTAGRAM POST")

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
    section_title("リール企画案作成", "SHEET 02 — SHORT VIDEO REEL")

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
    section_title("ブログ・Web記事作成", "SHEET 03 — ARTICLE")

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
    section_title("現場・物件 撮影指示書作成", "SHEET 04 — SITE PHOTOGRAPHY")

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
    section_title("ブランドガイドライン管理", "SHEET 05 — BRAND GUIDELINE")

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
    section_title("投稿履歴", "SHEET 06 — ARCHIVE")

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
