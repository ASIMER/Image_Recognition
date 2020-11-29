import os
import io
from google.cloud import vision, translate_v2

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"ServiceAccountToken.json"
image_folder = 'Images/part 1/'


def translate(text: str,
              target_lang:str = 'ru'):
    client_translate = translate_v2.Client()
    text_info = client_translate.translate(text,
                                           target_language=target_lang)
    translated_text = text_info["translatedText"]
    return translated_text


def recognize(image_name: str,
              translate_to_lang:str = False):
    image_path = image_folder+image_name
    client = vision.ImageAnnotatorClient()

    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.label_detection(image=image)
    labels = response.label_annotations

    desc = []
    for label in labels:

        desc.append([translate(label.description) if translate_to_lang
                     else label.description,
                     label.score
                     ])

    return desc

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    rec_info = recognize('photo_2020-11-30_00-48-50.jpg')
    for label in rec_info:
        print(label)
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
