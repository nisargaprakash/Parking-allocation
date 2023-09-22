from twilio.rest import Client

# Your Twilio Account SID and Auth Token
account_sid = "AC80a97d702cdc852a178bc584f8607434"
auth_token = "cb4292ee3ff39bb6d46c63146662a91e"

# Create a Twilio client
client = Client(account_sid, auth_token)

# Send a message
def send_message(to_number, message):
    client.messages.create(to=to_number, from_="+17402003096", body=message)

# Example usage:

booking_details = """Hi  Aryan your
Slot booking details:
  Slot number: 12
  Parking lot address: #828 , 62nd cross , paris
"""

entry_time = "2023-09-21 10:00 AM"
exit_time = "2023-09-21 12:00 PM"

# Send a message to the user with their slot booking details
send_message("+91 97092 98279", f"Slot booking details:\n{booking_details}\nEntry time: {entry_time}\nExit time: {exit_time}")