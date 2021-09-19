from services.images import ImagesService
from utils import get_hash, get_path
from services.metadata import Metadata
from models import Single, SINGLE_NULL
from dynaconf import Dynaconf
from typing import Any, List, Dict, Set
from os.path import join
from pprint import pprint
from PIL import Image
import random
settings = Dynaconf(settings_files=["nft.config.json"])


def run(config_file: str):
    stackable_characteristics = settings.stackable_characteristics
    input_folder = settings.input_folder
    metadata = Metadata(input_folder=input_folder,
                        input_data=stackable_characteristics)
    image_service = ImagesService(metadata)
    output_folder = get_path(settings.output_folder)
    tokens = settings.tokens
    for i in range(tokens):
        random_pic, id_image = image_service.new_nft()
        generate_image(input_singles=random_pic,
                       output_folder=output_folder, filename=f"{i:03d}")


def generate_image(input_singles: List[Single], output_folder: str, filename: str):
    image = Image.open(input_singles[0].file_uri).convert("RGBA")
    for single in input_singles[1:]:
        if single != SINGLE_NULL:
            tmp_image = Image.open(single.file_uri).convert("RGBA")
            image = Image.alpha_composite(image, tmp_image)

    image.save(join(output_folder, f"{filename}.png"))


if __name__ == "__main__":
    run("nft.config.json")
