from .analyzer import analyze
from .models import Profile, Role


def create_app():
    """Build the optional FastAPI application; import FastAPI only when requested."""
    try:
        from fastapi import FastAPI
    except ImportError as exc:
        raise RuntimeError("Install the api extra: pip install 'linkedin-optimizer[api]'") from exc

    app = FastAPI(title="LinkedIn Optimizer", version="0.1.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/analyze")
    def analyze_profile(profile: Profile, role: Role):
        return analyze(profile, role)

    return app


app = create_app() if __name__ != "__main__" else None
