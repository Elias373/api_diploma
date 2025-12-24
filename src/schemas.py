from typing import List, Optional
from pydantic import BaseModel, Field, validator


class Pet(BaseModel):
    id: Optional[int] = None
    name: str = Field(..., min_length=1, max_length=100)
    photoUrls: List[str] = Field(default_factory=list)
    status: Optional[str] = Field(None, regex="^(available|pending|sold)$")

    @classmethod
    @validator("photoUrls")
    def validate_photo_urls(cls, v):
        for url in v:
            if not url.startswith(("http://", "https://")):
                raise ValueError(f"Invalid URL: {url}")
        return v

    def dict(self, **kwargs):
        return super().dict(exclude_none=True, **kwargs)


class Order(BaseModel):
    id: Optional[int] = None
    petId: Optional[int] = Field(None, ge=1)
    quantity: Optional[int] = Field(1, ge=1, le=100)
    status: Optional[str] = Field(None, regex="^(placed|approved|delivered)$")
    complete: Optional[bool] = False

    def dict(self, **kwargs):
        return super().dict(exclude_none=True, **kwargs)
