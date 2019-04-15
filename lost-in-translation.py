from __future__ import print_function
from os.path import join, dirname
from ibm_watson import TextToSpeechV1
from ibm_watson import SpeechToTextV1
from ibm_watson import LanguageTranslatorV3
from playsound import playsound

t2s = TextToSpeechV1(
    url='https://stream-fra.watsonplatform.net/text-to-speech/api',
    iam_apikey='Ia5Hm2hmHyofPhZw0iY6ZIehbE7miqUm1abf6SlTJ-7N')
s2t = SpeechToTextV1(
    url='https://stream-fra.watsonplatform.net/speech-to-text/api',
    iam_apikey='KChSwZGxpjGPTQr2uXOPjEEj2G0IbaOK2FZe78eAuaG5')
translator = LanguageTranslatorV3(
    version='2018-05-01',
    url='https://gateway-fra.watsonplatform.net/language-translator/api',
    iam_apikey='XWy87z-yWfCgk1fqRtpnntitN4N016pP0hox2g1BerCL')


def loose_in_translation(text, voice):
    print('text to speech')
    with open(join(dirname(__file__), './resources/' + voice + '.wav'),
              'wb') as audio_file:
        response = t2s.synthesize(
            text, accept='audio/wav',
            voice=voice).get_result()
        audio_file.write(response.content)

    print('playing result...')
    playsound('./resources/' + voice + '.wav')

    print('speech to text')
    print('possible transcripts:')
    transcript = None
    with open(join(dirname(__file__), './resources/' + voice + '.wav'),
              'rb') as audio_file:
        for r in s2t.recognize(
                audio=audio_file,
                content_type='audio/wav').get_result()["results"]:
            for i in r['alternatives']:
                if transcript is None:
                    transcript = i['transcript']
                print(i['transcript'])

    print('translating')
    print('possible translations:')
    translation = None
    for t in translator.translate(text=transcript, model_id='en-de').get_result()['translations']:
        if translation is None:
            translation = t['translation']
        print(t['translation'])


defaultText = 'Try to think logically!'
print('input text to be translated [default: "' + defaultText + '"]:')
text = input()
if len(text) == 0:
    text = defaultText
print()

print('performing "Englisch als Arbeitssprache" variant')
loose_in_translation(text, 'de-DE_BirgitVoice')
print()

print('performing proper variant')
loose_in_translation(text, 'en-US_MichaelVoice')

