import json
import os
from automation_engine import process_login_events

def load_simulated_data():
    base_path = os.path.dirname(os.path.dirname(__file__))
    file_path = os.path.join(base_path, "data", "simulated_login_events.json")
    with open(file_path, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    print("=== Incident Automation PoC Execution ===")
    login_events = load_simulated_data()
    process_login_events(login_events)
    print("=== Execution Completed ===")