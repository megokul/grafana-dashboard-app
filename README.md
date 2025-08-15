# 🧭 Banking Analytics Dashboard (Grafana + PostgreSQL + Synthetic Data)

> 🚀 A containerized, production-style demo that continuously generates synthetic card-transaction data, writes to PostgreSQL (local or AWS RDS), and visualizes key metrics in Grafana via auto-provisioned datasource and dashboard.

---

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python\&logoColor=white)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F46800?logo=grafana\&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)
![Pandas](https://img.shields.io/badge/Pandas-ETL-150458?logo=pandas)
![Faker](https://img.shields.io/badge/Faker-Data_Generator-00C853)

---

## ✅ Features

* **End-to-end stack**: Synthetic data generator ➜ PostgreSQL ➜ Grafana dashboards
* **Auto-provisioned Grafana**: Datasource + dashboard loaded at container start
* **RDS or local PostgreSQL**: SSL (`require`) for RDS, or disable SSL for local dev
* **Config via `.env`**: Works with `PG_*` and `DB_*` prefixes (generator supports both)
* **Resilient startup**: Creates schema if missing, batched inserts with `execute_batch`
* **Composable**: Everything runs with `docker compose up`

---

## 📂 Project Structure

```text
grafana-dashboard-app/
├── data_generator/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py          # Loads env, supports DB_* or PG_*; batching/interval config
│   │   ├── db.py              # Connect, ensure schema, batched inserts
│   │   ├── generator.py       # Faker-based transaction records
│   │   ├── logging.py         # Central logging config
│   │   ├── main.py            # Service loop: generate → insert
│   │   └── rules.py           # Simple business rules → decision + explanations
│   └── Dockerfile             # Slim Python image; copies app + sql
├── grafana/
│   ├── dashboards/
│   │   ├── banking_dashboard.json
│   │   └── provider.yaml      # Dashboard provisioning
│   └── datasources/
│       └── postgres.yaml      # Datasource provisioning (points to your PG/RDS)
├── sql/
│   ├── schema.sql             # Table + indexes
│   └── insert.sql             # Insert statement
├── docker-compose.yml         # Grafana + data_generator services
├── .env                       # Your secrets and connection info (do NOT commit)
└── requirements.txt
```

---

## 🔁 Data Flow

```text
Synthetic Generator (Faker + rules)
            │  batched rows
            ▼
       PostgreSQL (local or RDS)
            │  SQL queries
            ▼
         Grafana (provisioned datasource + dashboard)
```

---

## ⚙️ Configuration

Create and fill a **`.env`** file in the repo root:

```dotenv
# --- PostgreSQL (RDS or local) ---
PG_HOST=banking-db.xxxxxx.us-east-1.rds.amazonaws.com   # or host.docker.internal for local PG
PG_PORT=5432
PG_DB=postgres
PG_USER=postgres
PG_PASSWORD=your_password
PG_SSLMODE=require                   # RDS: require | Local: disable

# --- Generator tuning ---
BATCH_SIZE=10                        # rows per cycle
SLEEP_SECONDS=15                     # seconds between batches

# --- Optional logging ---
LOG_LEVEL=INFO
```

> The generator also accepts `DB_*` (DB\_HOST/DB\_NAME/…) if you prefer that prefix.
> Grafana provisioning uses the `PG_*` variables.

---

## 🚀 Run

### 1) With Docker Compose

```bash
docker compose up --build -d
# follow generator logs
docker compose logs -f data_generator
```

Open Grafana at **[http://localhost:3000](http://localhost:3000)**.
This setup enables **anonymous Viewer** access for local demo.

### 2) Using a local PostgreSQL instead of RDS

* Set `PG_HOST=host.docker.internal`
* Set `PG_SSLMODE=disable`
* Ensure your local PostgreSQL is listening on 5432 and accessible.

---

## 📊 Grafana Setup & Usage

Grafana is fully **provisioned** from files to avoid manual clicks:

* **Datasource**: `grafana/datasources/postgres.yaml`

  * Uses environment variables from `.env`
  * Stab
