import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import tensorflow as tf
from keras.models import load_model
import serial
import time

ser = serial.Serial('COM3', 9600, timeout=1)
CATEGORIES = ["Cercospora", "Healthy", "Leaf Rust", "Phoma"]

model = tf.keras.models.load_model("CNN.model")

def prepare(file):
    IMG_SIZE = 50
    img_array = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    new_array = cv2.resize(img_array, (IMG_SIZE, IMG_SIZE))
    return new_array.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

def detect(filename):
    prediction = model.predict([prepare(filename)])
    prediction = list(prediction[0])
    print(prediction)
    label = CATEGORIES[prediction.index(max(prediction))]
    print(CATEGORIES[prediction.index(max(prediction))])
    output = str(prediction.index(max(prediction)))
    return output

def openfile():
    global file_path, img, orig_panel, gray_panel, thresh_panel, ft
    file_path = filedialog.askopenfilename()
    ft = detect(file_path)
    img = cv2.imread(file_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    orig_img = Image.fromarray(img)
    orig_img = ImageTk.PhotoImage(orig_img)
    orig_panel.configure(image=orig_img)
    orig_panel.image = orig_img

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray_img = Image.fromarray(gray)
    gray_img = ImageTk.PhotoImage(gray_img)
    gray_panel.configure(image=gray_img)
    gray_panel.image = gray_img

    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    thresh_img = Image.fromarray(thresh)
    thresh_img = ImageTk.PhotoImage(thresh_img)
    thresh_panel.configure(image=thresh_img)
    thresh_panel.image = thresh_img

    process_image()

def process_image():
    global file_path, img, orig_panel, gray_panel, thresh_panel, ft
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    ret, thresh = cv2.threshold(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area > 1000:
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            crop_img = img[y:y+h, x:x+w]
            crop_gray = cv2.cvtColor(crop_img, cv2.COLOR_RGB2GRAY)
            ret, crop_thresh = cv2.threshold(crop_gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
            pixel_count = cv2.countNonZero(crop_thresh)
            total_pixels = crop_thresh.shape[0] * crop_thresh.shape[1]
            percent_white = (pixel_count / total_pixels) * 100
            print(percent_white)
            print(i)
            if int(ft) == 0:
                print(f"Contour {i}: Cercospora")
                output = str(0)
                ser.write(output.encode())
                time.sleep(0.01)
                ser.flush()
                disease = "Cercospora"
            elif int(ft) == 2:
                print(f"Contour {i}: Leaf Rust")
                output = str(1)
                ser.write(output.encode())
                time.sleep(0.01)
                ser.flush()
                disease = "Leaf Rust"
            elif int(ft) == 3:
                print(f"Contour {i}: Phoma")
                output = str(2)
                ser.write(output.encode())
                time.sleep(0.01)
                ser.flush()
                disease = "Phoma"
            else:
                print(f"Contour {i}: Healthy leaf")
                disease = "Healthy"
            time.sleep(3)
            cv2.imshow("Crop " + str(i), crop_img)
            disease_label.config(text=disease)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img = ImageTk.PhotoImage(img)
            orig_panel.configure(image=img)
            orig_panel.image = img
    cv2.destroyAllWindows()

root = tk.Tk()
root.title("Leaf Disease Classification")
root.geometry("800x600")

label = tk.Label(root, text="Select an image to classify:")
label.pack()

button = tk.Button(root, text="Open File", command=openfile)
button.pack()

orig_panel = tk.Label(root)
orig_panel.pack(side="left", padx=10, pady=10)
gray_panel = tk.Label(root)
gray_panel.pack(side="left", padx=10, pady=10)
thresh_panel = tk.Label(root)
thresh_panel.pack(side="left", padx=10, pady=10)

disease_label = tk.Label(root, text="")
disease_label.pack()

root.mainloop()
