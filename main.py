import json
from src.engine.orchestrator import DecisionEngine
from src.mocks.external_api import ExternalBureau
from src.utils.logger import AuditLogger

# Simple in-memory storage mock to satisfy Idempotency requirements
class MockDB:
    def __init__(self): self.db = {}
    def get(self, rid): return self.db.get(rid)
    def save(self, rid, val): self.db[rid] = val

def run_system():
    # 1. Load Configuration (Fulfills 'Problem Structuring')
    try:
        with open('config/loan_workflow.json') as f:
            config = json.load(f)
    except FileNotFoundError:
        print("Error: config/loan_workflow.json not found!")
        return

    # 2. Initialize Components
    storage = MockDB()
    api = ExternalBureau() 
    logger = AuditLogger()
    
    engine = DecisionEngine(config, storage, api, logger)

    # TEST 1: New Request (Happy Path)
    print("--- Processing Request 1 ---")
    req_id = "REQ_001"
    user_data = {"age": 25}
    res, mode = engine.process(req_id, user_data)
    print(f"Result: {res['final_status']} | Mode: {mode}")
    
    # TEST 2: Same Request ID (Fulfills 'Idempotency' requirement)
    print("\n--- Processing Request 2 (Duplicate ID) ---")
    res2, mode2 = engine.process(req_id, user_data)
    print(f"Result: {res2['final_status']} | Mode: {mode2}")

    # 3. Generate Audit Log (Fulfills 'Explainability')
    logger.save_to_file(req_id)

if __name__ == "__main__":
    run_system()