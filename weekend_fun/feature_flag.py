import json

from pydantic import BaseModel


class FeatureFlags(BaseModel):
    scrape: bool
    extract: bool
    rank: bool
    email: bool

    @classmethod
    def read_feature_flags(cls, file_path: str = "config/feature_flags.json"):
        with open("feature_flags.json") as f:
            data = json.load(f)
            return FeatureFlags(**data)
