# Omnichannel Data Ingestion Engine

A production-ready CDP data pipeline that unifies customer data 
from Shopify, Point-of-Sale, and a Loyalty Program into a single 
clean profile per customer.

## What it does
- Fetches data from 3 sources via REST APIs and CSV
- Cleans messy data: dates, phones, emails, names
- Deduplicates customers across all sources
- Outputs unified profiles to AWS S3 or MySQL

## Tech Stack
Python · Pandas · Flask · FastAPI · MySQL · AWS S3

## Quick Start
pip install -r requirements.txt
python generate_mock_data.py
bash start.sh

## Pipeline
395 raw records → 66 unified profiles (83% deduplication rate)
