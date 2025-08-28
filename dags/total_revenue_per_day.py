from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.dates import days_ago
from datetime import timedelta
import pandas as pd 
import matplotlib.pyplot as plt

PG_CONN_ID='postgres_conn'

default_args = {
    'owner': 'kiwilytics',
    'retries': 1,
    'retry_delay':timedelta(minutes=1)
}

def get_conn():
    hook = PostgresHook(postgres_conn_id=PG_CONN_ID)
    return hook.get_conn()

#fetch sales data

def fetch_sales_data_from_postgres():
    conn=get_conn()
    query='''
            select o.orderdate::date as sale_date,
                p.productid,
                p.productname,
                p.price,od.quantity
            from orders as o
            join order_details as od
            on o.orderid=od.orderid
            join products as p
            on p.productid=od.productid
        '''
    df=pd.read_sql(query,conn)
    df.to_csv("/home/kiwilytics/assignment_outputs/sales_data.csv",index=False)

#calculate total_revenue

def calculate_total_revenue():
    df=pd.read_csv("/home/kiwilytics/assignment_outputs/sales_data.csv")
    df['total_revenue']=df['price']*df['quantity']

    revenue_per_day=df.groupby('sale_date')['total_revenue'].sum()
    revenue_per_day.to_csv("/home/kiwilytics/assignment_outputs/revenue_per_day_data.csv")

#visualize total revenue per day

def visualize_revenue_per_day():
    df=pd.read_csv("/home/kiwilytics/assignment_outputs/revenue_per_day_data.csv")
    df['sale_date']=pd.to_datetime(df['sale_date'])

    plt.plot(df['sale_date'],df['total_revenue'],marker='o',linestyle='-')
    plt.title('Daily total revenue per day')
    plt.xlabel('Date')
    plt.ylabel('Total revenue')
    plt.xticks(rotation=45)
    plt.grid()
    plt.tight_layout()

    outputpath="/home/kiwilytics/assignment_outputs/total_revenue_per_day.png"
    plt.savefig(outputpath)

#Our DAG

with DAG (
     dag_id='total_revenue_per_day_flow',
     default_args=default_args,
     description='comnpute and plot total_revenue_per_day using pandas , matplotlib and Airflow',
     start_date=days_ago(1),
     schedule_interval='@daily',
    catchup=False
) as dag:
    task_fetch_data=PythonOperator(
            task_id='fetch_sales_data_from_postgres',
            python_callable=fetch_sales_data_from_postgres
    )

    task_calculate_total_revenue=PythonOperator(
        task_id='calculate_total_revenue',
        python_callable=calculate_total_revenue
    )

    task_visualize_total_revenue_per_day=PythonOperator(
        task_id='visualize_revenue_per_day',
        python_callable=visualize_revenue_per_day
    )

    task_fetch_data >> task_calculate_total_revenue >> task_visualize_total_revenue_per_day

 