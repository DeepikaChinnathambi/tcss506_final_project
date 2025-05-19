# users.py

users_db = {}  # In-memory user store: {username: password}

def register_user(username, password):
    print(f"[INFO] Attempting to register user: {username}")
    if username in users_db:
        return False, "Username already exists"
    
    users_db[username] = password
    return True, "User registered successfully"

def validate_login(username, password):
        # Validate user credentials
    
    print(f"[INFO] Validating login for user: {username}")
    if username in users_db and users_db[username] == password:
        return True, "Login successful"
    else:
        return False, "Invalid username or password"

def get_all_users():
    return users_db
