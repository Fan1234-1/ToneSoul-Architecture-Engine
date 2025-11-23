.PHONY: test verify clean

PYTHON = python
TEST_DIR = body

test:
	@echo "Running Unit Tests..."
	$(PYTHON) $(TEST_DIR)/test_ledger.py
	$(PYTHON) $(TEST_DIR)/test_guardian.py
	$(PYTHON) $(TEST_DIR)/test_sensor.py
	$(PYTHON) $(TEST_DIR)/test_constitution.py

verify: test
	@echo "Running Integration Verification..."
	$(PYTHON) $(TEST_DIR)/test_integration.py

clean:
	@echo "Cleaning artifacts..."
	rm -f $(TEST_DIR)/ledger.jsonl
	rm -rf __pycache__

test-ts:
	@echo "Running TypeScript Spine Tests..."
	cd modules/spine-ts && npm install && npm test

test-all: verify test-ts
	@echo "All Systems (Python + TS) Verified."
