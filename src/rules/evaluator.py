class RuleEvaluator:
    def evaluate(self, rule, data):
        field = rule.get('field')
        actual_value = data.get(field)
        operator = rule.get('operator')
        threshold = rule.get('value')

        if actual_value is None:
            return False, "Missing Data"

        if operator == ">=":
            passed = actual_value >= threshold
        elif operator == "<":
            passed = actual_value < threshold
        elif operator == "==":
            passed = actual_value == threshold
        else:
            passed = False

        msg = "Passed" if passed else f"Value {actual_value} failed {operator} {threshold}"
        return passed, msg