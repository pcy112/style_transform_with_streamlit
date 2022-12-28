import torch
import torch.onnx
from PIL import Image

from fnst import train_learner, Stylizer
import streamlit as st

# we will use the conecpt of caching here that is once a user has used a particular model instead of loading
# it again and again everytime they use it we will cache the model.

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def stylizing(model_path, output_path, input_image):
    torch.cuda.empty_cache()
    with torch.no_grad():
        stl = Stylizer(model_path, output_path)
        img = stl.stylize(input_image)
        img = img.detach().clamp(0, 255).cpu().numpy()
        img = img.transpose(1, 2, 0).astype("uint8")
        img = Image.fromarray(img)
        return img

@st.cache
def train(style_image, im_size, epochs):
    torch.cuda.empty_cache()
    model_path = train_learner(style_image, im_size, epochs)
    return model_path

def main():
    pass

if __name__ == "__main__":
    main()