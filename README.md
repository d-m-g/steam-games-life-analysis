# Steam Decline Watch: which live games will collapse relative to the market?

Given 90 days of Steam player counts, Twitch attention and store metadata, we score every live Steam game (≥ 10 average players) for the risk of a **collapse**: its players over months 6–12 fall below **half of where the typical live game ends up**. Each score is a calibrated probability with three plain-language reasons. The target users are publishers and live-ops teams. Each quarter they decide which games get updates, sales, marketing and server budget.

**Headline results.** Monthly backtest, Jan–Aug 2019: each month the model is retrained on all outcomes known by then and scores about 1,550 live games it has not seen.

| | Trend rule | Model, one start date (previous) | **Model, all known start dates** |
| --- | ---: | ---: | ---: |
| ROC-AUC, average of 8 months | 0.593 | 0.797 | **0.834** |
| Collapses caught by the top-10% watch list, average | 34% | 49% | **56%** |
| Feb 2019 test: ROC-AUC (95% CI) | 0.645 | 0.814 | **0.843 (0.78–0.90)** |
| Feb 2019 test: collapses on the watch list | 48% | 57% | **65%** |

- **Probabilities hold across years:** predicted 4.5–6.1% against an actual 4.0–4.8% collapse rate each month. The earlier "lost half of its own players" target was up to 3× off, because the market swings.
- **Every flag is explained.** For example, *The Division*: "falling about 50% a month · last month 77% below the first · more volatile than 95% of live games".
- **Limits:** too few big games collapse to judge them (6 in the Feb 2019 test); on launches the model is only slightly better than a trend rule; Twitch adds nothing.
- **Write-up and site:** [reports/technical_report.md](reports/technical_report.md). The project website with a searchable watch list is [website/index.html](website/index.html).

## Repository layout

```text
src/
  data-preprocessing/
    preprocess.ipynb          1. five-minute Steam histories -> daily panel + game summary
    twitch-mapping.ipynb      2. validate the Twitch<->Steam mapping, build monthly Twitch table
  decline-analysis.ipynb      3. MAIN: market-relative collapse model (monthly start dates, models,
                                 monthly backtest, calibration, big games, launches, ablation,
                                 explanations, watch lists)
  retention-analysis.ipynb    4. secondary: end-of-life model (stays above 10 players)
  data-exploration.ipynb      (optional) first look at the raw files
reports/
  technical_report.md         technical report with results and limitations
  figures/decline/            figures for the main (decline) model
  figures/                    figures for the secondary (end-of-life) model
  decline_metrics.json        every number of the main model
  decline_watchlist_backtest_2019.csv/.json    backtest watch list: probability, tier, reasons, outcome
  decline_watchlist_forecast_2020-08.csv/.json forward watch list from the latest 90 days
  metrics.json, risk_table_backtest_2019.csv, risk_forecast_2020-08.csv   secondary model
website/index.html            project website (self-contained; open in a browser)
data/                         not in git (see below)
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
3. `src/decline-analysis.ipynb` (≈7 min) → `reports/decline_*`, `reports/figures/decline/`
4. `src/retention-analysis.ipynb` (≈4 min, optional) → secondary model outputs in `reports/`

All models use fixed random seeds, so a rerun reproduces the reported numbers.
