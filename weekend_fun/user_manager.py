import json
from typing import Any


def get_user_info() -> dict[str, Any]:
    try:
        with open("config/user_info.json", "r") as f:
            user_info = json.load(f)
            return {
                "name": user_info["name"],
                "city": user_info["city"],
                "email": user_info["email"],
                "interests": [i.strip() for i in user_info["interests"]],
            }
    except FileNotFoundError:
        print("Error: data/user_info.json file not found")
        return {}
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in data/user_info.json")
        return {}
    except KeyError as e:
        print(f"Error: Missing required field {e} in user_info.json")
        return {}
