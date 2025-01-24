def check_missing_values(data, columns=None, print_per_column=True):
    if columns is None:
        columns = data.columns

    if print_per_column:
        print("Valeurs manquantes par colonne :")
        for col in columns:
            print(f'{col} : {data[col].isna().sum()}')

    print(f"Nombre total de valeurs manquantes : {data[columns].isna().sum().sum()}")

def handle_missing_values(data, strategy="drop", columns=None):
    if columns is None:
        columns = data.columns

    for col in columns:
        if strategy == "mean":
            data[col].fillna(data[col].mean(), inplace=True)
        elif strategy == "median":
            data[col].fillna(data[col].median(), inplace=True)
        elif strategy == "drop":
            data.dropna(subset=[col], inplace=True)
        else:
            raise ValueError(f"Stratégie inconnue : {strategy}")
        
    print(f"Nombre total de valeurs manquantes : {data[columns].isna().sum().sum()}")
    
    return data
