import requests
from pydub import AudioSegment
from pydub.playback import play
import serial_service.constants as constants


def run_operation(op_id, data):
    if op_id == 'check_card':
        return check_card(data['card'])
    elif op_id == 'play_greet':
        return get_greet(data['card'])


def check_card(card):
    res = requests.post('http://176.99.11.114/card', {'card': card})
    res = res.text.split(';')
    append_sounds(res[1:])
    return res[0]


def get_greet(card):
    res = requests.post('http://176.99.11.114/greet', {'card': card})
    res = res.text.split(';')
    constants.sounds_queue.append(res)
    append_sounds(res)
    return res


def append_sounds(s):
    for a in s:
        constants.sounds_queue.append(a)


def play_queue():
    if len(constants.sounds_queue) > 0:
        play_sound(constants.sounds_queue)


def play_sound(sounds):
    for sound in sounds:
        while len(sound) < 4:
            sound = '0' + sound
        sound = sound + '.mp3'
        sound = AudioSegment.from_mp3("mp3/" + sound)
        play(sound)


