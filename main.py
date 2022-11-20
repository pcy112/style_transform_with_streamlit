import streamlit as st
from PIL import Image
import style
import os
from io import BytesIO
import base64
import torch

# style image paths:
root_model = "./models"
root_style = "./images/style"
input_path = "./tmp/input.jpg"
style_path = "./tmp/style.jpg"


# download image function
def get_image_download_link(img, file_name, style_name):
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a style = "color:black" href="data:file/jpg;base64,{img_str}" download="{style_name+"_"+file_name+".jpg"}"><input type="button" value="Download"></a>'
    return href


st.markdown("<h1 style='text-align: center; color: #508DC6;'>Style Transfer</h1>",
            unsafe_allow_html=True)
st.markdown("<h3 style='text-align: right; color: #508DC6;'>앱으로 보는 ai</h3>",
            unsafe_allow_html=True)


main_bg = "./images/pyto.png"
main_bg_ext = "jpg"

st.markdown(
    f"""
    <style>
    .reportview-container {{
        background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()})
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# creating a side bar for picking the style of image
models = os.listdir(root_model)
style_name = st.sidebar.selectbox(
    'Select Style',
    ('custom' if i == len(models) else models[i].split('.')[0] for i in range(len(models) + 1))
)
if style_name != 'custom':
    path_style = os.path.join(root_style, style_name+".jpg")
else:
    path_style = None


# Upload image functionality
img = None
uploaded_file = st.file_uploader(
    "Choose an image...", type=["jpg", "jpeg", "png"], key = 'img')

show_file = st.empty()

# checking if user has uploaded any file
if not uploaded_file:
    show_file.info("Please Upload an Image")
else:
    img = Image.open(uploaded_file)
    img.save(input_path, "JPEG")
    # check required here if file is an image file
    st.image(img, caption='Uploaded Image.', use_column_width=True)
    if path_style != None:
        st.image(path_style, caption='Style Image', use_column_width=True)
        img_size = st.select_slider(
                    'Select a image size',
                    options=[8, 16, 32, 64, 128, 256, 512])
        st.write('이미지 사이즈가 크면 결과는 좋아지지만 크기가 너무 크면 결과가 나오지 않을 수 있습니다.')
    else:
        img2 = None
        uploaded_st_file = st.file_uploader(
            "Choose a style...", type=["jpg", "jpeg", "png"], key = 'style')
        
        if not uploaded_st_file:
            show_file.info("Please Upload an Image")
        else:
            img2 = Image.open(uploaded_st_file)
            img2.save(style_path, "JPEG")
            # check required here if file is an image file
            st.image(img2, caption='Uploaded Style Image.', use_column_width=True)
            
            img_size = st.select_slider(
                    'Select a image size',
                    options=[8, 16, 32, 64, 128, 256, 512])
            st.write('이미지 사이즈가 크면 결과는 좋아지지만 학습이 오래 걸리거나 학습이 되지 않을 수 있습니다.')
            epoch = st.select_slider(
                    'Input epoch',
                    options=[1, 2, 3, 4, 5])
            st.write('학습 횟수가 늘어나면 결과는 좋아질 수도 있지만 그만큼 학습이 오래 걸립니다.')
extensions = [".png", ".jpeg", ".jpg"]

if uploaded_file is not None and any(extension in uploaded_file.name for extension in extensions):

    name_file = uploaded_file.name.split(".")
    
    model_path = os.path.join(root_model, style_name+".pth")

    img = img.convert('RGB')
    input_image = img

    root_output = "./images/sample"

    stylize_button = st.button("Stylize")
    
    if path_style == None:
          st.warning("새로운 스타일을 학습할 때는 시간이 오래 걸리며, 기기에 발열이 있을 수 있습니다.")
          
    if stylize_button:
        try:
            if path_style == None:
                img2 = img2.convert('RGB')
                #with st.spinner("학습 중..."):
                model_path = style.train(style_path, img_size, epoch)
            stylized = style.stylizing(model_path, root_output, input_path)
            # displaying the output image
            st.write("### Output Image")
            # image = Image.open(output_image)
            st.image(stylized, width=400, use_column_width=True)
            st.markdown(get_image_download_link(
                stylized, name_file[0], style_name), unsafe_allow_html=True)
        except Exception as e:
            
            st.error("이미지가 너무 크거나 예기치 못한 문제가 발생하였습니다.\n이미지 크기를 줄이고 다시 시도해 주세요")
            st.write(e)