import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi


# Check for repositoy functioning
print("Hello World")


# Check kaggle dataset
# kaggle datasets download -d rusiano/madrid-airbnb-data

# Connect to kaggle

api = KaggleApi()
api.authenticate()
print("Kaggle ready")

df_calendar = pd.read_csv("/Users/diegoma/kaggle/calendar.csv")
print("pandas dataframe ready")