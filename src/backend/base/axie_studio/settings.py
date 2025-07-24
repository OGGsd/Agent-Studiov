from typing import Optional

AXIE_STUDIO_BACKEND_HOST: Optional[str] = None
AXIE_STUDIO_API_URL: str = "https://api.axiestudio.se"
AXIE_STUDIO_DOCS_URL: str = "https://docs.axiestudio.se"
AXIE_STUDIO_FRONTEND_URL: str = "https://axiestudio.se"

# Global development mode flag
DEV: bool = False

def set_dev(value: bool) -> None:
    """Set the global development mode flag."""
    global DEV
    DEV = value
