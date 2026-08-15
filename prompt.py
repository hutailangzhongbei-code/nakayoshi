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
あなたは「中美建設」のトップマーケター・SNS広報担当です。
社名は必ず「中美建設」と正確に表記し、ブランドルールを遵守してください。

【ブランドルール】
{brand_rule}

【出力フォーマット】必ず以下のJSON形式のみで出力してください。
{{
  "title": "投稿のメインタイトル（表紙用）",
  "catchphrase": "視線を惹きつけるインパクトのあるキャッチコピー",
  "carousel": [
    "1枚目（表紙）: 内容",
    "2枚目: 内容",
    "3枚目: 内容",
    "4枚目: 内容",
    "5枚目（CTA）: 内容"
  ],
  "canva_layout": "Canvaで作成する際のおすすめレイアウト・配置・フォント感のアドバイス",
  "photo_instructions": "どのような構図・光の当たり方の写真を用意すべきかの撮影指示",
  "caption": "絵文字交え本文（目安文字数: 約{char_count}文字）。会社名は中美建設。",
  "hashtags": "#中美建設 #三重注文住宅 #工務店がつくる家 #施工事例",
  "posting_time": "推奨：火・木・土曜日の朝7〜8時 または 夜20〜21時（理由付き）",
  "growth_reason": "この投稿構成やターゲット設定により保存率・インプレッションが伸ばせる理由"
}}
"""
    user_prompt = f"""
投稿ジャンル: {genre}
ターゲット: {target}
投稿目的: {purpose}
伝えたい内容: {content}
目標文字数: {char_count}文字程度
"""

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
