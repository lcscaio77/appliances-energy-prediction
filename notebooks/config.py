import os, sys
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

RAW_DATA_FILE = '../data/raw/energydata_complete.csv'
RENAMED_DATA_FILE = '../data/processed/renamed_data.csv'
PROCESSED_DATA_FILE = '../data/processed/processed_data.csv'

_processed_data = pd.read_csv('../appliances-energy-prediction/data/processed/processed_data.csv')

FEATURES = _processed_data.columns.drop('Energy')
TARGET = 'Energy'

X = _processed_data[FEATURES].values
Y = _processed_data['Energy'].values
