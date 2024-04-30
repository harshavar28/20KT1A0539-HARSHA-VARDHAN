import pandas as pd
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from scipy.stats import randint as sp_randint

# Load the dataset
df = pd.read_csv('rainfall.csv') 

# Data Preparation
df.drop(['ANNUAL', 'Jan-Feb', 'Mar-May', 'Jun-Sep', 'Oct-Dec'], axis=1, inplace=True)
df = df.dropna()  # Remove any rows with missing values

# Ensure no leading/trailing whitespaces in label values
df['SUBDIVISION'] = df['SUBDIVISION'].str.strip()

# Encode categorical features
label_encoder = LabelEncoder()
df['SUBDIVISION'] = label_encoder.fit_transform(df['SUBDIVISION'])

# Define the features and target columns
features = ['SUBDIVISION', 'YEAR']
target_columns = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target_columns], test_size=0.2, random_state=42)

# Model Training
model = RandomForestRegressor(random_state=42)

# Define the parameter grid for tuning
param_dist = {
    'n_estimators': sp_randint(50, 200),
    'max_depth': sp_randint(5, 20),
    'min_samples_split': sp_randint(2, 10)
}

# Randomized search for hyperparameter tuning
random_search = RandomizedSearchCV(estimator=model, param_distributions=param_dist, n_iter=10, cv=3, scoring='neg_mean_absolute_error', random_state=42)
random_search.fit(X_train, y_train)

# Retrieve the best model from the search
best_model = random_search.best_estimator_

# Prediction function
def predict_rainfall(location, year, month):
    # Ensure location formatting consistency
    location = location.strip()

    # Convert input to a DataFrame
    input_data = pd.DataFrame([[location, year]], columns=features)

    # Encode location using the same label encoder
    input_data['SUBDIVISION'] = label_encoder.transform(input_data['SUBDIVISION'])

    # Predict rainfall for the given input
    prediction = best_model.predict(input_data)

    # Return the predicted rainfall for the given month
    return prediction[0][month]