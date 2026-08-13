import yagmail
import os
import sys
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

# -----------------------------
# Email Configuration (from environment variables)
# -----------------------------
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")


def _require_env():
    missing = []
    if not SENDER_EMAIL:
        missing.append("SENDER_EMAIL")
    if not APP_PASSWORD:
        missing.append("APP_PASSWORD")
    if not RECEIVER_EMAIL:
        missing.append("RECEIVER_EMAIL")
    if missing:
        logging.error("Missing environment variables: %s", ", ".join(missing))
        logging.info("Example (macOS/Linux): export SENDER_EMAIL=you@example.com")
        logging.info("export APP_PASSWORD=app-password")
        logging.info("export RECEIVER_EMAIL=dest@example.com")
        sys.exit(1)


# -----------------------------
# Send Alert
# -----------------------------
def send_alert(image_path):
    _require_env()

    try:
        yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)
    except Exception as e:
        logging.error("Failed to initialize SMTP client: %s", e)
        return False

    subject = "🚨 VisionEdge Security Alert"

    body = f"""Unknown person detected.

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Please check the attached image.
"""

    attachments = None
    if image_path:
        if os.path.exists(image_path):
            attachments = [image_path]
        else:
            logging.warning("Attachment not found: %s", image_path)

    try:
        yag.send(to=RECEIVER_EMAIL, subject=subject, contents=body, attachments=attachments)
        logging.info("✅ Alert email sent to %s", RECEIVER_EMAIL)
        return True
    except Exception as e:
        logging.error("Failed to send alert email: %s", e)
        return False


def get_latest_image(folder):
    if not os.path.exists(folder):
        logging.error("Folder not found: %s", folder)
        return None
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if not files:
        logging.info("No files found in %s", folder)
        return None
    files = sorted(files)
    return os.path.join(folder, files[-1])


# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    folder = "motion_images"

    latest_image = get_latest_image(folder)

    if not latest_image:
        logging.info("No motion images found. Exiting.")
        sys.exit(0)

    logging.info("Sending alert for %s", latest_image)
    send_alert(latest_image)