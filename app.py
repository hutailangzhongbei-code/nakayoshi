import streamlit as st
import os
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

from prompt import (
    generate_instagram_post, 
    generate_reel, 
    generate_blog, 
    generate_shooting, 
    load_brand_rules, 
    save_brand_rules
)

# --- ページ設定 ---
st.set_page_config(
    page_title="中美建設 AI広報部",
    page_icon="🏠",
    layout="wide"
)

# --- カスタムCSS（ブランドガイドラインのカラー＆デザインルールを反映） ---
st.markdown("""
<style>
    /* 全体フォント（游ゴシック優先） */
    html, body, [class*="css"] {
        font-family: '游ゴシック', 'Yu Gothic', sans-serif;
        color: #5A5A5A;
    }
    
    /* ヘッダー・タイトル */
    .main-header {
        color: #5EB0B1;
        font-weight: bold;
        border-bottom: 3px solid #5EB0B1;
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    
    /* メインボタン */
    .stButton>button {
        background-color: #5EB0B1;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 0.75rem 1.5rem;
        width: 100%;
    }
    .stButton>button:hover {
        background-color: #4A9798;
        color: white;
    }
    
    /* アクセント強調枠 */
    .accent-box {
        background-color: #FFFDF0;
        border-left: 5px solid #EEC600;
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
    }
    
    /* サブコンテンツカード */
    .section-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 15px;
    }

    .hashtag-chip {
        background-color: #e6f7f7;
        color: #5EB0B1;
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

# 履歴データの初期化
if "history" not in st.session_state:
    st.session_state.history = []

# --- サイドバー表示 ---
st.sidebar.title("🏠 中美建設 AI広報部")

menu = st.sidebar.radio(
    "メニューを選択",
    [
        "Instagram投稿作成",
        "リール企画",
        "ブログ作成",
        "撮影指示",
        "ブランドガイドライン",
        "投稿履歴",
        "── 今後追加予定 ──",
        "Instagramトレンド分析",
        "Instagram API連携",
        "Canva連携",
        "AI画像生成",
        "外壁カラーシミュレーター",
        "施工事例管理",
        "投稿カレンダー",
        "ブランドチェック機能",
        "PDF出力",
        "画像アップロード",
        "複数ブランド対応"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("© 中美建設")

# --- メインコンテンツ切り替え ---

# 1. Instagram投稿作成 画面
if menu == "Instagram投稿作成":
    st.markdown("<h1 class='main-header'>中美建設 AI広報部 - Instagram投稿作成</h1>", unsafe_allow_html=True)
    
    if not os.getenv("OPENAI_API_KEY"):
        st.error("⚠️ .env に OPENAI_API_KEY が設定されていません。")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📋 投稿条件の入力")
        
        genre = st.text_input("投稿ジャンル", placeholder="例: 施工事例 / 完成見学会 / 木の家 / リノベーション")
        target = st.text_input("ターゲット", placeholder="例: 自然素材の家に憧れる30代子育て世代")
        purpose = st.text_input("投稿目的", placeholder="例: 見学会予約の獲得 / 認知拡大 / ファン化")
        content = st.text_area("伝えたい内容", placeholder="例: 木の温もりあふれる大空間LDK、家事動線に優れた回遊間取り、職人の造作家具", height=120)
        char_count = st.slider("文字数（キャプション目安）", min_value=200, max_value=1500, value=600, step=50)

        submit_btn = st.button("投稿を作成")

    with col2:
        st.subheader("📄 生成結果")
        
        if submit_btn:
            if not genre or not target or not purpose or not content:
                st.warning("すべての入力項目（ジャンル・ターゲット・目的・伝えたい内容）を入力してください。")
            else:
                with st.spinner("AIが最新トレンド分析とブランドルールを適用して生成中..."):
                    try:
                        res = generate_instagram_post(genre, target, purpose, content, char_count)

                        st.markdown(f"### 📌 タイトル\n**{res.get('title')}**")
                        
                        st.markdown("<div class='accent-box'>", unsafe_allow_html=True)
                        st.markdown(f"### 💡 キャッチコピー\n**{res.get('catchphrase')}**")
                        st.markdown("</div>", unsafe_allow_html=True)

                        st.markdown("### 🖼️ カルーセル構成")
                        for slide in res.get('carousel', []):
                            st.write(f"- {slide}")

                        st.markdown("### 🎨 Canvaレイアウト")
                        st.info(res.get('canva_layout'))

                        st.markdown("### 📷 撮影指示")
                        st.warning(res.get('photo_instructions'))

                        st.markdown("### 📝 キャプション")
                        st.code(res.get('caption'), language=None)

                        st.markdown("### 🏷️ ハッシュタグ")
                        st.code(res.get('hashtags'), language=None)

                        st.markdown("### ⏰ 投稿時間")
                        st.write(res.get('posting_time'))

                        st.markdown("### 📈 伸びる理由")
                        st.success(res.get('growth_reason'))

                        st.session_state.history.append({"type": "Instagram", "title": res.get('title'), "content": res.get('caption')})

                    except Exception as e:
                        st.error(f"エラーが発生しました: {e}")

# 2. リール企画
elif menu == "リール企画":
    st.markdown("<h1 class='main-header'>リール企画案作成</h1>", unsafe_allow_html=True)
    theme = st.text_input("動画テーマ", placeholder="例：ルームツアー、失敗しない間取りの選び方")
    target = st.text_input("ターゲット", placeholder="例：子育て世代の夫婦")
    if st.button("リール企画を生成"):
        if theme and target:
            with st.spinner("生成中..."):
                res = generate_reel(theme, target)
                st.markdown(f"### 🪝 フック\n{res.get('hook')}")
                st.markdown(f"### 🎬 構成案\n{res.get('script')}")
                st.markdown(f"### 🎵 BGM\n{res.get('music')}")

# 3. ブログ作成
elif menu == "ブログ作成":
    st.markdown("<h1 class='main-header'>ブログ・Web記事作成</h1>", unsafe_allow_html=True)
    title_kw = st.text_input("キーワード / テーマ", placeholder="例：注文住宅 高気密高断熱 三重県")
    target = st.text_input("想定読者", placeholder="例：冬暖かい家を建てたいファミリー")
    if st.button("ブログを生成"):
        if title_kw:
            with st.spinner("生成中..."):
                res = generate_blog(title_kw, target)
                st.text_area("本文", value=res, height=350)

# 4. 撮影指示
elif menu == "撮影指示":
    st.markdown("<h1 class='main-header'>現場・物件 撮影指示書作成</h1>", unsafe_allow_html=True)
    house_type = st.text_input("物件特徴", placeholder="例：開放感のある吹抜けリビングと平屋風動線")
    highlights = st.text_area("特に見せたいポイント", placeholder="例：造作キッチン、無垢材の床、玄関手洗い")
    if st.button("指示書を生成"):
        if house_type:
            with st.spinner("生成中..."):
                res = generate_shooting(house_type, highlights)
                st.text_area("指示内容", value=res, height=300)

# 5. ブランドガイドライン 画面
elif menu == "ブランドガイドライン":
    st.markdown("<h1 class='main-header'>ブランドガイドライン</h1>", unsafe_allow_html=True)
    current_rule = load_brand_rules()
    new_rule = st.text_area("brand/brand_rule.txt の内容", current_rule, height=400)
    if st.button("ガイドラインを保存"):
        save_brand_rules(new_rule)
        st.success("ガイドラインを保存しました！")

# 6. 投稿履歴
elif menu == "投稿履歴":
    st.markdown("<h1 class='main-header'>投稿履歴</h1>", unsafe_allow_html=True)
    if not st.session_state.history:
        st.info("履歴はありません。")
    else:
        for idx, item in enumerate(reversed(st.session_state.history)):
            with st.expander(f"【{item['type']}】 {item['title']}"):
                st.text_area(f"内容-{idx}", value=item["content"], height=150)

# 7. その他のメニュー（拡張用枠組み）
else:
    st.markdown(f"<h1 class='main-header'>{menu}</h1>", unsafe_allow_html=True)
    st.info(f"【{menu}】機能は今後拡張可能な設計になっています。")
