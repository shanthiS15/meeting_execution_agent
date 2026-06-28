from email_reply_agent import get_latest_replies

replies = get_latest_replies()

print("\nReplies Found")
print("=" * 50)

for reply in replies:

    print(reply)