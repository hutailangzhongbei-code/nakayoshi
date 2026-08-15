import os
import json
from google import genai
from google.genai import types

def load_brand_rules():
    rule_path = os.path.join("brand", "brand_rule.txt")
    if os.path.exists(rule_path):
        with open(rule_path, "r", encoding="utf-8") as f:
            return f.read()
    return """【中美建設 ブランドガイドライン】

■ 基本理念・ブランドイメージ
・地域密着、職人の手仕事、木の温もり、信頼感、現場第一を徹底する。
・「家づくりの失敗を防ぐアドバイザー」「一緒に夢を叶えるパートナー」としての姿勢で発信する。

■ ブランドカラー
・メインカラー: RGB(94, 176, 177) / #5EB0B1
・サブカラー: RGB(90, 90, 90) / #5A5A5A（本文等）
・アクセントカラー: RGB(238, 198, 0) / #EEC600（強調のみ使用）

■ フォント
・Illustrator: A-OTF ゴシック StdN
・Office: 游ゴシック

■ デザインルール
・メインカラーを基調とし、アクセントはイエローのみ使用する。
・本文はグレー(#5A5A5A)を使用する。
・ロゴの変形禁止。ロゴ周囲には十分な余白を確保する。
・ブランドイメージを崩さず、シンプルで余白を活かした読みやすいデザインにする。
・情報を詰め込み過ぎず、スマホ閲覧を最優先とする。"""

def save_brand_rules(content):
    os.makedirs("brand", exist_ok=True)
    rule_path = os.path.join("brand", "brand_rule.txt")
    with open(rule_path, "w", encoding="utf-8") as f:
        f.write(content)

# Gemini Client初期化
def get_client():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません。")
    return genai.Client(api_key=api_key)

# 1. Instagram投稿作成
def generate_instagram_post(genre, target, purpose, content, char_count=600):
    client = get_client()
    brand_rule = load_brand_rules()
    
    system_prompt = f"""
あなたは「中美建設」の専属トップマーケターおよびSNS広報担当です。
以下の【中美建設 ブランドガイドライン】を100%厳格に適用し、ブランドイメージを損なわないアウトプットを出力してください。

==================================================
【中美建設 ブランドガイドライン（最優先適用ルール）】
{brand_rule}
==================================================

【生成時の絶対厳守事項】
1. 会社名は必ず「中美建設」と正確に表記してください。
2. ガイドラインで指定されたトーン＆マナー（木の温もり、職人の手仕事、信頼感など）を文章表現に強く反映させてください。
3. ハッシュタグには必ず #中美建設 を含めてください。
4. Canvaレイアウトや撮影指示の提案においても、ブランドカラー（#5EB0B1 / #EEC600）やデザインルール（シンプル・スマホ閲覧優先）を反映させてください。

【出力フォーマット】
必ず以下のJSON形式のみで返答してください。
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
  "canva_layout": "ブランドカラー（#5EB0B1 / #EEC600）を踏まえたCanvaレイアウト・配色アドバイス",
  "photo_instructions": "ブランド理念（木の温もり・職人の手仕事など）を表現するための撮影指示",
  "caption": "キャプション本文（目安: 約{char_count}文字）。トーン＆マナーを厳守。",
  "hashtags": "#中美建設 #三重注文住宅 #工務店がつくる家 #施工事例",
  "posting_time": "推奨投稿時間帯（理由付き）",
  "growth_reason": "ガイドラインに沿った発信がターゲット層に響く理由"
}}
"""
    user_prompt = f"【ジャンル】: {genre}\n【ターゲット】: {target}\n【目的】: {purpose}\n【伝えたい内容】: {content}\n【目標文字数】: 約{char_count}文字"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=0.2
        )
    )
    return json.loads(response.text)

# 2. リール企画
def generate_reel(theme, target):
    client = get_client()
    brand_rule = load_brand_rules()

    system_prompt = f"あなたは中美建設のリールディレクターです。\n【ブランドルール】\n{brand_rule}\n\n以下のJSON形式で返答してください:\n{{\n  \"hook\": \"最初の3秒のフック\",\n  \"script\": \"動画構成・テロップ\",\n  \"music\": \"推奨BGMイメージ\"\n}}"
    user_prompt = f"テーマ: {theme}\nターゲット: {target}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            response_mime_type="application/json",
            temperature=0.3
        )
    )
    return json.loads(response.text)

# 3. ブログ作成
def generate_blog(title_keyword, target):
    client = get_client()
    brand_rule = load_brand_rules()

    system_prompt = f"あなたは中美建設のライターです。\n【ブランドルール】\n{brand_rule}\nSEOを意識した丁寧なブログ記事（見出し・本文）を作成してください。会社名は必ず「中美建設」と表記してください。"
    user_prompt = f"キーワード: {title_keyword}\n想定読者: {target}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3
        )
    )
    return response.text

# 4. 撮影指示
def generate_shooting(house_type, highlights):
    client = get_client()
    brand_rule = load_brand_rules()

    system_prompt = f"あなたは中美建設の撮影ディレクターです。\n【ブランドルール】\n{brand_rule}\n現場で使いやすい撮影カットリストと指示内容を作成してください。"
    user_prompt = f"物件特徴: {house_type}\n見せたいポイント: {highlights}"

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=user_prompt,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.3
        )
    )
    return response.text
