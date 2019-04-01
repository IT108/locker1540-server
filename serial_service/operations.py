import requests
from pydub import AudioSegment
from pydub.playback import play


def run_operation(op_id, data):
    if op_id == 'check_card':
        return check_card(data['card'])


def check_card(card):
    res = requests.post('http://176.99.11.114/card', {'card': card})
    res = res.text.split(';')
    return res[0]


def play_sound(sounds):
    for sound in sounds:
        while len(sound) < 4:
            sound = '0' + sound
        sound = sound + '.mp3'
        sound = AudioSegment.from_mp3("mp3/" + sound)
        play(sound)


play_sound('1')
