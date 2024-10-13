import streamlit as st
import torch
import torchvision.transforms as transforms
from PIL import Image
from torch import nn
import torchvision.models as models
from torchvision.models import ViT_B_16_Weights

# モデルのロード関数
@st.cache_resource  # キャッシュすることで効率的にモデルを再利用
def load_model():
    # ViTモデルの構築
    model = models.vit_b_16(weights=ViT_B_16_Weights.IMAGENET1K_V1)
    model.heads[0] = nn.Linear(768, 10)  # CIFAR-10用に出力層を調整

    # ローカルの`trained_model.pth`からstate_dictをロード
    try:
        state_dict = torch.load("trained_model.pth", map_location=torch.device('cpu'))
        model.load_state_dict(state_dict)  # モデルに重みを適用
        model.eval()  # 推論モードに切り替え
    except Exception as e:
        st.error(f"モデルのロード中にエラーが発生しました: {e}")
        raise e  # エラーが出た場合には詳細を表示

    return model

# CIFAR-10のクラスラベル
CIFAR10_CLASSES = [
    "飛行機", "自動車", "鳥", "猫", "鹿",
    "犬", "カエル", "馬", "船", "トラック"
]

# 前処理の定義（学習時と同じ変換を適用）
def transform_image(image):
    transform = transforms.Compose([
        transforms.Resize(256),  # 短辺を256にリサイズ
        transforms.CenterCrop(224),  # 224x224に切り抜き
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return transform(image).unsqueeze(0)  # バッチ次元を追加

# 予測関数
def predict(image, model):
    with torch.no_grad():  # 勾配計算を無効にする
        outputs = model(image)
        _, predicted = torch.max(outputs, 1)  # 最も確率の高いクラスを取得
    return predicted.item()

# StreamlitアプリのUI構成
st.header("画像認識アプリ")

# 横並びにする
col1, col2 = st.columns(2)

# ユーザーからの画像アップロード
with col1:
    uploaded_file = st.file_uploader("画像をアップロードしてください", type=["jpg", "png", "jpeg"])

with col2:
    if uploaded_file is not None:
        # 画像を表示
        image = Image.open(uploaded_file)
        st.image(image, caption="アップロードされた画像", use_column_width=True)

        # モデルをロード
        model = load_model()

        # 画像の前処理と予測
        tensor_image = transform_image(image)  # 画像をテンソルに変換
        predicted_class = predict(tensor_image, model)  # クラスを予測

        # 予測結果を表示
        st.write(f"予測結果: {CIFAR10_CLASSES[predicted_class]}")
