# Virality-predictor

**Opsis Virality Prediktor** procjenjuje viralnost kratkih vertikalnih videa za Opsis Dalmatia (TikTok, Instagram Reels, YouTube Shorts).

Aplikacija: https://claude.ai/artifact/797fhei2y8wM7eGXroSzuX

## Kako se koristi
1. Uploadaj video (povuci ga u okvir ili klikni za odabir).
2. Odaberi platformu i temu, pa upiši opis i hashtagove.
3. Klikni **Analiziraj video**.

## Što dobiješ
- **Tehnička procjena (0–100)** izračunata u pregledniku: format, trajanje, hook u prve 3 s, broj rezova i tempo, svjetlina i boje, zvuk, opis i hashtagovi.
- **AI procjena** (na claude.ai): Claude pregleda do 8 ključnih kadrova i izmjerene podatke. Vraća ocjenu hooka, zadržavanja i potencijala za dijeljenje, savjete po prioritetu, tekst na ekranu, novi opis, hashtagove i preporuku kada objaviti.
- Ukupna ocjena = 60 % AI + 40 % tehnička.

Video ne napušta preglednik; Claudeu se šalje samo nekoliko kadrova. Ocjena je procjena, a ne jamstvo viralnosti.

`virality-predictor.html` je izvorni kod stranice.
