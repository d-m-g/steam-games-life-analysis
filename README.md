# Steam game retention: will this game still have players in 6–12 months?

Given 90 days of Steam player counts, Twitch attention and store metadata, we predict whether a game will still average **at least 10 concurrent players** 6–12 months later. The target users are publishers and live-ops teams deciding where to spend on updates, community and marketing across a catalogue of live games.

**Headline results** (out-of-time backtest: trained on Dec 2017 data, tested on 1,851 games from Feb 2019 → Jan 2020):

| | Simple rule "≥10 players today" | Random forest |
| --- | ---: | ---: |
| ROC-AUC, all games | 0.982 | 0.982 |
| Balanced accuracy, all games | 0.927 | 0.957 |
| Lost games caught (recall) | 87% | 94% |
| ROC-AUC, 537 borderline games (5–50 players) | 0.931 | 0.961 |

- In the backtest, 87% of games flagged **high risk** fell below 10 players; only 0.4% of **low risk** games did.
- Twitch viewership adds nothing once Steam numbers are known (+0.0002 AUC).
- The full write-up is in [reports/technical_report.md](reports/technical_report.md); the numbers come from [reports/metrics.json](reports/metrics.json).

## Repository layout

```text
src/
  data-preprocessing/
    preprocess.ipynb        1. five-minute Steam histories -> daily panel + game summary
    twitch-mapping.ipynb    2. validate the Twitch<->Steam mapping, build monthly Twitch table
  retention-analysis.ipynb  3. features, EDA, models, backtest, ablation, risk tables
  data-exploration.ipynb    (optional) first look at the raw files
reports/
  technical_report.md       technical report with results and limitations
  figures/                  every figure used in the report and slides (PNG)
  metrics.json              all reported numbers, written by retention-analysis.ipynb
  risk_table_backtest_2019.csv   backtest risk tiers with actual outcomes
  risk_forecast_2020-08.csv      forward risk forecast from the latest 90 days
data/                       not in git (see below)
```

## Data

`data/` is git-ignored because of its size (≈6 GB). Put the files here:

| Path | Source | Content |
| --- | --- | --- |
| `data/steam-games-dataset/` | Kaggle Steam games dataset (TODO: add the exact Kaggle link) | `applicationInformation.csv`, `applicationGenres.csv`, `applicationTags.csv`, `applicationDevelopers.csv`, `applicationPublishers.csv`, `applicationPackages.csv`, `applicationSupportedlanguages.csv`, and `PlayerCountHistoryPart1/2/<appid>.csv` (five-minute concurrent players, 14 Dec 2017 – 12 Aug 2020, 2,000 apps) |
| `data/sullygnome/monthly/YYYY-MM.csv` | [SullyGnome](https://sullygnome.com/) monthly game statistics, top 2,000 Twitch categories per month, Jan 2017 – Dec 2020 | viewers, watch time, channels |
| `data/sullygnome/appid_map.csv` | Built by the team by matching SullyGnome category URLs and names to Steam names (TODO: commit the script that produced it) | candidate Twitch ↔ Steam links |

## How to run

```bash
python -m venv .venv
.venv/Scripts/activate            # Windows; use source .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
python -m ipykernel install --user --name steam-games --display-name steam-games-life-analysis
```

Then run the notebooks in this order (each reads the previous one's output):

1. `src/data-preprocessing/preprocess.ipynb` (≈6 min, reads 6 GB) → `data/processed/steam_daily_panel.parquet`, `steam_game_summary.csv`
2. `src/data-preprocessing/twitch-mapping.ipynb` → `data/sullygnome/twitch_monthly_by_appid.csv`, `appid_map_validated.csv`
3. `src/retention-analysis.ipynb` (≈2 min) → everything in `reports/`

All models use fixed random seeds, so a rerun reproduces the reported numbers.
