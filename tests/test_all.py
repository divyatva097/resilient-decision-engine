import pytest
import json
from src.engine.orchestrator import DecisionEngine
from src.mocks.external_api import ExternalBureau

class MockDB:
    def __init__(self): self.db = {}
    def get(self, rid): return self.db.get(rid)
    def save(self, rid, val): self.db[rid] = val

class MockLogger:
    def log(self, rid, msg): pass
    def record_decision(self, rid, stage, rule, passed, reason): pass

@pytest.fixture
def engine():
    with open('config/loan_workflow.json') as f:
        config = json.load(f)
    # Using a fresh MockDB for every test
    return DecisionEngine(config, MockDB(), ExternalBureau(), MockLogger())

def test_happy_path(engine):
    req_id = "HAPPY_001"
    data = {"age": 25}
    res, mode = engine.process(req_id, data)
    assert res['final_status'] == "APPROVED"
    assert mode == "NEW_DECISION"

def test_idempotency_logic(engine):
    req_id = "IDEM_001"
    data = {"age": 30}
    res1, mode1 = engine.process(req_id, data)
    res2, mode2 = engine.process(req_id, data)
    assert mode1 == "NEW_DECISION"
    assert mode2 == "IDEMPOTENT_RETRIEVAL"
    assert res1 == res2

def test_rejection_logic(engine):
    req_id = "REJECT_001"
    data = {"age": 16} # Fails R1_AGE_CHECK (min 18)
    res, mode = engine.process(req_id, data)
    assert res['final_status'] == "REJECT"