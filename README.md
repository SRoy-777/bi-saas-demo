---
title: ABC Jewellers Analytics Dashboard
emoji: 💎
colorFrom: indigo
colorTo: purple
sdk: docker
pinned: false
---

# 💎 ABC Jewellers — BI Analytics Dashboard

A full-stack **Business Intelligence dashboard** built with Python Dash, demonstrating a real-world, multi-role analytics platform for a jewellery retail chain. All data is **100% synthetic**.

---

## 🚀 Live Demo

**👉 [Open Live App](https://roy-subhankar-bi-demo.hf.space/)**

| Field | Value |
|-------|-------|
| **Email** | `demo@admin.com` |
| **Password** | `demo@1234` |

> Full admin access — all dashboards and all locations unlocked.

---

## 📊 Dashboards Included

| Dashboard | Description |
|-----------|-------------|
| **Performance** | Branch-wise NSV, gold weight, targets vs actuals |
| **Comparison** | Period-over-period sales comparison |
| **Aging Stock** | Inventory aging analysis by counter and category |
| **Daily Customer** | New vs returning customer footfall tracking |
| **Mini NSV** | Mobile-friendly quick revenue snapshot |
| **Stock Movement** | Inward vs sold stock movement analytics |
| **Basket Analysis** | Weight bucket level stock and sales intelligence |
| **Branch Health** | KPI tracking, collections, and branch benchmarking |
| **Old Gold** | Customer old gold exchange and purchase analytics |
| **Period Comparison** | Offer period vs benchmark period analysis |
| **Company Snapshot** | Company-wide D-1 summary for senior management |

---

## 🏗️ Architecture

```
Cloudflare R2 (Parquet Storage)
        ↓  download_from_r2.py on startup
   In-Memory Cache (backend/cache/data_cache.py)
        ↓
   Backend Services (backend/services/)
        ↓
   Plotly Dash Pages (app/pages/)
        ↓
   Deployed on Hugging Face Spaces (Docker)
```

- **No database** — all data stored as Parquet files on Cloudflare R2
- **Role-Based Access** — each user sees only their permitted dashboards and locations
- **Activity Logging** — user login events logged back to R2 asynchronously

---

## 🛠️ Tech Stack

- **Frontend/Backend**: [Plotly Dash](https://dash.plotly.com/) + Flask
- **Data**: Pandas + PyArrow (Parquet)
- **Storage**: Cloudflare R2 (S3-compatible)
- **Deployment**: Docker → Hugging Face Spaces
- **Synthetic Data**: Custom ETL pipeline (`etl/generate_synthetic_data.py`)

---

## 🗂️ Project Structure

```
├── app/
│   ├── app.py                  # Main Dash app, routing, login callback
│   └── pages/                  # One file per dashboard
├── backend/
│   ├── cache/data_cache.py     # Global in-memory parquet loader
│   └── services/               # Business logic per dashboard
├── etl/
│   ├── generate_synthetic_data.py   # Synthetic data generator
│   └── run_pipeline.py              # ETL pipeline runner
├── download_from_r2.py         # Startup: pulls parquet files from R2
├── Dockerfile
└── requirements.txt
```

---

*Developed by [Subhankar Roy](https://github.com/SRoy-777)*
