import streamlit as st
from PIL import Image
from io import BytesIO

def image_to_byte(img):
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    return buffer

st.write("# 내 페이지")
st.write("## 테스트 페이지입니다.")
d = st.sidebar.selectbox('Select Style',['1개의 사진', '2개의 사진','3개의 사진','4개의 사진'])
for i in range(1, 5):
    if d >= f'{i}개의 사진':
        img = st.file_uploader(f"{i}번째 이미지를 골라주세요", type = ['jpg','jpeg'],key = f'이미지{i}')
        if img:
            img = Image.open(img)
            st.image(img, caption = f"내가 {i}번째로 올린 이미지")
