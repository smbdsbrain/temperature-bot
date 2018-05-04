import asyncio
import json
import logging

from aiotg import Bot, Chat

from bot.web_worker import get_office_state


def run(config):

    logging.info('Start bot...')
    bot = Bot(api_token=config.token, proxy=config.proxy['proxy_url'])

    sensor_host = config.sensor_address.host
    sensor_port = config.sensor_address.port

    @bot.command(r"/start")
    def start(chat: Chat, match):
        keyboard = {
            "keyboard": [['Get air temperature in office.']],
            "resize_keyboard": True
        }
        return chat.send_text("My only task is to tell you air temperature in NapoleonIT office.",
                              reply_markup=json.dumps(keyboard))

    @bot.default
    def answerer(chat, message):
        logging.info(f"{chat}: {message}")
        return chat.reply(get_office_state(sensor_host, sensor_port))

    channel = bot.channel(config.chanel)

    async def chanel_posting():
        while True:
            await channel.send_text(get_office_state(sensor_host, sensor_port))
            await asyncio.sleep(60 * config.interval)

    loop = asyncio.get_event_loop()

    bot_loop = loop.create_task(bot.loop())
    chanel_loop = loop.create_task(chanel_posting())
    loop.run_until_complete(asyncio.gather(bot_loop, chanel_loop))
    loop.close()
