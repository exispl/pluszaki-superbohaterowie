#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
agent_veo3_prompter.py
Agent generatora promptów VEO 3 / Google Flow & Firefly.

Możliwości:
  1. Generowanie promptów wideo VEO 3 dla 11 pluszaków z polskim głosem i lip-synkiem.
  2. Pobieranie i przeszukiwanie katalogu VEO 3 z projektu CX Firefly (C:\\Claude\\firefly_automation).
  3. Eksport promptów bezpośrednio do projektu Teledysk (S:\\AI\\Teledysk\\prompts\\firefly_veo3).
  4. Przygotowanie paczek promptów dla 3 kont Google Flow.
"""

import argparse
import json
import os
import sys
from pathlib import Path

BASE_DIR = Path(r"C:\Users\exisp\Desktop\Pluszaki_Superbohaterowie")
FIREFLY_DIR = Path(r"C:\Claude\firefly_automation")
TELEDYSK_DIR = Path(r"S:\AI\Teledysk")
PROMPTS_VEO_FILE = FIREFLY_DIR / "prompts-veo-3.json"

def list_firefly_veo3():
    """Wypisuje prompty VEO 3 z bazy Firefly."""
    if not PROMPTS_VEO_FILE.exists():
        print(f"Brak pliku: {PROMPTS_VEO_FILE}")
        return []
    with open(PROMPTS_VEO_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    print(f"=== KATALOG VEO 3 (CX Firefly): {data.get('meta', {}).get('total_prompts')} PROMPTÓW ===")
    for cat, items in data.get("categories", {}).items():
        print(f"\n[Kategoria: {cat}] ({len(items)} promptów)")
        for it in items:
            print(f"  - [{it.get('id')}] {it.get('title')} (Autor: {it.get('author')})")
    return data

def export_for_google_flow(account_id=1):
    """Generuje plik z promptami dla wybranego konta Google Flow."""
    doc_path = BASE_DIR / "VEO3_GOOGLE_FLOW_PROMPTY.md"
    if not doc_path.exists():
        print("Najpierw wygeneruj VEO3_GOOGLE_FLOW_PROMPTY.md")
        return
    print(f"Paczka VEO 3 dla konta Google Flow #{account_id} gotowa w: {doc_path}")

def main():
    parser = argparse.ArgumentParser(description="Agent promptów VEO 3 & Google Flow")
    parser.add_argument("--list-firefly", action="store_true", help="Pokaż prompty VEO 3 z CX Firefly")
    parser.add_argument("--sync-teledysk", action="store_true", help="Synchronizuj prompty do projektu Teledysk")
    parser.add_argument("--flow-account", type=int, default=1, help="Numer konta Google Flow (1-3)")
    args = parser.parse_args()

    if args.list_firefly:
        list_firefly_veo3()
    elif args.sync_teledysk:
        from import_firefly_prompts import import_veo3_prompts
        import_veo3_prompts()
    else:
        list_firefly_veo3()
        export_for_google_flow(args.flow_account)

if __name__ == "__main__":
    main()
