import json

class AuditLogger:
    def __init__(self):
        self.full_log = {}

    def log(self, rid, msg):
        if rid not in self.full_log: self.full_log[rid] = []
        self.full_log[rid].append({"event": msg})

    def record_decision(self, rid, stage, rule_id, passed, reason):
        self.full_log[rid].append({
            "stage": stage,
            "rule": rule_id,
            "result": "PASS" if passed else "FAIL",
            "detail": reason
        })

    def save_to_file(self, rid):
        filename = f"api_examples/decision_{rid}.json"
        with open(filename, 'w') as f:
            json.dump(self.full_log[rid], f, indent=4)
        print(f"Audit log saved to {filename}")