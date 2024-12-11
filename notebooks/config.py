import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

RAW_DATA_FILE = os.path.join('..', 'data', 'raw', 'energydata_complete.csv')
PROCESSED_DATA_FIL = '../data/processed/processed_data.csv'
