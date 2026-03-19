import pytest
import os
from src.engines.engine_volc import VolcEngine
from src.engines.engine_auth_gen import PollinationsEngine

def test_volc_engine_init():
    engine = VolcEngine(api_key="test_key")
    assert engine.api_key == "test_key"
    assert "volces.com" in engine.url

def test_pollinations_engine_init():
    engine = PollinationsEngine(api_key="sk_test")
    assert engine.api_key == "sk_test"
    assert "pollinations.ai" in engine.base_url

# 模拟测试，不实际调用网络
def test_engine_prompt_encoding():
    import urllib.parse
    prompt = "汉代 大将军"
    encoded = urllib.parse.quote(prompt)
    assert "%" in encoded
