from pathlib import Path

from .analyzer import analyze
from .analyzer_v2 import analyze_v2
from .models import Profile, Role


def create_app():
    try:
        from fastapi import FastAPI
        from fastapi.staticfiles import StaticFiles
    except ImportError as exc:
        raise RuntimeError("Install the api extra: pip install 'linkedin-optimizer[api]'") from exc

    app = FastAPI(
        title="LinkedIn Optimizer",
        version="0.1.0",
        description="Evidence-first career intelligence with a deterministic compatibility baseline and calibrated v2 analysis.",
    )

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": "linkedin-optimizer"}

    @app.post("/analyze")
    def analyze_profile(profile: Profile, role: Role):
        """Compatibility endpoint for the original scoring contract."""
        return analyze(profile, role)

    @app.post("/v2/analyze")
    def analyze_profile_v2(profile: Profile, role: Role):
        """Calibrated analysis with independent quality dimensions and safe rewrites."""
        return analyze_v2(profile, role)

    web_root = Path(__file__).resolve().parents[2] / "web"
    if web_root.exists():
        app.mount("/", StaticFiles(directory=web_root, html=True), name="web")
    return app


app = create_app() if __name__ != "__main__" else None
