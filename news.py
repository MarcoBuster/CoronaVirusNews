from scraper import scrape
import json

import config

import botogram

import jellyfish

bot = botogram.create(config.BOT_TOKEN)

ls = json.load(open('last_scrape.json', 'r'))
stats = scrape()

for news in stats['news']:
    abort = False
    if news not in ls['news']:
        for n in ls['news']:
            if jellyfish.jaro_distance(news, n) > 0.9:
                abort = True
        if abort:
            continue
        bot.chat(config.CHANNEL_ID) \
            .send(f"⚠️ {news.lstrip().rstrip()}\n\n🔗 By @CoronaVirusOfficialNews", syntax='html')

json.dump({**ls, 'news': stats['news']}, open('last_scrape.json', 'w'))
