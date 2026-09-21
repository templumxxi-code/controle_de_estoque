from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / 'frontend'
if str(FRONTEND) not in sys.path:
    sys.path.insert(0, str(FRONTEND))

from services.api import call


class FakeResponse:
    status_code = 200
    content = b'<html>not json</html>'

    def json(self):
        raise ValueError('not json')


def test_call_handles_non_json_success_response(monkeypatch):
    def fake_request(method, url, headers=None, timeout=None, **kwargs):
        return FakeResponse()

    monkeypatch.setattr('services.api.HTTP_SESSION.request', fake_request)

    with pytest.raises(RuntimeError, match='Resposta inválida|JSON|API'):
        call('GET', '/public/branding')
