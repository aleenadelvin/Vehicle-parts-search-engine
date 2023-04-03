import streamlit as st 
import os
from PIL import Image
import tensorflow
from tensorflow.keras.applications.resnet50 import preprocess_input, ResNet50
from keras.layers import GlobalMaxPooling2D
import cv2
import numpy as np
from numpy.linalg import norm
import pickle
from  sklearn.neighbors import NearestNeighbors
  
feature_list=np.array(pickle.load(open("featurevector.pkl","rb")))
filenames=pickle.load(open("filenames.pkl","rb"))

model=ResNet50(weights='imagenet',include_top=False,input_shape=(224,224,3))
model.trainable=False
 
model=tensorflow.keras.Sequential([model, GlobalMaxPooling2D()])
st.title('Image Search Engine')

def save_uploaded_file(uploaded_file):
    try:
        with open(os.path.join('uploads', uploaded_file.name),'wb') as f:
            f.write(uploaded_file.getbuffer())
            return 1
    except:
        return 0
def extract_feature(img_path, model):
    img=cv2.imread(img_path)
    img=cv2.resize(img,(224,224))
    img=np.array(img)
    expand_img=np.expand_dims(img, axis=0)
    pre_img=preprocess_input(expand_img)
    result=model.predict(pre_img).flatten()
    normalized=result/norm(result)
    return normalized

def recommend(faetures,feature_list):
    neighbors=NearestNeighbors(n_neighbors=6,algorithm="brute", metric="euclidean")
    neighbors.fit(feature_list)
    distance, indices = neighbors.kneighbors([features])
    return indices


#steps
#file upload
uploaded_file = st.file_uploader("choose an image")
print(uploaded_file)
if uploaded_file is not None:
    if save_uploaded_file(uploaded_file):
        #display the file
        display_image =Image.open(uploaded_file)
        resized_img = display_image.resize((200,200))
        st.image(resized_img)
        #feature extract
        features = extract_feature(os.path.join("uploads", uploaded_file.name),model)
        st.text(features)
        # recommendation
        indices = recommend(features,feature_list)   
        #show

        col1,col2,col3,col4,col5 = st.columns(5)

        with col1:
            st.image(filenames[indices[0][0]])
        with col2:
            st.image(filenames[indices[0][1]])
        with col3:
            st.image(filenames[indices[0][2]])
        with col4:
            st.image(filenames[indices[0][3]])
        with col5:
            st.image(filenames[indices[0][4]])
    else:
        st.header("some error occured in file upload")
           