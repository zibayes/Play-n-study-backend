def user_to_json(user):
    return {
        "id": user.user_id,
        "email": user.email,
        "username": user.username,
        "city": user.city,
        "password": user.password
    }
