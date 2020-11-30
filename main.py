import os
import io
from google.cloud import vision, translate_v2
import xlrd, xlwt

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"ServiceAccountToken.json"
image_folder = 'Images/333/'


def translate(text: str,
              client_translate = False,
              target_lang:str = 'ru'):
    if not client_translate:
        # create client if not created
        client_translate = translate_v2.Client()

    text_info = client_translate.translate(text,
                                           target_language=target_lang)
    translated_text = text_info["translatedText"]
    return translated_text


def recognize(image_name: str,
              img_rec_client = False,
              translate_client = False,
              translate_to_lang:str = False,
              min_confidence: float = 0.65):
    image_path = image_folder+image_name
    if not img_rec_client:
        # create client if not created
        img_rec_client = vision.ImageAnnotatorClient()
    with io.open(image_path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = img_rec_client.label_detection(image=image)
    labels = response.label_annotations

    desc = []
    for label in labels:
        if label.score <= min_confidence:
            break
        desc.append([translate(text=label.description,
                               client_translate=translate_client)
                        if translate_to_lang
                        else label.description,
                     label.score
                     ])

    return desc

if __name__ == '__main__':
    img_rec_client = vision.ImageAnnotatorClient()
    client_translate = translate_v2.Client()
    report_filename = 'report.txt'
    files = os.listdir(image_folder)
    #print(files)
    wb = xlwt.Workbook()
    ws = wb.add_sheet('Test')
    i = 0
    for img_name in files:
        rec_info = recognize(image_name=img_name,
                             img_rec_client=img_rec_client,
                             translate_client=client_translate,
                             translate_to_lang='ru',
                             min_confidence=0)
        #print(f'{img_name} : ', end='')
        #print(*[label[0] for label in rec_info], sep='; ')

        ws.write(i, 0, img_name)
        for col in range(len(rec_info)):
            ws.write(i, col+1, rec_info[col][0])
        i+= 1
    wb.save('xl_rec 2.xls')
