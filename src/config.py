import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


@dataclass
class APIConfig:
    base_url: str
    timeout: int = 30

    @classmethod
    def from_env(cls, env_file: Optional[str] = None) -> "APIConfig":
        load_dotenv(env_file)
        base_url = os.getenv("BASE_URL", "https://petstore.swagger.io/v2")
        timeout = int(os.getenv("API_TIMEOUT", "30"))

        if not base_url:
            raise ValueError("BASE_URL cannot be empty")

        if not base_url.startswith(("http://", "https://")):
            raise ValueError(f"Invalid BASE_URL: {base_url}")

        return cls(base_url=base_url, timeout=timeout)
