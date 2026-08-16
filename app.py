import os
import streamlit as st
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# --- ページ基本設定 ---
st.set_page_config(
    page_title="中美建設 AI広報部",
    page_icon="🏠",
    layout="wide"
)

# --- 簡易パスワード認証機能 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False

    if st.session_state["password_correct"]:
        return True

    st.markdown("""
    <style>
        .login-box {
            max-width: 400px;
            margin: 80px auto;
            padding: 30px;
            background-color: #FFFFFF;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
            border: 1px solid #E2E8F0;
            text-align: center;
        }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("## 🔒 関係者専用アクセス")
        st.caption("利用するにはパスワードを入力してください。")
        
        password_input = st.text_input("パスワード", type="password", key="login_password_field")
        
        if st.button("ログイン", use_container_width=True):
            if password_input == "1118":
                st.session_state["password_correct"] = True
                st.rerun()
            else:
                st.error("パスワードが正しくありません。")
                
    return False

if not check_password():
    st.stop()

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

# --- サイドバー ---
st.sidebar.markdown("<h2 style='color: #5EB0B1; font-weight: bold;'>🏠 中美建設 AI広報部</h2>", unsafe_allow_html=True)

if st.sidebar.button("🔒 ログアウト"):
    st.session_state["password_correct"] = False
    st.rerun()

st.sidebar.markdown("---")

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
with st.sidebar.expander("🚀 今後追加予定の機能"):
    st.caption("""
    ・Instagramトレンド分析  
    ・Instagram API連携  
    ・Canva連携  
    ・AI画像生成  
    ・施工事例管理  
    ・投稿カレンダー
    """)

st.sidebar.caption("© 中美建設")

# --- メインコンテンツ ---

# 1. Instagram投稿作成
if menu == "Instagram投稿作成":
    st.markdown("<div class='main-title'>Instagram投稿作成</div>", unsafe_allow_html=True)
    
    if not os.getenv("GEMINI_API_KEY"):
        st.error("⚠️ 環境変数 GEMINI_API_KEY が設定されていません。")

    col_input, col_result = st.columns([1, 1])

    with col_input:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
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

        submit_btn = st.button("✨ 投稿案を生成する", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_result:
        st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
        st.markdown("<div class='sub-title'>📄 生成結果</div>", unsafe_allow_html=True)
        
        if submit_btn:
            if not genre or not target or not purpose or not content:
                st.warning("すべての入力項目（ジャンル・ターゲット・目的・伝えたい内容）を入力してください。")
            else:
                st.session_state["genre"] = genre
                st.session_state["target"] = target
                st.session_state["purpose"] = purpose
                st.session_state["content"] = content

                with st.spinner("ブランドガイドラインに沿って生成中..."):
                    try:
                        res = generate_instagram_post(genre, target, purpose, content, char_count)
                        st.session_state["latest_res"] = res
                        st.session_state.history.append({"type": "Instagram", "title": res.get('title'), "content": res.get('caption')})
                    except Exception as e:
                        st.error(f"エラーが発生しました: {e}")

        if "latest_res" in st.session_state and st.session_state["latest_res"]:
            res = st.session_state["latest_res"]
            
            tab1, tab2, tab3 = st.tabs(["📝 キャプション・ハッシュタグ", "🖼️ カルーセル・デザイン", "💡 撮影・分析"])

            with tab1:
                st.markdown(f"**タイトル:** {res.get('title')}")
                st.markdown("<div class='highlight-box'>", unsafe_allow_html=True)
                st.markdown(f"**キャッチコピー:**\n{res.get('catchphrase')}")
                st.markdown("</div>", unsafe_allow_html=True)

                st.write("▼ キャプション（コピーしてそのまま使えます）")
                st.code(res.get('caption'), language=None)
                
                st.write("▼ ハッシュタグ")
                st.code(res.get('hashtags'), language=None)

            with tab2:
                st.markdown("### 🖼️ カルーセル構成案")
                for slide in res.get('carousel', []):
                    st.info(slide)

                st.markdown("### 🎨 Canvaレイアウト指示")
                st.write(res.get('canva_layout'))

            with tab3:
                st.markdown("### 📷 撮影指示")
                st.warning(res.get('photo_instructions'))

                st.markdown("### ⏰ 推奨投稿時間")
                st.write(res.get('posting_time'))

                st.markdown("### 📈 ポイント")
                st.success(res.get('growth_reason'))
        else:
            st.info("左側のフォームに入力し、「投稿案を生成する」を押してください。")
            
        st.markdown("</div>", unsafe_allow_html=True)

# 2. リール企画
elif menu == "リール企画":
    st.markdown("<div class='main-title'>リール企画案作成</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    theme = st.text_input("動画テーマ", placeholder="例：ルームツアー、平屋のメリット3選")
    target = st.text_input("ターゲット", placeholder="例：子育て世代の夫婦")
    btn = st.button("リール企画を生成", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if btn:
        if theme and target:
            with st.spinner("生成中..."):
                try:
                    res = generate_reel(theme, target)
                    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                    st.markdown(f"### 🪝 フック（冒頭3秒）\n**{res.get('hook')}**")
                    st.markdown("### 🎬 構成・テロップ案")
                    st.code(res.get('script'), language=None)
                    st.markdown(f"### 🎵 BGMイメージ\n{res.get('music')}")
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.session_state.history.append({"type": "リール", "title": theme, "content": f"フック: {res.get('hook')}\n\n構成:\n{res.get('script')}"})
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("動画テーマとターゲットを入力してください。")

# 3. ブログ作成
elif menu == "ブログ作成":
    st.markdown("<div class='main-title'>ブログ・Web記事作成</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    title_kw = st.text_input("キーワード / テーマ", placeholder="例：注文住宅 高気密高断熱 三重県")
    target = st.text_input("想定読者", placeholder="例：冬暖かい家を建てたいファミリー")
    btn = st.button("ブログ記事を生成", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if btn:
        if title_kw and target:
            with st.spinner("生成中..."):
                try:
                    res = generate_blog(title_kw, target)
                    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                    st.markdown("### 📄 生成されたブログ文章")
                    st.code(res, language=None)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.session_state.history.append({"type": "ブログ", "title": title_kw, "content": res})
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("キーワードと想定読者を入力してください。")

# 4. 撮影指示
elif menu == "撮影指示":
    st.markdown("<div class='main-title'>現場・物件 撮影指示書作成</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    house_type = st.text_input("物件特徴", placeholder="例：開放感のある吹抜けリビングと平屋風動線")
    highlights = st.text_area("特に見せたいポイント", placeholder="例：造作キッチン、無垢材の床、玄関手洗い")
    btn = st.button("撮影指示書を生成", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if btn:
        if house_type and highlights:
            with st.spinner("生成中..."):
                try:
                    res = generate_shooting(house_type, highlights)
                    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
                    st.markdown("### 📷 撮影カットリスト")
                    st.code(res, language=None)
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.session_state.history.append({"type": "撮影指示", "title": house_type, "content": res})
                except Exception as e:
                    st.error(f"エラーが発生しました: {e}")
        else:
            st.warning("物件特徴と見せたいポイントを入力してください。")

# 5. ブランドガイドライン
elif menu == "ブランドガイドライン":
    st.markdown("<div class='main-title'>ブランドガイドライン管理</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
    current_rule = load_brand_rules()
    new_rule = st.text_area("brand/brand_rule.txt の内容", current_rule, height=350)
    if st.button("ガイドラインを更新・保存", use_container_width=True):
        save_brand_rules(new_rule)
        st.success("ガイドラインを保存しました！今後の生成に即時反映されます。")
    st.markdown("</div>", unsafe_allow_html=True)

# 6. 投稿履歴
elif menu == "投稿履歴":
    st.markdown("<div class='main-title'>投稿履歴</div>", unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.info("まだ生成履歴はありません。")
    else:
        if st.button("履歴をすべてクリア"):
            st.session_state.history = []
            st.rerun()

        for idx, item in enumerate(reversed(st.session_state.history)):
            st.markdown("<div class='custom-card'>", unsafe_allow_html=True)
            st.markdown(f"**【{item['type']}】 {item['title']}**")
            st.code(item["content"], language=None)
            st.markdown("</div>", unsafe_allow_html=True)
