from utils import get_hash, get_path
from services.metadata import Metadata
from models.stats import SingleStat
from schemas import BodyPartSchema, SingleSchema

from models import BodyPart, Single, SINGLE_NULL
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
    output_folder = get_path(settings.output_folder)
    tokens = settings.tokens
    univoques = set()
    for i in range(tokens):
        random_pic, id_image = random_metadata(input_singles=metadata.indexed, univoques=univoques)
        univoques.add(id_image)
        generate_image(input_singles=random_pic, output_folder=output_folder, filename=f"{i:03d}")


def random_metadata(input_singles: Dict[int, Dict[str, List[Single]]], univoques: Set) -> List[Single]:
    g_image = []
    for _, list_body_part in input_singles.items():
        for _, possibles in list_body_part.items():
            random_choice = random.choice(possibles)
            g_image.append(random_choice)
    id_image = get_hash(g_image)
    if id_image in univoques:
        return random_metadata(input_singles=input_singles, univoques=univoques)
    else:
        return (g_image, id_image)


def generate_image(input_singles: List[Single], output_folder: str, filename: str):
    image = Image.open(input_singles[0].file_uri).convert("RGBA")
    for single in input_singles[1:]:
        if single != SINGLE_NULL:
            tmp_image = Image.open(single.file_uri).convert("RGBA")
            image = Image.alpha_composite(image, tmp_image)

    image.save(join(output_folder,f"{filename}.png"))


if __name__ == "__main__":
    run("nft.config.json")
