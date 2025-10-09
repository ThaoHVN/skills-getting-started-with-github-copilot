import pytest
from fastapi.testclient import TestClient
from src.app import app, activities
import copy

client = TestClient(app)

# Initial activities data for test reset
default_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Gym Class": {
        "description": "Physical education and sports activities",
        "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice basketball skills and play in tournaments",
        "schedule": "Wednesdays and Fridays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create your own masterpieces",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    }
}

@pytest.fixture(autouse=True)
def reset_activities():
    # Reset activities before each test
    activities.clear()
    activities.update(copy.deepcopy(default_activities))


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_register_and_unregister():
    activity_name = list(client.get("/activities").json().keys())[0]
    email = "testuser@example.com"
    # Register
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert response.status_code == 200
    # Unregister
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": email})
    assert response.status_code == 200


def test_register_invalid_activity():
    response = client.post("/activities/invalid_activity/signup", params={"email": "foo@bar.com"})
    assert response.status_code == 404


def test_unregister_not_signed_up():
    activity_name = list(client.get("/activities").json().keys())[0]
    response = client.post(f"/activities/{activity_name}/unregister", params={"email": "notfound@example.com"})
    assert response.status_code == 400
