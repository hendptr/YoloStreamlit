import cv2
import streamlit as st
import torch

st.title("Uji Yolo Live (YoloV5s) Streamlit")
run = st.checkbox('Run')
FRAME_WINDOW = st.image([])
camera = cv2.VideoCapture(0)

array_img = []
array_label = []

widget = st.empty()

import requests

def upload(image):
    reqUrl = "http://127.0.0.1:8000/upload"
    
    post_files = {
    "image": image,
    }
    headersList = {
    "Accept": "*/*",
    "User-Agent": "Thunder Client (https://www.thunderclient.com)" 
    }

    payload = ""

    response = requests.request("POST", reqUrl, data=payload, files=post_files, headers=headersList)

    print(response.text)


def detect(img, data):
    data = data.to_numpy()
    n = len(data)
    label = ''
    for i in range(n):
        xmin = int(data[i][0])
        ymin = int(data[i][1])
        xmax = int(data[i][2])
        ymax = int(data[i][3])
        label = data[i][6]
        
        (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
        cv2.rectangle(img, (xmin, ymin - 25), (xmin + (w+50), ymin), (204, 204, 0), -1)
        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (255, 255, 0), 2)
        cv2.putText(img, label.capitalize(), (xmin, ymin-10), cv2.FONT_HERSHEY_TRIPLEX, 0.7, (255,255,255), 2)
    if len(label) >2:   
        return label, img[ymin:ymax, xmin:xmax]
    else:
        return 'exit'

        

def run_cv2():
    while run:
        _, frame = camera.read()
        orr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        upload(frame)

        FRAME_WINDOW.image(orr)


    else:
        st.write('Stopped')
        for i in range(len(array_img)):
            st.write(array_img[i][0])

run_cv2()
