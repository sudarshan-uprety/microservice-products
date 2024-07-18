from pydantic import BaseModel, field_validator


class S3Delete(BaseModel):
    """schema for product model"""
    name: str
