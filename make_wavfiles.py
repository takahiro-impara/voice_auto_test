from google.cloud import texttospeech
from variable import VOICE_SET, OPERATION_VERBS
import os

SYNONYM_TEXT = "./synonym.txt"
def list_languages():
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices().voices
    languages = unique_languages_from_voices(voices)

    print(f" Languages: {len(languages)} ".center(60, "-"))
    for i, language in enumerate(sorted(languages)):
        print(f"{language:>10}", end="" if i % 5 < 4 else "\n")

def unique_languages_from_voices(voices):
    language_set = set()
    for voice in voices:
        for language_code in voice.language_codes:
            language_set.add(language_code)
    return language_set

def list_voices(language_code=None):
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f" Voices: {len(voices)} ".center(60, "-"))
    for voice in voices:
        languages = ", ".join(voice.language_codes)
        name = voice.name
        gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name
        rate = voice.natural_sample_rate_hertz
        print(f"{languages:<8} | {name:<24} | {gender:<8} | {rate:,} Hz")

def text_to_wav(voice_name, text, filename):
    language_code = "-".join(voice_name.split("-")[:2])
    text_input = texttospeech.SynthesisInput(text=text)
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16
    )

    client = texttospeech.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    with open(filename, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to "{filename}"')

def get_synonym_from_text(text):
    with open(text) as rfile:
        readlines = [x.strip().split(',') for x in rfile.readlines()]
    return readlines

def make_dir(dir):  
    os.makedirs(dir, exist_ok=True)

def call_google_voice(**kwargs):
    WAKE_WORD = VOICE_SET["WAKE_WORD"]["GOOGLE"]
    device_name = kwargs["device_name"]
    dir_name = "./google/{}".format(device_name)
    file_name = "{dir_name}/{synonym}_{operation_verb}_{voice_set}.wav".format(dir_name=dir_name, synonym=kwargs["synonym"], operation_verb=kwargs["operation_verb"], voice_set=kwargs["voice_set"])
    make_dir(dir_name)

    operation_sentence = "{WAKE_WORD}{synonym}を{operation_verb}。".format(WAKE_WORD=WAKE_WORD, synonym=kwargs["synonym"], operation_verb=kwargs["operation_verb"])
    text_to_wav(kwargs["voice_set"], operation_sentence, file_name)
if __name__ == "__main__":
    #list_languages()
    #list_voices(JAPANESE_LOCALE)
    synonyms_list = get_synonym_from_text(SYNONYM_TEXT)
    for synonym_list in synonyms_list:
        device_name = synonym_list[0]
        for synonym in synonym_list:
            for operation_verb in OPERATION_VERBS:
                call_google_voice(voice_set=VOICE_SET["MALE"], synonym=synonym, operation_verb=operation_verb, device_name=device_name)
    #text_to_wav(VOICE_SET["MALE"], "アレクサ、床ワイパーをオンにして")