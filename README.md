# Steam early decline warning: which live games will lose half their players?

Given 90 days of Steam player counts, Twitch attention and store metadata, we rank live Steam games (≥ 10 average players) by their risk of a **major decline**, meaning their average players in months 6–12 fall to **less than half** of today's level. The target users are publishers and live-ops teams. Each quarter they decide which games get updates, sales, marketing and server budget, and which are about to lose a large part of their audience.

**Headline results.** Out-of-time backtest: trained on Dec 2017 data, tested on 1,559 live games starting Feb 2019, of which 5.6% lost half.

| | Trend rule | Game-age rule | Random forest |
| --- | ---: | ---: | ---: |
| ROC-AUC, all live games | 0.586 | 0.611 | **0.826** |
| ROC-AUC, games with 1,000+ players | 0.469 | 0.574 | **0.802** |
| ROC-AUC, 141 launch-stage games | 0.774 | – | **0.787** |
| Watch list (top 10%): share that lost half | 22% | 8% | **28%** (5× the base rate) |
| Share of all collapses on the watch list | 39% | 14% | **50%** |

- The ranking held in the 2020 lockdown period (AUC 0.826), even though market-wide decline rates swung from 20% to 3%. That swing is why the product is a **ranked watch list**, not a probability.
- On launch-stage games the model is only on par with the trend rule. Twitch adds nothing once Steam data is known.
- A secondary **end-of-life model** (will a game stay above 10 players?) is in `retention-analysis.ipynb`.
- The full write-up is in [reports/technical_report.md](reports/technical_report.md).

## Repository layout

```text
src/
  data-preprocessing/
    preprocess.ipynb          1. five-minute Steam histories -> daily panel + game summary
    twitch-mapping.ipynb      2. validate the Twitch<->Steam mapping, build monthly Twitch table
  decline-analysis.ipynb      3. MAIN: relative-decline watch list (features, EDA, models, backtest,
                                 big games, launch stage, ablation, robustness, watch lists)
  retention-analysis.ipynb    4. secondary: end-of-life model (stays above 10 players)
  data-exploration.ipynb      (optional) first look at the raw files
reports/
  technical_report.md         technical report with results and limitations
  figures/decline/            figures for the main (decline) model
  figures/                    figures for the secondary (end-of-life) model
  decline_metrics.json        every number of the main model
  decline_watchlist_backtest_2019.csv    backtest watch list with actual outcomes
  decline_watchlist_forecast_2020-08.csv forward watch list from the latest 90 days
  metrics.json, risk_table_backtest_2019.csv, risk_forecast_2020-08.csv   secondary model
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
3. `src/decline-analysis.ipynb` (≈4 min) → `reports/decline_*`, `reports/figures/decline/`
4. `src/retention-analysis.ipynb` (≈4 min, optional) → secondary model outputs in `reports/`

All models use fixed random seeds, so a rerun reproduces the reported numbers.
