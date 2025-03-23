import numpy as np
import cv2 as cv


class GeometrikIslemler:


    def buyutme(self,resim):
        satirr = resim.shape[0]
        sutunn = resim.shape[1]
        yeni_satir = satirr * 2
        yeni_sutun = sutunn * 2
        yeniimg = np.zeros((yeni_satir, yeni_sutun, resim.shape[2]), dtype=np.uint8)

        for i in range(satirr):
            for j in range(sutunn):

                piksel = resim[i, j]


                yeniimg[i * 2, j * 2] = piksel
                yeniimg[i * 2 + 1, j * 2] = piksel
                yeniimg[i * 2, j * 2 + 1] = piksel
                yeniimg[i * 2 + 1, j * 2 + 1] = piksel

        print(resim.shape)

        return yeniimg

    def kucultme(self,resim):
        satir = resim.shape[0]
        sutun = resim.shape[1]


        yeni_satir = int(satir / 2)
        yeni_sutun = int(sutun / 2)


        yeniimg = np.zeros((yeni_satir, yeni_sutun, resim.shape[2]), dtype=np.uint8)

        for i in range(0, satir - 1, 2):
            for j in range(0, sutun - 1, 2):

                piksel = np.mean(resim[i:i + 2, j:j + 2], axis=(0, 1)).astype(int)
                yeniimg[i // 2, j // 2] = piksel


        return yeniimg

    def oteleme(self,resim,a,b):
        satir = resim.shape[0]
        sutun = resim.shape[1]

        yeniimg=np.zeros((satir,sutun,resim.shape[2]),dtype=np.uint8)

        for i in range(satir-a):
            for j in range(sutun-b):
                piksel = resim[i, j]
                yeniimg[i + a, j + b] = piksel



        return yeniimg
class AritmetikIslemler:
    img = cv.imread("resim11.jpg")  # 359 satır 640 sütun
    img2=cv.imread("resim12.png")
    def toplama(self,aresim,bresim):

        satir = aresim.shape[0]
        sutun = aresim.shape[1]
        yeniimg = np.zeros((satir, sutun, aresim.shape[2]), dtype=np.uint8)
        if aresim.shape == bresim.shape:
            for i in range(satir):
                for j in range(sutun):
                    yeniimg[i,j]=aresim[i,j]+bresim[i,j]

            return yeniimg
        else:
            return None

    def Cikarma(self,aresim,bresim):

        satir = aresim.shape[0]
        sutun = aresim.shape[1]
        yeniimg = np.zeros((satir, sutun, aresim.shape[2]), dtype=np.uint8)
        if aresim.shape == bresim.shape:
            for i in range(satir):
                for j in range(sutun):
                    yeniimg[i,j]=aresim[i,j]-bresim[i,j]
            return yeniimg
        else:
            return None

    def Carpma(self,aresim,bresim):
        satir = aresim.shape[0]
        sutun = aresim.shape[1]
        yeniimg = np.zeros((satir, sutun, aresim.shape[2]), dtype=np.uint8)
        if aresim.shape == bresim.shape:
            for i in range(satir):
                for j in range(sutun):
                    yeniimg[i, j] = aresim[i, j] * bresim[i, j]
            return yeniimg
        else:
            return None



class Parlaklik:

    def parlaklikarttir(self,resim,deger):
        satirr = resim.shape[0]
        sutunn = resim.shape[1]
        yeniimg = np.zeros((satirr, sutunn, resim.shape[2]), dtype=np.uint8)

        if deger>0:
            for i in range(satirr):
                for j in range(sutunn):
                    if resim[i,j]+deger>255:
                        yeniimg[i, j]=255
                    else:
                        yeniimg[i,j]=resim[i,j]+deger

            cv.imshow("weer",yeniimg)
        else:
            return None

    def ParlaklikAzalt(self,resim,deger):
        print(resim)








a=Parlaklik()
img = cv.imread("camermaan.jpg")
img2 = cv.imread("resim12.png")
a.ParlaklikAzalt(img,60)
cv.waitKey(0)
cv.destroyAllWindows()
