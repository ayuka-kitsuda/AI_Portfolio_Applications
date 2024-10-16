import streamlit as st
from transformers import BertJapaneseTokenizer, BertForSequenceClassification
import torch

# トークナイザとモデルのロード
@st.cache_resource
def load_model():
    tokenizer = BertJapaneseTokenizer.from_pretrained("christian-phu/bert-finetuned-japanese-sentiment")
    model = BertForSequenceClassification.from_pretrained("christian-phu/bert-finetuned-japanese-sentiment")
    return tokenizer, model

# プレースホルダーを作成
with st.spinner("感情分析モデルを読み込んでいます。少々お待ちください。"):
    tokenizer, model = load_model()

# Streamlit UI
st.title("感情分析アプリ")
st.markdown('''
            文章から感情を分析できるアプリです。
            **ポジティブ**・**ネガティブ**・**中立**から選ばれます。
            ''')

# 文章を入力
text = st.text_input("感情を分析したい文章を入力してください:：")

if st.button("分析"):
    if text.strip() == "":
        st.warning("文章を入力してください")
    else:
        try:
            # 入力を表示してデバッグ
            st.write(f"入力された文章: {text}")

            inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=128)
            outputs = model(**inputs)
            prediction = torch.argmax(outputs.logits, dim=-1).item()

            sentiment = {0: "ネガティブ", 1: "中立", 2: "ポジティブ"}
            st.success(f"予測結果: **{sentiment[prediction]}**")
        except Exception as e:
            st.error(f"分析中にエラーが発生しました: {str(e)}")
