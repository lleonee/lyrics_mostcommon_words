from lyricsgenius import Genius
import json
import re
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from nltk.corpus import stopwords
import os
from typing import Dict, List, Tuple
from tqdm import tqdm
import time
from difflib import SequenceMatcher

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
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate similarity between two texts using SequenceMatcher.
        
        Args:
            text1 (str): First text to compare
            text2 (str): Second text to compare
            
        Returns:
            float: Similarity ratio between 0 and 1
        """
        # Normalize texts for comparison
        text1_clean = re.sub(r'[^\w\s]', '', text1.lower().strip())
        text2_clean = re.sub(r'[^\w\s]', '', text2.lower().strip())
        
        return SequenceMatcher(None, text1_clean, text2_clean).ratio()
    
    def _remove_duplicate_lyrics(self, lyrics_list: List[str], similarity_threshold: float = 0.85) -> List[str]:
        """
        Remove duplicate lyrics based on similarity threshold.
        Keeps the longer version when duplicates are found.
        
        Args:
            lyrics_list (List[str]): List of lyrics strings
            similarity_threshold (float): Similarity threshold (0.85 = 85%)
            
        Returns:
            List[str]: List of unique lyrics
        """
        if len(lyrics_list) <= 1:
            return lyrics_list
            
        print(f"\n🔍 {len(lyrics_list)} şarkı arasında benzer sözler kontrol ediliyor...")
        
        unique_lyrics = []
        removed_count = 0
        
        for i, current_lyrics in enumerate(tqdm(lyrics_list, desc="Benzerlik Kontrolü")):
            is_duplicate = False
            
            # Compare with already selected unique lyrics
            for j, unique_lyrics_item in enumerate(unique_lyrics):
                similarity = self._calculate_similarity(current_lyrics, unique_lyrics_item)
                
                if similarity >= similarity_threshold:
                    is_duplicate = True
                    # Keep the longer version
                    if len(current_lyrics) > len(unique_lyrics_item):
                        unique_lyrics[j] = current_lyrics  # Replace with longer version
                    removed_count += 1
                    break
            
            if not is_duplicate:
                unique_lyrics.append(current_lyrics)
        
        print(f"✅ {removed_count} benzer şarkı kaldırıldı. {len(unique_lyrics)} benzersiz şarkı kaldı.")
        return unique_lyrics
    
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
        
        # Remove duplicate lyrics (remixes, demo versions, etc.)
        all_lyrics = self._remove_duplicate_lyrics(all_lyrics)
            
        return all_lyrics
    
    def process_lyrics(self, lyrics_list: List[str], min_song_count: int = 2) -> List[str]:
        """
        Process and clean the lyrics data.
        Only includes words that appear in at least min_song_count songs.
        
        Args:
            lyrics_list (List[str]): List of lyrics strings
            min_song_count (int): Minimum number of songs a word must appear in to be included
            
        Returns:
            List[str]: List of cleaned words that meet the criteria
        """
        print(f"\n🧹 Şarkı sözleri işleniyor... (En az {min_song_count} şarkıda geçen kelimeler)")
        
        # Get stopwords based on language
        stop_words = set(stopwords.words(self.language))
        stop_words.update(["im", "oh", "la", "da", "de", "lyrics"])  # Common words to remove
        
        # Add custom Turkish stopwords
        if self.language == "turkish":
            custom_stopwords = {
                "ben", "bana", "beni",
                "sen", "sana", "seni",
                "bi", "bir"
            }
            stop_words.update(custom_stopwords)
        
        # Process each song separately to track word occurrence across songs
        word_song_count = {}  # Track how many songs each word appears in
        all_valid_words = []  # Final list of words that meet criteria
        
        for song_lyrics in lyrics_list:
            # Clean lyrics for this song
            clean_lyrics = song_lyrics.lower()
            clean_lyrics = re.sub(r"\[.*?\]", "", clean_lyrics)
            clean_lyrics = re.sub(r"\(.*?\)", "", clean_lyrics)
            clean_lyrics = re.sub(r"[^\w\s]", "", clean_lyrics)
            
            # Get unique words in this song (to avoid counting same word multiple times per song)
            song_words = set([word for word in clean_lyrics.split() 
                            if word not in stop_words and not word.isdigit()])
            
            # Count song appearances for each word
            for word in song_words:
                word_song_count[word] = word_song_count.get(word, 0) + 1
        
        # Filter words that appear in at least min_song_count songs
        valid_words = {word for word, count in word_song_count.items() if count >= min_song_count}
        
        # Now collect all instances of valid words from all songs
        for song_lyrics in lyrics_list:
            clean_lyrics = song_lyrics.lower()
            clean_lyrics = re.sub(r"\[.*?\]", "", clean_lyrics)
            clean_lyrics = re.sub(r"\(.*?\)", "", clean_lyrics)
            clean_lyrics = re.sub(r"[^\w\s]", "", clean_lyrics)
            
            words = [word for word in clean_lyrics.split() 
                    if word in valid_words]
            all_valid_words.extend(words)
        
        filtered_count = len([word for word, count in word_song_count.items() if count < min_song_count])
        print(f"✅ {len(all_valid_words)} kelime işlendi. {filtered_count} kelime en az {min_song_count} şarkıda geçmediği için filtrelendi.")
        return all_valid_words
    
    def plot_word_frequency(self, words: List[str], artist_name: str, top_n: int = 20, lyrics_list: List[str] = None):
        """Generate and display bar plot of most frequent words."""
        print("\n📊 En çok kullanılan kelimeler grafiği oluşturuluyor...")
        word_counts = Counter(words)
        most_common_words = word_counts.most_common(top_n)
        
        # Calculate word occurrence across songs if lyrics_list is provided
        word_song_count = {}
        if lyrics_list:
            for song_lyrics in lyrics_list:
                clean_lyrics = song_lyrics.lower()
                clean_lyrics = re.sub(r"\[.*?\]", "", clean_lyrics)
                clean_lyrics = re.sub(r"\(.*?\)", "", clean_lyrics)
                clean_lyrics = re.sub(r"[^\w\s]", "", clean_lyrics)
                
                song_words = set([word for word in clean_lyrics.split() if len(word) > 1])
                for word in song_words:
                    word_song_count[word] = word_song_count.get(word, 0) + 1
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar([word[0] for word in most_common_words], [word[1] for word in most_common_words])
        
        # Add labels on bars showing song count
        for i, (bar, (word, count)) in enumerate(zip(bars, most_common_words)):
            if lyrics_list and word in word_song_count:
                song_count = word_song_count[word]
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{count}\n({song_count} şarkı)', ha='center', va='bottom', fontsize=8)
            else:
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{count}', ha='center', va='bottom', fontsize=8)
        
        plt.xticks(rotation=45)
        plt.xlabel("Kelimeler")
        plt.ylabel("Frekans")
        
        # Enhanced title with song count
        total_songs = len(lyrics_list) if lyrics_list else "?"
        plt.title(f"{artist_name} Şarkılarında En Çok Kullanılan {top_n} Kelime\n({total_songs} şarkı analiz edildi)", fontsize=14)
        plt.tight_layout()
        plt.show()
    
    def plot_min_length_words(self, words: List[str], artist_name: str, min_length: int = 3, lyrics_list: List[str] = None):
        """Generate and display distribution of words with minimum length."""
        print(f"\n📊 En çok kullanılan {min_length}+ harfli kelimeler grafiği oluşturuluyor...")
        # Filter words with minimum length
        filtered_words = [word for word in words if len(word) >= min_length]
        word_counts = Counter(filtered_words)
        most_common_words = word_counts.most_common(20)  # Top 20 words
        
        # Calculate word occurrence across songs if lyrics_list is provided
        word_song_count = {}
        if lyrics_list:
            for song_lyrics in lyrics_list:
                clean_lyrics = song_lyrics.lower()
                clean_lyrics = re.sub(r"\[.*?\]", "", clean_lyrics)
                clean_lyrics = re.sub(r"\(.*?\)", "", clean_lyrics)
                clean_lyrics = re.sub(r"[^\w\s]", "", clean_lyrics)
                
                song_words = set([word for word in clean_lyrics.split() if len(word) >= min_length])
                for word in song_words:
                    word_song_count[word] = word_song_count.get(word, 0) + 1
        
        plt.figure(figsize=(12, 6))
        bars = plt.bar([word[0] for word in most_common_words], [word[1] for word in most_common_words])
        
        # Add labels on bars showing song count
        for i, (bar, (word, count)) in enumerate(zip(bars, most_common_words)):
            if lyrics_list and word in word_song_count:
                song_count = word_song_count[word]
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{count}\n({song_count} şarkı)', ha='center', va='bottom', fontsize=8)
            else:
                plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                        f'{count}', ha='center', va='bottom', fontsize=8)
        
        plt.xticks(rotation=45)
        plt.xlabel("Kelimeler")
        plt.ylabel("Frekans")
        
        # Enhanced title with song count
        total_songs = len(lyrics_list) if lyrics_list else "?"
        plt.title(f"{artist_name} Şarkılarında En Çok Kullanılan {min_length}+ Harfli Kelimeler\n({total_songs} şarkı analiz edildi)", fontsize=14)
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
    GENIUS_TOKEN = "ZbnyK1sk7uBtTb_utudfWyP5WHRMlfh0dufRmf2SFpTVRaHCbHAKZOvsYq2zEQ_z"
    
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
        analyzer.plot_word_frequency(processed_words, artist_name, lyrics_list=lyrics_list)
        analyzer.plot_min_length_words(processed_words, artist_name, lyrics_list=lyrics_list)
        
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