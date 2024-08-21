import pandas as pd
import joblib

def predict_size(weight, age, height):
    """
    Predicts the size based on weight, age, and height using a pre-trained model.

    Parameters:
    weight (float): Weight of the individual
    age (float): Age of the individual
    height (float): Height of the individual in centimeters

    Returns:
    str: Predicted size (e.g., XS, S, M, L, XL)
    """

    # Load the pre-trained model and label encoder
    model = joblib.load('/home/mohammad/Desktop/Needle-Haven-main (1)/Needle-Haven-main/main_models_classes/size_pred/size_prediction_model.pkl')
    label_encoder = joblib.load('/home/mohammad/Desktop/Needle-Haven-main (1)/Needle-Haven-main/main_models_classes/size_pred/size_label_encoder.pkl')

    # Create a DataFrame for the input
    input_data = pd.DataFrame({
        'weight': [weight],
        'age': [age],
        'height': [height]
    })

    # Make a prediction
    predicted_size_encoded = model.predict(input_data)

    # Decode the predicted size
    predicted_size = label_encoder.inverse_transform(predicted_size_encoded)

    # Return the predicted size
    return predicted_size[0]

# Example usage:
predicted_size = predict_size(62, 28.0, 172.72)
print(f'Predicted Size: {predicted_size}')
