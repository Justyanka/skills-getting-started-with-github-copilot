import pytest


def test_get_activities(client):
    # Arrange: (fixture provides client and clean state)

    # Act
    res = client.get("/activities")

    # Assert
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success_and_appears_in_list(client):
    # Arrange
    activity = "Art Club"
    email = "testuser+1@example.com"

    # Act
    res = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert res.status_code == 200
    assert email in res.json().get("message", "")

    # Act: fetch activities and verify participant present
    all_res = client.get("/activities")
    participants = all_res.json()[activity]["participants"]
    assert email in participants


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity = "Chess Club"
    email = "duplicate@example.com"

    # Act - first signup
    first = client.post(f"/activities/{activity}/signup?email={email}")
    assert first.status_code == 200

    # Act - duplicate signup
    second = client.post(f"/activities/{activity}/signup?email={email}")

    # Assert
    assert second.status_code == 400
    assert "already" in second.json().get("detail", "").lower()


def test_unregister_success_and_removed(client):
    # Arrange: sign someone up first
    activity = "Programming Class"
    email = "toremove@example.com"
    signup = client.post(f"/activities/{activity}/signup?email={email}")
    assert signup.status_code == 200

    # Act: remove
    res = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert res.status_code == 200
    # Verify removed
    all_res = client.get("/activities")
    participants = all_res.json()[activity]["participants"]
    assert email not in participants


def test_unregister_not_found_returns_404(client):
    # Arrange
    activity = "Gym Class"
    email = "nonexistent@example.com"

    # Act
    res = client.delete(f"/activities/{activity}/participants?email={email}")

    # Assert
    assert res.status_code == 404
    assert "not found" in res.json().get("detail", "").lower()
