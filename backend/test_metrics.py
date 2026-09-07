from backend.metrics import send_metric

status = send_metric(
    "filmops_schedule_delay_minutes",
    45
)

print(status)