# 🧸 Pluszaki: Uniwersum Supermocy & Magiczna Przygoda w Pokoju 🌟

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI: Google Imagen 3](https://img.shields.io/badge/AI%20Model-Google%20Imagen%203-blue.svg)](https://deepmind.google/technologies/imagen-3/)
[![Engine: Web Audio & TTS](https://img.shields.io/badge/Audio-Web%20Audio%20%26%20SpeechSynthesis-green.svg)]()
[![Target: Kids 4--6 yo](https://img.shields.io/badge/Age-4--6%20Lat-pink.svg)]()

> **Kompletny projekt interaktywnych gier przeglądarkowych, galerii 3D oraz uniwersum ewolucji 11 prawdziwych pluszaków z dziecięcego pokoju.**

---

## 📸 O Projekcie

Projekt przekształca autentyczne fotografie 11 maskotek z pokoju dziecięcego w postacie superbohaterskie i magiczne, tworząc spójne uniwersum z 5 poziomami ewolucji (w stylu Pokémonów) oraz interaktywne gry edukacyjne dla dzieci w wieku 4, 5 i 6 lat.

### 🎮 Aplikacje w zestawie:

1. **[`gra_dla_4latki.html`](gra_dla_4latki.html)** – Interaktywna gra fabularna *"Krok po Kroku"* z autentycznymi motywami z pokoju (różowa pościel minky, poduszka w sówki, haft metryczki na uszkach Diany, dzwoneczek pieska), lektorem czytającym tekst na głos oraz **Trybem Kina (Auto-Play)**, w którym sceny i grafiki zmieniają się same co kilka sekund.
2. **[`gra_edukacyjna.html`](gra_edukacyjna.html)** – *Akademia Pluszowych Bohaterów*: wybór 11 postaci, zadania edukacyjne (kolory, cyferki, literki, empatia, dobre maniery), efekty dźwiękowe Web Audio API, fanfary i modal ewolucji.
3. **[`index.html`](index.html)** – Główna galeria multimedialna z podglądem pełnoekranowym (Lightbox), filtrowaniem (*Bez Tła*, *Cyberpunk*, *Mistyczny Las*, *Duety w Pokoju*), porównaniem oryginałów ze zdjęć oraz leksykonem promptów z przyciskiem *„Kopiuj Prompt”*.

---

## 🧸 Pełna Lista 11 Pluszaków i Żywiołów

| # | Bohater | Żywioł | Oryginał w Pokoju | Mega Ewolucja (Poziom 5) |
|---|---|---|---|---|
| **1** | **🐱 Kotek-Babeczka** | ⚡ Tęczowa Plazma | Pluszak w foremce z posypką | **Kosmiczny Feniks-Kot 👑** |
| **2** | **🐧 Błękitny Pingwinek** | ❄️ Astralny Lód | Mięciutki niebieski pingwin | **Tytan Polarnych Komet 👑** |
| **3** | **🐰 Króliczka Diana** | 🌙 Magia Księżyca | Lalka z haftem `13.06.2022` | **Bogini Gwiezdnego Pyłu 👑** |
| **4** | **🐶 Dźwiękowy Piesek K9** | 🔊 Fale Sonaru & Piorun | Piesek z dzwoneczkiem | **Gwiezdny Awatar Lojalności 👑** |
| **5** | **🐒 Cyber-Małpka (Gizmo)** | 🦾 Antygrawitacja & Tech | Małpka ssąca kciuk | **Mecha-Tytan Technologii 👑** |
| **6** | **🐮 Tytaniczna Krowa** | ⚡ Złote Rogi & Grzmot | Wielka łaciata krowa | **Gaia Matka Burzy 👑** |
| **7** | **🍯 Złoty Miś Miodowy** | 🍯 Słoneczny Bursztyn | Kubuś w czerwonej koszulce | **Astralny Niedźwiedź Słońca 👑** |
| **8** | **🍄 Gwiezdny Skoczek Mario** | 🍄 Ogień & Super-Skok | Mario w ogrodniczkach | **Kosmiczny Bohater Wymiarów 👑** |
| **9** | **✨ Kocia Czarodziejka Gabby** | 🎀 Magia Wyobraźni | Lalka ze świecącymi uszkami | **Królowa Kosmicznej Wyobraźni 👑** |
| **10** | **🍒 Wiśniowa Minnie** | 🍒 Wiśniowy Kwiat & Balet | Minnie w piżamce w wisienki | **Kryształowa Księżniczka Uśmiechu 👑** |
| **11** | **🍼 Kryształowy Niemowlaczek** | 🍼 Czyste Światło & Opieka | Niemowlę w różowym śpiworku | **Złote Dziecko Gwiazd 👑** |

---

## 📂 Struktura Repozytorium

```text
├── index.html                  # Główna galeria grafik, filtrów i promptów
├── gra_dla_4latki.html         # Gra przygodowa dla 4-latki (Krok po Kroku + Auto-Play)
├── gra_edukacyjna.html         # Gra ewolucji 11 pluszaków (Pokédex & Zadania)
├── HISTORIA_POSTACI.md         # Kompletna baza wiedzy, biografie i ewolucje
├── PROMPTS.md                  # Dokładne prompty do Google Imagen 3
├── postacie.json               # Baza danych JSON z postaciami i grafikami
├── README.md                   # Niniejsza dokumentacja projektu
├── LICENSE                     # Licencja MIT
├── .gitignore                  # Plik ignorowanych plików gita
├── duo_cat_penguin_*.jpg       # Scena w pokoju dziecięcym (Kotek & Pingwinek)
├── cyber_cupcake_cat_*.jpg     # Wersje 3D Kotka (z tłem oraz cutout bez tła)
├── astral_penguin_*.jpg        # Wersje 3D Pingwinka
├── lunar_bunny_*.jpg           # Wersje 3D Króliczki Diany
├── sonic_puppy_*.jpg           # Wersja 3D Pieska K9
├── techno_monkey_*.jpg         # Wersja 3D Małpki Gizmo
├── thunder_cow_*.jpg           # Wersja 3D Łaciatej Krówki
└── originals/                  # Oryginalne zdjęcia pluszaków z pokoju
    ├── cat_original.jpg
    ├── penguin_original.jpg
    ├── diana_original.jpg
    ├── dog_original.jpg
    ├── monkey_original.jpg
    ├── cow_original.jpg
    ├── pooh_original.jpg
    ├── mario_original.jpg
    ├── gabby_original.jpg
    ├── minnie_original.jpg
    └── baby_original.jpg
```

---

## 🚀 Jak Uruchomić Lokalnie

Projekt nie wymaga żadnych zewnętrznych serwerów ani instalacji bibliotek – działa w 100% natywnie w dowolnej nowoczesnej przeglądarce internetowej (Chrome, Edge, Firefox, Safari):

1. Sklonuj repozytorium lub pobierz jako ZIP:
   ```bash
   git clone https://github.com/twoj-login/pluszaki-superbohaterowie.git
   ```
2. Otwórz plik `gra_dla_4latki.html` lub `index.html` bezpośrednio w przeglądarce:
   ```bash
   # Windows PowerShell
   Start-Process index.html
   ```

---

## 🛠️ Technologie

* **Front-end:** Czysty HTML5, CSS3 Glassmorphism, Vanilla JavaScript.
* **Synteza Mowy:** Web Speech API (`SpeechSynthesisUtterance`) z polskim akcentem dla dzieci.
* **Audio FX:** Web Audio API – programowe generowanie dźwięków (dzwoneczki, syntezatory, fanfary) bez zewnętrznych plików audio.
* **AI Graphics:** Google Imagen 3 (Vertex AI / Google GenAI SDK).

---

## 📄 Licencja

Projekt udostępniony na licencji **MIT**. Zobacz plik [LICENSE](LICENSE) po więcej szczegółów.
