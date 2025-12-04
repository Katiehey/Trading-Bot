# Crypto Quant Trading Bot Project

An ambitious 12-week development roadmap to design, backtest, and deploy a robust, rule-based, and eventually machine learning-enhanced cryptocurrency trading robot. This project emphasizes risk management, iterative testing (paper trading), and cautious real-money deployment.

## Table of Contents

- [Project Overview](#project-overview)
- [Development Roadmap (12 Weeks)](#development-roadmap-12-weeks)
- [Technology Stack](#technology-stack)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
- [Risk Warning](#risk-warning)

## Project Overview

This project aims to automate a trading strategy on the Binance exchange, starting with simple technical indicators (RSI, Moving Averages) and progressing to a predictive machine learning model. The development follows a structured agile approach to minimize risk and ensure thorough validation at each stage, from local backtesting to a supervised micro-live deployment.

## Development Roadmap (12 Weeks)

The project is broken down into three main phases:

### Weeks 1–4: Foundations & Data

Focus on establishing the environment, gathering data, and creating a baseline strategy.

*   **Week 1:** Environment setup (Python, `pip`, `venv`), learn `ccxt` library basics. *Deliverable: Notebook that downloads 1h BTC/USDT OHLCV data for the last 2 years.*
*   **Week 2:** Data cleaning and Exploratory Data Analysis (EDA). *Deliverable: Notebook with plots, return calculations, and basic indicators (MA, RSI).*
*   **Week 3:** Feature engineering pipeline. *Deliverable: Script that outputs CSV of features + target variable (ensuring no future data leakage).*
*   **Week 4:** Simple rule-based strategy & backtest (e.g., MA crossover). *Deliverable: Backtest script showing PnL and Drawdown metrics.*

### Weeks 5–8: First ML Model & Backtesting

Focus on integrating a machine learning approach and improving testing robustness.

*   **Week 5:** Baseline ML model (`RandomForest`/`XGBoost`) to predict future price direction. *Deliverable: Model predicting next 24h up/down, with cross-validation results.*
*   **Week 6:** Walk-forward validation implementation + adding realistic slippage/fees to the backtest. *Deliverable: Robust backtest report (Sharpe Ratio, Max Drawdown).*
*   **Week 7:** Paper-trading implementation (connecting to exchange testnet). *Deliverable: Paper bot that executes signals using mock money.*
*   **Week 8:** Logging, alerts, and dashboard prototype (`Streamlit`). *Deliverable: Dashboard showing live signals and PnL metrics.*

### Weeks 9–12: Live Micro-Deployment & Improvement

Focus on a cautious transition to live trading and system hardening.

*   **Week 9:** Micro real-money deployment plan (R100–R500): risk rules, position sizing, stop loss definitions. *Deliverable: Checklist & config file for the live run.*
*   **Week 10:** Go live with a very small capital amount (spot trading). Monitor logs and alerts closely. *Deliverable: Live trades successfully logged and executed.*
*   **Week 11:** Analyze the first month of live performance; fix any operational issues. *Deliverable: Performance tracker & lessons learned document.*
*   **Week 12:** Scale plan & automation hardening (Dockerize, add simple auto-pause on drawdown). *Deliverable: Automated, containerized service ready to scale to the next capital step.*

## Technology Stack

*   **Python:** The core programming language for all logic and data analysis.
*   **Libraries:** `pandas`, `numpy`, `ccxt`, `scikit-learn`, `matplotlib`, `streamlit`.
*   **Exchange API:** Binance Testnet (for paper trading) and Binance Spot (for live trading).
*   **Environment:** `venv` for virtual environments, Docker (planned for Week 12).

## Installation and Setup

1.  **Clone the repository:**
    ```bash
    git clone 

    cd your-repo-name
    ```
2.  **Create and activate a virtual environment:**
    *   **macOS/Linux:**
        ```bash
        python3 -m venv venv
        source venv/bin/activate
        ```
    *   **Windows (PowerShell):**
        ```powershell
        python -m venv venv
        .\venv\Scripts\Activate.ps1
        ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt 
    # (You will need to create a requirements.txt file with pandas, ccxt, numpy, etc.)
    ```
4.  **Configuration:** Create a configuration file (e.g., `config.toml` or environment variables) to securely store your Binance API keys. **Never commit API keys directly to this repository.** The bot uses the Binance Testnet by default.

## Usage

Instructions on how to run specific scripts will be added as the project progresses.

*   To run the initial data download script: `python scripts/01_data_download.py`
*   To run the backtest script: `python scripts/04_run_backtest.py`

*(Note: Specific script names may vary as the project is developed.)*

## Risk Warning

**AUTOMATED TRADING IS INHERENTLY RISKY.** This repository is for educational and development purposes. Strategies that work in backtesting may fail in live markets. We emphasize rigorous testing, starting with paper trading, and using only minimal risk capital (R100-R500) during initial live deployment. **Use at your own financial risk.**
