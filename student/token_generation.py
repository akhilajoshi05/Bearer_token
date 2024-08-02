import secrets

def generate_bearer_token():
    return secrets.token_urlsafe(32)

# Generate a token
token = generate_bearer_token()
print(token)
