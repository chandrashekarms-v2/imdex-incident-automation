from collections import defaultdict
from password_service import reset_password
from email_service import send_email
import json
import os

FAILED_LOGIN_THRESHOLD = 3

def process_login_events(events):
    failure_tracker = defaultdict(int)
    user_roles = {}
    escalations = []
    password_resets = 0

    for event in events:
        event_type = event.get("event_type")
        user = event.get("user_id")
        role = event.get("role", "employee")

        user_roles[user] = role

        # Track failed login attempts
        if event_type == "login_attempt" and not event.get("success", True):
            failure_tracker[user] += 1

        # Geo anomaly detection
        if event.get("failure_reason") == "Geo-location anomaly":
            escalations.append(f"Geo anomaly detected for {user}")

    # Apply automation rules
    for user, fail_count in failure_tracker.items():
        role = user_roles.get(user)

        if fail_count >= FAILED_LOGIN_THRESHOLD:
            print(f"[RULE MATCH] {user} exceeded failed login threshold")

            if role in ["admin", "service"]:
                print(f"[ESCALATION] {user} is {role} — no auto reset")
                escalations.append(f"High-privilege account failed logins: {user}")
            else:
                reset_password(user)
                send_email(user, "Your password has been reset due to multiple failed login attempts.")
                password_resets += 1

    # Print summary metrics
    print("\n=== AUTOMATION SUMMARY ===")
    print(f"Total unique users evaluated: {len(user_roles)}")
    print(f"Users exceeding failure threshold: {len(failure_tracker)}")
    print(f"Password resets triggered: {password_resets}")
    print(f"Escalations triggered: {len(escalations)}")

    # Save audit log
    save_audit_log(password_resets, escalations)


def save_audit_log(password_resets, escalations):
    log_data = {
        "password_resets": password_resets,
        "escalations": escalations
    }

    os.makedirs("logs", exist_ok=True)

    with open("logs/automation_audit.json", "w") as f:
        json.dump(log_data, f, indent=4)

    print("Audit log saved to logs/automation_audit.json")