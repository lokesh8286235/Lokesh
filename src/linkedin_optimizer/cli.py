import argparse
import json

from .analyzer import analyze
from .analyzer_v2 import analyze_v2
from .compare import compare
from .documents import load_document
from .io import read_text
from .models import Profile, Role


def _load_profile(path: str | None, resume: str | None) -> Profile:
    if resume:
        return load_document(resume)
    if not path:
        raise ValueError("Provide a profile JSON path or --resume.")
    with open(path, encoding="utf-8") as handle:
        return Profile.model_validate(json.load(handle))


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze a LinkedIn profile against a target role.")
    parser.add_argument("profile", nargs="?", help="Path to a JSON profile document")
    parser.add_argument("--resume", help="Path to a TXT/Markdown/PDF/DOCX resume")
    parser.add_argument("--role", required=True, help="Target role title")
    parser.add_argument(
        "--scoring",
        choices=("v1", "v2"),
        default="v1",
        help="Scoring engine to use (default: v1).",
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--description", default=None, help="Target role description")
    source.add_argument("--job", help="Path to a UTF-8 job description")
    source.add_argument("--compare", nargs=2, metavar=("BEFORE", "AFTER"), help="Compare two JSON profiles")
    args = parser.parse_args()

    description = read_text(args.job) if args.job else (args.description or "")
    role = Role(title=args.role, description=description)
    if args.compare:
        if args.scoring == "v2":
            raise ValueError("--compare currently supports the v1 scoring contract only.")
        with open(args.compare[0], encoding="utf-8") as handle:
            before = Profile.model_validate(json.load(handle))
        with open(args.compare[1], encoding="utf-8") as handle:
            after = Profile.model_validate(json.load(handle))
        print(json.dumps(compare(before, after, role).model_dump(), indent=2))
        return

    profile = _load_profile(args.profile, args.resume)
    analyzer = analyze_v2 if args.scoring == "v2" else analyze
    print(json.dumps(analyzer(profile, role).model_dump(), indent=2))
