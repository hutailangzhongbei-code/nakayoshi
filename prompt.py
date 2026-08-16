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
    
    # 正しいモデル名を指定 (gemini-1.5-flash)
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

以下の必須キーを持つ**完全なJSONフォーマットのみ**で出力してください。Markdownの装飾コードブロック（
