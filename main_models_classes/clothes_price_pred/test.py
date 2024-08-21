import pandas as pd
import joblib

def predict_price(brand, category, color, size, material):
    """
    Predicts the price of an item based on its features using a pre-trained model.

    Parameters:
    brand (str): Brand of the item
    category (str): Category of the item (e.g., Dress, Shirt, etc.)
    color (str): Color of the item
    size (str): Size of the item (e.g., XS, S, M, L, XL)
    material (str): Material of the item (e.g., Nylon, Cotton, etc.)

    Returns:
    float: Predicted price of the item
    """

    # Load the pre-trained model
    model = joblib.load('/home/mohammad/Desktop/Needle-Haven-main (1)/Needle-Haven-main/main_models_classes/clothes_price_pred/clothes_price_predprice_prediction_model.pkl')

    # Create a DataFrame for the input
    input_data = pd.DataFrame({
        'Brand': [brand],
        'Category': [category],
        'Color': [color],
        'Size': [size],
        'Material': [material]
    })

    # Make a prediction
    predicted_price = model.predict(input_data)

    # Return the predicted price
    return predicted_price[0]

# Example usage:
predicted_price = predict_price('New Balance', 'Dress', 'White', 'XS', 'Nylon')
print(f'Predicted Price: {predicted_price}')
