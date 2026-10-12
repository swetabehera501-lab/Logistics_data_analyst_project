# Logistics Delivery Performance Analysis

## Project purpose
A beginner-friendly Python data analytics project that explores delivery delays, delivery costs, and vehicle utilization. It demonstrates data cleaning, KPI calculation, grouped analysis, and chart generation.

**Important:** `logistics_data.csv` is synthetic/illustrative data created for this portfolio exercise. It is not real YuvaIntern or company data. Do not present its results as real business findings.

## Questions explored
1. What percentage of orders arrived on or before planned transit time?
2. How many hours late were delayed orders, on average?
3. How much did actual delivery cost differ from planned cost?
4. How does on-time performance vary by destination?
5. What data quality issues should be checked before analysis?

## KPIs
- On-time delivery rate = orders delivered within planned transit time / total orders × 100
- Average delay among late orders = average of positive (actual − planned) transit hours
- Average cost overrun = average (actual cost − planned cost)
- Average vehicle utilization = mean utilization percentage
- Duplicate order IDs = count of repeated order identifiers

## Project structure
```text
logistics_data_analyst_project/
├── logistics_data.csv
├── analyze.py
├── requirements.txt
├── README.md
└── outputs/                  # generated after running the script
```

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Optional: create and activate a virtual environment.
4. Install dependencies:
   `pip install -r requirements.txt`
5. Run:
   `python analyze.py`

The script creates KPI and destination CSV summaries plus PNG charts in `outputs/`.

## Roadmap
- Week 1: define the problem, explore sample data, establish KPIs, and document limitations.
- Next: improve data quality checks and investigate delay patterns by origin/destination/date.
- Later: with enough reliable historical records, evaluate a regression model for delay estimation and compare it with a simple baseline.
- Route optimization should only be attempted when road-network distances, vehicle capacity, delivery windows, and operational constraints are available.

## Limitations
The dataset is small and synthetic. It supports code demonstration only; no statistical or operational conclusion should be generalized to a real logistics company. The first version calculates descriptive KPIs, not a trained predictive model.
