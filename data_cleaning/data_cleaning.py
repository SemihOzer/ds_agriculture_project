import pandas as pd

import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)


def clean_dataset(name):
    try:
        df = pd.read_csv(f"../data_collection/datasets/{name}.csv")
        # Drop rows that has no sales quantity
        df = df[df['Sales Quantity'] != 0]

        # Drop High, Closing and Low Prices(only using average price as the price)
        df = df.drop(columns=['High Price', 'Low Price', 'Closing Price'])
        df.rename(columns={"Average Price": "Price"}, inplace=True)

        # Delete "R"s of numbers (R012 --> 012)
        df["Price"] = df["Price"].str.extract(r"(\d+)").astype(int)
        df["Total Sales"] = df["Total Sales"].str.extract(r"(\d+)").astype(int)

        # Unit kg remove
        df["Unit"] = df["Unit"].str.extract(r"(\d+)").astype(int)

        # Market naming
        df["Market"] = df["Market"].str.rsplit("(", 1).str[-1].str.rstrip(")")

        # Drop rows which have NOT GRADED class
        df = df[df["Class"] != "NOT GRADED"]

        # Categorical data type of columns
        df["Variety"] = df["Variety"].astype("category")
        df["Variety_labeled"] = pd.factorize(df["Variety"])[0]

        df["Class"] = df["Class"].astype("category")
        df["Class_labeled"] = pd.factorize(df["Class"])[0]

        df["Size"] = df["Size"].astype("category")
        df["Size_labeled"] = pd.factorize(df["Size"])[0]

        df["Package"] = df["Package"].astype("category")
        df["Package_labeled"] = pd.factorize(df["Package"])[0]

        df["Market"] = df["Market"].astype("category")
        df["Market_labeled"] = pd.factorize(df["Market"])[0]

        # Drop Product column
        df.drop("Product", axis=1, inplace=True)

        print(df.info())

        df.to_csv(f"{name.lower()}_cleaned.csv", index=False)
    except:
        print(f"Could not find dataset which is name {name}")

clean_dataset('BANANAS')









