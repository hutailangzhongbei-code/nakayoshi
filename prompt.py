import os
import json
from openai import OpenAI

def load_brand_rules():
    rule_path = os.path.join("brand", "brand_rule.txt")
    if os.path.exists(rule_path):
        with open(rule_path, "r", encoding="utf-8") as f:
            return f.read()
    return "会社名：中美建設\n特徴：木の温もりを感じる注文住宅、地域密着の丁寧な施工"

def save_brand_rules(content):
    os.makedirs("brand", exist_ok=True)
    rule_path = os.path.join("brand", "brand_rule.txt")
    with open(rule_path, "w", encoding="utf-8") as f:
        f.write(content)

# 1. Instagram投稿作成
def generate_instagram_post(genre, target, purpose, content, char_count=600):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brand_rule = load_brand_rules()
    
    system_prompt = f"""
あなたは「中美建設」のプロのSNS広報担当者です。
社名は必ず「中美建設」と表記し、ブランドルールを厳守してください。

【ブランドルール】
{brand_rule}

【出力フォーマット】必ず以下のJSON形式のみで返答してください。
{{
  "title": "投稿タイトル",
  "catchphrase": "キャッチコピー",
  "carousel": ["1枚目: 表紙", "2枚目: ポイント", "3枚目: 詳細", "4枚目: まとめ", "5枚目: CTA"],
  "canva_layout": "Canvaデザインのアドバイス",
  "photo_instructions": "撮影・画像選定の指示",
  "caption": "キャプション本文",
  "hashtags": "#中美建設 #施工事例 #注文住宅",
  "posting_time": "推奨投稿時間帯",
  "growth_reason": "伸ばすためのポイント"
}}
"""
    user_prompt = f"ジャンル:{genre}\nターゲット:{target}\n目的:{purpose}\n詳細:{content}\n文字数:{char_count}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        response_format={"type": "json_object"},
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)

# 2. リール企画
def generate_reel(theme, target):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brand_rule = load_brand_rules()

    system_prompt = f"あなたは中美建設のリールディレクターです。\nブランドルール:\n{brand_rule}\n\n以下のJSON形式で返してください:\n{{\n  \"hook\": \"最初の3秒のフック\",\n  \"script\": \"動画構成・テロップ\",\n  \"music\": \"推奨BGMイメージ\"\n}}"
    user_prompt = f"テーマ: {theme}\nターゲット: {target}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        response_format={"type": "json_object"},
        temperature=0.5
    )
    return json.loads(response.choices[0].message.content)

# 3. ブログ作成
def generate_blog(title_keyword, target):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brand_rule = load_brand_rules()

    system_prompt = f"あなたは中美建設のライターです。\nブランドルール:\n{brand_rule}\nSEOを意識した丁寧なブログ記事（見出し・本文）を作成してください。"
    user_prompt = f"キーワード: {title_keyword}\n想定読者: {target}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content

# 4. 撮影指示
def generate_shooting(house_type, highlights):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = "あなたは建築写真のディレクターです。現場で使いやすい撮影カットリストと指示内容を作成してください。"
    user_prompt = f"物件特徴: {house_type}\n見せたいポイント: {highlights}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content
