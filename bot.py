import logging
from telethon import TelegramClient, functions, types, events
from settings import settings
import time
from typing import Optional

logging.basicConfig(level=logging.INFO)


# Replace these with your values
api_id = settings.APP_API_ID
api_hash = settings.APP_API_HASH
bot_token = settings.BOT_TOKEN

# Create the bot client(should be interactive)

client = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)



async def kick_all_members(chat_id,dry_run:Optional[bool]=False):
    # Counter to track how many members have been banned
    ban_count = 0

    # Define the delay duration in seconds
    delay_duration = 10  # Pause for 10 seconds after every 20 members banned

    async for member in client.iter_participants(chat_id):
        logging.info(f'Would ban and kick user: {member.id}')
        if dry_run:
            continue
        elif member.id == (await client.get_me()).id:
            print('Skipping myself')
            continue
        try:
            await client(functions.channels.EditBannedRequest(
                channel=chat_id,
                participant=member.id,
                banned_rights=types.ChatBannedRights(until_date=None, view_messages=False)
            ))
            print(f'Banned and kicked user: {member.id}')
            # Increment the counter
            ban_count += 1

            # Check if the counter has reached 20 (or another threshold)
            if ban_count % 20 == 0:
                # Pause for the specified duration to avoid rate limits
                logging.info(f'Pausing for {delay_duration} seconds to avoid rate limits...')
                time.sleep(delay_duration)
            if ban_count >= 1000:
                break
        except Exception as e:
            print(f'Error while banning user {member.id}: {e}')


@client.on(events.NewMessage(pattern='/kick_all'))
async def handle_kick_all(event):
    print('Received command to kick all members from the group')
    if event.is_private:
        print('Command received in a private chat')
        return

    chat = event.chat_id
    # Kick all members from the group
    await kick_all_members(chat,False)
    await event.reply(f'All members(or max of 1000 per one run) have been kicked from the group: {chat}.\n'
                      f'Run the command /kick_all again to kick more members. \n'
                      f'Bot has been developed by https://hrekov.com \n'
                      f'and is open source: https://github.com/webprice/kick_and_ban_all_members_bot')




# The main block of code that runs the bot
if __name__ == '__main__':
    logging.info('Bot started and running...')
    client.run_until_disconnected()
    logging.info('Bot has been disconnected and stopped running.')
