import pandas as pd
import joblib

def predict_average_rating(product_name, gender, category, color, age_group, season, price, material, sales_count, brand, discount):
    """
    Predicts the average rating of a product based on its features using a pre-trained model.

    Parameters:
    product_name (str): Name of the product
    gender (str): Gender for which the product is designed
    category (str): Category of the product (e.g., Shirt, Jacket)
    color (str): Color of the product
    age_group (str): Age group target (e.g., 25-35)
    season (str): Season for which the product is suitable (e.g., Spring)
    price (float): Price of the product
    material (str): Material of the product (e.g., Synthetic)
    sales_count (int): Number of sales made
    brand (str): Brand of the product
    discount (float): Discount applied on the product

    Returns:
    float: Predicted average rating of the product
    """

    # Load the pre-trained model
    model = joblib.load('/home/mohammad/Desktop/Needle-Haven-main (1)/Needle-Haven-main/main_models_classes/costumer _rating_pred/average_rating_prediction_model.pkl')

    # Create a DataFrame for the input
    input_data = pd.DataFrame({
        'product_name': [product_name],
        'gender': [gender],
        'category': [category],
        'color': [color],
        'age_group': [age_group],
        'season': [season],
        'price': [price],
        'material': [material],
        'sales_count': [sales_count],
        'brand': [brand],
        'discount': [discount]
    })

    # Make a prediction
    predicted_rating = model.predict(input_data)

    # Return the predicted average rating
    return predicted_rating[0]

# Example usage:
predicted_rating = predict_average_rating('Biker Jacket', 'Male', 'Shirt', 'White', '25-35', 'Spring', 70.36, 'Synthetic', 75, 'ZARA', 20)
print(f'Predicted Average Rating: {predicted_rating}')
