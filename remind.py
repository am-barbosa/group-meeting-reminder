import os
from datetime import datetime, timedelta

import pandas as pd
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

REMINDER_DAYS = 5
CHANNEL_ID = "C07HA12JP1C"

slack = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

# Load schedule
df = pd.read_csv("schedule.csv")
df["Date"] = pd.to_datetime(df["Date"]).dt.date

today = datetime.utcnow().date()
target_date = today + timedelta(days=REMINDER_DAYS)

upcoming = df[df["Date"] == target_date]

for _, row in upcoming.iterrows():
    message = (
        f"👋 Hej {row['Speaker']}!\n\n"
        f"Just a reminder that you’re up next to present at the group meeting "
        f"on *{row['Date']}*. "
        f"Thanks!"
    )

    try:
        slack.chat_postMessage(
            channel=CHANNEL_ID,
            text=message
        )
        print(f"Sent reminder to {row['Speaker']}")

    except SlackApiError as e:
        print(f"Failed to message {row['Speaker']}: {e.response['error']}")
