import pandas as pd
import joblib

def predict_growth(cagr_net_income, cagr_revenues):
    """
    Predicts the Expected Growth in Revenues for the Next 2 Years based on financial growth indicators.

    Parameters:
    cagr_net_income (float): CAGR in Net Income over the last 5 years
    cagr_revenues (float): CAGR in Revenues over the last 5 years

    Returns:
    float: Predicted Expected Growth in Revenues - Next 2 Years
    """

    # Load the pre-trained model
    model = joblib.load('/home/mohammad/Desktop/Needle-Haven-main (1)/Needle-Haven-main/main_models_classes/eps_growth_pred/growth_prediction_model.pkl')

    # Create a DataFrame for the input
    input_data = pd.DataFrame({
        'CAGR_Net_Income_5Y': [cagr_net_income],
        'CAGR_Revenues_5Y': [cagr_revenues]
    })

    # Make a prediction
    predicted_growth = model.predict(input_data)

    # Return the predicted growth
    return predicted_growth[0]

# Example usage:
predicted_growth = predict_growth(2.19, 11.57)
print(f'Predicted Expected Growth in Revenues - Next 2 Years: {predicted_growth}')
