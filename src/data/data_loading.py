import pandas as pd


def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        print("Données chargées avec succès.")
        return data
    except Exception as e:
        raise ValueError(f"Erreur lors du chargement des données : {e}")


def save_data(data, filename):
    try:
        data.to_csv("../data/processed/" + filename + ".csv", index=False)
        print("Données sauvegardées avec succès.")
    except Exception as e:
        raise ValueError(f"Erreur lors de la sauvegarde des données : {e}")
