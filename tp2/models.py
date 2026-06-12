import json
import os


class Gorev:
    def __init__(self, baslik, tarih, onem_derecesi, tamamlandi=False):
        self.baslik = baslik
        self.tarih = tarih
        self.onem_derecesi = onem_derecesi
        self.tamamlandi = tamamlandi

    def sozluge_cevir(self):
        return {
            "baslik": self.baslik,
            "tarih": self.tarih,
            "onem_derecesi": self.onem_derecesi,
            "tamamlandi": self.tamamlandi
        }


class AjandaYoneticisi:
    def __init__(self, dosya_adi="gorevler.json"):
        self.dosya_adi = dosya_adi
        self.gorevler = []
        self.verileri_yukle()

    def gorev_ekle(self, gorev):
        self.gorevler.append(gorev)
        self.verileri_kaydet()

    def gorev_tamamla(self, index):
        if 0 <= index < len(self.gorevler):
            self.gorevler[index].tamamlandi = True
            self.verileri_kaydet()

    # YENİ EKLENEN: Görev Silme Fonksiyonu
    def gorev_sil(self, index):
        if 0 <= index < len(self.gorevler):
            del self.gorevler[index]
            self.verileri_kaydet()

    # YENİ EKLENEN: Görev Güncelleme Fonksiyonu
    def gorev_guncelle(self, index, baslik, tarih, onem_derecesi):
        if 0 <= index < len(self.gorevler):
            self.gorevler[index].baslik = baslik
            self.gorevler[index].tarih = tarih
            self.gorevler[index].onem_derecesi = onem_derecesi
            self.verileri_kaydet()

    def verileri_kaydet(self):
        try:
            with open(self.dosya_adi, "w", encoding="utf-8") as dosya:
                json.dump([g.sozluge_cevir() for g in self.gorevler], dosya, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Kayıt sırasında hata oluştu: {e}")

    def verileri_yukle(self):
        try:
            if os.path.exists(self.dosya_adi):
                with open(self.dosya_adi, "r", encoding="utf-8") as dosya:
                    veriler = json.load(dosya)
                    self.gorevler = [Gorev(**veri) for veri in veriler]
        except FileNotFoundError:
            self.gorevler = []
        except json.JSONDecodeError:
            self.gorevler = []

    def rapor_uret(self):
        toplam = len(self.gorevler)
        tamamlanan = sum(1 for g in self.gorevler if g.tamamlandi)
        kalan = toplam - tamamlanan
        yuksek_onemli = sum(1 for g in self.gorevler if g.onem_derecesi == "Yüksek" and not g.tamamlandi)

        return {
            "Toplam Görev": toplam,
            "Tamamlanan": tamamlanan,
            "Bekleyen": kalan,
            "Yüksek Öncelikli Bekleyen": yuksek_onemli
        }