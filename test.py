import streamlit as st
from PIL import Image
from io import BytesIO

input_path = "./test/input.jpg"

# 이미지를 바이트로 바꾸어 주는 함수
# st.download_button은 바이트 데이터만 읽을 수 있음
def image_to_byte(img):
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    return buffer

# text 써보기
st.write("# 내 페이지")
st.write("### 테스트 페이지입니다.")

# 사이드 바 만들기
side_list = ['내용1', '내용2', '내용3', '내용4']
style_name = st.sidebar.selectbox(
    'Select Style',
    side_list
)

# 사진 업로드
img = None
uploaded_file = st.file_uploader(
    "이미지를 골라주세요", type=["jpg", "jpeg"], key = 'img')

# 파일이 업로드 됐는지 확인
if uploaded_file:
    #업로드한 이미지 열기
    img = Image.open(uploaded_file)
    img.save(input_path, "JPEG")
    
    # 업로드한 이미지 띄워주기
    st.image(img, caption='내가 올린 이미지', use_column_width=True)
    
    # 숫자를 고를 수 있는 슬라이더 만들기
    num = st.select_slider(
            '숫자를 골라주세요',
            options=[1, 2, 3, 4, 5])
    st.write(num)
    
    # 이미지를 내려 받을 수 있는 버튼 만들기
    st.download_button(
        label="이미지 다운로드",
        data=image_to_byte(img),
        file_name='output_img.jpg'
    )