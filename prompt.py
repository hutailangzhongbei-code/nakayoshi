import os
import json
from openai import OpenAI

def load_brand_rule():
    rule_path = os.path.join("brand", "brand_rule.txt")
    if os.path.exists(rule_path):
        with open(rule_path, "r", encoding="utf-8") as f:
            return f.read()
    return "会社名：中美建設\n特徴：木の温もりを感じる注文住宅、地域密着の丁寧な施工"

def save_brand_rule(content):
    os.makedirs("brand", exist_ok=True)
    rule_path = os.path.join("brand", "brand_rule.txt")
    with open(rule_path, "w", encoding="utf-8") as f:
        f.write(content)

# 1. Instagram投稿生成
def generate_post(genre, target, purpose, details):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brand_rule = load_brand_rule()
    
    system_prompt = f"""
あなたは「中美建設」のプロのSNS広報担当者です。
社名は必ず「中美建設」と表記し、ブランドルールを厳守してください。

【ブランドルール】
{brand_rule}

【出力フォーマット】必ず以下のJSON形式のみで返答してください。
{{
  "caption": "投稿用キャプション文章",
  "hashtags": ["#中美建設", "#施工事例", "#注文住宅"],
  "best_time": "推奨：火・木・土曜日の朝7〜8時 または 夜20〜21時\\n理由：ターゲット層が情報収集しやすい時間帯。"
}}
"""
    user_prompt = f"ジャンル:{genre}\nターゲット:{target}\n目的:{purpose}\n詳細:{details}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        response_format={"type": "json_object"},
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)

# 2. リール企画生成
def generate_reel(theme, target):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brand_rule = load_brand_rule()

    system_prompt = f"""
あなたは中美建設のリール動画ディレクターです。
【ブランドルール】\n{brand_rule}

以下のJSON形式で回答してください：
{{
  "hook": "最初の3秒で惹きつけるインパクトのある言葉・映像指示",
  "script": "【0-3秒】〜\\n【3-10秒】〜\\n【10-20秒】〜\\n【ラスト】〜",
  "music": "テンポ感や雰囲気に合った推奨BGMのジャンル"
}}
"""
    user_prompt = f"テーマ: {theme}\nターゲット: {target}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        response_format={"type": "json_object"},
        temperature=0.5
    )
    return json.loads(response.choices[0].message.content)

# 3. ブログ生成
def generate_blog(title_keyword, target):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brand_rule = load_brand_rule()

    system_prompt = f"""
あなたは中美建設のWebライターです。
【ブランドルール】\n{brand_rule}
SEOに強く、読みやすい丁寧なブログ記事（見出し・導入・本文・まとめ）を作成してください。会社名は「中美建設」で統一してください。
"""
    user_prompt = f"キーワード: {title_keyword}\n想定読者: {target}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content

# 4. 撮影指示生成
def generate_shooting(house_type, highlights):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    system_prompt = "あなたは建築写真の撮影ディレクターです。撮影スタッフや広報担当が現場でスムーズに撮影できるカットリストと構図指示を作成してください。"
    user_prompt = f"物件特徴: {house_type}\n見せたいポイント: {highlights}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content
