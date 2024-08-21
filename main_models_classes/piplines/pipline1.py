import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import pickle

class DecisionTreeRegressorModel:
    def __init__(self, csv_path, target_feature):
        self.csv_path = csv_path
        self.target_feature = target_feature
        self.model = None
        self.pipeline = None

    def load_and_preprocess_data(self):
        # Load data from CSV
        data = pd.read_csv(self.csv_path)
        
        # Drop columns that are purely numerical (like 1, 2, 3, ...)
        data = data.loc[:, ~data.columns.str.match(r'^\d+$')]
        
        # Split data into features and target
        X = data.drop(columns=[self.target_feature])
        y = data[self.target_feature]
        
        # Identify categorical features (strings) and numerical features
        categorical_features = X.select_dtypes(include=['object']).columns
        numerical_features = X.select_dtypes(exclude=['object']).columns
        
        # Define preprocessing for categorical and numerical features
        preprocessor = ColumnTransformer(
            transformers=[
                ('num', StandardScaler(), numerical_features),
                ('cat', OneHotEncoder(), categorical_features)
            ])
        
        # Create a pipeline with preprocessing and model
        self.pipeline = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', DecisionTreeRegressor(random_state=42))
        ])
        
        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        return X_train, X_test, y_train, y_test

    def train(self):
        # Load and preprocess data
        X_train, X_test, y_train, y_test = self.load_and_preprocess_data()
        
        # Train the Decision Tree Regressor
        self.pipeline.fit(X_train, y_train)
        
        # Predict and evaluate the model
        y_pred = self.pipeline.predict(X_test)
        mse = mean_squared_error(y_test, y_pred)
        print(f'Mean Squared Error: {mse}')
        
        # Save the trained model
        self.save_model()
        
        # Generate a usage file
        self.generate_usage_instructions()

    def save_model(self):
        model_filename = 'decision_tree_regressor_model.pkl'
        
        # Save the model to disk
        with open(model_filename, 'wb') as model_file:
            pickle.dump(self.pipeline, model_file)
        
        print(f'Model saved as {model_filename}')
    
    def generate_usage_instructions(self):
        instructions = (
            "To use the saved model:\n"
            "1. Load the model using pickle:\n"
            "   with open('decision_tree_regressor_model.pkl', 'rb') as model_file:\n"
            "       model = pickle.load(model_file)\n\n"
            "2. Prepare your data (make sure it has the same features as the training data):\n"
            "   X_new = ...  # Your new data\n\n"
            "3. Predict using the loaded model:\n"
            "   predictions = model.predict(X_new)\n"
        )
        
        with open('regressor_model_usage_instructions.txt', 'w') as file:
            file.write(instructions)
        
        print('Instructions for using the saved model have been written to regressor_model_usage_instructions.txt')

    def predict(self, X_new):
        # Predict using the trained model
        predictions = self.pipeline.predict(X_new)
        return predictions
    
    
#DecisionTreeRegressorModel(r"C:\Users\MR Wa2el\OneDrive\Desktop\model generator\CHIC\main_models_classes\datasets\EPS_Growth.csv","Expected Growth in Revenues - Next 2 years").train()

#DecisionTreeRegressorModel(r"C:\Users\MR Wa2el\OneDrive\Desktop\model generator\CHIC\main_models_classes\datasets\costumer_rating_0-5.csv","average_rating").train()

#DecisionTreeRegressorModel(r"C:\Users\MR Wa2el\OneDrive\Desktop\model generator\CHIC\main_models_classes\datasets\clothes_price_prediction_data.csv","Price").train()