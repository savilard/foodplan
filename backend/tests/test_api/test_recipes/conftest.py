import base64

from PIL import Image
import pytest


@pytest.fixture
def image_file(tmp_path_factory):
    img_path = tmp_path_factory.mktemp('data') / 'pil_red.png'
    img = Image.new('RGB', (60, 30), color='red')
    img.save(img_path)
    return img_path


@pytest.fixture
def base64_string_image(image_file):
    with open(image_file, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')
