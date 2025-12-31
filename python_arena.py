import random

class Karakter:
    def __init__(self, isim, can, guc):
        self.isim = isim
        self.can = can
        self.guc = guc
    
    def saldir(self, hedef):
        print(f"{self.isim} saldırıyor!")
        hedef.hasar_al(self.guc)
    
    def hasar_al(self, miktar):
        self.can -= miktar
        if self.can <= 0: self.can = 0
        print(f"{self.isim}, {miktar} hasar aldı! Kalan can {self.can}\n")
        
    def kendini_tanit(self):
        print(f"Adım {self.isim}, can değerim {self.can}, gücüm {self.guc}")
        
    @staticmethod
    def oyun_kurallari():
        print("Bu bir ölüm kalım savaşıdır, son hayatta kalan kazanır!")
        
    @classmethod
    def standart_savasci(cls, isim):
        return cls(isim, 80, 5, 2)

class Savasci(Karakter):
    def __init__(self, isim, can, guc, zirh):
        self.zirh = zirh
        super().__init__(isim, can, guc)
    
    def hasar_al(self, miktar):
        zirh_hasari = miktar * 0.1
        can_hasari = miktar * 0.9
        self.zirh -= zirh_hasari
        self.can -= can_hasari
        if self.can <= 0: 
            self.can = 0
            return
        if self.zirh <= 0:
            self.zirh = 0
            print(f"{self.isim}, zırhı tükendi!\n")
            if random.random() <= 0.5:
                self.guc = 20
                print("Güç artışı! %100")
        print(f"{self.isim} hasar aldı! Kalan zırh {self.zirh: .2f}, kalan can {self.can: .2f}\n")
        
class Canavar(Karakter):
    def __init__(self, isim, can, guc):
        super().__init__(isim, can, guc)
    
    def saldir(self, hedef):
        if hedef.can <= 30:
            print(f"{self.isim}, yaralı düşman tespit etti, verdiği hasar arttı!")
            hedef.hasar_al(self.guc * 2)
        else:
            hedef.hasar_al(self.guc)
        
class Buyucu(Karakter):
    def __init__(self, isim, can, guc):
        super().__init__(isim, can, guc)
        self.mana = 60
    
    def saldir(self, hedef):
        if self.mana >= 10:
            self.mana -= 10
            hedef.hasar_al(self.guc)
            print(f"Kalan mana {self.mana}")
        else:
            print("Yetersiz mana, hasar düştü!")
            yeni_hasar = self.guc * 0.5
            hedef.hasar_al(yeni_hasar)
            
    @classmethod
    def efsanevi_buyucu(cls, isim):
        yeni_buyucu = cls(isim, 100, 20)
        yeni_buyucu.mana = 80
        return yeni_buyucu
    
    def spell_atisi(self, hedef):
        self.mana -= 20
        hasar = self.guc * 1.8
        print(f"Kritik vuruş! {self.isim} büyü atışını isabet ettirdi!")
        hedef.hasar_al(hasar)
        
def kazanani_kaydet():
    try:
        with open("kazananlar.txt", 'a', encoding='utf-8') as dosya:
            dosya.write(f"{arena[0].isim}\n")
        print("\n[SİSTEM] Kazanan liderlik tablosuna kaydedildi.")
    except Exception as e:
        print(f"Dosyaya yazılırken hata oluştu: {e}")

def liderlik_tablosunu_goster():
    istatistik = {}
    try:
        with open("kazananlar.txt", 'r', encoding='utf-8') as f:
            satirlar = f.readlines()
            
            for satir in satirlar:
                isim = satir.strip()
                if isim in istatistik:
                    istatistik[isim] += 1
                else:
                    istatistik[isim] = 1
                    
        print("\n --- LİDERLİK TABLOSU ---\n")
        sirali_liste = sorted(istatistik.items(), key=lambda x: x[1], reverse=True)

        for sira, (isim, sayi) in enumerate(sirali_liste, 1):
            print(f"{sira}. {isim}: {sayi} Galibiyet")
    except Exception as e:
        print(f"Hata oluştu: {e}")
        
def listeyi_temizle():
    with open("kazananlar.txt", 'w', encoding='utf-8') as f:
        pass
    print("[SİSTEM] Liderlik tablosu sıfırlandı.")
    
def oyunu_baslat():      
    global arena 
    
    buyucu = Buyucu("Büyücü", 100, 20)
    canavar = Canavar("Canavar", 100, 10)
    savasci = Savasci("Savaşçı", 100, 10, 15)
    efso = Buyucu.efsanevi_buyucu("Ak Gandalf")
    
    arena = [savasci, canavar, buyucu, efso]
    
    print("\n--- YENİ SAVAŞ BAŞLIYOR! ---\n")        
    while len(arena) > 1:
        for saldiran in arena:
            potansiyel_hedefler = [k for k in arena if k != saldiran]
            print(f"Saldıran: {saldiran.isim}")
            if not potansiyel_hedefler: break
            hedef = random.choice(potansiyel_hedefler)
            print(f"Hedef: {hedef.isim}\n")
            if saldiran == efso and saldiran.mana >= 20:
                if random.random() < 0.2:
                    saldiran.spell_atisi(hedef)
                else:
                    saldiran.saldir(hedef)
            else:
                saldiran.saldir(hedef)
            if hedef.can <= 0:
                print(f"{hedef.isim} elendi!")
                arena.remove(hedef)
        print("\n--- TUR SONU ---\n")
        
    print(f"Kazanan: {arena[0].isim}\n")

while True:
    print("--Menü--\n1: Oyunu başlat\n2: Liderlik tablosunu göster\n3: Kazananı kaydet\n4: Listeyi temizle")
    secim = input("Seçiminiz: ")
    try:
        if secim == '1':
            oyunu_baslat()
        elif secim == '2':
            liderlik_tablosunu_goster()
        elif secim == '3':
            kazanani_kaydet()
        elif secim == '4':
            listeyi_temizle()
    except KeyError:
        print("Sadece numara girin!")
    