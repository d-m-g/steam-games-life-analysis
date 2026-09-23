# Can Early Signals Predict Future Steam Player Retention?

## Executive summary

This project studies whether the first 90 days of Steam activity, Twitch attention, and game metadata can predict meaningful future Steam player retention.

The main outcome is defined as the mean Steam player count during days 180-365 after the first observed day. A game is classified as retained when this mean is at least 10 players, with at least 150 observed days required in the future window. The model uses a chronological evaluation design: earlier-observed games are used for training and later-observed games are used for testing.

The central expected finding is that early Steam player activity is the strongest predictor of later Steam retention. Twitch viewership adds limited predictive value after early Steam activity is included. This is useful because it shows that external attention and direct platform behavior should be evaluated separately rather than assumed to be interchangeable.

## Problem and target audience

Game developers, publishers, and marketing analysts need an early indication of whether a game is likely to maintain an active player base. The project provides a data-driven retention-risk estimate using information available near the beginning of a game's observed history.

## Research question

> Can early Steam activity, Twitch viewership, and game metadata predict whether a game retains at least 10 average Steam players during months 6-12?

This is a predictive and associative analysis. It does not claim that Twitch activity or any other feature causes retention.

## Data lifecycle

1. Steam five-minute player histories were aggregated to daily summaries.
2. Invalid dates and negative player counts were removed.
3. Steam metadata, genres, tags, and Twitch monthly statistics were joined by `appid`.
4. Features were calculated from the first 90 observed days.
5. Future targets were calculated from days 180-365.
6. Exploratory comparisons were made by free-to-play status and genre.
7. Logistic regression, random forest classification, linear regression, and random forest regression were evaluated.
8. Results were compared against an always-retained baseline and across metadata, Steam, and Twitch feature sets.

## Features

- Early mean, median, peak, volatility, and growth in Steam players
- Early Twitch average viewers, peak viewers, viewing minutes, and channel activity
- Free-to-play status
- Game type and primary genre
- Game age at the first observation

## Evaluation design

The target window requires at least 150 observed days between days 180 and 365. The model split is chronological rather than random: games observed earlier are used for training, and games observed later are used for testing. This better approximates predicting retention for a future game.

Because retention is imbalanced, the primary classification metrics are balanced accuracy, ROC-AUC, precision, and recall. Raw accuracy is reported only as supplementary information.

## Expected presentation findings

- Early Steam player counts should dominate permutation importance.
- Metadata alone should be weaker than metadata plus Steam activity.
- Twitch-only features should test whether Twitch is useful when Steam activity is unavailable.
- The full model should be compared directly with metadata plus Steam to measure the incremental value of Twitch.
- Threshold sensitivity should be reported for 1, 5, 10, 25, and 50 future mean players.

The current chronological evaluation produced these results:

| Model | Balanced accuracy | ROC-AUC |
|---|---:|---:|
| Always retained baseline | 0.500 | 0.500 |
| Logistic regression | 0.709 | 0.791 |
| Random forest | 0.878 | 0.958 |

Feature ablation produced these results:

| Feature set | Balanced accuracy | ROC-AUC |
|---|---:|---:|
| Metadata only | 0.648 | 0.706 |
| Twitch + metadata | 0.756 | 0.803 |
| Metadata + Steam | 0.870 | 0.951 |
| Metadata + Steam + Twitch | 0.878 | 0.958 |

The random forest regression achieved an MAE of approximately 26.3 players, RMSE of 65.9 players, and $R^2$ of 0.95 on the chronological test set. These are results for this historical test split, not a guarantee of production performance.

## Actionable output

The notebook creates a retention-risk table containing:

- App ID and game name
- First observation date
- Early mean and median Steam players
- Predicted retention probability
- Risk category: high, medium, or low

This can support an early review workflow. High-risk games could receive additional player-retention analysis, community support, or marketing attention. These categories are decision-support estimates, not universal business rules.

## Limitations

- The threshold of 10 players is an operational choice.
- Twitch coverage is incomplete; missing Twitch observations are not necessarily zero activity.
- The dataset is observational and does not identify causal effects.
- Developers, franchises, and release cohorts may create dependencies between games.
- Chronological validation is stronger than a random split but still reflects one historical period.
- The original observed-lifespan measure is descriptive only because all games share the same administrative collection end date.

## Final conclusion template

> Early Steam activity is the most useful signal for predicting future Steam retention. The model provides a practical early risk estimate, but its performance should be judged using chronological test data and class-imbalance-aware metrics. Twitch viewership should not automatically be treated as an additional source of predictive power: its incremental value must be compared with direct Steam activity. In this dataset, the most actionable information comes from early player-count level, stability, and growth.

## Suggested presentation structure

1. Business problem and target audience
2. Research question and retention definition
3. Data sources and data lifecycle
4. Feature construction and leakage prevention
5. Exploratory retention differences
6. Baseline and model comparison
7. Twitch ablation experiment
8. Feature importance and risk table
9. Limitations and responsible interpretation
10. Conclusions and possible applications
