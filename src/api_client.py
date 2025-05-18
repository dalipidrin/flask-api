# This script interacts with the Bank API using HTTP requests to create, read, update, and delete bank records.

import requests

base_url = "http://localhost:5000/api/banks"

# create a new bank
response = requests.post(base_url, json={"name": "Bank A", "location": "London"})
print("Created:", response.json())

# retrieve all banks
response = requests.get(base_url)
print("All Banks:", response.json())

# get details of a specific bank
bank_id = '<bank_id>'  # bank id should be taken from db
response = requests.get(f"{base_url}/{bank_id}")
print(f"Details for bank with id: {bank_id}", response.json())

# update a bank
response = requests.put(f"{base_url}/{bank_id}", json={"name": "Updated Bank", "location": "Paris"})
print(f"Updated bank with id: {bank_id}", response.json())

# delete a bank
response = requests.delete(f"{base_url}/{bank_id}")
print(f"Deleted bank with id: {bank_id}", response.json())
