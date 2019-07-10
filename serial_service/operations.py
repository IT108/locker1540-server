import requests
from pydub import AudioSegment
from pydub.playback import play
import constants as constants
import json


def run_operation(op_id, data):
    if op_id == 'check_card':
        return check_card(data['card'])
    elif op_id == 'play_greet':
        return get_greet(data['card'])
    elif op_id == 'status':
        return send_status(data)


def check_card(card):
    res = requests.post('http://176.99.11.114/card', {'card': card})
    print(res.text)
    if res.text == 'False':
        return 'N'
    res = res.text.split(';')
    constants.sounds.extend(res[1:-1])
    return 'Y'


def send_status(data):
    res = json.dumps(data)
    address = constants.api_address + constants.STATUS_PAGE
    resp = requests.post(address, {'status': res})
    return ''


def get_greet(card):
    res = requests.post('http://176.99.11.114/greet', {'card': card})
    res = res.text.split(';')
    constants.sounds_queue.append(res)
    constants.sounds.extend(res[1:-1])
    return ''


def process_sounds(sounds):
    if len(sounds) > 0:
        append_sounds(sounds)


def append_sounds(s):
    tmp = []
    for a in s:
        if a == '-1':
            pass
        while len(a) < 4:
            a = '0' + a
        a = "mp3/" + a + '.mp3'
        a = AudioSegment.from_mp3(a)
        tmp.append(a)
    res = tmp[0]
    tmp = tmp[1:]
    for p in tmp:
        res = res + p
    constants.sounds_queue.append(res)
    print(constants.sounds_queue)


def play_queue():
    if len(constants.sounds_queue) > 0:
        play_sound(constants.sounds_queue)
    constants.sounds_queue.clear()


def play_sound(sounds):
    for sound in sounds:
        play(sound)
