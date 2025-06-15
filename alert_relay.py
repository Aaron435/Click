from flask import Flask, request
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = 'https://discord.com/api/webhooks/1377848859362984107/kd1cHUgARJlA76r_khFVCeZQTGOIoye2H5YGvdOJP2j2Y-_sCicGW8Ys3Ek-KFuzhbJk'

@app.route('/alert', methods=['POST'])
def alert():
    data = request.json

    alerts = data.get("alerts", [])
    messages = []

    for alert in alerts:
        status = alert.get("status")
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})
        instance = labels.get("instance", "unknown")
        summary = annotations.get("summary", "Sin resumen")
        description = annotations.get("description", "")

        msg = f"[{status.upper()}] {summary} - {description} (instancia: {instance})"
        messages.append(msg)

    if messages:
        content = "\n".join(messages)
        payload = { "content": content }

        resp = requests.post(DISCORD_WEBHOOK_URL, json=payload)

        if resp.status_code != 204:
            return f"Error al enviar a Discord: {resp.status_code} {resp.text}", 500

    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
