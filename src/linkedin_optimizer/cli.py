import argparse
import json

from .analyzer import analyze
from .io import read_text
from .models import Profile, Role


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a LinkedIn profile against a target role.")
    parser.add_argument("profile", help="Path to a JSON profile document")
    parser.add_argument("--role", required=True, help="Target role title")
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--description", default=None, help="Target role description")
    source.add_argument("--job", help="Path to a UTF-8 job description")
    args = parser.parse_args()

    with open(args.profile, encoding="utf-8") as handle:
        profile = Profile.model_validate(json.load(handle))

    description = read_text(args.job) if args.job else (args.description or "")
    report = analyze(profile, Role(title=args.role, description=description))
    print(json.dumps(report.model_dump(), indent=2))
