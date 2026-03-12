# Resilient Decision Engine
A configuration-driven workflow engine designed for high reliability, fault tolerance, and decision transparency. This system handles complex business logic while remaining resilient to external dependency failures.
- **Engineering Robustness**: Implemented **Exponential Backoff and Retry Logic** to handle flaky external API dependencies (simulated in mocks).
- **Idempotency**: Integrated a request-validation layer to ensure that duplicate requests with the same ID do not result in redundant processing.
- **Explainability**: Automatically generates structured **Audit Logs** (JSON) in the `api_examples/` folder, explaining exactly why a request was approved or rejected.
- **Zero-Code Configurability**: Business rules are externalized in `config/loan_workflow.json`. New rules or thresholds can be added without modifying the core Python engine.

## 🏗 Project Structure
- `config/`: JSON models for business workflows (e.g., Loan Approval).
- `src/engine/`: The orchestrator handling workflow state and idempotency.
- `src/rules/`: Evaluation logic for threshold and mandatory checks.
- `src/mocks/`: Simulated external dependencies with failure scenarios.
- `src/utils/`: Audit logging and helper utilities.
- `tests/`: Automated test suite for happy paths and resilience.
## Setup and Execution

### 1. Install Dependencies
Ensure you have Python installed, then run:
```powershell
python -m pip install pytest
