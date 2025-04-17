def get_user_payload(username="user1", role="user"):
    return {
        "username": username,
        "email": f"{username}@example.com",
        "password": "testpass123",
        "role": role
    }
