import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random
import imageio.v2 as imageio

# tkinter penceremiz
pencere = tk.Tk()
pencere.title("Görüntü İşleme")

# global değişkenler
resim = None
resim_cv = None
panel = None

def resim_sec():
    global resim, resim_cv, panel
    dosya_yolu = filedialog.askopenfilename(filetypes=[("Görüntü Dosyaları", "*.jpg;*.jpeg;*.png")])

    if dosya_yolu:
        resim_cv = cv.imread(dosya_yolu)
        resim_cv = cv.cvtColor(resim_cv, cv.COLOR_BGR2RGB)
        resim = Image.fromarray(resim_cv)
        resim_tk = ImageTk.PhotoImage(resim)

        if panel is None:
            panel = tk.Label(pencere, image=resim_tk)
            panel.image = resim_tk
            panel.pack(padx=10, pady=10)
        else:
            panel.configure(image=resim_tk)
            panel.image = resim_tk

def gri_donusum():
    global resim_cv, panel
    if resim_cv is not None:
        gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114])
        gri_image = Image.fromarray(gri.astype(np.uint8))
        gri_tk = ImageTk.PhotoImage(gri_image)
        panel.configure(image=gri_tk)
        panel.image = gri_tk

def binary_donusum(esik=127):
    global resim_cv, panel
    if resim_cv is not None:
        gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114])
        binary = (gri > esik) * 255
        binary_image = Image.fromarray(binary.astype(np.uint8))
        binary_tk = ImageTk.PhotoImage(binary_image)
        panel.configure(image=binary_tk)
        panel.image = binary_tk

def goruntu_dondur(aci=45):
    global resim_cv, panel
    if resim_cv is not None:
        yukseklik, genislik = resim_cv.shape[:2]
        aci_radyan = np.radians(aci)
        cos_aci, sin_aci = np.cos(aci_radyan), np.sin(aci_radyan)
        yeni_genislik = int(abs(genislik * cos_aci) + abs(yukseklik * sin_aci))
        yeni_yukseklik = int(abs(genislik * sin_aci) + abs(yukseklik * cos_aci))
        yeni_img = np.zeros((yeni_yukseklik, yeni_genislik, 3), dtype=np.uint8)
        cx, cy = yeni_genislik // 2, yeni_yukseklik // 2
        eski_cx, eski_cy = genislik // 2, yukseklik // 2

        for y in range(yeni_yukseklik):
            for x in range(yeni_genislik):
                eski_x = int((x - cx) * cos_aci + (y - cy) * sin_aci + eski_cx)
                eski_y = int(-(x - cx) * sin_aci + (y - cy) * cos_aci + eski_cy)
                if 0 <= eski_x < genislik and 0 <= eski_y < yukseklik:
                    yeni_img[y, x] = resim_cv[eski_y, eski_x]

        dondurulmus_resim = Image.fromarray(yeni_img)
        dondurulmus_tk = ImageTk.PhotoImage(dondurulmus_resim)
        panel.configure(image=dondurulmus_tk)
        panel.image = dondurulmus_tk

# EKLENEN METOTLAR
def threshold_gui(thresh=127):
    global resim_cv, panel
    if resim_cv is not None:
        gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114])
        thresholded = np.where(gri >= thresh, 255, 0).astype(np.uint8)
        thresh_img = Image.fromarray(thresholded)
        thresh_tk = ImageTk.PhotoImage(thresh_img)
        panel.configure(image=thresh_tk)
        panel.image = thresh_tk

def sobel_gui():
    global resim_cv, panel
    if resim_cv is not None:
        gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114])
        img = gri.astype(float)
        Gx = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
        Gy = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]])
        height, width = img.shape
        result = np.zeros((height, width))

        for i in range(1, height - 1):
            for j in range(1, width - 1):
                region = img[i-1:i+2, j-1:j+2]
                sx = np.sum(Gx * region)
                sy = np.sum(Gy * region)
                result[i, j] = np.sqrt(sx**2 + sy**2)

        sobel_result = np.clip(result, 0, 255).astype(np.uint8)
        sobel_img = Image.fromarray(sobel_result)
        sobel_tk = ImageTk.PhotoImage(sobel_img)
        panel.configure(image=sobel_tk)
        panel.image = sobel_tk

def salt_pepper_gui(amount=0.05):
    global resim_cv, panel
    if resim_cv is not None:
        gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)
        noisy = gri.copy()
        total = noisy.size
        num_noise = int(total * amount)

        for _ in range(num_noise):
            i = random.randint(0, noisy.shape[0] - 1)
            j = random.randint(0, noisy.shape[1] - 1)
            noisy[i, j] = 0 if random.random() < 0.5 else 255

        noisy_img = Image.fromarray(noisy)
        noisy_tk = ImageTk.PhotoImage(noisy_img)
        panel.configure(image=noisy_tk)
        panel.image = noisy_tk

def mean_filter_gui():
    global resim_cv, panel
    if resim_cv is not None:
        gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114]).astype(np.uint8)
        padded = np.pad(gri, ((1, 1), (1, 1)), mode='edge')
        filtered = np.zeros_like(gri)

        for i in range(gri.shape[0]):
            for j in range(gri.shape[1]):
                region = padded[i:i+3, j:j+3]
                filtered[i, j] = np.mean(region)

        filtered_img = Image.fromarray(filtered.astype(np.uint8))
        filtered_tk = ImageTk.PhotoImage(filtered_img)
        panel.configure(image=filtered_tk)
        panel.image = filtered_tk

# GUI ELEMANLARI (BUTONLAR)
btn_sec = tk.Button(pencere, text="Görüntü Seç", command=resim_sec)
btn_sec.pack(pady=5)

btn_gri = tk.Button(pencere, text="Manuel Gri Dönüşüm", command=gri_donusum)
btn_gri.pack(pady=5)

btn_binary = tk.Button(pencere, text="Manuel Binary Dönüşüm", command=lambda: binary_donusum(127))
btn_binary.pack(pady=5)

btn_dondur = tk.Button(pencere, text="Manuel Görüntü Döndür (45°)", command=lambda: goruntu_dondur(45))
btn_dondur.pack(pady=5)

btn_threshold = tk.Button(pencere, text="Eşikleme (Threshold)", command=lambda: threshold_gui(127))
btn_threshold.pack(pady=5)

btn_sobel = tk.Button(pencere, text="Sobel Kenar Algılama", command=sobel_gui)
btn_sobel.pack(pady=5)

btn_noise = tk.Button(pencere, text="Tuz ve Karabiber Gürültüsü Ekle", command=lambda: salt_pepper_gui(0.05))
btn_noise.pack(pady=5)

btn_mean = tk.Button(pencere, text="Ortalama Filtre (Noise Azaltma)", command=mean_filter_gui)
btn_mean.pack(pady=5)

# Tkinter'ı çalıştır
pencere.mainloop()
