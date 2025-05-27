# 🇵🇱 morrowind_pl_ai_voice

**Polski Lektor AI do gry The Elder Scrolls III: Morrowind – Złota Edycja**  
_Modyfikacja dla silnika OpenMW_

---

## 📜 Opis

To repozytorium zawiera skrypty i narzędzia służące do wygenerowania polskiego lektora (a w przyszłości może również pełnego dubbingu AI) dla gry **TES III: Morrowind – Złota Edycja**, uruchamianej na silniku **OpenMW 0.49+**.

Projekt wykorzystuje model tekst-do-mowy (TTS) do automatycznego generowania ścieżek dźwiękowych z polskich dialogów i integruje się z istniejącą modyfikacją **Voices of Vvardenfell**.

> ❗ Udostępnione instrukcje i skrypty stworzone były z myślą o systemach **Linux**.  
> ❗ Wersja gry: **TES3: Morrowind – Złota Edycja (polska)**  
> ❗ Silnik: **OpenMW 0.49 lub nowszy**

---

## 🧩 Wymagane modyfikacje

Przed rozpoczęciem należy zainstalować następujące modyfikacje:

1. [Voices of Vvardenfell 0.2.3+](https://www.nexusmods.com/morrowind/mods/52279?tab=files)  
2. [OpenMW patch for VoV](https://www.nexusmods.com/morrowind/mods/54137?tab=files)  
3. [OpenMW Lua helper utility](https://www.nexusmods.com/morrowind/mods/54629?tab=files)  

Zalecane jest umieszczenie modów w folderze `Mods` OpenMW — bez ingerencji w oryginalne pliki gry.

---

## ⚙️ Instrukcja krok po kroku

### 1. Ekstrakcja dialogów z plików `.esm`

Użyj zmodyfikowanego narzędzia `tes3conv_pl` (ze wsparciem dla kodowania `WIN_1250`) do wyodrębnienia polskich danych dialogowych:

```bash
tes3conv_pl Morrowind.esm morrowind_pl.json
tes3conv_pl Tribunal.esm tribunal_pl.json
tes3conv_pl Bloodmoon.esm bloodmoon_pl.json
```

---

### 2. Połączenie dialogów w jeden plik JSON

Uruchom skrypt `1_generate_pl_dialog_json.py`, aby połączyć dane w jeden plik:

```python
input_files = [
    "morrowind_pl.json",
    "tribunal_pl.json",
    "bloodmoon_pl.json"
]
```

Wynikiem będzie plik:  
`Polish_VoiceDialogue_Mod.json`

---

### 3. Konwersja JSON do pliku `.esp`

Zamień dialogi z powrotem na format `esp`:

```bash
tes3conv_pl Polish_VoiceDialogue_Mod.json OpenMW_luahelper_dialog_pl.esp
```

Plik `.esp` zastąpi oryginalny `OpenMW_luahelper_dialog.esp` z modyfikacji Lua Helper Utility.

---

### 4. Generowanie ścieżek dźwiękowych

Uruchom skrypt `2_generate_speech.py`, który:

- Wczytuje model `tts_models/pl/mai_female/vits`
- Generuje pliki dźwiękowe `.mp3` na podstawie polskich dialogów
- Umieszcza je w strukturze folderów zgodnej z Voices of Vvardenfell

#### Konfiguracja ścieżek (przykład):

```python
# === CONFIG ===
original_vov_root = Path("/ścieżka/do/oryginalnego/VoV/Sound/Vo/AIV")
output_root = Path("/ścieżka/docelowa/dla/pl/Sound/Vo/AIV")
json_path = Path("Polish_VoiceDialogue_Mod.json")
```

- `original_vov_root` – ścieżka do folderu `Sound/Vo/AIV` z Voices of Vvardenfell  
- `output_root` – miejsce zapisu polskich plików dźwiękowych  
- `json_path` – plik wygenerowany w kroku 2

### 5. Kompresja i przyspieszenie audio

Po wygenerowaniu plików `.mp3`, użyj skryptu `3_compress_audio.py`, aby **skomprymować i przyspieszyć dźwięk o 10%** (lektor mówi szybciej, zachowując naturalność).

Skrypt używa **FFmpeg** oraz **wielowątkowości** do szybkiego przetwarzania wszystkich plików w folderze `Sound`.

#### ⚙️ Konfiguracja (`3_compress_audio.py`)

```python
input_root = Path("./Sound")               # Folder z oryginalnymi plikami .mp3
output_root = Path("./Sound_Compressed")   # Folder wynikowy z plikami po kompresji
max_workers = 4                            # Liczba wątków (zależna od CPU)

# Tryb kompresji: VBR (zmienna jakość) lub CBR (stały bitrate)
use_vbr = True
vbr_quality = "7"                          # 2 = najwyższa jakość, 9 = najniższa

# Alternatywa dla VBR (jeśli use_vbr = False)
target_bitrate = "32k"
target_sample_rate = "22050"

# Przyspieszenie lektora: 1.10 = 10% szybciej
audio_speed_factor = 1.10
```

#### ▶️ Uruchomienie

```bash
python3 3_compress_audio.py
```

Po wykonaniu skryptu, nowe pliki `.mp3` znajdziesz w folderze `./Sound_Compressed`, z zachowaną strukturą folderów zgodną z Voices of Vvardenfell.

> 🔄 Zaleca się **podmienić** folder `Sound/Vo/AIV` z Voices of Vvardenfell na wersję `Sound_Compressed/Vo/AIV` uzyskaną po tym kroku.


---

## 🎯 Integracja z grą

- Zastąp plik `OpenMW_luahelper_dialog.esp` swoim `OpenMW_luahelper_dialog_pl.esp`
- Podmień zawartość folderu `Sound/Vo/AIV` w Voices of Vvardenfell na wygenerowane pliki `.mp3`

---

## 📌 Cel projektu

Ułatwienie polskim graczom przeżycia Morrowinda z pełnym wsparciem lektora AI, przy zachowaniu immersji i zgodności z istniejącą strukturą modów.

---

## 🐧 System operacyjny

Projekt tworzony i testowany wyłącznie na systemie **Linux** (Pop!\_OS). Działa w środowisku zgodnym z Python 3 i `pip`.

---

## 🤝 Wkład i pomoc

Jeśli chcesz pomóc w rozwoju, tłumaczeniu lub testowaniu — zapraszam do kontaktu i zgłaszania problemów poprzez Issues lub Pull Requests.
