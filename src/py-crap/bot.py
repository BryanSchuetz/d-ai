import slack

# O-auth token for slack bot
SLACK_TOKEN="xoxb-2190897728-5030141376935-fFwIcIn08qafOSzrzwHSmyHb"

client = slack.WebClient(token=SLACK_TOKEN)
client.chat_postMessage(channel='#d-ai',text='Hello')