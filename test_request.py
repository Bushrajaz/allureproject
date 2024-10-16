import requests

url = 'http://127.0.0.1:5000/recommend'  # Use the correct port here
data = {
    "skin_type": "oily"
}

response = requests.post(url, json=data)

# Print the response
print(response.json())
