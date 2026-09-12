import argparse
import json

from .analyzer import analyze
from .models import Profile, Role


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a LinkedIn profile against a target role.")
    parser.add_argument("profile", help="Path to a JSON profile document")
    parser.add_argument("--role", required=True, help="Target role title")
    parser.add_argument("--description", default="", help="Target role description")
    args = parser.parse_args()

    with open(args.profile, encoding="utf-8") as handle:
        profile = Profile.model_validate(json.load(handle))
    report = analyze(profile, Role(title=args.role, description=args.description))
    print(json.dumps(report.model_dump(), indent=2))
