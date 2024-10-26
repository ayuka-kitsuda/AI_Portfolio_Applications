import streamlit as st
import torch
import torchvision.transforms as transforms
import torch.nn as nn
import torchvision.models as models
from torchvision.models import ViT_B_16_Weights
from PIL import Image

st.header("ポートフォリオ", divider="gray")

pages = st.navigation([st.Page("app_pages/imageRecognition.py", title="画像認識アプリ"),
                       st.Page("app_pages/chatbot.py", title="チャットボットアプリ"),
                       st.Page("app_pages/emotion.py", title="感情分析アプリ")])
pages.run()