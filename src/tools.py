import matplotlib.pyplot as plt
import os

os.makedirs("output", exist_ok=True)


def plot_per_year(df):
    df['year'] = df['date'].dt.year
    result = df.groupby('year')['sales'].sum()

    path = "output/year.png"

    result.plot(kind='bar')
    plt.title("Sales per Year")
    plt.savefig(path)
    plt.close()

    return path


def plot_per_month(df):
    df['month'] = df['date'].dt.to_period('M')
    result = df.groupby('month')['sales'].sum()

    path = "output/month.png"

    result.plot(kind='line')
    plt.title("Sales per Month")
    plt.savefig(path)
    plt.close()

    return path


def plot_per_store(df):
    result = df.groupby('store')['sales'].sum().sort_values(ascending=False)

    path = "output/store.png"

    result.plot(kind='bar')
    plt.title("Sales per Store")
    plt.savefig(path)
    plt.close()

    return path