import os
from openai import OpenAI

def load_brand_rule():
    rule_path = os.path.join("brand", "brand_rule.txt")
    if os.path.exists(rule_path):
        with open(rule_path, "r", encoding="utf-8") as f:
            return f.read()
    return ""

def generate_post(theme, target, details):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brand_rule = load_brand_rule()
    
    system_prompt = f"""
あなたは中美建設のプロのSNS広報担当者です。
以下の「ブランドルール」を厳守し、親しみやすく魅力的なSNS投稿文（Instagram/Facebook向け）を作成してください。

【ブランドルール】
{brand_rule}
"""

    user_prompt = f"""
【投稿テーマ】: {theme}
【ターゲット】: {target}
【詳細・アピールポイント】: {details}

上記の情報をもとに、絵文字を交えた読みやすい投稿文と、関連するハッシュタグ（5〜10個程度）を作成してください。
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )
    
    return response.choices[0].message.content
