from scraper import scrape

import config

import botogram
import json

bot = botogram.create(config.BOT_TOKEN)


def _dar(a, b):
    # Divide and round
    return f"({round((a / b) * 100, 1)}%)"


def diff(a, b):
    d = a - b
    if d > 0:
        sign = '+'
    elif d < 0:
        sign = '-'
    else:
        sign = '±'
    return f"[{sign}{abs(d)}]"


ls = json.load(open('last_scrape.json', 'r'))

stats = scrape()
tc = stats['total_cases']
active_cases = stats['mild_condition'] + stats['critical_condition']
closed_cases = stats['recovered'] + stats['deaths']
msg = bot.chat(config.CHANNEL_ID).send(
    "📊 <b>COVID-19 STATS</b>"
    f"\n🤒 <b>Total cases</b>: {tc} {diff(tc, ls['total_cases'])}"
    f"\n\n➤ <b><i>ACTIVE CASES</i></b>: {active_cases} {_dar(active_cases, tc)} {diff(active_cases, ls['mild_condition'] + ls['critical_condition'])}"
    f"\n😷 <b>Mild condition</b>: {stats['mild_condition']} {_dar(stats['mild_condition'], active_cases)} {diff(stats['mild_condition'], ls['mild_condition'])}"
    f"\n🥵 <b>Critical condition</b>: {stats['critical_condition']} {_dar(stats['critical_condition'], active_cases)} {diff(stats['critical_condition'], ls['critical_condition'])}"
    f"\n\n➤ <b><i>CLOSED CASES</i></b>: {closed_cases} {_dar(closed_cases, tc)} {diff(closed_cases, ls['recovered'] + ls['deaths'])}"
    f"\n😀 <b>Recovered</b>: {stats['recovered']} {_dar(stats['recovered'], closed_cases)} {diff(stats['recovered'], ls['recovered'])}"
    f"\n☠️ <b>Deaths</b>: {stats['deaths']} {_dar(stats['deaths'], closed_cases)} {diff(stats['deaths'], ls['deaths'])}"
    f"\n\n🔗 By @CoronaVirusOfficialNews"
)
bot.chat(config.CHANNEL_ID).pin_message(msg, notify=False)

json.dump(stats, open('last_scrape.json', 'w'))
