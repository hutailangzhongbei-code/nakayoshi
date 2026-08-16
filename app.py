import os
import json
import google.generativeai as genai

# --- Gemini APIの初期化 ---
def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません。")
    genai.configure(api_key=api_key)

# --- ブランドルール読み込み・保存機能 ---
BRAND_RULE_PATH = "brand/brand_rule.txt"

def load_brand_rules() -> str:
    if os.path.exists(BRAND_RULE_PATH):
        try:
            with open(BRAND_RULE_PATH, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return ""
    return ""

def save_brand_rules(content: str):
    os.makedirs(os.path.dirname(BRAND_RULE_PATH), exist_ok=True)
    with open(BRAND_RULE_PATH, "w", encoding="utf-8") as f:
        f.write(content)

# --- JSONパース用補助関数 ---
def clean_json_response(text: str) -> dict:
    """Geminiの返答からコードブロックを除去してJSONにパースする"""
    text = text.strip()
    if text.startswith("```json"):
        text = text[7:]
    if text.startswith("```"):
        text = text[3:]
    if text.endswith("```"):
        text = text[:-3]
    return json.loads(text.strip())

# --- 1. Instagram投稿生成 ---
def generate_instagram_post(genre: str, target: str, purpose: str, content: str, char_count: int = 600) -> dict:
    init_gemini()
    brand_rule = load_brand_rules()
    
    model = genai.GenerativeModel("gemini-1.5-flash")

    system_prompt = f"""
あなたは住宅会社（中美建設）の優秀なSNSマーケター・AI広報です。
以下の【ブランドガイドライン】を遵守して投稿を作成してください。

【ブランドガイドライン】
{brand_rule}

【依頼内容】
- 投稿ジャンル: {genre}
- ターゲット: {target}
- 投稿目的: {purpose}
- 伝えたい内容: {content}
- キャプション文字数目安: {char_count}文字程度

以下のキーを持つ完全なJSONフォーマットのみで出力してください。

{{
    "title": "投稿タイトル",
    "catchphrase": "キャッチコピー（1行）",
    "caption": "Instagram本文キャプション",
    "hashtags": "#ハッシュタグ1 #ハッシュタグ2 ...（15〜20個程度）",
    "carousel": ["1スライド目", "2スライド目", "3スライド目", "4スライド目", "5スライド目"],
    "canva_layout": "Canvaでの画像デザイン・レイアウトの具体的な指示",
    "photo_instructions": "撮影現場への写真アングルやライティングの指示",
    "posting_time": "おすすめの投稿曜日・時間帯とその理由",
    "growth_reason": "この投稿がターゲットに響く理由・アルゴリズム上の狙い"
}}
"""

    response = model.generate_content(system_prompt)
    return clean_json_response(response.text)

# --- 2. リール企画生成 ---
def generate_reel(theme: str, target: str) -> dict:
    init_gemini()
    brand_rule = load_brand_rules()

    model = genai.GenerativeModel("gemini-1.5-flash")

    system_prompt = f"""
あなたは住宅会社（中美建設）のSNSマーケターです。
リール動画の企画案を作成してください。

【ブランドガイドライン】
{brand_rule}

【条件】
- 動画テーマ: {theme}
- ターゲット: {target}

以下のJSONフォーマットのみで出力してください。
{{
    "hook": "冒頭3秒のフック（惹きつけるテキストまたは演出）",
    "script": "【0〜3秒】フック\\n【3〜10秒】シーン1の映像とテロップ\\n【10〜20秒】シーン2の映像とテロップ\\n【20〜30秒】まとめ・CTA",
    "music": "おすすめの音源・BGMの雰囲気"
}}
"""

    response = model.generate_content(system_prompt)
    return clean_json_response(response.text)

# --- 3. ブログ作成 ---
def generate_blog(title_kw: str, target: str) -> str:
    init_gemini()
    brand_rule = load_brand_rules()

    model = genai.GenerativeModel("gemini-1.5-flash")

    system_prompt = f"""
あなたは住宅会社（中美建設）のWebライターです。
SEOを意識したブログ記事・Web記事を作成してください。

【ブランドガイドライン】
{brand_rule}

【条件】
- キーワード/テーマ: {title_kw}
- 想定読者: {target}

見出し（H2, H3）を適切に使い、読者が惹き込まれる自然でわかりやすい文章を作成してください。
"""

    response = model.generate_content(system_prompt)
    return response.text

# --- 4. 撮影指示書作成 ---
def generate_shooting(house_type: str, highlights: str) -> str:
    init_gemini()
    brand_rule = load_brand_rules()

    model = genai.GenerativeModel("gemini-1.5-flash")

    system_prompt = f"""
あなたは住宅建築のプロフェッショナルです。
ルームツアー動画やSNS投稿用写真のための「撮影指示書」を作成
