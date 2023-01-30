import streamlit as st
from PIL import Image
import style
import os
from io import BytesIO

# 경로 설정
root_model = "./models"
root_style = "./images/style"
input_path = "./tmp/input.jpg"
style_path = "./tmp/style.jpg"

# 이미지를 바이트로 바꾸어 주는 함수
# byte array: 1비트 단위의 값을 연속적으로 저장하는 시퀀스 자료형(1byte == 8bits)
def image_to_byte(img):
    buffer = BytesIO()
    img.save(buffer, format='JPEG')
    return buffer

# 제목
st.markdown('<p style="font-family:Courier; color:#FFA500; font-size: 40px;">양식 바꾸기</p>', unsafe_allow_html=True)
st.markdown('<p style="font-family:Courier; color:#FF8C00; font-size: 24px;">인공지능을 이용한 나만의 편리한 인터넷!</p>', unsafe_allow_html=True)
# 사이드 바 만들기
models = os.listdir(root_model)
style_name = st.sidebar.selectbox(
    '양식',
    ('custom' if i == len(models) else models[i].split('.')[0] for i in range(len(models) + 1))
)
if style_name != 'custom':
    path_style = os.path.join(root_style, style_name+".jpg")
else:
    path_style = None


# 스타일을 바꿀 사진 업로드
img = None
uploaded_file = st.file_uploader(
    "사진을 선택해주세요", type=["jpg", "jpeg"], key = 'img')

show_file = st.empty()

# 파일이 업로드 됐는지 확인
if uploaded_file:
    # 업로드한 이미지 열기
    img = Image.open(uploaded_file)
    img.save(input_path, "JPEG")
    
    # 업로드한 이미지 띄워주기
    st.image(img, caption="내가 선택한 사진", use_column_width=True)
    
    # 이미 학습된 스타일을 선택하면 스타일 이미지 띄우기
    if path_style != None:
        st.image(path_style, caption='양식을 입힐 사진', use_column_width=True)
    # 커스텀을 선택하면 스타일 이미지를 업로드
    else:
        img2 = None
        uploaded_st_file = st.file_uploader( 
            "입히고 싶은 이미지 선택", type=["jpg", "jpeg"], key = 'style')
        
        # 스타일 이미지가 업로드 됐는지 확인
        if uploaded_st_file:
            img2 = Image.open(uploaded_st_file)
            img2.save(style_path, "JPEG")
            st.image(img2, caption='완성된 사진', use_column_width=True)
            
            # 학습할 때 사용할 이미지들의 크기 선택
            img_size = st.select_slider(
                    '사진의 크기',
                    options=[8,16,32,64,128,256,512])
            st.markdown('<p style="font-family:Courier; color:#8B0000; font-size: 15px;">사진의 크기가 크면 결과는 좋아질 수 있지만 학습이 오래걸리거나 학습이되지 않을 수 있습니다.</p>', unsafe_allow_html=True)
            # 학습 횟수 선택
            epoch = st.select_slider(
                    '학습 횟수',
                    options=[1,2,3,4,5])
            st.markdown('<p style="font-family:Courier; color:#8B0000; font-size: 14px;">학습 횟수가 늘어나면 결과는 좋아질 수도 있지만 그만큼 학습이 오래 걸립니다.</p>', unsafe_allow_html=True)
           
extensions = [".png", ".jpeg", ".jpg"]
if uploaded_file is not None and any(extension in uploaded_file.name for extension in extensions):

    name_file = uploaded_file.name.split(".")
    
    model_path = os.path.join(root_model, style_name+".pth")

    img = img.convert('RGB')
    input_image = img

    root_output = "./images/sample"

    stylize_button = st.button("양식 입히기")
    
    if path_style == None:
        st.markdown('<p style="font-family:Courier; color:#B22222; font-size: 14px;">Streamlit 배포 환경에서는  학습하는 것을 권장하지 않습니다.(약 10시간 이상 필요).PC에서 local로 진행해 주시기 바랍니다.</p>', unsafe_allow_html=True)
          
    if stylize_button:
        try:
            if path_style == None:
                # 새로운 모델 학습하기
                img2 = img2.convert('RGB')
                model_path = style.train(style_path, img_size, epoch)
            # 학습된 모델로 새로운 이미지 만들기
            stylized = style.stylizing(model_path, root_output, input_path)
            
            # 결과 이미지 출력
            st.markdown('<p style="font-family:Courier; color:#32CD32; font-size: 20px;">완성된 사진</p>', unsafe_allow_html=True)
            st.image(stylized, width=400, use_column_width=True)
            # 다운로드 버튼을 눌러 만들어진 이미지 내려받기
            st.download_button(
                label="사진을 내려받기",
                data=image_to_byte(stylized),
                file_name=f"{style_name}_{name_file[0]}.jpg"
            )
            
        except Exception as e:
            st.write(e)
