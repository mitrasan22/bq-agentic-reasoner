import google.auth
import google.auth.transport.requests
import requests

def get_session_id() -> str:
    try:
        # 1. Load the Application Default Credentials (ADC) you just created
        credentials, project = google.auth.default(
            scopes=["https://www.googleapis.com/auth/userinfo.email"]
        )

        # 2. Refresh the token to make it active
        auth_request = google.auth.transport.requests.Request()
        credentials.refresh(auth_request)

        # 3. Call the Google UserInfo API using the token
        response = requests.get(
            "https://www.googleapis.com/oauth2/v3/userinfo",
            headers={"Authorization": f"Bearer {credentials.token}"}
        )
        
        if response.status_code == 200:
            email = response.json().get("email")
            return email
            
    except Exception as e:
        print(f"Error fetching identity: {e}")
    
    return "unknown_user"