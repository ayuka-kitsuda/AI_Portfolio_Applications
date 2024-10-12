import streamlit as st
import torch
import torchvision.transforms as transforms
import torch.nn as nn
import torchvision.models as models
from torchvision.models import ViT_B_16_Weights
from PIL import Image

st.title("ポートフォリオ")

pages = st.navigation([st.Page("pages/imageRecognition.py", title="画像認識アプリ"),
                       st.Page("pages/chatbot.py", title="チャットボットアプリ")])
pages.run()