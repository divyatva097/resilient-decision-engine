import uuid
import datetime
from src.rules.evaluator import RuleEvaluator

class DecisionEngine:
    def __init__(self, config, storage, external_api, logger):
        self.config = config
        self.storage = storage # Mock DB
        self.api = external_api
        self.logger = logger
        self.evaluator = RuleEvaluator()

    def process(self, request_id, input_data):
        # 1. IDEMPOTENCY CHECK (Engineering Robustness)
        existing = self.storage.get(request_id)
        if existing:
            return existing, "IDEMPOTENT_RETRIEVAL"

        self.logger.log(request_id, f"Starting Workflow: {self.config['workflow_name']}")
        current_data = input_data.copy()
        
        for stage in self.config['stages']:
            self.logger.log(request_id, f"Entering Stage: {stage['name']}")

            # 2. EXTERNAL DEPENDENCY & RETRY FLOW
            if stage.get('type') == "EXTERNAL_API":
                try:
                    ext_result = self.api.call_with_retry(request_id)
                    current_data.update(ext_result)
                except Exception as e:
                    return self.finalize(request_id, "FAILED", f"System Error: {str(e)}")

            # 3. RULE EVALUATION (Explainability)
            for rule in stage['rules']:
                passed, reason = self.evaluator.evaluate(rule, current_data)
                self.logger.record_decision(request_id, stage['name'], rule['id'], passed, reason)

                if not passed:
                    return self.finalize(request_id, rule['on_fail'], f"Rule {rule['id']} failed")

        return self.finalize(request_id, "APPROVED", "All stages passed")

    def finalize(self, request_id, status, reason):
        result = {
            "request_id": request_id,
            "final_status": status,
            "reason": reason,
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.storage.save(request_id, result)
        return result, "NEW_DECISION"