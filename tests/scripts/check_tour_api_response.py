"""
Check API Response - Create Tour
Run: python tests/scripts/check_tour_api_response.py
"""

import requests
import json
import time

BASE_URL       = "http://localhost:8000/api/v1"
ADMIN_EMAIL    = "admin@example.com"
ADMIN_PASSWORD = "password"

def login():
    print(f"Logging in as {ADMIN_EMAIL}...")
    res = requests.post(f"{BASE_URL}/auth/login", json={
        "email": ADMIN_EMAIL,
        "password": ADMIN_PASSWORD
    })
    if res.status_code == 200:
        data = res.json()
        token = data.get("data", {}).get("token") or data.get("token")
        return token
    print(f"Login failed: {res.status_code} - {res.text}")
    return None

def get_category_id(token):
    print("Fetching tour categories...")
    res = requests.get(f"{BASE_URL}/tour-categories", headers={"Authorization": f"Bearer {token}"})
    if res.status_code == 200:
        categories = res.json().get("data", [])
        if categories:
            return categories[0].get("id")
    return None

def check_create_tour(token, category_id):
    if not category_id:
        print("No category ID found, using fallback 1")
        category_id = 1

    timestamp = int(time.time())
    tour_data = {
        "name": f"Test Tour {timestamp}",
        "slug": f"test-tour-{timestamp}",
        "tour_category_id": category_id,
        "description": "This is a test tour created to check API response attributes.",
        "short_desc": "Short description of the test tour.",
        "itinerary": [
            {"day": 1, "title": "Welcome", "content": "Arrive and check-in."},
            {"day": 2, "title": "Touring", "content": "Visit famous places."}
        ],
        "inclusions": "Transportation, Guide, Lunch",
        "exclusions": "Personal expenses, Tips",
        "price_adult": 1500000,
        "price_child": 1000000,
        "price_infant": 500000,
        "discount_percent": 10,
        "duration": "2 days 1 night",
        "start_time": "08:00",
        "meeting_point": "Da Nang International Airport",
        "max_people": 20,
        "min_people": 2,
        "status": "active",
        "is_featured": True,
        "is_hot": False
    }

    print("\nSending POST /admin/tours request...")
    res = requests.post(
        f"{BASE_URL}/admin/tours",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        json=tour_data
    )

    print(f"Status Code: {res.status_code}")
    print("Response Body:")
    print(json.dumps(res.json(), indent=2, ensure_ascii=False))

    if res.status_code == 201:
        tour_id = res.json().get("data", {}).get("tour", {}).get("id")
        return tour_id
    return None

def cleanup(token, tour_id):
    if not tour_id:
        return
    print(f"\nCleaning up: Deleting tour ID {tour_id}...")
    res = requests.delete(
        f"{BASE_URL}/admin/tours/{tour_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    print(f"Delete Status: {res.status_code}")

if __name__ == "__main__":
    token = login()
    if token:
        cat_id = get_category_id(token)
        tour_id = check_create_tour(token, cat_id)
        if tour_id:
            cleanup(token, tour_id)
    else:
        print("Could not proceed without token.")
