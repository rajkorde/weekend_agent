from __future__ import annotations

import json

from pydantic import BaseModel


class FeatureFlags(BaseModel):
    scrape: bool
    extract: bool
    filter: bool
    rank: bool
    email: bool
    save: bool
    use_test_events: bool
    use_docker: bool

    @classmethod
    def read_feature_flags(
        cls, file_path: str = "config/feature_flags.json"
    ) -> FeatureFlags:
        with open(file_path, "r") as f:
            data = json.load(f)
            return FeatureFlags(**data)
