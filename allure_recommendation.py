#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# Load the datasets uploaded by the user
products_df = pd.read_csv('product_info.csv')
reviews_df = pd.read_csv('reviews_250-500.csv')

# Display the first few rows of each dataset to understand their structure
reviews_df.head(), products_df.head()


# In[2]:


# Drop rows with null values in both datasets
reviews_df_cleaned = reviews_df.dropna()
products_df_cleaned = products_df.dropna()

# Filter products to only include 'makeup' in primary_category
makeup_products_df = products_df_cleaned[products_df_cleaned['primary_category'].str.lower() == 'makeup']

# Display the cleaned datasets' basic info to confirm the changes
reviews_df_cleaned.info(), makeup_products_df.info()


# In[3]:


def recommend_products(skin_type, reviews_df, products_df, max_recommendations=5):
    # Step 1: Filter reviews based on skin type
    filtered_reviews = reviews_df[reviews_df['skin_type'].str.lower() == skin_type.lower()]
    
    # Step 2: Sort by rating and helpfulness (highest ratings and most helpful reviews first)
    sorted_reviews = filtered_reviews.sort_values(by=['rating', 'helpfulness'], ascending=False)
    
    # Step 3: Get top-rated and most helpful product recommendations
    top_reviewed_products = sorted_reviews['product_name'].unique()[:max_recommendations]

    # Step 4: Sort products by loves_count and rating in the products dataset
    sorted_products = products_df.sort_values(by=['loves_count', 'rating'], ascending=False)

    # Step 5: Filter out any products already recommended based on reviews
    top_product_recommendations = sorted_products[~sorted_products['product_name'].isin(top_reviewed_products)]
    
    # Get the next highest-rated products from the products dataset
    final_recommendations = list(top_reviewed_products) + list(top_product_recommendations['product_name'].unique()[:max_recommendations - len(top_reviewed_products)])
    
    # Return up to max_recommendations unique products
    return final_recommendations[:max_recommendations]

# Example: Recommend for "oily" skin type
recommendations = recommend_products('oily', reviews_df_cleaned, makeup_products_df)
recommendations


# In[4]:


# Function to recommend products for all skin types
def recommend_for_all_skin_types(reviews_df, products_df, skin_types, max_recommendations=5):
    recommendations = {}
    
    for skin_type in skin_types:
        recommendations[skin_type] = recommend_products(skin_type, reviews_df, products_df, max_recommendations)
    
    return recommendations

# Define the skin types
skin_types = ['oily', 'dry', 'combination', 'normal']

# Generate recommendations for all skin types
all_skin_type_recommendations = recommend_for_all_skin_types(reviews_df_cleaned, makeup_products_df, skin_types)

all_skin_type_recommendations


# In[5]:


def recommend_products_for_skin_type(skin_type, reviews_df, products_df, max_recommendations=5, exclude_products=[]):
    # Step 1: Filter reviews for the specific skin type and exclude already recommended products
    filtered_reviews = reviews_df[(reviews_df['skin_type'].str.lower() == skin_type.lower()) & (~reviews_df['product_name'].isin(exclude_products))]
    
    # Step 2: Sort by rating and helpfulness to get top-rated products
    sorted_reviews = filtered_reviews.sort_values(by=['rating', 'helpfulness'], ascending=False)
    top_reviewed_products = sorted_reviews['product_name'].unique()[:max_recommendations]

    # Step 3: Filter product dataset for makeup category and exclude already recommended products
    sorted_products = products_df[~products_df['product_name'].isin(list(top_reviewed_products) + exclude_products)].sort_values(by=['loves_count', 'rating'], ascending=False)
    
    # Step 4: Combine top review-based and product-based recommendations
    recommendations = list(top_reviewed_products) + list(sorted_products['product_name'].unique()[:max_recommendations - len(top_reviewed_products)])
    
    # Return the final recommendations (maximum of max_recommendations)
    return recommendations[:max_recommendations]

def recommend_for_all_skin_types(reviews_df, products_df, skin_types, max_recommendations=5):
    recommendations = {}
    all_recommended_products = []  # Keep track of all recommended products to avoid duplicates
    
    for skin_type in skin_types:
        # Get recommendations for each skin type and exclude already recommended products
        recommendations[skin_type] = recommend_products_for_skin_type(skin_type, reviews_df, products_df, max_recommendations, all_recommended_products)
        
        # Add the recommended products for this skin type to the exclusion list
        all_recommended_products.extend(recommendations[skin_type])
    
    return recommendations

# Define the skin types
skin_types = ['oily', 'dry', 'combination', 'normal']

# Generate recommendations for all skin types
all_skin_type_recommendations = recommend_for_all_skin_types(reviews_df_cleaned, makeup_products_df, skin_types)

print(all_skin_type_recommendations)


# In[6]:


def recommend_products_with_weights(skin_type, reviews_df, products_df, max_recommendations=5, exclude_products=[], 
                                   weight_rating=0.4, weight_helpfulness=0.3, weight_loves=0.3):
    # Step 1: Filter reviews for the specific skin type and exclude already recommended products
    filtered_reviews = reviews_df[(reviews_df['skin_type'].str.lower() == skin_type.lower()) & (~reviews_df['product_name'].isin(exclude_products))]
    
    # Step 2: Add a weighted score for each product in the review dataset
    filtered_reviews['weighted_score'] = (weight_rating * filtered_reviews['rating'] + 
                                          weight_helpfulness * filtered_reviews['helpfulness'])
    
    # Sort by weighted score to get top-rated products
    sorted_reviews = filtered_reviews.sort_values(by='weighted_score', ascending=False)
    top_reviewed_products = sorted_reviews['product_name'].unique()[:max_recommendations]

    # Step 3: Sort products in the product dataset based on loves_count and rating
    products_df['weighted_score'] = (weight_rating * products_df['rating'] + 
                                     weight_loves * products_df['loves_count'])
    
    sorted_products = products_df[~products_df['product_name'].isin(list(top_reviewed_products) + exclude_products)]
    sorted_products = sorted_products.sort_values(by='weighted_score', ascending=False)

    # Step 4: Combine top review-based and product-based recommendations
    recommendations = list(top_reviewed_products) + list(sorted_products['product_name'].unique()[:max_recommendations - len(top_reviewed_products)])
    
    return recommendations[:max_recommendations]


# In[7]:


# Recommendations for "dry" skin type with more emphasis on ratings and helpfulness
recommendations_dry = recommend_products_with_weights('dry', reviews_df_cleaned, makeup_products_df, 
                                                     weight_rating=0.5, weight_helpfulness=0.4, weight_loves=0.1)

print(recommendations_dry)


# In[8]:


# List of skin types to test
skin_types = ['oily', 'dry', 'combination', 'normal']

# Loop through each skin type and print the recommendations
for skin_type in skin_types:
    print(f"Recommendations for {skin_type} skin:")
    
    # Call the recommendation function for the current skin type
    recommendations = recommend_products_with_weights(
        skin_type, 
        reviews_df_cleaned,   # Pass the cleaned reviews dataframe
        makeup_products_df,   # Pass the products dataframe filtered to 'makeup'
        max_recommendations=5, # You can change this number as needed
        weight_rating=0.5,    # Adjust weights to your preference
        weight_helpfulness=0.3,
        weight_loves=0.2
    )
    
    # Print the recommendations for this skin type
    print(recommendations)
    print('-' * 50)  # Separator for better readability


# In[ ]:




