import pandas as pd

def load_data(path):
    df = pd.read_csv(path)

    # rename kolom
    df.rename(columns={
        "Date": "date",
        "Weekly_Sales": "sales",
        "Store": "store"
    }, inplace=True)

    # fix datetime
    df["date"] = pd.to_datetime(df["date"], dayfirst=True)

    return df