import streamlit as st
import google.generativeai as genai

# ★ 変更点: APIキーを直接書かず、クラウドの「金庫」から読み込む
API_KEY = st.secrets["GEMINI_API_KEY"]

system_instruction_text = """
あなたは「駅の出口案内AI」です。
ユーザーが「目的地」を入力したら、以下の情報を簡潔に教えてください。

1. **最寄り駅**: どこ駅か
2. **最適な出口**: 何番出口（例: B1出口、中央改札）
3. **徒歩ルート**: 簡単な道順
4. **所要時間**: およその分数

回答は箇条書きでシンプルに。
"""

st.set_page_config(page_title="Station Exit Guide", layout="centered")

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash", 
        system_instruction=system_instruction_text
    )
except Exception as e:
    st.error(f"設定エラー: {e}")

st.title("🚉 Station Exit Guide")
st.caption("目的地を入れるだけで、最適な「駅」と「出口」を案内します。")

destination = st.text_input("目的地を入力してください", placeholder="例: 東京タワー、六本木ヒルズ")

if st.button("案内を開始", type="primary"):
    if destination:
        with st.spinner(f"「{destination}」を検索中..."):
            try:
                response = model.generate_content(destination)
                
                st.markdown("### 📍 案内結果")
                st.markdown(response.text)
                
                # Googleマップボタン
                map_url = f"https://www.google.com/maps/search/?api=1&query={destination}"
                st.link_button("🗺️ Googleマップで見る", map_url)

            except Exception as e:
                st.error(f"エラーが発生しました: {e}")
    else:
        st.warning("目的地を入力してください。")
