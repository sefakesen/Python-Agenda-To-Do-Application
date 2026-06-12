import customtkinter as ctk
from tkinter import messagebox
from models import Gorev, AjandaYoneticisi
from utils import tarih_dogrula

# Temayı ayarlıyoruz (Dark mode ve Mavi vurgular)
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AjandaArayuzu(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Modern Görev ve Ajanda Uygulaması")
        self.geometry("850x600")

        self.yonetici = AjandaYoneticisi()
        self.duzenlenen_index = None

        self.arayuz_olustur()
        self.listeyi_guncelle()

    def arayuz_olustur(self):
        # --- ÜST FORM ÇERÇEVESİ ---
        form_frame = ctk.CTkFrame(self, corner_radius=15)
        form_frame.pack(pady=20, padx=20, fill="x")

        # Girdi Alanları (Grid sistemi ile yan yana dizilim)
        ctk.CTkLabel(form_frame, text="Görev Başlığı:", font=("Arial", 14, "bold")).grid(row=0, column=0, padx=10,
                                                                                         pady=15, sticky="w")
        self.entry_baslik = ctk.CTkEntry(form_frame, width=200, placeholder_text="Örn: Proje Sunumu")
        self.entry_baslik.grid(row=0, column=1, padx=10, pady=15)

        ctk.CTkLabel(form_frame, text="Tarih (GG/AA/YYYY):", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=10,
                                                                                              pady=15, sticky="w")
        self.entry_tarih = ctk.CTkEntry(form_frame, width=150, placeholder_text="Örn: 15/04/2026")
        self.entry_tarih.grid(row=0, column=3, padx=10, pady=15)

        ctk.CTkLabel(form_frame, text="Önem:", font=("Arial", 14, "bold")).grid(row=0, column=4, padx=10, pady=15,
                                                                                sticky="w")
        self.combo_onem = ctk.CTkOptionMenu(form_frame, values=["Düşük", "Normal", "Yüksek"])
        self.combo_onem.set("Normal")
        self.combo_onem.grid(row=0, column=5, padx=10, pady=15)

        # Üst Butonlar
        self.btn_ekle = ctk.CTkButton(form_frame, text="Görev Ekle", command=self.gui_gorev_ekle, fg_color="#2ecc71",
                                      hover_color="#27ae60", font=("Arial", 12, "bold"))
        self.btn_ekle.grid(row=1, column=1, columnspan=2, pady=10, sticky="e")

        self.btn_guncelle = ctk.CTkButton(form_frame, text="Değişiklikleri Kaydet", command=self.gui_gorev_kaydet,
                                          state="disabled", fg_color="#f39c12", hover_color="#d68910",
                                          font=("Arial", 12, "bold"))
        self.btn_guncelle.grid(row=1, column=3, columnspan=2, pady=10, sticky="w")

        # --- ORTA LİSTE ÇERÇEVESİ (Kaydırılabilir) ---
        self.liste_frame = ctk.CTkScrollableFrame(self, label_text="📋 Görevleriniz", label_font=("Arial", 16, "bold"),
                                                  corner_radius=15)
        self.liste_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # --- ALT RAPOR ÇERÇEVESİ ---
        alt_frame = ctk.CTkFrame(self, fg_color="transparent")
        alt_frame.pack(pady=10, padx=20, fill="x")

        btn_rapor = ctk.CTkButton(alt_frame, text="📊 Raporları Göster", command=self.gui_rapor_goster,
                                  fg_color="#9b59b6", hover_color="#8e44ad", font=("Arial", 14, "bold"), height=40)
        btn_rapor.pack(side="right")

    def kutulari_temizle(self):
        self.entry_baslik.delete(0, ctk.END)
        self.entry_tarih.delete(0, ctk.END)
        self.combo_onem.set("Normal")
        self.duzenlenen_index = None
        self.btn_guncelle.configure(state="disabled")

    def girdileri_dogrula(self, baslik, tarih):
        if not baslik:
            raise ValueError("Görev başlığı boş bırakılamaz!")
        if not tarih_dogrula(tarih):
            raise ValueError("Geçersiz tarih formatı! Lütfen GG/AA/YYYY formatında giriniz.")

    def gui_gorev_ekle(self):
        baslik = self.entry_baslik.get()
        tarih = self.entry_tarih.get()
        onem = self.combo_onem.get()

        try:
            self.girdileri_dogrula(baslik, tarih)
            yeni_gorev = Gorev(baslik, tarih, onem)
            self.yonetici.gorev_ekle(yeni_gorev)
            self.listeyi_guncelle()
            self.kutulari_temizle()
        except ValueError as e:
            messagebox.showerror("Hata", str(e))

    def gui_gorev_duzenle_hazirla(self, index):
        self.duzenlenen_index = index
        gorev = self.yonetici.gorevler[index]

        self.kutulari_temizle()
        self.entry_baslik.insert(0, gorev.baslik)
        self.entry_tarih.insert(0, gorev.tarih)
        self.combo_onem.set(gorev.onem_derecesi)

        self.duzenlenen_index = index
        self.btn_guncelle.configure(state="normal")

    def gui_gorev_kaydet(self):
        if self.duzenlenen_index is not None:
            baslik = self.entry_baslik.get()
            tarih = self.entry_tarih.get()
            onem = self.combo_onem.get()

            try:
                self.girdileri_dogrula(baslik, tarih)
                self.yonetici.gorev_guncelle(self.duzenlenen_index, baslik, tarih, onem)
                self.listeyi_guncelle()
                self.kutulari_temizle()
            except ValueError as e:
                messagebox.showerror("Hata", str(e))

    def gui_gorev_sil(self, index):
        cevap = messagebox.askyesno("Onay", "Görevi silmek istediğinize emin misiniz?")
        if cevap:
            self.yonetici.gorev_sil(index)
            self.listeyi_guncelle()
            self.kutulari_temizle()

    def gui_gorev_durum_degistir(self, index, var):
        # Checkbox işaretlendiğinde veya kaldırıldığında çalışır
        durum = var.get() == 1
        self.yonetici.gorevler[index].tamamlandi = durum
        self.yonetici.verileri_kaydet()
        self.listeyi_guncelle()

    def gui_rapor_goster(self):
        rapor = self.yonetici.rapor_uret()
        rapor_metni = "\n\n".join([f"📌 {k}:  {v}" for k, v in rapor.items()])
        messagebox.showinfo("Sistem Raporu", rapor_metni)

    def listeyi_guncelle(self):
        # Önceki eklenen tüm widgetları temizle
        for widget in self.liste_frame.winfo_children():
            widget.destroy()

        for i, g in enumerate(self.yonetici.gorevler):
            # Her görev için özel bir satır çerçevesi
            satir_frame = ctk.CTkFrame(self.liste_frame, fg_color="#2b2b2b", corner_radius=10)
            satir_frame.pack(fill="x", pady=5, padx=5)

            # Renk mantığı
            renk = "white"
            if g.tamamlandi:
                renk = "#808080"  # Gri
            elif g.onem_derecesi == "Yüksek":
                renk = "#ff4d4d"  # Kırmızı
            elif g.onem_derecesi == "Düşük":
                renk = "#4dabf7"  # Mavi

            # Onay Kutusu (Tamamlandı durumu)
            chk_var = ctk.IntVar(value=1 if g.tamamlandi else 0)
            chk = ctk.CTkCheckBox(satir_frame, text=g.baslik, variable=chk_var,
                                  command=lambda index=i, v=chk_var: self.gui_gorev_durum_degistir(index, v),
                                  text_color=renk, font=("Arial", 14, "bold"),
                                  hover_color="#2ecc71", border_color=renk)
            chk.pack(side="left", padx=15, pady=10)

            # Tarih ve Önem Bilgisi
            lbl_info = ctk.CTkLabel(satir_frame, text=f"Tarih: {g.tarih}   |   Önem: {g.onem_derecesi}",
                                    text_color=renk, font=("Arial", 12))
            lbl_info.pack(side="left", padx=20)

            # Sil Butonu
            btn_sil = ctk.CTkButton(satir_frame, text="Sil", width=60, fg_color="#e74c3c", hover_color="#c0392b",
                                    command=lambda index=i: self.gui_gorev_sil(index))
            btn_sil.pack(side="right", padx=10, pady=10)

            # Düzenle Butonu
            btn_duz = ctk.CTkButton(satir_frame, text="Düzenle", width=70, fg_color="#f39c12", hover_color="#d68910",
                                    command=lambda index=i: self.gui_gorev_duzenle_hazirla(index))
            btn_duz.pack(side="right", padx=5, pady=10)


if __name__ == "__main__":
    uygulama = AjandaArayuzu()
    uygulama.mainloop()