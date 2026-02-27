.PHONY: run query ui clean help

PYTHON := python

help:
	@echo "Available commands:"
	@echo "  make run         - Start all agents (Coordinator + Sub-agents)"
	@echo "  make query q=... - Send a query to the coordinator (e.g., make query q='Hello')"
	@echo "  make ui          - Start the Web GUI (http://localhost:8888)"
	@echo "  make clean       - Kill all Python processes related to this project (zombie cleanup)"

run:
	$(PYTHON) -m a4a_lab.run_all

ui:
	$(PYTHON) -m a4a_lab.web

query:
	@if [ -z "$(q)" ]; then \
		echo "Error: Please specify a query using q='Your query here'"; \
		exit 1; \
	fi
	$(PYTHON) -m a4a_lab.a2a_query "$(q)" --port 8000

# Careful with this! It might kill other python processes if not specific enough.
# Here we just suggest the user to use pkill or manual kill if run_all fails to cleanup.
clean:
	@echo "Killing Python processes related to a2a_agent..."
	-pkill -f "a2a_agent"
	@echo "Killing Python processes related to a4a_lab.agent..."
	-pkill -f "a4a_lab.agent"
	@echo "Done."
