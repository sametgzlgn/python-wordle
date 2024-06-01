import string
import random
import tkinter as tk
import ttkbootstrap as ttk
import threading
from tkinter.font import Font
from tkinter.simpledialog import askstring
from tkinter.messagebox import showwarning,showinfo
from ttkbootstrap.constants import *


kullanilabilir_harfler = string.ascii_lowercase + "şğçöüı"
kelimeler = open("bes_harfli_kelimeler.txt","r")
kelime_listesi = kelimeler.read()
kelimeler.seek(0)
bulmaca = list(random.choice(kelimeler.readlines()))[0:5]
bulmaca_str = str(bulmaca).replace("[","").replace("]","").replace("'","").replace(",","").replace(" ","")
deneme = 0
renkler = []
harfler = bulmaca.copy()
toplam_hak = 5
yanit = ""
cevaplar = []

def yanit():
    global kullanilabilir_kelimeler,bulmaca,renkler,harfler,toplam_hak,deneme,cevaplar_lst,yanit
    while deneme < toplam_hak:
        renkler.append([])
        analiz = bytearray(len(bulmaca) * b"*")
        yeniPencere = tk.Tk()
        yeniPencere.withdraw()
        try:
            tahmin = askstring("Wordle","Yanıtınız:",parent=yeniPencere).lower()
        except AttributeError:
            showwarning("Hata","Boş değer giremezsiniz.")
            continue
        yeniPencere.destroy()
        yanit = tahmin
        if tahmin not in cevaplar:
            cevaplar.append(tahmin)
        else:
            showwarning("Hata","Bu giri daha önce yapılmış.")
            continue
        if yanit not in kelime_listesi:
            showwarning("Hata","Yazdığınız kelime listede yok.")
            continue
        if not set(yanit).issubset(set(kullanilabilir_harfler)) or len(yanit) != len(bulmaca):
            showwarning("Hata","Girdiğiniz kelime 5 harfli değil veya kabul edilmeyen bir karakter içeriyor.")
            continue
        for i,z in enumerate(tahmin):
            if z in bulmaca and z in harfler:
                if bulmaca[i] == tahmin[i]:
                    analiz[i] = ord(z)
                    renkler[deneme].append("green")
                    harfler.pop(harfler.index(z))
                    continue
                renkler[deneme].append("yellow")
                harfler.pop(harfler.index(z))
            else:
                renkler[deneme].append("red")
        formatlama()
        if analiz.decode() == tahmin:
            showinfo("Tebrikler","Doğru yanıt!")
            break
        cevaplar_lst.insert(0,"{} - {}".format(tahmin,str(renkler[deneme]).replace("[","").replace("]","").replace("'","")))
        deneme += 1
        harfler = bulmaca.copy()
    kelimeler.close()
    if deneme == toplam_hak:
        showwarning("Hata","Bilemediniz. Doğru yanıt: {}".format(bulmaca_str))

def formatlama():
    global lbl_listesi,deneme,renkler,yanit,kalanhak_lbl
    for i,z in enumerate(lbl_listesi):
        z["background"] = renkler[deneme][i]
        z["text"] = yanit[i]
        z.pack(side=LEFT,padx=25)
        kalanhak_lbl["text"] = "Kalan hak: {}".format(5 - deneme - 1)

pencere = tk.Tk()
pencere.geometry("700x500")
pencere.resizable(False,False)
ttk.Style("darkly")
ana_font = Font(family="Liberation Sans",size=100,weight="bold")
lbl_listesi = [ttk.Label(font=ana_font),ttk.Label(font=ana_font),ttk.Label(font=ana_font),ttk.Label(font=ana_font),ttk.Label(font=ana_font)]
cevaplar_lst = tk.Listbox(height=5,width=70)
cevaplar_lst.pack(side=BOTTOM,pady=25)
kalanhak_lbl = ttk.Label(text="Kalan hak: {}".format(toplam_hak - deneme))
kalanhak_lbl.pack(side=TOP)
pencere.title("Wordle")
thr = threading.Thread(target=yanit)
thr.start()
pencere.mainloop()
