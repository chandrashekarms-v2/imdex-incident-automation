import json
from automation_engine import process_login_events

def load_simulated_data():
    with open("data/simulated_logins.json", "r") as f:
        return json.load(f)

if __name__ == "__main__":
    print("=== Incident Automation PoC Execution ===")
    login_events = load_simulated_data()
    process_login_events(login_events)
    print("=== Execution Completed ===")