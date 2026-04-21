<img width="1398" height="908" alt="Screenshot 2026-04-20 231232" src="https://github.com/user-attachments/assets/5da14161-2f89-4e3e-9953-99428bb04504" />
This project organizes trading data by broker × stock, sorted by brokers with the highest transaction volume within a selected period. For each top broker, the system highlights the top 20 stocks they buy or sell.
Users can also generate a custom heatmap by selecting specific brokers and stocks. The visualization will indicate whether transactions occurred between the chosen brokers and stocks.
All data is collected using a custom scraper located in scrapper/scrapper.py, which retrieves:
- Broker transaction summaries
- Stock listings
- Broker lists from BEI/IDX


<img width="800" height="450" alt="ezgif-1f1b2afe746d4a60" src="https://github.com/user-attachments/assets/22b05936-baff-41f5-bf65-fb8964ad52b5" />
The scraper navigates through the broker summary pages of a trading platform, where users can specify:

- The stocks to analyze
- The time period for the data

For storage, this project uses MariaDB to persist:

- Transaction values
- Average prices
- Buy/sell actions

Alternatively, the data can be exported to CSV if a database is not required. However, in this project, a database is necessary to support dynamic data retrieval and visualization through the web application.

The system architecture includes:

- Backend: Built with FastAPI (Python) to serve processed data via APIs
- Frontend: Built with Vue.js to render interactive heatmaps and user-defined configurations
  
*This project does not publish or redistribute data from any specific platform.
It is intended for personal and academic purposes only and is not for commercial use

# Indonesian Stock Broker Activity Dashboard

End-to-end project for collecting Indonesian stock broker activity, storing it in MariaDB, and visualizing broker/stock flow in a Vue heatmap dashboard.

## What This Repo Contains

- `scrapper/`: Selenium scraper for broker summary data from the trading platform and IDX pages.
- `web/backend/`: FastAPI service that aggregates broker activity from MariaDB.
- `web/frontend/`: Vue 3 + Vuetify + ApexCharts dashboard (heatmap).
- `discord_bot/`: FastAPI + Discord bot service for running-trade alerts and transaction ingestion.
- `db/`: local DB connector helper module.
- `csv_reader.py`: one-off importer for stock symbol CSV into MariaDB.

## High-Level Flow

1. Scraper pulls broker summary and writes into `broker_summary`.
2. Backend queries/aggregates DB data for API consumers.
3. Frontend calls backend endpoints and renders heatmap.
4. Optional Discord service ingests transaction batches and pushes alerts to Discord channels.

## Tech Stack

- Python (Selenium, FastAPI, discord.py, MariaDB connector)
- MariaDB
- Vue 3 + TypeScript + Vite + Vuetify + ApexCharts

## Prerequisites

- Python 3.11+ (recommended)
- Node.js 20+ and npm
- MariaDB running locally (default code assumes `127.0.0.1:3307`)
- Google Chrome (for Selenium)

## Installation

### 1) Python dependencies

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2) Frontend dependencies

```bash
cd web/frontend
npm install
```

## Environment Variables

### `scrapper/.env`

Use `scrapper/.env.example` as template:

```env
EMAIL='youremail@com'
PASSWORD='pass'
PLATFORM='https://mybrokerplatform.com/login'

DB_USER='user'
DB_PASS='pass'
DB_HOST='127.0.0.1'
DB_PORT=3307
DB_DATABASE='stocks'
```

### `discord_bot/.env`

Required variables used by current code:

```env
DISCORD_KEY='your_discord_bot_token'

DB_USERNAME='user'
DB_PASSWORD='pass'
DB_HOST='127.0.0.1'
DB_PORT=3307
DB_DATABASE='stocks'
```

## Database Setup (Minimum Required Tables)

Create database:

```sql
CREATE DATABASE stocks;
```

Main tables expected by code:

- `broker_summary`
  - `broker_code`, `value`, `total_lot`, `price_average`, `stock_symbol`
  - `date_start`, `date_end`, `time_range`, `action`
- `stock_symbols`
  - `stock_symbol`, `stock_name`, `register_date`
- `brokers`
  - `broker_code`, `broker_name`
- `tbl_transactions`
  - `stock_code`, `tick_time`, `price`, `shares`, `type`

## Running the Project

Run each component in separate terminals.

### 1) Backend API (FastAPI, port `8000`)

```bash
cd web/backend
python main.py
```

### 2) Frontend (Vite, default port `5173`)

```bash
cd web/frontend
npm run dev
```

### 3) Scraper (writes to `broker_summary`)

```bash
cd scrapper
python scrapper.py
```

### 4) Discord alert service (optional, port `5000`)

```bash
cd discord_bot
python main.py
```

## HTTP Endpoints

### Backend (`web/backend/main.py`)

- `POST /broker-summary`
  - body: `first_date`, `second_date`, `broker_codes[]`, `stocks[]`
- `POST /broker-summary-screened`
  - body: `first_date`, `second_date`, `limit`, `page`
- `GET /get-all-stocks`
- `GET /get-all-brokers`

### Discord service (`discord_bot/routers/alert.py`)

- `GET /alert` (single alert by query params)
- `GET /alert/many` (batch insert handler; currently implemented as GET)

## Useful Scripts / Files

- `csv_reader.py`: imports stock symbol CSV into `stock_symbols`.
- `scrapper/main.py`: marked as "NOT USED" (legacy Playwright approach).
- `error_log.txt`: scraper error logs.

## Notes

- Backend DB connection in `web/backend/connect.py` and `db/connect.py` is currently hardcoded; update it before production use.
- Frontend currently targets `http://127.0.0.1:8000`, and backend CORS allows `http://localhost:5173`.
- Keep local credentials in `.env` files only; do not commit real secrets.
