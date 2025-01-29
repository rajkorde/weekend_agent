from typing import Dict, List, Union


def get_user_info() -> Dict[str, Union[str, List[str]]]:
    """Get user information through command line input."""
    print("Welcome to Fun Finder!")
    print("Please provide some information to help us find events for you.")

    name = input("What's your name? ")
    city = input("What city do you live in? ")
    email = input("What's your email address? ")
    interests = input("What are your interests? (separate with commas) ")

    return {
        "name": name,
        "city": city,
        "email": email,
        "interests": [i.strip() for i in interests.split(",")],
    }
