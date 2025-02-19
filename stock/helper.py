
import datetime
import plotly.express as px
import pandas_ta as ta
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import os
from sklearn.preprocessing import StandardScaler
import numpy as np


from .forecast_bgru import train_gru_model,test_gru_model,PriceForecasterGRU
# from helper import normalize_with_sklearn,denormalize_with_sklearn


# Normalize data using StandardScaler
def normalize_with_sklearn(df, columns):
    """
    Normalize specified columns in the DataFrame using sklearn's StandardScaler.

    Args:
        df (DataFrame): Input DataFrame.
        columns (list): List of columns to normalize.

    Returns:
        DataFrame: Normalized DataFrame.
        scaler (StandardScaler): Fitted StandardScaler object for inverse transformation.
    """
    df = df.copy()  # Avoid modifying the original DataFrame
    scaler = StandardScaler()
    df[columns] = scaler.fit_transform(df[columns])
    return df, scaler

# Denormalize predictions
def denormalize_with_sklearn(predictions, scaler, column_index):
    print("******************")
    print("Trying to denormalize")
    """
    Denormalize predictions using the fitted StandardScaler.

    Args:
        predictions (numpy.ndarray): Normalized predictions (1D array for a single column).
        scaler (StandardScaler): Fitted StandardScaler object.
        column_index (int): Index of the column in the scaler to reverse-transform.

    Returns:
        numpy.ndarray: Denormalized predictions.
    """
    # Ensure predictions are reshaped to 2D for inverse_transform
    predictions = predictions.reshape(-1, 1)  # (n_samples, 1)
    
    # Create a dummy array to match scaler's fitted columns
    dummy_array = np.zeros((predictions.shape[0], scaler.n_features_in_))
    
    # Populate the specific column to denormalize
    dummy_array[:, column_index] = predictions.flatten()
    
    # Apply inverse_transform and extract the denormalized column
    denormalized = scaler.inverse_transform(dummy_array)[:, column_index]
    
    return denormalized



def prepare_data(df,user_input):
    
    #Calculate RSI  
    df["RSI"] = ta.rsi(df["Close"], length=14)
    df = df[['Close','RSI']]

    df = df.dropna()
    
    model_path = "/home/janak/Documents/Django_NM/Django_For_Numerical_Methods/stock/trained_models/feb_price_forecaster_gru_l2_four_layers.pth"
    # model_path = "/home/gopal/Documents/Django_For_Numerical_Methods/stock/trained_models/feb_price_forecaster_gru_l2_four_layers.pth"
        
    
    print(df.head())
    
    return df,model_path

   

    
def train_and_test(df,model_path):
    # model_path= "rsi_bgru.pth"
     #Train and test split
    train_size = 0.8
    split_index = int(len(df) * train_size)
    df_train = df[:split_index]
    df_test = df[split_index:]


    #Normalize
    columns_to_normalize = ['Close', 'RSI']
    df_train_normalized, scaler_train = normalize_with_sklearn(df_train, 
                                                               columns_to_normalize)
    df_test_normalized, scaler_test = normalize_with_sklearn(df_test,
                                                             columns_to_normalize)

    
    #Train
    n_days = 5


    model, mape = train_gru_model(df_train_normalized, n_days,model_path=model_path,
                                epochs=50)
    print(len(df_train_normalized))


    #Predict on test data
    predictions,test_mape = test_gru_model(model,df_test_normalized,n_days)
    print(len(predictions))
    print(predictions)

    # Re-transform predictions to original scale
    # Denormalize predictions to original scale (for 'Close' column only)
    predictions_original_scale = denormalize_with_sklearn(predictions,scaler_test, column_index=0)

    print(f"Testing MAPE (Original Scale): {test_mape:.2f}%")

    print("predictions_original_scale")
    print(predictions_original_scale)
    # # # Save the trained model

    torch.save(model.state_dict(), model_path)
    print(f"Model saved to {model_path}")
    # # # # Convert predictions to a Pandas Series with the appropriate index
    predictions_series = pd.Series(predictions_original_scale, index=df_test.index[n_days:])
    print(predictions_series)
    print(df_test)

    # # # Rename the series to a meaningful column name, e.g., 'Predicted Value'
    predictions_series = predictions_series.rename('Predicted Value')

    # # # Merge the series with the DataFrame on the index
    merged_df = df_test.merge(predictions_series, left_index=True,
                            right_index=True, how='left')

    # # print(merged_df)
    df_test = merged_df.dropna()
    last_5_days = df_test_normalized[['Close', 'RSI']].tail(5).values  # Extract last 5 days as input
    last_5_days_tensor = torch.tensor(last_5_days, dtype=torch.float32).unsqueeze(0)  # Add batch dim
    with torch.no_grad():
        predicted_tomorrow_price = model(last_5_days_tensor).item()  # Get prediction
        print(predicted_tomorrow_price)
        print(type(predicted_tomorrow_price))

    predicted_tomorrow_price = np.array(predicted_tomorrow_price)
    # # Denormalize the predicted price
    predicted_tomorrow_price_original = denormalize_with_sklearn(predicted_tomorrow_price, scaler_test, column_index=0)[0]
    
    print(predicted_tomorrow_price_original)

    # # # # Print the last few rows to verify
    # print(df_test.tail())


    
    
    return mape,test_mape,predicted_tomorrow_price_original


def just_test(df,model_path):
    model = PriceForecasterGRU(input_size=2, hidden_size=64,
                               output_size=1, num_layers=2,
                               dropout=0.3)
    try:
        model.load_state_dict(torch.load(model_path))
        print("Model successfully loaded")
    except Exception as e:
        print(f"Exception occured: {e}")
        
        
    train_size = 0.8
    split_index = int(len(df) * train_size)
    df_train = df[:split_index]
    df_test = df[split_index:]


    #Normalize
    columns_to_normalize = ['Close', 'RSI']
    df_train_normalized, scaler_train = normalize_with_sklearn(df_train, 
                                                               columns_to_normalize)
    df_test_normalized, scaler_test = normalize_with_sklearn(df_test,
                                                             columns_to_normalize)

    
    #Train
    n_days = 5
    predictions,test_mape = test_gru_model(model,df_test_normalized,n_days)
    predictions_original_scale = denormalize_with_sklearn(predictions,scaler_test, column_index=0)
    print(f"Testing MAPE (Original Scale): {test_mape:.2f}%")
    predictions_series = pd.Series(predictions_original_scale, index=df_test.index[n_days:])
    predictions_series = predictions_series.rename('Predicted Value')

    # # # Merge the series with the DataFrame on the index
    merged_df = df_test.merge(predictions_series, left_index=True,
                            right_index=True, how='left')

    # # print(merged_df)
    df_test = merged_df.dropna()
    # # # # Print the last few rows to verify
    print("******* Actual vs Prediction **************")
    df_test = df_test[['Close','Predicted Value']]
    print(df_test.tail())
    
    
    
    last_5_days = df_test_normalized[['Close', 'RSI']].tail(5).values  # Extract last 5 days as input
    last_5_days_tensor = torch.tensor(last_5_days, dtype=torch.float32).unsqueeze(0)  # Add batch dim
    with torch.no_grad():
        predicted_tomorrow_price = model(last_5_days_tensor).item()  # Get prediction
        print(predicted_tomorrow_price)
        print(type(predicted_tomorrow_price))

    predicted_tomorrow_price = np.array(predicted_tomorrow_price)
    # # Denormalize the predicted price
    predicted_tomorrow_price_original = denormalize_with_sklearn(predicted_tomorrow_price, scaler_test, column_index=0)[0]
    
    print(predicted_tomorrow_price_original)
    
    
    
    
    return df_test,test_mape,predicted_tomorrow_price_original

        
    
    

#read the data from api
#symbol = "ADBL","NTC","JOSHI","KBL","MMKJL","NICA","PHCL",
# "OHL","SCBD","SHLB","SINDU","UNL","WNLB"
# user_input = "ANLB"
# # selected_date = "2020-01-01"


# df,model_path = read_prepare_data(user_input=user_input)
# mape,test_mape = train_and_test(df,model_path=model_path)
# print(f"Train ERROR: {mape}, Test ERROR:{test_mape}")

# #retrain the model if test_mape is greater than 100
# while test_mape>100:
#     model_path = f"{user_input}_price_forecaster_gru_l2_four_layers.pth"
#     mape,test_mape = train_and_test(df,model_path=model_path)
#     print(f"Train ERROR: {mape}, Test ERROR:{test_mape}")
    
    
    