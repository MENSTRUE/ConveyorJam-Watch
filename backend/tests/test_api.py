import os
from pathlib import Path

os.environ["CONVEYOR_DATA_DIR"] = str(Path(__file__).resolve().parent / ".runtime_test")
from fastapi.testclient import TestClient
from app.main import app, DwellEngine, MonitorConfig

client = TestClient(app)

def test_health():
    r = client.get('/api/v1/health')
    assert r.status_code == 200 and r.json()['mode'] == 'research-prototype'

def test_config_roundtrip():
    config = client.get('/api/v1/config').json()
    assert client.post('/api/v1/config', json=config).status_code == 200
    bad = {**config, 'roi': [0.8, 0.1, 0.2, 0.9]}
    assert client.post('/api/v1/config', json=bad).status_code == 422

def test_empty_history():
    assert isinstance(client.get('/api/v1/history').json(), list)

def test_missing_model_returns_503():
    from app import main
    original = main.MODEL_PATH
    main.MODEL_PATH = Path('/missing/test/champion.pt')
    try:
        assert client.post('/api/v1/analyze/image', files={'file': ('test.png', b'not-real-image', 'image/png')}).status_code == 422
        # Test a valid encoded image
        import cv2, numpy as np
        ok, buffer = cv2.imencode('.png', np.zeros((64, 64, 3), dtype=np.uint8))
        assert ok
        result = client.post('/api/v1/analyze/image', files={'file': ('test.png', buffer.tobytes(), 'image/png')})
        assert result.status_code == 503
    finally:
        main.MODEL_PATH = original

def test_dwell_positive_case():
    engine = DwellEngine(MonitorConfig(dwell_seconds=1, stationary_px_per_second=8, min_observations=2), 640, 360)
    for i in range(30):
        obj = {'track_id': 5, 'bbox': [110, 110, 150, 150], 'label': 'conveyor'}
        engine.update([obj], i/10)
    assert len(engine.events) == 1
