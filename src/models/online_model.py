# Imports classiques
import numpy as np
import pandas as pd

# Imports des métriques
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error, mean_squared_error, root_mean_squared_error


def check_model_module(model):
    # Si le modèle n'est pas instancié
    if isinstance(model, type):
        if 'statsmodels' in model([0]).__class__.__module__: 
            return 'statsmodels'
        if 'sklearn' in model().__class__.__module__:
            return 'sklearn'
        else:
            raise ValueError(f'Modèle non supporté : {model.__name__}')
    # Si le modèle est déjà instancié
    else:
        if 'statsmodels' in model.__class__.__module__: 
            return 'statsmodels'
        if 'sklearn' in model.__class__.__module__:
            return 'sklearn'
        else:
            raise ValueError(f'Modèle non supporté : {model.__name__}')

def initialize_model(model_type, model_params, y=None):
    # Si le modèle est déjà instancié
    if not isinstance(model_type, type):
        return model_type
    # Si le modèle n'est pas instancié
    else:
        if check_model_module(model_type) == 'statsmodels':
            return model_type(y, **model_params)
        if check_model_module(model_type) == 'sklearn':
            return model_type(**model_params)

def fit_model(model, X=None, y=None):
    if check_model_module(model) == 'statsmodels':
        return model.fit(disp=0)
    if check_model_module(model) == 'sklearn':
        model.fit(X, y)
        return model

def model_forecast(model, X):
    if check_model_module(model) == 'statsmodels':
        return model.forecast(steps=len(X))
    if check_model_module(model) == 'sklearn':
        return model.predict(X)

def compute_metrics(y_true, y_pred):
    return {
        'MSE': mean_squared_error(y_true, y_pred),
        'RMSE': root_mean_squared_error(y_true, y_pred),
        'MAE': mean_absolute_error(y_true, y_pred),
        'MAPE': mean_absolute_percentage_error(y_true, y_pred)
    }

def online_window_fit(forecast_model, residual_model, X, y, window_size, step_size, forecast_model_params=None, residual_model_params=None, verbose=True):
    predictions = []
    true_values = []
    metrics_evolution = []

    n_iter = 0 
    for start in range(0, len(X) - window_size, step_size):
        n_iter += 1
        
        end = start + window_size

        if verbose:
            train_period = X.index[start:end]
            test_period = X.index[end:end + step_size]
            print(f'{n_iter} | Apprentissage des données de {train_period[0]} à {train_period[-1]} | Prévision de {test_period[0]} à {test_period[-1]}')

        X_train, y_train = X.iloc[start:end], y.iloc[start:end]
        X_test, y_test = X.iloc[end:end + step_size], y.iloc[end:end + step_size]

        initialized_forecast_model = initialize_model(forecast_model, forecast_model_params, y_train)
        fitted_forecast_model = fit_model(initialized_forecast_model, X_train, y_train)

        y_pred_train = model_forecast(fitted_forecast_model, X_train)
        y_pred_test = model_forecast(fitted_forecast_model, X_test)

        residuals = y_train - y_pred_train

        initialized_residual_model = initialize_model(residual_model, residual_model_params, residuals)
        fitted_residual_model = fit_model(initialized_residual_model, X_train, residuals)

        future_residuals = model_forecast(fitted_residual_model, X_test)
        
        future_prediction = np.maximum(y_pred_test + future_residuals, 0)

        predictions.extend(future_prediction)
        true_values.extend(y_test)

        metrics_evolution.append(compute_metrics(true_values, predictions))
    
    results = pd.DataFrame({'y_true': true_values, 'y_pred': predictions}).set_index(X.index[window_size:])

    metrics = pd.DataFrame([{
        'MSE': mean_squared_error(true_values, predictions),
        'RMSE': root_mean_squared_error(true_values, predictions),
        'MAE': mean_absolute_error(true_values, predictions),
        'MAPE': mean_absolute_percentage_error(true_values, predictions)
    }])

    metrics_evolution = pd.DataFrame(metrics_evolution)

    return results, metrics, metrics_evolution
