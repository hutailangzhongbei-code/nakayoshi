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

# 1. Instagram投稿作成（ガイドライン適用強化版）
def generate_instagram_post(genre, target, purpose, content, char_count=600):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brand_rule = load_brand_rules()
    
    system_prompt = f"""
あなたは「中美建設」の専属トップマーケターおよびSNS広報担当です。
以下の【中美建設 ブランドガイドライン】を100%厳格に適用し、ブランドイメージを損なわないアウトプットを出力してください。

==================================================
【中美建設 ブランドガイドライン（最優先適用ルール）】
{brand_rule}
==================================================

【生成時の絶対厳守事項】
1. 会社名は必ず「中美建設」と正確に表記してください。（表記揺れ・英字表記不可）
2. ガイドラインで指定されたトーン＆マナー（木の温もり、職人の手仕事、信頼感、寄り添う姿勢など）をキャプションやキャッチコピーの文章表現に強く反映させてください。
3. ハッシュタグには必ず `#中美建設` を含めてください。
4. Canvaレイアウトや撮影指示の提案においても、ガイドラインで定められたブランドカラー（メイン: #5EB0B1、サブ: #5A5A5A、アクセント: #EEC600）やデザインルール（シンプル・余白重視・スマホ閲覧優先）を反映した指示を出してください。

【出力フォーマット】
必ず以下のJSON形式のみで返答してください：
{{
  "title": "投稿のメインタイトル（表紙用）",
  "catchphrase": "ブランドイメージに沿ったキャッチコピー",
  "carousel": [
    "1枚目（表紙）: 内容",
    "2枚目: 内容",
    "3枚目: 内容",
    "4枚目: まとめ",
    "5枚目（CTA）: 内容"
  ],
  "canva_layout": "ブランドカラー（#5EB0B1 / #EEC600）とデザインルールを踏まえたCanvaレイアウト・配色アドバイス",
  "photo_instructions": "ブランドの基本理念（木の温もり・職人の手仕事など）を表現するための撮影指示",
  "caption": "キャプション本文（目安: 約{char_count}文字）。トーン＆マナーを厳守。",
  "hashtags": "#中美建設 #三重注文住宅 #工務店がつくる家 #施工事例",
  "posting_time": "推奨投稿時間帯（理由付き）",
  "growth_reason": "ガイドラインに沿った発信がターゲット層に響く理由"
}}
"""
    user_prompt = f"""
【投稿ジャンル】: {genre}
【ターゲット】: {target}
【投稿目的】: {purpose}
【伝えたい内容】: {content}
【目標文字数】: 約{char_count}文字
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        response_format={"type": "json_object"},
        temperature=0.2  # 温度を下げてガイドライン順守率を高める
    )
    return json.loads(response.choices[0].message.content)

# 2. リール企画
def generate_reel(theme, target):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brand_rule = load_brand_rules()

    system_prompt = f"""
あなたは中美建設のリールディレクターです。
以下のブランドガイドラインを遵守して企画を作成してください。
\n【ブランドルール】\n{brand_rule}\n
以下のJSON形式で回答してください:
{{
  "hook": "最初の3秒のフック",
  "script": "動画構成・テロップ（トーン＆マナー遵守）",
  "music": "ブランドイメージに合った推奨BGM"
}}
"""
    user_prompt = f"テーマ: {theme}\nターゲット: {target}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        response_format={"type": "json_object"},
        temperature=0.3
    )
    return json.loads(response.choices[0].message.content)

# 3. ブログ作成
def generate_blog(title_keyword, target):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brand_rule = load_brand_rules()

    system_prompt = f"""
あなたは中美建設のライターです。
以下のブランドガイドラインを厳守し、会社名は「中美建設」で統一した丁寧なブログを作成してください。
\n【ブランドルール】\n{brand_rule}
"""
    user_prompt = f"キーワード: {title_keyword}\n想定読者: {target}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content

# 4. 撮影指示
def generate_shooting(house_type, highlights):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    brand_rule = load_brand_rules()

    system_prompt = f"""
あなたは中美建設の撮影ディレクターです。
ブランド理念（木の温もり・職人の手仕事・自然光など）を活かした撮影カットリストを作成してください。
\n【ブランドルール】\n{brand_rule}
"""
    user_prompt = f"物件特徴: {house_type}\n見せたいポイント: {highlights}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
        temperature=0.3
    )
    return response.choices[0].message.content
