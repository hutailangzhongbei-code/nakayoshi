import os
import re
import json
import google.generativeai as genai

# --- Gemini APIの初期化 ---
def init_gemini():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY が設定されていません。")
    genai.configure(api_key=api_key)


# --- エラー時に使えるモデルを順番に試す自動リトライ生成関数 ---
#
# 注意（2026年8月時点）: gemini-2.0-flash / gemini-1.5-flash / gemini-1.5-pro / gemini-pro は
# いずれも提供終了(シャットダウン)済みで、リクエストは404になります。
# 古いモデル名を候補に残すと「全部失敗して例外を投げる」だけの無駄なリトライになるため、
# 現行の稼働モデルのみをリストにしています。
# 参考: https://ai.google.dev/gemini-api/docs/deprecations
CANDIDATE_MODELS = [
    "gemini-flash-latest",   # 常に最新のFlashモデルを指すエイリアス（自動追従）
    "gemini-2.5-flash",      # 安定版（2026年10月16日以降に終了予定 - 要定期確認）
    "gemini-3.1-flash-lite", # 軽量・低コストな最新モデル
]


def generate_with_fallback(prompt_text: str) -> str:
    init_gemini()

    last_exception = None

    for model_name in CANDIDATE_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt_text)
            text = _extract_text(response)
            if text:
                return text
        except Exception as e:
            last_exception = e
            continue  # エラーが起きた場合は次のモデルを試す

    raise RuntimeError(
        f"利用可能なモデルが見つかりませんでした（候補: {', '.join(CANDIDATE_MODELS)}）。"
        f"詳細: {last_exception}"
    )


def _extract_text(response) -> str:
    """response.text へのアクセスで発生しうる例外（安全フィルタ等）を分かりやすく変換する。"""
    try:
        return response.text
    except Exception as e:
        reason = None
        try:
            reason = response.candidates[0].finish_reason
        except Exception:
            pass
        raise ValueError(
            f"Geminiから有効なテキスト応答を取得できませんでした（finish_reason={reason}）。"
        ) from e


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
    """Geminiの返答からコードブロック（```json ... ```など）を除去してJSONにパースする。

    固定文字数の切り出しではなく正規表現を使うことで、
    前後に空白や余分な文字列が付いても崩れないようにしている。
    """
    if not text or not text.strip():
        raise ValueError("Geminiからの応答が空でした。安全フィルタ等でブロックされた可能性があります。")

    stripped = text.strip()

    match = re.search(r"```(?:json)?\s*(.*?)\s*```", stripped, re.DOTALL)
    json_str = match.group(1) if match else stripped

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        preview = stripped[:300]
        raise ValueError(
            f"Geminiの応答をJSONとして解析できませんでした: {e}\n"
            f"--- 応答の冒頭300文字 ---\n{preview}"
        ) from e


# --- 1. Instagram投稿生成 ---
def generate_instagram_post(genre: str, target: str, purpose: str, content: str, char_count: int = 600) -> dict:
    brand_rule = load_brand_rules()

    json_template = """{
    "title": "投稿タイトル",
    "catchphrase": "キャッチコピー（1行）",
    "caption": "Instagram本文キャプション",
    "hashtags": "#ハッシュタグ1 #ハッシュタグ2 ...（15〜20個程度）",
    "carousel": ["1スライド目", "2スライド目", "3スライド目", "4スライド目", "5スライド目"],
    "canva_layout": "Canvaでの画像デザイン・レイアウトの具体的な指示",
    "photo_instructions": "撮影現場への写真アングルやライティングの指示",
    "posting_time": "おすすめの投稿曜日・時間帯とその理由",
    "growth_reason": "この投稿がターゲットに響く理由・アルゴリズム上の狙い"
}"""

    system_prompt = (
        "あなたは住宅会社の優秀なSNSマーケター・AI広報です。\n"
        "以下の【ブランドガイドライン】を遵守して投稿を作成してください。\n\n"
        "【ブランドガイドライン】\n"
        + str(brand_rule) + "\n\n"
        "【依頼内容】\n"
        "- 投稿ジャンル: " + str(genre) + "\n"
        "- ターゲット: " + str(target) + "\n"
        "- 投稿目的: " + str(purpose) + "\n"
        "- 伝えたい内容: " + str(content) + "\n"
        "- キャプション文字数目安: " + str(char_count) + "文字程度\n\n"
        "以下のキーを持つ完全なJSONフォーマットのみで出力してください。\n\n"
        + json_template
    )

    response_text = generate_with_fallback(system_prompt)
    return clean_json_response(response_text)


# --- 2. リール企画生成 ---
def generate_reel(theme: str, target: str) -> dict:
    brand_rule = load_brand_rules()

    json_template = """{
    "hook": "冒頭3秒のフック（惹きつけるテキストまたは演出）",
    "script": "【0〜3秒】フック\\n【3〜10秒】シーン1の映像とテロップ\\n【10〜20秒】シーン2の映像とテロップ\\n【20〜30秒】まとめ・CTA",
    "music": "おすすめの音源・BGMの雰囲気"
}"""

    system_prompt = (
        "あなたは住宅会社のSNSマーケターです。\n"
        "リール動画の企画案を作成してください。\n\n"
        "【ブランドガイドライン】\n"
        + str(brand_rule) + "\n\n"
        "【条件】\n"
        "- 動画テーマ: " + str(theme) + "\n"
        "- ターゲット: " + str(target) + "\n\n"
        "以下のJSONフォーマットのみで出力してください。\n"
        + json_template
    )

    response_text = generate_with_fallback(system_prompt)
    return clean_json_response(response_text)


# --- 3. ブログ作成 ---
def generate_blog(title_kw: str, target: str) -> str:
    brand_rule = load_brand_rules()

    system_prompt = (
        "あなたは住宅会社のWebライターです。\n"
        "SEOを意識したブログ記事・Web記事を作成してください。\n\n"
        "【ブランドガイドライン】\n"
        + str(brand_rule) + "\n\n"
        "【条件】\n"
        "- キーワード/テーマ: " + str(title_kw) + "\n"
        "- 想定読者: " + str(target) + "\n\n"
        "見出し（H2, H3）を適切に使い、読者が惹き込まれる自然でわかりやすい文章を作成してください。"
    )

    return generate_with_fallback(system_prompt)


# --- 4. 撮影指示書作成 ---
def generate_shooting(house_type: str, highlights: str) -> str:
    brand_rule = load_brand_rules()

    system_prompt = (
        "あなたは住宅建築のプロフェッショナルです。\n"
        "ルームツアー動画やSNS投稿用写真のための「撮影指示書」を作成してください。\n\n"
        "【ブランドガイドライン】\n"
        + str(brand_rule) + "\n\n"
        "【条件】\n"
        "- 物件特徴: " + str(house_type) + "\n"
        "- 見せたいポイント: " + str(highlights) + "\n\n"
        "カメラマンや現場スタッフが迷わないよう、具体的な撮影アングル、時間帯、小物の配置、光の取り込み方などをリスト形式で作成してください。"
    )

    return generate_with_fallback(system_prompt)
