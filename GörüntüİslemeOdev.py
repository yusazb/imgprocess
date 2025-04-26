import numpy as np
import matplotlib.pyplot as plt
import imageio.v2 as imageio
import random
import cv2 as cv
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

def load_grayscale_image(path):
    img = imageio.imread(path)
    if len(img.shape) == 3:
        img = np.dot(img[..., :3], [0.2989, 0.5870, 0.1140])
    return img.astype(np.uint8)

def threshold(image, thresh):
    return np.where(image >= thresh, 255, 0).astype(np.uint8)


def esikleme_uygula():
    global resim_cv, panel
    if resim_cv is not None:
        # Eşik değeri penceresini açalım
        esik_degeri = simpledialog.askinteger("Eşik Değeri", "Bir eşik değeri girin:", minvalue=0, maxvalue=255,
                                              initialvalue=127)

        # Eğer geçerli bir eşik değeri girildiyse
        if esik_degeri is not None:
            gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114])
            esiklenmis = threshold(gri, esik_degeri)
            esiklenmis_image = Image.fromarray(esiklenmis)
            esiklenmis_tk = ImageTk.PhotoImage(esiklenmis_image)
            panel.configure(image=esiklenmis_tk)
            panel.image = esiklenmis_tk


def sobel_edge_detection(image):
    Gx = np.array([[-1, 0, 1],
                   [-2, 0, 2],
                   [-1, 0, 1]])
    Gy = np.array([[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]])
    img = image.astype(float)
    height, width = img.shape
    result = np.zeros((height, width))
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            region = img[i-1:i+2, j-1:j+2]
            sx = np.sum(Gx * region)
            sy = np.sum(Gy * region)
            result[i, j] = np.sqrt(sx**2 + sy**2)
    return np.clip(result, 0, 255).astype(np.uint8)

def add_salt_and_pepper_noise(image, amount=0.05):
    noisy = image.copy()
    total = image.size
    num_noise = int(total * amount)
    for _ in range(num_noise):
        i = random.randint(0, image.shape[0] - 1)
        j = random.randint(0, image.shape[1] - 1)
        noisy[i, j] = 0 if random.random() < 0.5 else 255
    return noisy

def mean_filter(image):
    padded = np.pad(image, ((1, 1), (1, 1)), mode='edge')
    filtered = np.zeros_like(image)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            region = padded[i:i+3, j:j+3]
            filtered[i, j] = np.mean(region)
    return filtered.astype(np.uint8)

# Ana pencere
pencere = tk.Tk()
pencere.title("🔍 Görüntü İşleme Arayüzü")
pencere.geometry("1000x700")
pencere.configure(bg="#f0f0f0")

# Başlık
baslik = tk.Label(pencere, text="Görüntü İşleme Uygulaması", font=("Helvetica", 24, "bold"), bg="#f0f0f0")
baslik.pack(pady=20)

# Frame oluştur (Butonlar ve Resim için ayrı)
frame_buttons = tk.Frame(pencere, bg="#f0f0f0")
frame_buttons.pack(side="left", padx=20, pady=20)

frame_image = tk.Frame(pencere, bd=2, relief="groove")
frame_image.pack(side="right", padx=20, pady=20)

# Global değişkenler
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
            panel = tk.Label(frame_image, image=resim_tk)
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

def sobel_uygula():
    global resim_cv, panel
    if resim_cv is not None:
        gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114])
        kenar = sobel_edge_detection(gri)
        kenar_image = Image.fromarray(kenar)
        kenar_tk = ImageTk.PhotoImage(kenar_image)
        panel.configure(image=kenar_tk)
        panel.image = kenar_tk

def gurultu_ekle():
    global resim_cv, panel
    if resim_cv is not None:
        gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114])
        noisy = add_salt_and_pepper_noise(gri)
        noisy_image = Image.fromarray(noisy)
        noisy_tk = ImageTk.PhotoImage(noisy_image)
        panel.configure(image=noisy_tk)
        panel.image = noisy_tk

def ortalama_filtre_uygula():
    global resim_cv, panel
    if resim_cv is not None:
        gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114])
        filtered = mean_filter(gri)
        filtered_image = Image.fromarray(filtered)
        filtered_tk = ImageTk.PhotoImage(filtered_image)
        panel.configure(image=filtered_tk)
        panel.image = filtered_tk


def buton(text, command, row, col):
    btn = tk.Button(frame_buttons, text=text, command=command, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
    btn.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

# Butonları grid sisteminde yerleştir
buton("Görüntü Seç", resim_sec, 0, 0)
buton("Gri Dönüşüm", gri_donusum, 1, 0)
buton("Binary Dönüşüm", lambda: binary_donusum(127), 2, 0)
buton("Görüntü Döndür", lambda: goruntu_dondur(45), 3, 0)
buton("Sobel Kenar", sobel_uygula, 4, 0)
buton("Gürültü Ekle", gurultu_ekle, 5, 0)
buton("Ortalama Filtre", ortalama_filtre_uygula, 6, 0)
buton("Eşikleme", lambda :esikleme_uygula(),7,0)

# Çalıştır
pencere.mainloop()
