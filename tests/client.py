import requests


class StatusApiClient:
    """Client for interacting with the Status API"""

    def __init__(self, session: requests.Session, base_url: str) -> None:
        self.client = session
        self.base_url = base_url

    def _make_url(self, endpoint: str) -> str:
        """Helper to construct full URL for API requests."""
        return f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

    def get_status(self) -> tuple[int, str | None]:
        """Get current version status"""
        response = self.client.get(self._make_url("/status"))
        data = response.json()
        return response.status_code, data.get("version") if data else None

    def set_status(self) -> int:
        """Set initial version status"""
        response = self.client.post(self._make_url("/setStatus"))
        return response.status_code

    def update_status(self) -> int:
        """Update to next minor version"""
        response = self.client.patch(self._make_url("/updateStatus"))
        return response.status_code

    def rewrite_status(self) -> int:
        """Rewrite to next major version"""
        response = self.client.put(self._make_url("/rewriteStatus"))
        return response.status_code

    def remove_status(self) -> int:
        """Remove version status"""
        response = self.client.delete(self._make_url("/removeStatus"))
        return response.status_code

    def rollback_status(self, version: str | None = None) -> int:
        """Rollback to previous or specific version"""
        data = {"version": version} if version else {}
        response = self.client.post(self._make_url("/rollbackStatusVersion"), json=data)
        return response.status_code
