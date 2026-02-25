from collections import defaultdict
from password_service import reset_password
from email_service import send_email

FAILED_LOGIN_THRESHOLD = 3

def process_login_events(login_events):
    failure_tracker = defaultdict(int)

    for event in login_events:
        if not event["success"]:
            failure_tracker[event["user_id"]] += 1

    for user, fail_count in failure_tracker.items():
        if fail_count >= FAILED_LOGIN_THRESHOLD:
            print(f"[RULE MATCH] {user} exceeded failed login threshold")
            reset_password(user)
            send_email(user, "Your password has been reset due to multiple failed login attempts.")