import json

from linkedin_optimizer.cli import main


def test_cli_accepts_v2_scoring(tmp_path, monkeypatch, capsys):
    profile = {
        "headline": "Senior AI Engineer | Python | RAG",
        "about": "I build production AI systems with measurable outcomes.",
        "experience": [
            "Architected and deployed a RAG service for 10K users, reducing latency by 35%."
        ],
        "skills": ["Python", "RAG", "PostgreSQL"],
    }
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(profile), encoding="utf-8")

    monkeypatch.setattr(
        "sys.argv",
        ["linkedin-optimizer", str(path), "--role", "Senior AI Engineer", "--scoring", "v2"],
    )

    main()
    output = json.loads(capsys.readouterr().out)
    names = {signal["name"] for signal in output["signals"]}
    assert "evidence_quality" in names
    assert "seniority_alignment" in names


def test_cli_defaults_to_v1(tmp_path, monkeypatch, capsys):
    profile = {"headline": "AI Engineer", "experience": ["Built software."]}
    path = tmp_path / "profile.json"
    path.write_text(json.dumps(profile), encoding="utf-8")

    monkeypatch.setattr("sys.argv", ["linkedin-optimizer", str(path), "--role", "AI Engineer"])

    main()
    output = json.loads(capsys.readouterr().out)
    names = {signal["name"] for signal in output["signals"]}
    assert "evidence_quality" not in names
    assert "measurable_evidence" in names
