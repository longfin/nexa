# -*- coding: utf-8 -*-
import sys
import os.path

import requests
from wand.image import Image

FILE_HEADER = """{set} Spoiler List
Copyright 2012 CMC.
(Released August 4, 2013)

200 Cards Total


""".replace('\n', '\r\n')
CARD_TEMPLATE = """Card Name:	{code}
Card Set:	{set}
Card Color:	{color}
Type & Class:	{type} - SP/E
Card Text:	{text}
		-----
		
		-----
		{tags}
Rarity:	        {rarity}

                *****


""".replace('\n', '\r\n')


if __name__ == '__main__':
    pack_id = sys.argv[1]
    card_set = sys.argv[2]

    list_url = 'http://www.carddass.com/cdmasters/nexa/cardlist/controller/request.php'
    list_headers = {
        'Pragma': 'no-cachpe',
        'Host': ' www.carddass.com',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Accept': '*/*',
        'Origin': 'http//www.carddass.com',
        'X-Requested-With': 'XMLHttpRequest',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/40.0.2214.111 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': 'http//www.carddass.com/cdmasters/nexa/cardlist/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ko,en-US;q=0.8,en;q=0.6,ja;q=0.4,pt;q=0.2',
        'Cookie': 'NEX-A_COOKIE_CHK=1; PHPSESSID=b3u4f5ise81sou7r5mr0s57bn7; __utma=136845986.1030128933.1424013529.1424150690.1424159019.11; __utmb=136845986.67.10.1424159019; __utmc=136845986; __utmz=136845986.1424099558.4.4.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)',
    }
    list_payload = {
        'cmdno': 1,
        'free': '',
        'character_id': 179,
        'prod': pack_id,
        'info_18': '',
        'info_3': '',
        'info_4': '',
        'info_5': '',
        'info_6': '',
        'cardno': ''
    }
    r = requests.post(list_url, data=list_payload, headers=list_headers)
    cards = r.json()['data']

    if not os.path.isdir(card_set):
        os.mkdir(card_set)
    if not os.path.isdir(os.path.join(card_set, 'LargeJPG')):
        os.mkdir(os.path.join(card_set, 'LargeJPG'))

    with open(os.path.join(card_set, 'list.txt'), 'wb') as f:
        f.write(FILE_HEADER.format(set=card_set).encode('Shift-JIS'))
        for c in cards:
            card_code = c['info_1'].replace('/', '_')
            f.write(CARD_TEMPLATE.format(
                set=card_set,
                code=card_code,
                type=c['info_3'],
                text=c['info_12'].replace('<br />', '\n'),
                tags=c['info_11'],
                rarity=c['info_17'] if c['info_17'] != '-' else 'O',
                color={
                    '青': 'U',
                    '緑': 'G',
                    '黒': 'B',
                    '白': 'W',
                    '赤': 'R',
                    '茶': 'A',
                    '紫': 'L',
                }[c['info_18']],
            ).encode('Shift-JIS', errors='ignore'))

            image_filename = os.path.join(card_set, 'LargeJPG', '{}.jpg'.format(card_code.replace(' ', '_')))
            image_url = 'http://www.carddass.com/cdmasters/nexa/images/cardlist/{}/{}.png'.format(
                pack_id, c['info_25'],
            )
            r = requests.get(image_url)
            with Image(blob=r.content) as img:
                with img.convert('jpg'):
                    img.save(filename=image_filename)
