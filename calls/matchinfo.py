import json
import requests

out_list = []
output = ''

heroes = json.load(open('data/heroes.json'))

def matchinfo(match_id):
    global output
    api_call = 'https://api.opendota.com/api/matches/' + str(match_id)
    response = requests.get(api_call)
    print(response.status_code)
    data = response.json()

    # Match duration
    r_score = data['radiant_score']
    d_score = data['dire_score']
    g_length = data['duration']
    g_sec = g_length%60
    if g_sec < 10:
        g_sec = f'0{g_sec}'
    if g_sec == 0:
        g_sec = '00'
    g_min = int((g_length - g_length%60)/60)

    if data['radiant_win']:
        output += 'Radiant Victory!\n'
    else:
        output += 'Dire Victory!\n'

    out_list.append(output)
    output = ''

    # score and time
    output += f'{r_score} - {d_score}, {g_min}:{g_sec}\n'
    out_list.append(output)
    output = ''

    # Match ID
    output += f'{data["match_id"]}\n'
    out_list.append(output)
    output = ''

    # TODO
    # match type parse
    #match_type = ''

    players = data['players']

    # Radiant
    output += 'Radiant' + '\n'
    out_list.append(output)
    output = ''

    output += f'`L. {addspace("Hero",20)}{addspace("K/D/A",9)}{addspace("LH/D",7)}{addspace("HD",7)}{addspace("TD",7)}{addspace("GPM",4)}{addspace("XPM`",4)}\n'
    for p in players:
        if p['isRadiant']:
            playerinfo(p)
    out_list.append(output)
    output = ''

    # Dire
    output += 'Dire' + '\n'
    out_list.append(output)
    output = ''

    output += f'`L. {addspace("Hero",20)}{addspace("K/D/A",9)}{addspace("LH/D",7)}{addspace("HD",7)}{addspace("TD",7)}{addspace("GPM",4)}{addspace("XPM`",4)}\n'
    for p in players:
        if not p['isRadiant']:
            playerinfo(p)
    out_list.append(output)
    output = ''

    # return msg
    return out_list

# adds a specific number of spaces to the end of the word based on desired length (d_len) and the word length
def addspace(word: str, d_len: int):
    spaces = (d_len - len(word)) * ' \u200b'
    return word + spaces

def rround(val: int):
    if val >= 1000:
        num = f'{round(val/1000, 1)}k'
    else:
        num = val
    return num

def playerinfo(p):
    global output

    # Level and Hero
    output += '`'
    output += addspace(str(p['level']), 3)
    output += addspace(heroes[str(p['hero_id'])]['localized_name'], 20)
    # KDA
    output += addspace(f'{p["kills"]}/{p["deaths"]}/{p["assists"]}', 9)
    # LH/D
    output += addspace(f'{p["last_hits"]}/{p["denies"]}', 7)
    # HD
    output += addspace(f'{rround(p["hero_damage"])}', 7)
    # TD
    output += addspace(f'{rround(p["tower_damage"])}', 7)
    # GPM
    output += addspace(f'{p["gold_per_min"]}', 4)
    # XPM
    output += addspace(f'{p["xp_per_min"]}', 5)

    # Account ID
    if p['account_id'] == None:
        output += 'Unknown`\n'
    else:
        if 'personaname' in p:
            output += f'{p["personaname"][:7]}`\n'


def lastmatch(pid):
    api_call = 'https://api.opendota.com/api/players/' + str(pid) +'/recentMatches'
    response = requests.get(api_call)
    print(response.status_code)
    data = response.json()

    match_id = data[0]['match_id']
    return matchinfo(match_id)


for x in matchinfo(4795869142):
    print(x, end='')

#lastmatch(108552597)
