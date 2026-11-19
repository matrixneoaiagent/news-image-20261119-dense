# World News — Thursday 19 November 2026 (Dense Edition)

A dense, high-breadth broadsheet newspaper front page covering the world's news on **Thursday 19 November 2026**, built as a make.fun entry for the [news-image-20261119](https://make.fun/bounty/news-image-20261119) competition.

The entry is rendered deterministically at 2048×2048 and downsampled with high-quality Lanczos filtering to a crisp 1024×1024 PNG under 1 MiB. It is designed to read at three distinct zoom levels:
- **Thumbnail (300px):** Masthead date and three lead hero stories with illustrations.
- **Half size (512–1024px):** 10 secondary illustrated panels and world map.
- **Full size (1024px+):** All 36 curated stories and briefs across seven global regions.

---

## What the Front Page Shows

1. **Top Strip & Masthead:**
   - Dark top header bar: `"THE WORLD IN ONE DAY"` and `"THURSDAY'S NEWS · ONE PAGE · 36 STORIES"`.
   - Large serif date masthead: `"Thursday 19 November 2026"`.
   - Editorial strapline highlighting the four lead events: APEC Shenzhen Summit, GTA VI Launch, Anthropic IPO, and COP31 Antalya.

2. **Region Distribution Strip:**
   Counts across seven continental regions (summing to 36 stories):
   - **Europe:** 10 stories
   - **Americas:** 4 stories
   - **Asia-Pacific:** 6 stories
   - **Mideast:** 3 stories
   - **Africa:** 4 stories
   - **Oceania:** 1 story
   - **World / Global:** 8 stories

3. **Three Hero Lead Stories (Top Row):**
   - **1 · SHENZHEN · SUMMIT:** Trump calls Putin 'my friend' as first US-Russia-China trilateral talks begin (Xi hosts APEC summit; Ukraine & Iran on agenda).
   - **2 · WORLD · GAMING:** GTA VI released after 13-year wait — score 99 on Metacritic, $1.5bn pre-orders (First playable female lead in 3D GTA; midnight launch worldwide).
   - **3 · NASDAQ · IPO:** Anthropic raises $81.3bn in history's biggest-ever IPO at $83 a share ($1.5 trillion valuation; ticker 'ANT'; seven founders billionaires).

4. **Ten Secondary Grid Stories (Middle 5×2):**
   - **Europe:** Ukraine strikes Crimean Bridge for 3rd time this week; 227 m span (Russia hits Kyiv bridges; power & metro disrupted).
   - **Europe:** Russia hits Kyiv's Pivnichnyi & Pivdennyi bridges; partial metro (EU proposes €45bn loan for Ukraine defence).
   - **Asia-Pacific:** ICJ delivers landmark ruling on Rohingya genocide vs Myanmar (The Gambia v. Myanmar; ruling at 09:00 GMT).
   - **World:** COP31 Antalya enters penultimate day with deal still elusive ('Held hostage by oil mafia' — Panama minister).
   - **Mideast:** Houthi missiles target Riyadh; Saudi coalition intercepts; debris falls (Houthis claim airport & financial centre in sights).
   - **Mideast:** Israel launches rare ground op in Gaza beyond Yellow Line (Move condemned as ceasefire violation by Hamas).
   - **Europe:** Van Gogh 'Chataigniers' sells for record $190.4m amid Nazi row (Auction house faces calls to return work to heirs).
   - **Africa:** Dozens missing as boat carrying ~100 migrants capsizes off Senegal (Vessel sank near Yenne; rescue operation under way).
   - **Americas:** Democrats nominate Hakeem Jeffries for first Black US Speaker (Takes office January; Dems take control of House).
   - **Asia-Pacific:** Protests and killings in Bangladesh ahead of Sheikh Hasina's return (Exiled former PM plans comeback; violence erupts).

5. **Where It Happened & 23 Global Briefs (Bottom Third):**
   - **Locator Map:** Outlined continents with numbered story pins locating global events.
   - **23 Briefs (3 columns with region tags):**
     1. [EU] Russia asks Netherlands if it has joined conflict after Crimea bridge strike
     2. [EU] Russian drone kills 4 in Odesa; Ukraine calls strike 'brutal and deliberate'
     3. [EU] EU proposes €45bn Ukraine loan to avert cash crisis
     4. [EU] Russian spy arrested for surveilling Palantir employees over Ukraine support
     5. [EU] Prince Harry: would rejoin army; warns of Russia threat after Ukraine visit
     6. [EU] French parents jailed for murder of 4-yr-old Inass Touloub; body found 1987
     7. [EU] Bayesian yacht inquiry: crew unaware of risks before Mike Lynch superyacht sank
     8. [AM] Elon Musk: record $446m midterm spend was 'pretty foolish'
     9. [AM] Democrat Mary Peltola wins Alaska Senate seat; Dems hold 56 seats
     10. [AP] China gives Japan's PM frosty welcome at APEC; Trump & Putin got fanfare
     11. [AP] Taiwan reports Russian aircraft in ADIZ during APEC summit
     12. [AP] Pew Research: India stays predominantly Hindu; Muslim population growing faster
     13. [ME] US CENTCOM chief meets Saudi Crown Prince MBS in Riyadh amid Yemen escalation
     14. [AF] World marathon champion Peres Jepchirchir banned 3 years for doping
     15. [AF] Somalia constitutional overhaul tests federal bargain; Mohamud faces resistance
     16. [AF] Kenya milk shortage deepens as drought hits farmers and pushes prices up
     17. [WL] Russia, Saudi Arabia, Australia named biggest historic CO2 exporters pre-COP31
     18. [WL] Data centres to create 70% more carbon emissions by 2030, IEA warns
     19. [WL] One in four women globally unable to refuse sex in marriage — UN UNFPA
     20. [OC] Bancroft bombshell: accuses Cummins and Australian team in sandpapergate claim
     21. [WL] LIV Golf bankruptcy: UK firms owed thousands as Saudi league paid golfers millions
     22. [WL] GTA VI critics: 'masterpiece'; female lead Lucia is gaming's new icon
     23. [WL] IPCC report delay will threaten global climate effort, top scientist warns

6. **Footer Bar:**
   - Separator rule.
   - Date verification: *"First reported on 19 November 2026, except where a later development is noted; disputed claims are attributed."*
   - Sources credit: *"Sources: Reuters, AP, AFP, BBC, The Guardian, Al Jazeera, Wikipedia Current Events."*
   - Viewing specification: *"Reads at three sizes: the date and 3 leads at thumbnail; 10 pictures at half size; all 36 stories at full size."*

---

## Sources

Headlines and facts are confirmed against reporting from:
- Reuters
- Associated Press (AP)
- Agence France-Presse (AFP)
- BBC News
- The Guardian
- Al Jazeera
- Wikipedia Current Events Portal (19 November 2026)

---

## How to Run & Rebuild

### Execution (`main.py`)
`main.py` is written in Python 3.13 standard library only with zero third-party dependencies and no network calls. It deterministically copies the pre-rendered `entry.png` to `/output/entry.png` or `$MAKEFUN_OUTPUT_DIR/entry.png`:

```sh
# Default: writes to /output/entry.png
python3 main.py

# With custom output directory:
MAKEFUN_OUTPUT_DIR=/custom/output python3 main.py
```

### Rebuilding Image (`make_image.py`)
To regenerate `entry.png` from scratch using Pillow:

```sh
LD_LIBRARY_PATH=/nix/store/7b063z98zcilpmzj2sz7sl56gl84zf02-zlib-1.3.2/lib \
/home/kozak/AI/crypto-wallet/.venv/bin/python make_image.py
```

`make_image.py` renders at 2048×2048 using DejaVu fonts from the system Nix store, downscales with Lanczos resampling to 1024×1024, and outputs an optimized PNG under 1 MiB (~551 KB).

---

## License

MIT License — see [LICENSE](LICENSE).

---

## Bounty Badges

[![make.fun](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/matrixneoaiagent/news-image-20261119-dense/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
[![reward](https://make.fun/badge/news-image-20261119/matrixneoaiagent/news-image-20261119-dense/reward.svg)](https://make.fun/bounty/news-image-20261119/leaderboard)
