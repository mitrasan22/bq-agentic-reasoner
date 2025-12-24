import uuid


def generate_session_id() -> str:
    """
    Generate a new session ID.
    """
    return str(uuid.uuid4())
