# MikroQuest Krtko – PWA (Brython)

## Čo to je
PWA stránka pre “mikroquesty” (aktuálna + predchádzajúca v archíve) s odomykaním ukážkových riešení
cez mini Python warmup otázky. Obsahuje aj baseline “Krtko” demo.

## Nasadenie na GitHub Pages
1. Nahraj obsah priečinka do GitHub repa (napr. `microquest-krtko-pwa`).
2. GitHub → Settings → Pages → Deploy from branch → `main` / root.
3. Otvor URL.

## Inštalácia do zariadenia
- Tlačidlo “Nahoď do zariadenia” sa zobrazuje, kým app nebeží v standalone režime.
- Po inštalácii sa zobrazí “Zobraziť QR”, ktoré ukáže QR kód pre originálnu URL (QR sa generuje online).

## Offline poznámka
Service worker precacheuje lokálne súbory. Brython skripty sa cacheujú runtime (po prvej návšteve),
aby sa minimalizovalo riziko zlyhania inštalácie SW kvôli cross-origin precache.
Pre 100% offline first-run si stiahni brython skripty lokálne a uprav `index.html` + `sw.js`.

## Upraviteľné veci
- Harmonogram výziev: `RELEASES` v `app.py`
- Texty výziev + warmup: `QUESTS` v `app.py`
