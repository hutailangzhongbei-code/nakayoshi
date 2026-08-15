import streamlit as st
from prompt import generate_post

st.set_page_config(page_title="中美建設 AI広報部", layout="centered")

st.title("中美建設 AI広報部 🏠")
st.caption("イベント情報や見学会の概要から、SNS投稿文を自動作成します。")

with st.form("input_form"):
    theme = st.text_input("イベント・投稿のテーマ", placeholder="例：松阪市下村町 モデルハウスオープンイベント")
    target = st.text_input("ターゲット層", placeholder="例：子育て世代、家づくりを検討し始めたご夫婦")
    details = st.text_area("詳細・おすすめポイント", placeholder="例：家事動線が抜群の平屋、見学予約でQuoカードプレゼント！", height=150)
    
    submitted = st.form_submit_button("投稿文を生成する")

if submitted:
    if not theme or not details:
        st.warning("「テーマ」と「詳細・おすすめポイント」を入力してください。")
    else:
        with st.spinner("文章を作成中..."):
            try:
                result = generate_post(theme, target, details)
                st.success("作成が完了しました！")
                st.subheader("生成結果")
                st.text_area("そのままコピーして使えます", value=result, height=300)
            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
