from types import SimpleNamespace

from app import ask as ask_module


def test_ask_prints_token_usage(monkeypatch, capsys):
    response = SimpleNamespace(
        usage_metadata=SimpleNamespace(prompt_token_count=12, candidates_token_count=7),
        text="回答",
    )
    calls = []

    def generate_content(**kwargs):
        calls.append(kwargs)
        return response

    client = SimpleNamespace(
        models=SimpleNamespace(generate_content=generate_content)
    )
    monkeypatch.setattr(ask_module, "get_api_key", lambda: "test-key")
    monkeypatch.setattr(ask_module.genai, "Client", lambda **kwargs: client)

    assert ask_module.ask("質問") == "回答"
    output = capsys.readouterr().out
    assert calls[0]["config"].temperature == ask_module.TEMPERATURE
    assert "入力トークン数: 12" in output
    assert "出力トークン数: 7" in output