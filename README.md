# Multi-Exchange Crypto Trading Bot

> **Note:** This is an earlier iteration of the project. The current production version is deployed on Oracle Cloud.

⚠️ Educational & research purposes only.

A multi-exchange cryptocurrency trading bot with ML signal generation, walk-forward backtesting, and Docker deployment. Built over a structured 12-week development roadmap progressing from a simple rule-based strategy through machine learning integration to a live containerised deployment.

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Risk Warning](#risk-warning)

## Project Overview

The bot automates a trading strategy on the Binance exchange, starting with Moving Average crossover signals and progressing to a `RandomForest`/`XGBoost` predictive model. Development followed a structured agile approach: local backtesting → paper trading on the exchange testnet → supervised micro-live deployment. Risk management is treated as a first-class concern at every stage.

## Features

- **Rule-based strategy** — MA/EMA crossover with configurable fast/slow windows
- **ML signal generation** — `RandomForestClassifier` trained with time-series cross-validation (`TimeSeriesSplit`) to predict next-candle direction
- **Walk-forward backtesting** — out-of-sample validation with realistic slippage and fee modelling
- **Risk management** — volatility-targeted position sizing, max-drawdown circuit-breaker, per-trade risk cap, daily loss limit, and cooldown after consecutive losses
- **Live paper trading** — connects to Binance Testnet via `ccxt` before any real capital is risked
- **Containerised deployment** — Docker + Docker Compose with a health check, automatic restarts, and a nightly backup cron job
- **CI/CD pipeline** — GitHub Actions pushes a rebuild to the VPS on every merge to `main`
- **Telegram alerts** — trade signals, errors, and daily summaries delivered via bot

## Technology Stack

| Layer | Tools |
|---|---|
| Language | Python 3.11 |
| Data & Features | `pandas`, `numpy`, `pandas-ta` |
| ML | `scikit-learn` (RandomForest, TimeSeriesSplit) |
| Exchange connectivity | `ccxt` (Binance Spot + Testnet) |
| Configuration | YAML + `.env` (python-dotenv) |
| Containerisation | Docker, Docker Compose |
| CI/CD | GitHub Actions |
| Alerts | Telegram Bot API |
| Visualisation | `matplotlib`, `streamlit` (prototype) |

## Installation and Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/trading-bot.git
   cd trading-bot
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # macOS / Linux
   python3 -m venv venv
   source venv/bin/activate

   # Windows (PowerShell)
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure credentials:**
   ```bash
   cp .env.example .env
   # Edit .env and fill in your exchange API keys and Telegram token
   ```
   Never commit `.env` — it is already listed in `.gitignore`.

5. **Review the bot configuration:**

   Edit `config.yaml` to set your symbol, timeframe, strategy parameters, and risk limits. The bot runs in paper-trading mode (`mode: paper`) by default.

## Usage

### Run the feature engineering pipeline

```bash
python -m src.data.preprocess
```

### Train the ML classifier

```bash
python -m src.models.train_classifier
```

### Run a walk-forward backtest

```bash
python -m src.backtest.walk_forward
```

### Start the paper-trading bot

```bash
python -m src.bot.paper_run
```

### Start with Docker

```bash
docker compose up -d --build
docker compose logs -f bot
```

## Project Structure

```
trading-bot/
├── src/
│   ├── backtest/        # Walk-forward backtesting, MA crossover, metrics
│   ├── bot/             # Paper trading runner, market data, risk engine
│   ├── data/            # Data ingestion and preprocessing
│   ├── exchange/        # ccxt connector with retry logic
│   ├── execution/       # Transaction cost modelling
│   ├── features/        # Technical indicator pipeline (pandas-ta)
│   ├── live/            # Live data feed and paper trader
│   ├── models/          # Label generation, classifier training
│   ├── risk/            # Position sizing, drawdown management
│   ├── system/          # Config loader, alerts, backup, heartbeat, logger
│   └── visualization/   # Plotting utilities
├── configs/             # Strategy and logging configuration
├── config.yaml          # Main bot configuration
├── docker-compose.yml
├── Dockerfile
├── .env.example         # Credential template
├── OPERATIONS.md        # Deployment and ops runbook (not for public use)
└── requirements.txt
```

## Risk Warning

**AUTOMATED TRADING IS INHERENTLY RISKY.** This repository is for educational and development purposes. Strategies that perform well in backtesting may fail in live markets due to regime changes, slippage, and execution latency. This project emphasises rigorous testing, paper trading before going live, and using only minimal risk capital during initial live deployment. **Use at your own financial risk.**
