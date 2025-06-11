<<<<<<< HEAD
# lyrics_mostcommon_words
=======
# LYRICS ANALYZER

BU PROJE TAMAMEN YAPAY ZEKA KULLANILARAK GELİŞTİRİLMİŞTİR.

---

# Lyrics Analyzer

Şarkı sözlerini Genius API üzerinden çekip, kelime analizleri ve görselleştirmeleri yapan Python uygulaması.

---

## Özellikler

- Belirtilen sanatçının şarkı sözlerini Genius API ile indirir  
- Şarkı sözlerini temizler ve stopword filtresi uygular (Türkçe veya İngilizce)  
- En çok kullanılan kelimeleri ve minimum uzunlukta kelimeleri grafikle gösterir  
- Kullanıcının belirttiği kelimenin şarkılarda kaç kere geçtiğini arama imkanı sağlar  

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
   (Daha güvenli kullanım için .env dosyası kullanılabilir.)  
4. Terminalden çalıştırın:

python main.py

5. İstenen dil ve sanatçı adı bilgilerini girin.  
6. İstatistikler grafiklerle gösterilecektir.  
7. İsterseniz kelime araması yapabilirsiniz, çıkmak için q girin.

---

## Örnek

🌍 Dil seçin (T: Türkçe, E: English): T

👤 Sanatçı adını girin: Sezen Aksu

...

🔍 Aranacak kelimeyi girin (Çıkmak için 'q'): aşk

✅ 'aşk' kelimesi 123 kez geçiyor.

🔍 Aranacak kelimeyi girin (Çıkmak için 'q'): q

✨ Analiz tamamlandı!

---


>>>>>>> 835aa70 (Initial commit: lyrics analysis project)
