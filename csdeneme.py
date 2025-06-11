from lyricsgenius import Genius
import re
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from nltk.corpus import stopwords
from typing import Dict, List, Tuple
from tqdm import tqdm
import time

class LyricsAnalyzer:
    def __init__(self, genius_token: str, language: str = "turkish"):
        """
        Initialize the LyricsAnalyzer with Genius API token and language preference.
        
        Args:
            genius_token (str): Genius API token
            language (str): Language for stopwords ('english' or 'turkish')
        """
        self.genius = Genius(genius_token)
        self.genius.timeout = 15  # Increase timeout to 15 seconds
        self.genius.retries = 3   # Add retries
        self.language = language.lower()
        self._download_required_nltk_data()
        
    def _download_required_nltk_data(self):
        """Download required NLTK data if not already downloaded."""
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
    
    def get_artist_lyrics(self, artist_name: str) -> List[str]:
        """
        Download and save lyrics for a given artist.
        
        Args:
            artist_name (str): Name of the artist
            
        Returns:
            List[str]: List of all lyrics from the artist's songs
        """
        print(f"\n🔍 {artist_name} için şarkı sözleri aranıyor...")
        
        # Try to get artist with retries
        max_retries = 3
        for attempt in range(max_retries):
            try:
                artist = self.genius.search_artist(artist_name)
                break
            except Exception as e:
                if attempt == max_retries - 1:
                    raise Exception(f"Sanatçı bulunamadı: {str(e)}")
                print(f"\n⚠️ Bağlantı hatası, yeniden deneniyor... ({attempt + 1}/{max_retries})")
                time.sleep(2)  # Wait before retrying
        
        all_lyrics = []
        
        print(f"\n📥 {len(artist.songs)} şarkı bulundu. Sözler indiriliyor...")
        for song in tqdm(artist.songs, desc="Şarkılar İndiriliyor"):
            try:
                if song.lyrics:
                    all_lyrics.append(song.lyrics)
            except Exception as e:
                print(f"\n⚠️ Şarkı indirilemedi: {song.title} - Devam ediliyor...")
                continue
        
        if not all_lyrics:
            raise Exception("Hiç şarkı sözü bulunamadı!")
            
        return all_lyrics
    
    def process_lyrics(self, lyrics_list: List[str]) -> List[str]:
        """
        Process and clean the lyrics data.
        
        Args:
            lyrics_list (List[str]): List of lyrics strings
            
        Returns:
            List[str]: List of cleaned words
        """
        print("\n🧹 Şarkı sözleri işleniyor...")
        all_lyrics = " ".join(lyrics_list)
        
        # Clean lyrics
        all_lyrics = all_lyrics.lower()
        all_lyrics = re.sub(r"\[.*?\]", "", all_lyrics)
        all_lyrics = re.sub(r"\(.*?\)", "", all_lyrics)
        all_lyrics = re.sub(r"[^\w\s]", "", all_lyrics)
        
        # Get stopwords based on language
        stop_words = set(stopwords.words(self.language))
        stop_words.update(["im", "oh", "la", "da", "de", "lyrics"])  # Common words to remove
        
        # Filter words: remove stopwords and purely numeric strings
        words = [word for word in all_lyrics.split() 
                if word not in stop_words and not word.isdigit()]
        
        print(f"✅ {len(words)} kelime işlendi.")
        return words
    
    def plot_word_frequency(self, words: List[str], artist_name: str, top_n: int = 20):
        """Generate and display bar plot of most frequent words."""
        print("\n📊 En çok kullanılan kelimeler grafiği oluşturuluyor...")
        word_counts = Counter(words)
        most_common_words = word_counts.most_common(top_n)
        
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x=[word[0] for word in most_common_words],
            y=[word[1] for word in most_common_words],
            hue=[word[0] for word in most_common_words],
            legend=False
        )
        plt.xticks(rotation=45)
        plt.xlabel("Kelimeler")
        plt.ylabel("Frekans")
        plt.title(f"{artist_name} Şarkılarında En Çok Kullanılan {top_n} Kelime", fontsize=14)
        plt.tight_layout()
        plt.show()
    
    def plot_min_length_words(self, words: List[str], artist_name: str, min_length: int = 3):
        """Generate and display distribution of words with minimum length."""
        print("\n📊 En çok kullanılan 3+ harfli kelimeler grafiği oluşturuluyor...")
        # Filter words with minimum length
        filtered_words = [word for word in words if len(word) >= min_length]
        word_counts = Counter(filtered_words)
        most_common_words = word_counts.most_common(20)  # Top 20 words
        
        plt.figure(figsize=(12, 6))
        sns.barplot(
            x=[word[0] for word in most_common_words],
            y=[word[1] for word in most_common_words],
            hue=[word[0] for word in most_common_words],
            legend=False
        )
        plt.xticks(rotation=45)
        plt.xlabel("Kelimeler")
        plt.ylabel("Frekans")
        plt.title(f"{artist_name} Şarkılarında En Çok Kullanılan {min_length}+ Harfli Kelimeler", fontsize=14)
        plt.tight_layout()
        plt.show()
    
    def search_word(self, words: List[str], search_word: str) -> int:
        """
        Search for a specific word in the lyrics.
        
        Args:
            words (List[str]): List of words to search in
            search_word (str): Word to search for
            
        Returns:
            int: Number of occurrences of the word
        """
        word_counts = Counter(words)
        return word_counts.get(search_word.lower(), 0)

def get_language_choice() -> str:
    """Get language choice from user."""
    while True:
        choice = input("\n🌍 Dil seçin (T: Türkçe, E: English): ").upper()
        if choice in ['T', 'E']:
            return "turkish" if choice == 'T' else "english"
        print("❌ Geçersiz seçim! Lütfen 'T' veya 'E' girin.")

def main():
    # Your Genius API token
    GENIUS_TOKEN = "INSERT_YOUR_GENIUS_TOKEN_HERE"
    
    print("🎵 Şarkı Sözü Analiz Aracı")
    print("=" * 30)
    
    # Get language choice
    language = get_language_choice()
    
    # Create analyzer instance
    analyzer = LyricsAnalyzer(GENIUS_TOKEN, language=language)
    
    # Get artist name from user
    artist_name = input("\n👤 Sanatçı adını girin: ")
    
    try:
        # Get and process lyrics
        lyrics_list = analyzer.get_artist_lyrics(artist_name)
        processed_words = analyzer.process_lyrics(lyrics_list)
        
        # Generate visualizations
        analyzer.plot_word_frequency(processed_words, artist_name)
        analyzer.plot_min_length_words(processed_words, artist_name)
        
        # Word search loop
        while True:
            search_word = input("\n🔍 Aranacak kelimeyi girin (Çıkmak için 'q'): ").strip()
            if search_word.lower() == 'q':
                break
                
            count = analyzer.search_word(processed_words, search_word)
            if count > 0:
                print(f"\n✅ '{search_word}' kelimesi {count} kez geçiyor.")
            else:
                print(f"\n❌ '{search_word}' kelimesi bulunamadı.")
        
        print("\n✨ Analiz tamamlandı!")
        
    except Exception as e:
        print(f"\n❌ Bir hata oluştu: {str(e)}")
        print("\n💡 İpuçları:")
        print("- İnternet bağlantınızı kontrol edin")
        print("- Sanatçı adını doğru yazdığınızdan emin olun")
        print("- Birkaç dakika bekleyip tekrar deneyin")

if __name__ == "__main__":
    main() 