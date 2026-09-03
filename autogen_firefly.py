#!/usr/bin/env python3
"""
Pluszaki Superbohaterowie — Firefly Auto-Generator
Generuje każdego pluszaka × każdy model Firefly, zapisuje z etykietami.

Uruchomienie:
    pip install playwright pillow
    python autogen_firefly.py

Wymagania:
    - Chrome zalogowany do Adobe Firefly (adobe.com)
    - Uruchomiony z flagą: chrome.exe --remote-debugging-port=9222
      LUB skrypt sam otworzy Chrome
"""

import asyncio
import json
import os
import time
from datetime import datetime
from pathlib import Path

from playwright.async_api import async_playwright, Page

try:
    from PIL import Image, ImageDraw, ImageFont
    PIL_OK = True
except ImportError:
    PIL_OK = False
    print("⚠ Pillow nie zainstalowane — etykiety na obrazach wyłączone")
    print("  Zainstaluj: pip install pillow")

# ─── ŚCIEŻKI ──────────────────────────────────────────────────────────────────
BASE_DIR = Path(r"C:\Users\exisp\Desktop\Pluszaki_Superbohaterowie")
ORIGINALS_DIR = BASE_DIR / "originals_png"
OUTPUT_DIR = BASE_DIR / "autogen_models"
FIREFLY_URL = "https://firefly.adobe.com/generate/image"
GENERATION_WAIT_SEC = 25

# ─── MODELE (kolejność = priorytet jakości) ────────────────────────────────────
MODELS = [
    "Firefly Image 5",
    "Firefly Image 4 Ultra",
    "Firefly Image 4",
    "Firefly Image 3",
    "Gemini 3.1 (w/ Nano Banana 2)",
    "Gemini 3 (w/ Nano Banana Pro)",
    "GPT Image 2",
    "GPT Image 1.5",
    "GPT Image 1",
    "FLUX.2 [pro]",
    "FLUX1.1 [pro] Ultra",
    "FLUX1.1 [pro] Ultra Raw",
    "FLUX1.1 [pro]",
    "FLUX1.1 Kontext [max]",
    "FLUX1 Kontext [pro]",
    "Runway Gen-4 Image",
]

# ─── PROMPTY DLA KAŻDEJ POSTACI ───────────────────────────────────────────────
CHARACTERS = {
    "cat": {
        "name": "Cyber Cupcake Cat",
        "emoji": "🐱",
        "prompt": (
            "Ultra-detailed plush toy superhero cat, cyberpunk style, cupcake themed "
            "accessories and decorations, neon pink and purple glowing accents, ultra-soft "
            "fluffy fur texture, big sparkling cute eyes, tiny superhero cape, futuristic "
            "city skyline background, vibrant saturated colors, collectible toy photography, "
            "8K resolution, photorealistic plush doll, studio lighting"
        ),
    },
    "dog": {
        "name": "Sonic Puppy",
        "emoji": "🐶",
        "prompt": (
            "Ultra-detailed plush toy superhero dog, sonic speed theme, electric lightning "
            "bolt markings, dynamic action pose, ultra-soft fluffy fur, big expressive eyes, "
            "electric blue and yellow superhero costume, speed lines in background, "
            "vibrant colors, collectible toy photography, 8K, photorealistic plush doll"
        ),
    },
    "penguin": {
        "name": "Astral Penguin",
        "emoji": "🐧",
        "prompt": (
            "Ultra-detailed plush toy superhero penguin, cosmic space theme, galaxy patterns "
            "on suit, star constellation markings, ultra-soft fluffy texture, big cute eyes, "
            "astronaut superhero helmet, deep space nebula background, deep purple and teal "
            "colors, collectible toy photography, 8K, photorealistic plush doll"
        ),
    },
    "cow": {
        "name": "Thunder Cow",
        "emoji": "🐄",
        "prompt": (
            "Ultra-detailed plush toy superhero cow, thunder and lightning theme, electric "
            "sparks crackling, black and white spots with golden lightning bolt accents, "
            "ultra-soft fluffy texture, big cute eyes, superhero cape with lightning symbol, "
            "dramatic storm clouds background, toy photography, 8K, photorealistic plush doll"
        ),
    },
    "monkey": {
        "name": "Techno Monkey",
        "emoji": "🐒",
        "prompt": (
            "Ultra-detailed plush toy superhero monkey, high-tech gadget theme, circuit board "
            "patterns on suit, holographic display accessories, ultra-soft fluffy texture, "
            "big cute eyes, tech-suit with glowing LEDs, cyberpunk laboratory background, "
            "green and orange neon colors, toy photography, 8K, photorealistic plush doll"
        ),
    },
    "pooh": {
        "name": "Cosmic Honey Pooh",
        "emoji": "🐻",
        "prompt": (
            "Ultra-detailed plush toy superhero Winnie-the-Pooh bear, cosmic honey magic "
            "theme, golden glowing honey aura, honey pot shield and crown, ultra-soft fluffy "
            "yellow fur, big innocent eyes, royal superhero cape, enchanted golden forest "
            "background, warm amber and gold colors, toy photography, 8K, photorealistic plush doll"
        ),
    },
    "mario": {
        "name": "Super Mario Plush Hero",
        "emoji": "🍄",
        "prompt": (
            "Ultra-detailed plush toy superhero Mario character, retro game theme, pixel "
            "mushroom and star accessories, ultra-soft fluffy texture, big cheerful eyes, "
            "red and blue superhero costume with M emblem, colorful game world background, "
            "vibrant primary colors, toy photography, 8K, photorealistic plush doll"
        ),
    },
    "minnie": {
        "name": "Minnie Mouse Superstar",
        "emoji": "🎀",
        "prompt": (
            "Ultra-detailed plush toy superhero Minnie Mouse, polka dot fashion theme, "
            "iconic bow as power accessory, ultra-soft fluffy texture, big sparkly eyes, "
            "elegant pink and white superhero gown with polka dots, magical sparkle background, "
            "pink gold and white colors, toy photography, 8K, photorealistic plush doll"
        ),
    },
    "gabby": {
        "name": "Gabby Dollhouse Hero",
        "emoji": "🏠",
        "prompt": (
            "Ultra-detailed plush toy superhero Gabby's Dollhouse character, magical toybox "
            "theme, cat ear headband, rainbow ribbon accessories, ultra-soft fluffy texture, "
            "big bright eyes, sparkly pastel superhero costume, magical dollhouse world "
            "background, rainbow pastel colors, toy photography, 8K, photorealistic plush doll"
        ),
    },
    "diana": {
        "name": "Princess Diana Hero",
        "emoji": "👑",
        "prompt": (
            "Ultra-detailed plush toy superhero princess Diana character, royal warrior theme, "
            "golden crown and shield accessories, ultra-soft fluffy texture, big determined "
            "eyes, pink and gold princess-warrior costume, magical castle background with "
            "shooting stars, pink gold and purple colors, toy photography, 8K, photorealistic plush doll"
        ),
    },
    "baby": {
        "name": "Baby Starlight Hero",
        "emoji": "⭐",
        "prompt": (
            "Ultra-detailed plush toy superhero baby character, dreamy celestial theme, "
            "star and crescent moon accessories, ultra-soft pastel plush texture, big adorable "
            "round eyes, tiny cozy superhero onesie with star pattern, dreamy cloud and "
            "constellation background, soft pastel lavender and cream colors, toy photography, "
            "8K, photorealistic plush doll"
        ),
    },
}


# ─── ETYKIETA NA OBRAZIE ──────────────────────────────────────────────────────
def add_label(image_path: Path, character_name: str, model_name: str, emoji: str = "") -> None:
    """Dodaje podpis (postać + model) na dole obrazu."""
    if not PIL_OK:
        return
    try:
        img = Image.open(image_path).convert("RGBA")
        w, h = img.size
        bar_h = max(60, h // 12)

        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Czarne półprzezroczyste tło na dole
        draw.rectangle([(0, h - bar_h), (w, h)], fill=(0, 0, 0, 180))

        # Tekst
        label = f"{emoji} {character_name}  |  {model_name}"
        font_size = max(18, bar_h // 2 - 4)
        try:
            font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", font_size)
        except Exception:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), label, font=font)
        text_w = bbox[2] - bbox[0]
        text_x = (w - text_w) // 2
        text_y = h - bar_h + (bar_h - (bbox[3] - bbox[1])) // 2

        draw.text((text_x + 2, text_y + 2), label, font=font, fill=(0, 0, 0, 200))
        draw.text((text_x, text_y), label, font=font, fill=(255, 255, 255, 255))

        combined = Image.alpha_composite(img, overlay).convert("RGB")
        combined.save(image_path)
    except Exception as e:
        print(f"    ⚠ Etykieta nieudana: {e}")


# ─── PLAYWRIGHT HELPERS ───────────────────────────────────────────────────────
async def wait_and_click(page: Page, selector: str, timeout: int = 5000) -> bool:
    try:
        el = page.locator(selector).first
        await el.wait_for(state="visible", timeout=timeout)
        await el.click()
        return True
    except Exception:
        return False


async def select_model(page: Page, model_name: str) -> bool:
    """Otwiera picker modelu i wybiera zadany model."""
    # Próba 1: kliknij aktualnie wybrany model (żeby otworzyć dropdown)
    opened = False
    for sel in [
        '[data-testid="model-picker-button"]',
        'button[aria-haspopup="listbox"]',
        'button[aria-haspopup="menu"]',
        'button:has-text("Firefly Image")',
        'button:has-text("Gemini")',
        'button:has-text("FLUX")',
        'button:has-text("GPT")',
        'button:has-text("Runway")',
        '[class*="model"][class*="button"]',
        '[class*="ModelPicker"]',
    ]:
        if await wait_and_click(page, sel, 3000):
            opened = True
            break

    if not opened:
        print(f"    ✗ Nie można otworzyć pickera modelu")
        return False

    await page.wait_for_timeout(800)

    # Próba kliknięcia opcji modelu
    for sel in [
        f'[role="option"]:has-text("{model_name}")',
        f'[role="menuitem"]:has-text("{model_name}")',
        f'li:has-text("{model_name}")',
        f'button:has-text("{model_name}")',
        f'[data-value="{model_name}"]',
    ]:
        if await wait_and_click(page, sel, 3000):
            await page.wait_for_timeout(600)
            print(f"    ✓ Model: {model_name}")
            return True

    # Fallback: szukaj po częściowym tekście
    short = model_name.split("(")[0].strip()
    for sel in [
        f'[role="option"]:has-text("{short}")',
        f'li:has-text("{short}")',
    ]:
        if await wait_and_click(page, sel, 2000):
            await page.wait_for_timeout(600)
            print(f"    ✓ Model (partial): {short}")
            return True

    print(f"    ✗ Model niedostępny: {model_name}")
    return False


async def upload_reference(page: Page, image_path: Path) -> bool:
    """Wgrywa zdjęcie referencyjne pluszaka."""
    try:
        # Firefly ma przycisk do uploadu referencji
        for sel in [
            'input[type="file"]',
            '[data-testid="image-upload-input"]',
            '[aria-label*="pload"]',
            '[aria-label*="reference"]',
            'button:has-text("Upload")',
            'button:has-text("Add image")',
            '[class*="upload"]',
        ]:
            try:
                el = page.locator(sel).first
                if await el.is_visible(timeout=2000):
                    await el.set_input_files(str(image_path))
                    await page.wait_for_timeout(2000)
                    print(f"    ✓ Referencja: {image_path.name}")
                    return True
            except Exception:
                continue

        # Jeśli nie ma input[file] — spróbuj drag and drop lub kliknij obszar
        for sel in ['[class*="ImageUpload"]', '[class*="dropzone"]', '[class*="reference"]']:
            try:
                el = page.locator(sel).first
                if await el.is_visible(timeout=1500):
                    await el.click()
                    await page.wait_for_timeout(500)
                    # Teraz input file powinien być widoczny
                    inp = page.locator('input[type="file"]').first
                    await inp.set_input_files(str(image_path))
                    await page.wait_for_timeout(2000)
                    print(f"    ✓ Referencja (click+upload): {image_path.name}")
                    return True
            except Exception:
                continue

        print(f"    ⚠ Nie znaleziono pola uploadu — generuję bez referencji")
        return False

    except Exception as e:
        print(f"    ✗ Upload error: {e}")
        return False


async def set_prompt_and_generate(page: Page, prompt: str) -> bool:
    """Wpisuje prompt i klika Generate."""
    # Wyczyść i wpisz prompt
    for sel in [
        'textarea[placeholder*="escribe"]',
        'textarea[placeholder*="escrib"]',
        '[data-testid="prompt-input"]',
        'textarea',
        '[contenteditable="true"]',
    ]:
        try:
            el = page.locator(sel).first
            if await el.is_visible(timeout=3000):
                await el.click()
                await page.keyboard.press("Control+a")
                await el.type(prompt[:800], delay=5)
                await page.wait_for_timeout(400)
                break
        except Exception:
            continue

    # Kliknij Generate
    for sel in [
        'button:has-text("Generate")',
        'button[data-testid="generate-button"]',
        '[aria-label="Generate"]',
        'button[type="submit"]',
    ]:
        if await wait_and_click(page, sel, 4000):
            print(f"    ⏳ Generuję... (czekam {GENERATION_WAIT_SEC}s)")
            return True

    print(f"    ✗ Nie znaleziono przycisku Generate")
    return False


async def download_result(page: Page, output_path: Path) -> bool:
    """Pobiera wygenerowany obraz."""
    await page.wait_for_timeout(GENERATION_WAIT_SEC * 1000)

    # Próba 1: przycisk Download
    for sel in [
        'button[aria-label*="ownload"]',
        'button:has-text("Download")',
        '[data-testid="download-button"]',
        'a[download]',
    ]:
        try:
            el = page.locator(sel).first
            if await el.is_visible(timeout=3000):
                async with page.expect_download(timeout=20000) as dl_info:
                    await el.click()
                dl = await dl_info.value
                await dl.save_as(str(output_path))
                print(f"    ✓ Pobrano: {output_path.name}")
                return True
        except Exception:
            continue

    # Fallback: screenshot widocznej strefy wyniku
    print(f"    ⚠ Download nieudany — robię screenshot")
    try:
        result_area = page.locator('[class*="result"], [class*="generated"], [class*="preview"], main').first
        await result_area.screenshot(path=str(output_path))
        print(f"    ✓ Screenshot: {output_path.name}")
        return True
    except Exception as e:
        print(f"    ✗ Screenshot też nieudany: {e}")
        return False


# ─── GŁÓWNA PĘTLA ─────────────────────────────────────────────────────────────
async def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    orig_files = sorted(ORIGINALS_DIR.glob("*_original.png"))
    if not orig_files:
        print(f"✗ Brak plików w: {ORIGINALS_DIR}")
        return

    total = len(orig_files) * len(MODELS)
    print(f"▶ Pluszaków: {len(orig_files)}  |  Modeli: {len(MODELS)}  |  Łącznie: {total} generacji")
    print(f"▶ Output: {OUTPUT_DIR}\n")

    results = []

    async with async_playwright() as p:
        # Spróbuj podłączyć do istniejącego Chrome (CDP)
        browser = None
        try:
            browser = await p.chromium.connect_over_cdp("http://localhost:9222")
            print("✓ Podłączono do istniejącego Chrome (CDP:9222)")
        except Exception:
            pass

        if not browser:
            print("⚠ Brak CDP — uruchamiam nowy Chrome (zaloguj się jeśli potrzeba)")
            browser = await p.chromium.launch(
                headless=False,
                channel="chrome",
                args=["--start-maximized"],
            )

        ctx = browser.contexts[0] if browser.contexts else await browser.new_context(
            viewport={"width": 1400, "height": 900}
        )
        page = await ctx.new_page()

        # Otwórz Firefly
        await page.goto(FIREFLY_URL, wait_until="networkidle", timeout=30000)
        print(f"✓ Firefly otwarty\n")

        if "login" in page.url.lower() or "ims-na1" in page.url.lower():
            print("⚠ POTRZEBNE LOGOWANIE — zaloguj się ręcznie i uruchom skrypt ponownie")
            await page.pause()

        done = 0
        for orig_file in orig_files:
            char_key = orig_file.stem.replace("_original", "")
            char = CHARACTERS.get(char_key, {
                "name": char_key.replace("_", " ").title(),
                "emoji": "🧸",
                "prompt": (
                    f"Ultra-detailed plush toy superhero {char_key}, vibrant colors, "
                    f"big cute eyes, superhero costume, 8K photorealistic plush doll"
                ),
            })

            char_dir = OUTPUT_DIR / char_key
            char_dir.mkdir(exist_ok=True)

            print(f"\n{'═'*60}")
            print(f"  {char['emoji']} {char['name'].upper()}")
            print(f"{'═'*60}")

            for model in MODELS:
                done += 1
                slug = (
                    model.replace(" ", "_")
                         .replace(".", "")
                         .replace("[", "").replace("]", "")
                         .replace("(", "").replace(")", "")
                         .replace("/", "_")
                )
                out_file = char_dir / f"{char_key}__{slug}.png"

                if out_file.exists():
                    print(f"  [{done:3}/{total}] POMIŃ (istnieje): {out_file.name}")
                    results.append({"char": char_key, "model": model, "status": "skip", "file": str(out_file)})
                    continue

                print(f"\n  [{done:3}/{total}] {char['name']} × {model}")

                # Nowa sesja na Firefly dla każdej generacji
                await page.goto(FIREFLY_URL, wait_until="domcontentloaded", timeout=20000)
                await page.wait_for_timeout(2500)

                model_ok = await select_model(page, model)
                ref_ok = await upload_reference(page, orig_file)
                gen_ok = await set_prompt_and_generate(page, char["prompt"])

                if gen_ok:
                    dl_ok = await download_result(page, out_file)
                else:
                    dl_ok = False

                if dl_ok and out_file.exists():
                    add_label(out_file, char["name"], model, char.get("emoji", "🧸"))
                    status = "ok"
                else:
                    status = "fail"

                results.append({
                    "char": char_key,
                    "char_name": char["name"],
                    "model": model,
                    "status": status,
                    "model_ok": model_ok,
                    "ref_ok": ref_ok,
                    "file": str(out_file),
                    "ts": datetime.now().isoformat(),
                })
                print(f"  → {'✓ OK' if status == 'ok' else '✗ FAIL'}")

                await page.wait_for_timeout(1500)

    # ─── LOG I RAPORT ─────────────────────────────────────────────────────────
    log_path = OUTPUT_DIR / "log.json"
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    ok_count = sum(1 for r in results if r["status"] == "ok")
    fail_count = sum(1 for r in results if r["status"] == "fail")
    skip_count = sum(1 for r in results if r["status"] == "skip")

    print(f"\n{'═'*60}")
    print(f"  GOTOWE: ✓ {ok_count} ok  ✗ {fail_count} nieudanych  ⏭ {skip_count} pominiętych")
    print(f"  Log: {log_path}")
    print(f"  Output: {OUTPUT_DIR}")

    # Wygeneruj prosty HTML raport
    _make_html_report(results, OUTPUT_DIR)


def _make_html_report(results: list, out_dir: Path) -> None:
    """Tworzy raport HTML z miniaturami."""
    html = ['<!DOCTYPE html><html lang="pl"><head><meta charset="UTF-8">',
            '<title>Pluszaki — Raport Generacji</title>',
            '<style>',
            'body{font-family:sans-serif;background:#111;color:#eee;margin:0;padding:16px}',
            'h1{color:#f80}',
            '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:16px}',
            '.card{background:#222;border-radius:10px;overflow:hidden;box-shadow:0 2px 8px #0008}',
            '.card img{width:100%;display:block}',
            '.card .info{padding:10px;font-size:13px}',
            '.ok{border-top:3px solid #4f4}',
            '.fail{border-top:3px solid #f44}',
            '.skip{border-top:3px solid #888;opacity:.5}',
            'h2{color:#fb0;margin:24px 0 8px}',
            '</style></head><body>',
            '<h1>🧸 Pluszaki Superbohaterowie — Generacje Firefly</h1>',
            f'<p>Wygenerowano: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>']

    # Grupuj po postaci
    by_char: dict = {}
    for r in results:
        by_char.setdefault(r["char"], []).append(r)

    for char_key, items in by_char.items():
        char_name = items[0].get("char_name", char_key)
        html.append(f'<h2>{char_name}</h2><div class="grid">')
        for r in items:
            file_path = Path(r["file"])
            rel = file_path.relative_to(out_dir) if file_path.exists() else None
            img_src = str(rel).replace("\\", "/") if rel else ""
            status_cls = r["status"]
            model_label = r["model"]
            html.append(f'<div class="card {status_cls}">')
            if img_src and file_path.exists():
                html.append(f'<img src="{img_src}" loading="lazy" alt="{model_label}">')
            else:
                html.append('<div style="height:180px;display:flex;align-items:center;justify-content:center;color:#555">Brak obrazu</div>')
            html.append(f'<div class="info"><b>{model_label}</b><br>Status: {status_cls}</div>')
            html.append('</div>')
        html.append('</div>')

    html.append('</body></html>')

    report_path = out_dir / "raport.html"
    report_path.write_text("\n".join(html), encoding="utf-8")
    print(f"  Raport HTML: {report_path}")


if __name__ == "__main__":
    asyncio.run(main())
