import cv2 as cv
import numpy as np
import tkinter as tk
from tkinter import filedialog #GUI oluşturmak için kullanılır
from PIL import Image, ImageTk #bu kütüphane görüntüleri işlemek ve GUI üzerinde göstermek için kullanılır

# tkinter penceremiz
pencere = tk.Tk()
pencere.title("Görüntü İşleme")

#global değişkenlerimiz her yerde kullanmak için
resim = None #PIL formatında görsel saklar
resim_cv = None #opencv formatında bir görsel saklar
panel = None #guı paneli


# görüntüyü GUI de açmak için
def resim_sec():
    global resim, resim_cv, panel
    #kullanıcının dosya yolu ile bir görüntü dosyası seçmesini sağlıcak
    dosya_yolu = filedialog.askopenfilename(filetypes=[("Görüntü Dosyaları", "*.jpg;*.jpeg;*.png")])

    if dosya_yolu:

        resim_cv = cv.imread(dosya_yolu)
        resim_cv = cv.cvtColor(resim_cv, cv.COLOR_BGR2RGB)  # görüntüyü BGR den RGB ye çeviricek
        resim = Image.fromarray(resim_cv)  # Opencv de okunan görüntüyü PIL yapar
        resim_tk = ImageTk.PhotoImage(resim) # görüntüyü GUI üzerinde gösterilebilir hale getirir

        if panel is None: #panelin oluşup oluşmadığının kontrolü için
            #eğer panel oluşmamışsa
            panel = tk.Label(pencere, image=resim_tk) #bir label oluşturup içine seçilen resmi koyduk
            panel.image = resim_tk #görüntüyü referanslama işlemi yaptık
            #nedeni ise guı de otomatik olarak hafızada görüntüyü tutması için aksi takdirde görüntü kaybolur
            panel.pack(padx=10, pady=10)#panelin penceredeki boyutları
        else:#eğer panel zaten oluşmuşsa
            panel.configure(image=resim_tk)#mevcut olan labelı yeniler yeni seçilen görüntüyü tutar
            panel.image = resim_tk#yine referanslama işlemi


def gri_donusum():
    global resim_cv, panel
    if resim_cv is not None:#görüntü var mı yok mu

        # dot metodu sayesinde her pikselin gri tonunu hesaplarız
        # bunu kullanabilirmiyiz kullanamazmıyız tam emin olamadım o yüzden formulunu koycam
        # Formül: 0.299 * R + 0.587 * G + 0.114 * B en kötü manuel bunu tanımlarız
        #:3 anlamı ilk 3 kanal üzerinde işlem yapacak
        gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114])

        #gri ton değerleri tamsayıya (0-255) aralığına dönüştürülür
        gri_image = Image.fromarray(gri.astype(np.uint8))

        #PIL formtaındaki görüntüyü tkinterda gösterebilecek hale getirir
        gri_tk = ImageTk.PhotoImage(gri_image)

        #görsel panel güncellemeleri klasik
        panel.configure(image=gri_tk)
        panel.image = gri_tk



def binary_donusum(esik=127):
    global resim_cv, panel

    if resim_cv is not None:#görüntü var mı yok mu

      #dot metodu sayesinde her pikselin gri tonunu hesaplarız
      #bunu kullanabilirmiyiz kullanamazmıyız tam emin olamadım o yüzden formulunu koycam
      #Formül: 0.299 * R + 0.587 * G + 0.114 * B
      #:3 anlamı ilk 3 kanal üzerinde işlem yapacak
        gri = np.dot(resim_cv[..., :3], [0.299, 0.587, 0.114])

      #piksel değeri eşikten büyükse 255, değilse 0 yap
        binary = (gri > esik) * 255


      # 8 bite çevirir numpy dizisinden yani görüntüyü standart bir formatta saklamayı sağlar
        binary_image = Image.fromarray(binary.astype(np.uint8))

      #binary formtaındaki görüntüyü tkinterda gösterebilecek hale getirir
        binary_tk = ImageTk.PhotoImage(binary_image)

      #mevcut panel güncellemeleri klasik
        panel.configure(image=binary_tk)
        panel.image = binary_tk



def goruntu_dondur(aci=45):#açıyı 45 istemiş
    global resim_cv, panel

    if resim_cv is not None:

        #görüntünün yüksekliğini ve genişliğini belirledik bu değerler döndürme işlemi sırasında gereklidir.
        yukseklik, genislik = resim_cv.shape[:2]

       #açısal hesaplamalar
        aci_radyan = np.radians(aci)
        cos_aci, sin_aci = np.cos(aci_radyan), np.sin(aci_radyan)

        #yaptığımız döndürme sonucunda görüntünün genişliği ve yüksekliği
        #görüntünün yeni boyutları hem döndürme matrisinin hemde mevcut matris boyutları ile belirlenir
        yeni_genislik = int(abs(genislik * cos_aci) + abs(yukseklik * sin_aci))
        yeni_yukseklik = int(abs(genislik * sin_aci) + abs(yukseklik * cos_aci))

        #yeni görüntü için boş bir matris bu boş matris döndürme sonrasında piksellerin yerleştirilmesi içimdir
        yeni_img = np.zeros((yeni_yukseklik, yeni_genislik, 3), dtype=np.uint8)

        #yeni ve eski görüntülerin merkez koordinatları hesaplanır
        # bu değerler, piksel dönüşümlerinde referans noktası olarak kullanılır.
        cx, cy = yeni_genislik // 2, yeni_yukseklik // 2
        eski_cx, eski_cy = genislik // 2, yukseklik // 2


        for y in range(yeni_yukseklik):
            for x in range(yeni_genislik):

                #yeni görüntüdeki bir pikselin eski görüntüde nereye denk geldiği bulunur
                #cx cy merkez noktalarıdır
                #matematiksel dönüşüm yapılarak x ve y koordinatları cos ve sin ile eski görüntüye haritalanıyor
                eski_x = int((x - cx) * cos_aci+ (y - cy) * sin_aci + eski_cx)
                eski_y = int(-(x - cx) * sin_aci+ (y - cy) * cos_aci + eski_cy)

                #bu koşul hesaplanan eski koordinatların orijinal görüntünün içinde olup olmadığına bakar
                if 0 <= eski_x < genislik and 0 <= eski_y < yukseklik:

                    #eğer koordinatlar geçerli ise eski görüntüdeki pikseller yeni görüntüdeki piksellere atanır
                    yeni_img[y, x] = resim_cv[eski_y, eski_x]

        #yeni resim bir numpy dizisi olarak saklanır ve bu diziyi fromarray ile resme çevirir
        dondurulmus_resim = Image.fromarray(yeni_img)

        #görüntüyü arayüzde gösterir güncellemeler yapar
        dondurulmus_tk = ImageTk.PhotoImage(dondurulmus_resim)
        panel.configure(image=dondurulmus_tk)
        panel.image = dondurulmus_tk


#guı elemanlarımız genellikle buton ve onlara basıldığında çalışacak metotlar
btn_sec = tk.Button(pencere, text="Görüntü Seç", command=resim_sec)
btn_sec.pack(pady=5)

btn_gri = tk.Button(pencere, text="Manuel Gri Dönüşüm", command=gri_donusum)
btn_gri.pack(pady=5)
#127 eşik değerimiz
btn_binary = tk.Button(pencere, text="Manuel Binary Dönüşüm", command=lambda: binary_donusum(127))
btn_binary.pack(pady=5)
#45 derece dondurur
btn_dondur = tk.Button(pencere, text="Manuel Görüntü Döndür", command=lambda: goruntu_dondur(45))
btn_dondur.pack(pady=5)

#tkinter'ı başlatmamız için ve sürekli çalıştırır butona tıklama vs olur bu yuzden
pencere.mainloop()
