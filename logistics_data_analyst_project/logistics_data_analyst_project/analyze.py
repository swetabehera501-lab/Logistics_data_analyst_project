"""
Logistics Data Analyst Internship — Week 1 starter analysis
Dataset is synthetic/illustrative and is not real company data.
Run: python analyze.py
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)
DATA = ROOT / "logistics_data.csv"

def main():
    df = pd.read_csv(DATA, parse_dates=["dispatch_date"])

    # Basic data quality checks
    required = ["order_id", "dispatch_date", "planned_transit_hours",
                "actual_transit_hours", "planned_cost_inr", "actual_cost_inr"]
    missing = df[required].isna().sum()
    duplicate_orders = int(df["order_id"].duplicated().sum())
    df = df.drop_duplicates(subset=["order_id"]).copy()

    # Recalculate metrics from source fields to avoid relying only on prefilled values
    df["delay_hours"] = df["actual_transit_hours"] - df["planned_transit_hours"]
    df["cost_overrun_inr"] = df["actual_cost_inr"] - df["planned_cost_inr"]
    df["is_on_time"] = df["actual_transit_hours"] <= df["planned_transit_hours"]

    total_orders = len(df)
    on_time_pct = 100 * df["is_on_time"].mean() if total_orders else 0
    avg_delay = df.loc[~df["is_on_time"], "delay_hours"].mean()
    avg_cost_overrun = df["cost_overrun_inr"].mean()
    avg_utilization = df["vehicle_utilization_pct"].mean()

    summary = pd.DataFrame([
        ["Total orders", total_orders, "count"],
        ["On-time delivery rate", round(on_time_pct, 2), "%"],
        ["Average delay among late orders", round(float(avg_delay or 0), 2), "hours"],
        ["Average cost overrun per order", round(float(avg_cost_overrun), 2), "INR"],
        ["Average vehicle utilization", round(float(avg_utilization), 2), "%"],
        ["Duplicate order IDs detected", duplicate_orders, "count"],
    ], columns=["metric", "value", "unit"])
    summary.to_csv(OUT / "kpi_summary.csv", index=False)

    by_destination = df.groupby("destination", as_index=False).agg(
        orders=("order_id", "count"),
        on_time_rate_pct=("is_on_time", lambda s: round(100 * s.mean(), 2)),
        average_delay_hours=("delay_hours", lambda s: round(s[s > 0].mean(), 2) if (s > 0).any() else 0),
        average_cost_overrun_inr=("cost_overrun_inr", "mean")
    ).sort_values(["on_time_rate_pct", "orders"], ascending=[True, False])
    by_destination.to_csv(OUT / "destination_performance.csv", index=False)

    # Visual 1: on-time rate by destination
    chart_data = by_destination.sort_values("on_time_rate_pct")
    plt.figure(figsize=(10, 7))
    plt.barh(chart_data["destination"], chart_data["on_time_rate_pct"])
    plt.xlabel("On-time rate (%)")
    plt.ylabel("Destination")
    plt.title("On-time delivery rate by destination (illustrative data)")
    plt.tight_layout()
    plt.savefig(OUT / "on_time_rate_by_destination.png", dpi=160)
    plt.close()

    # Visual 2: planned versus actual costs
    plt.figure(figsize=(8, 5))
    plt.scatter(df["planned_cost_inr"], df["actual_cost_inr"])
    max_cost = max(df["planned_cost_inr"].max(), df["actual_cost_inr"].max())
    plt.plot([0, max_cost], [0, max_cost], linestyle="--")
    plt.xlabel("Planned cost (INR)")
    plt.ylabel("Actual cost (INR)")
    plt.title("Planned vs actual delivery cost")
    plt.tight_layout()
    plt.savefig(OUT / "planned_vs_actual_cost.png", dpi=160)
    plt.close()

    # Save a clean dataset with calculated columns
    df.to_csv(OUT / "cleaned_logistics_data.csv", index=False, date_format="%Y-%m-%d")

    print("Analysis completed.")
    print(summary.to_string(index=False))
    print(f"\nFiles saved in: {OUT}")
    print("\nNote: this is synthetic sample data; replace it with approved real data if provided.")

if __name__ == "__main__":
    main()
