import streamlit as st
import openai
import os
from dotenv import load_dotenv

# .envファイルから環境変数を読み込む
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlitアプリのヘッダー
st.subheader("チャットボット")
st.write("ITに関する質問のみを受け付けます。それ以外にはお答えできません。")

# 初期メッセージを保持するためのセッションステートを設定
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "system", "content": "あなたはITに関する質問のみを回答できます。それ以外の質問の場合は「ITに関する質問以外は回答できません。」と返して。文字は100字以内。"}
    ]

# ユーザーからの入力を取得
user_input = st.chat_input("ITに関する質問を入力してください。")



if user_input:
    # メッセージリストにユーザーの入力を追加
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # 現在のメッセージリストを表示
    for message in st.session_state["messages"]:
        # systemのロールは表示しない
        if message["role"] == "system":
            continue
        elif message["role"] == "user":
            with st.chat_message("user"):
                st.write("あなた")
                st.write(message['content'])
        elif message["role"] == "assistant":
            with st.chat_message("assistant"):
                st.write("アシスタント")
                st.write(message["content"])

    # OpenAIのAPIを使って応答を生成
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # または "gpt-3.5-turbo"
            messages=st.session_state["messages"],
        )

        # 応答を取得してメッセージリストに追加
        bot_reply = response.choices[0].message['content']
        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})

        with st.chat_message("assistant"):
            st.write("アシスタント")
            st.write(bot_reply)

        # # Botの応答を表示
        # st.write(f"Bot: {bot_reply}")

    except Exception as e:
        st.error(f"エラーが発生しました: {e}")


