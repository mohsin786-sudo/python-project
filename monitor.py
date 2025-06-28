import psutil
import json
import smtplib
import requests

with open('config.json') as f:
    config = json.load(f)

def send_email(subject, message):
    if not config["email"]["send_alerts"]:
        return
    server = smtplib.SMTP(config["email"]["smtp_server"], config["email"]["port"])
    server.starttls()
    server.login(config["email"]["sender"], config["email"]["password"])
    msg = f"Subject: {subject}\n\n{message}"
    server.sendmail(config["email"]["sender"], config["email"]["receiver"], msg)
    server.quit()

def send_slack(message):
    if not config["slack"]["send_alerts"]:
        return
    requests.post(config["slack"]["webhook_url"], json={"text": message})

def check_metrics():
    alerts = []
import psutil
import json
import smtplib
import requests

with open('config.json') as f:
    config = json.load(f)

def send_email(subject, message):
    if not config["email"]["send_alerts"]:
        return
    server = smtplib.SMTP(config["email"]["smtp_server"], config["email"]["port"])
    server.starttls()
    server.login(config["email"]["sender"], config["email"]["password"])
    msg = f"Subject: {subject}\n\n{message}"
    server.sendmail(config["email"]["sender"], config["email"]["receiver"], msg)
    server.quit()

def send_slack(message):
    if not config["slack"]["send_alerts"]:
        return
    requests.post(config["slack"]["webhook_url"], json={"text": message})

def check_metrics():
    alerts = []
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent

    if cpu > config["cpu_threshold"]:
        alerts.append(f"High CPU Usage: {cpu}%")
    if mem > config["memory_threshold"]:
        alerts.append(f"High Memory Usage: {mem}%")
    if disk > config["disk_threshold"]:
        alerts.append(f"High Disk Usage: {disk}%")

    if alerts:
        alert_message = "\n".join(alerts)
        send_email("🚨 Server Health Alert", alert_message)
        send_slack(alert_message)

if __name__ == "__main__":
    check_metrics()
