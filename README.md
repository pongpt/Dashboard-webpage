# ONE TU Dashboard

A web dashboard for monitoring **Thammasat University KPIs** – students, personnel, finance and research – built as part of the *ONE Data for ONE TU* data governance project (DSI322/DSI324, Thammasat University).

![Python](https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?logo=django&logoColor=white)
![Plotly Dash](https://img.shields.io/badge/Plotly%20Dash-3F4F75?logo=plotly&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

## Features

- **Home page** – entry point to all dashboards
- **Student dashboard** – student data and satisfaction survey results
- **Personnel & finance views** – staff and budget indicators
- **Research data** – research projects, articles and awards
- Interactive charts with Plotly / Dash embedded in Django (`django-plotly-dash`)

## Data

Cleaned datasets live in `app/data/` (CSV), prepared from multiple university sources:

| File | Content |
|---|---|
| `TQF_GREATS_Combined_Clean_Year636465.csv` | TQF / GREATS learning outcomes, academic years 2563–2565 |
| `cleaned_survey_satisfaction_656667_full.csv` | Satisfaction survey, academic years 2565–2567 |
| `data_research_cleaned_ADD_new.csv` | Research projects |
| `data_article_cleaned.csv` | Published articles |
| `data_award_cleaned.csv` | Awards |

Data cleaning and standardization (merging sources, handling missing values, unifying field names) was my main role in the project.

## Tech stack

- **Backend:** Django 4.2, Django REST Framework
- **Visualization:** Plotly, Dash, dash-bootstrap-components
- **Data:** pandas, NumPy
- **Database:** PostgreSQL 16
- **Deployment:** Docker, Docker Compose, Gunicorn

## Project structure

```
app/
├── core/          # Django settings & URLs
├── dashboard/     # Dashboard app: views, templates, static files
│   └── views/     # home, student, personnel, finance views
├── data/          # Cleaned CSV datasets
└── manage.py
Dockerfile
docker-compose.yml
requirements.txt
```

## Getting started

```bash
git clone https://github.com/pongpt/Dashboard-webpage.git
cd Dashboard-webpage
cp .env.example .env   # then set your own password and secret key
docker compose up --build
```

Then open http://localhost:8000

## Author

**Peerawas Tantitemit** – Data Science & Innovation, Thammasat University  
[LinkedIn](https://www.linkedin.com/in/peerawas-tantitemit/)
