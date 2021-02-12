import typing
import re
from pathlib import Path
import PyPDF2
from PyPDF2.utils import PdfReadError
from PIL import Image
import pytesseract

IMAGES_PATH = Path(__file__).parent.joinpath('images')
if not IMAGES_PATH.exists():
    IMAGES_PATH.mkdir()


# TODO: Pdf to Image.
def pdf_image_extract(pdf_path: Path, images_path: Path = IMAGES_PATH) -> typing.List[Path]:
    result = []
    with pdf_path.open('rb') as file:
        try:
            pdf_file = PyPDF2.PdfFileReader(file)
        except PdfReadError as exc:
            # TODO: Записать информацию о ошибке чтения PDF в бд
            return result
        for idx, page in enumerate(pdf_file.pages):
            img_name = f'{pdf_path.name}.{idx}'
            img_data = page['/Resources']['/XObject']['/Im0']._data
            img_path = images_path.joinpath(img_name)
            img_path.write_bytes(img_data)
            result.append(img_path)
    return result


# TODO: Image to seril_number list.
def get_seril_numbers(img_path: Path) -> typing.List[str]:
    numbers = []
    pattern = re.compile(r'(заводской.*номер)')
    image = Image.open(img_path)
    text_rus = pytesseract.image_to_string(image, 'rus')
    matches_count = len(re.findall(pattern, text_rus))
    if matches_count:
        text_eng = pytesseract.image_to_string(image, 'eng').split("\n")
        for idx, line in enumerate(text_rus.split("\n")):
            if re.match(pattern, line):
                numbers.append(text_eng[idx].split()[-1])
            if len(numbers) == matches_count:
                break
    return numbers

if __name__ == '__main__':
    pdf_temp = Path(__file__).parent.joinpath('8416_4.pdf')
    images = pdf_image_extract(pdf_temp)
    numbers = list(map(get_seril_numbers, images))
    print(1)
