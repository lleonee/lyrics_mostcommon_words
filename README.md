# LYRICS ANALYZER

BU PROJE TAMAMEN YAPAY ZEKA KULLANILARAK GELİŞTİRİLMİŞTİR.

---

# Lyrics Analyzer

Şarkı sözlerini Genius API üzerinden çekip, kelime analizleri ve görselleştirmeleri yapan Python uygulaması.

---

## Özellikler

- Belirtilen sanatçının şarkı sözlerini Genius API ile indirir  
- Benzer şarkı sözlerini (remix, demo versiyonları) otomatik olarak tespit eder ve kaldırır
- Şarkı sözlerini temizler ve stopword filtresi uygular (Türkçe veya İngilizce)  
- En çok kullanılan kelimeleri ve minimum uzunlukta kelimeleri grafikle gösterir  
- Grafiklerde kaç şarkının analiz edildiğini ve her kelimenin kaç şarkıda geçtiğini gösterir
- Kullanıcının belirttiği kelimenin şarkılarda kaç kere geçtiğini arama imkanı sağlar  
- Sadece en az 2 şarkıda geçen kelimeleri analiz eder (gürültüyü azaltır)  

---

## Yeni Özellikler

### 🎯 Gelişmiş Grafik Gösterimi
- **Analiz edilen şarkı sayısı**: Her grafik başlığında toplam analiz edilen şarkı sayısı gösterilir
- **Kelime-şarkı ilişkisi**: Her bar üstünde kelimenin kaç kez geçtiği ve kaç şarkıda bulunduğu gösterilir
- **Örnek**: "aşk: 123 (28 şarkı)" - 'aşk' kelimesi toplamda 123 kez geçiyor ve 28 farklı şarkıda bulunuyor

### 🧹 Duplicate Detection
- **Otomatik benzer şarkı tespiti**: Remix, demo, akustik versiyonları otomatik tespit eder
- **%85 benzerlik algoritması**: Çok benzer şarkıları kaldırır, daha uzun olanı tutar
- **Temiz analiz**: Sadece benzersiz şarkılar analiz edilir

### 📊 Akıllı Filtreleme
- **Minimum şarkı sayısı**: Sadece en az 2 şarkıda geçen kelimeler analiz edilir
- **Gürültü azaltma**: Tek bir şarkıya özel kelimeleri filtreleyerek daha anlamlı sonuçlar
- **Dil özelleştirmesi**: Türkçe ve İngilizce için özel stopword listeleri

---

## Gereksinimler

- Python 3.7+  
- lyricsgenius  
- nltk  
- matplotlib  
- seaborn  
- tqdm  

pip install -r requirements.txt

---

## Kullanım

1. Genius API için https://genius.com/api-clients adresinden token alın.  
2. Projeyi klonlayın veya indirin.  
3. main.py içindeki GENIUS_TOKEN değişkenine kendi tokenınızı yapıştırın.  
<<<<<<< HEAD
4. Terminalden çalıştırın:

```bash
python main.py
```

=======
4. Terminalden çalıştırın
>>>>>>> 772f5156c848978b94d8bd6a04b39a1024d3b230
5. İstenen dil ve sanatçı adı bilgilerini girin.  
6. Program otomatik olarak benzer şarkıları tespit edip kaldıracaktır.
7. İstatistikler detaylı grafiklerle gösterilecektir.  
8. İsterseniz kelime araması yapabilirsiniz, çıkmak için 'q' girin.

---

## Örnek

```
🌍 Dil seçin (T: Türkçe, E: English): T

👤 Sanatçı adını girin: Sezen Aksu

🔍 45 şarkı arasında benzer sözler kontrol ediliyor...
✅ 3 benzer şarkı kaldırıldı. 42 benzersiz şarkı kaldı.

🧹 Şarkı sözleri işleniyor... (En az 2 şarkıda geçen kelimeler)
✅ 2847 kelime işlendi. 156 kelime en az 2 şarkıda geçmediği için filtrelendi.

📊 En çok kullanılan kelimeler grafiği oluşturuluyor...
   [Grafik: "Sezen Aksu Şarkılarında En Çok Kullanılan 20 Kelime (42 şarkı analiz edildi)"]
   
📊 En çok kullanılan 3+ harfli kelimeler grafiği oluşturuluyor...
   [Grafik: Her bar üstünde kelime frekansı ve kaç şarkıda geçtiği gösterilir]

🔍 Aranacak kelimeyi girin (Çıkmak için 'q'): aşk

✅ 'aşk' kelimesi 123 kez geçiyor.

🔍 Aranacak kelimeyi girin (Çıkmak için 'q'): q

✨ Analiz tamamlandı!
```

---
