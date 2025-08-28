# Total Revenue per Day ETL with Airflow

This project builds an **ETL pipeline** using **Apache Airflow** to fetch data from a PostgreSQL database, transform it with Python (pandas), and calculate **total revenue per day**.  
The DAG automates the process on a daily schedule.

---

## Project Structure

```
total_revenue_per_day_airflow/
│
├── dags/                      # Airflow DAGs
│   └── total_revenue_dag.py   # Main DAG definition
├── data/
│    └── categories.csv
│    └── customers.csv
│    └── employees.csv
│    └── order_details.csv
│    └── products.csv
│    └── sales.csv
│    └── shippers.csv
│    └── suppliers.csv
├── outputs/
│   └── revenue_per_day_data.csv
│    └── sales_data.csv
│   └── total_revenue_per_day.png
├── requirements.txt           # Python dependencies
└── README.md                  # Documentation
```

---

## Features

- **Extract**: Query order data from PostgreSQL
- **Transform**: Clean and aggregate revenue using pandas
- **Load**: Store transformed results back into local machine (or another destination)
- **Schedule**: Automated daily execution with Airflow

---

## Example DAG Flow

1. Extract data from Postgres
2. Transform using pandas (`groupby` on order_date, sum revenue)
3. Load results back into local machine

---

## Requirements

See [requirements.txt](./requirements.txt) for dependencies.

---

## 📌 Future Improvements

- Integrate with Data Warehouse (Snowflake/BigQuery/Redshift)
