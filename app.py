from flask import Flask, request, jsonify
import pandas as pd
from allure_recommendation import recommend_products_with_weights

app = Flask(__name__)

# Load your dataframes
reviews_df_cleaned = pd.read_csv("C:\\Users\\Bushra Jazeem\\Downloads\\allure123 projcet\\reviews_250-500.csv")
makeup_products_df = pd.read_csv("C:\\Users\\Bushra Jazeem\\Downloads\\allure123 projcet\\product_info.csv")

@app.route('/recommend', methods=['POST'])
def recommend():
    skin_type = request.json.get('skin_type', 'oily')  # Default to 'oily' if not provided
    recommendations = recommend_products_with_weights(skin_type, reviews_df_cleaned, makeup_products_df)
    return jsonify(recommendations)

if __name__ == "__main__":
    app.run(debug=True)


