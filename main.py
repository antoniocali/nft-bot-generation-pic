from schemas import BodyPartSchema, SingleSchema
from utils import get_files, get_path, get_rarity, remove_ext
from models import BodyPart, Single, SINGLE_NULL
from dynaconf import Dynaconf
from typing import Any, List, Dict
from os.path import join
from pprint import pprint
from PIL import Image
import random
settings = Dynaconf(settings_files=["nft.config.json"])


def run(config_file: str):
    input_folder = settings.input_folder
    output_folder = settings.output_folder
    stackable_characteristics = settings.stackable_characteristics
    body_parts = get_body_parts(stackable_characteristics)
    possible_choices = generate_dictionary(body_parts)
    random_pic = random_metadata(possible_choices)
    generate_image(random_pic)


def get_body_parts(_json: List[Dict[str, Any]]) -> List[BodyPart]:
    schema = BodyPartSchema()
    return [schema.load(item) for item in _json]


def generate_dictionary(stacks: List[BodyPart]) -> Dict[int, Dict[str, List[Single]]]:
    generated_dict = {}
    schema = SingleSchema()
    input_folder_name = get_path(settings.input_folder)
    for elem in stacks:
        _cur_z_index = generated_dict.get(elem.z_index, {})
        folder_name = join(input_folder_name, elem.folder_name)
        all_files = get_files(folder_name)
        enhanced_files = [{"body_name": elem.body_name, "file_name": f,
                           "folder_name": folder_name} for f in all_files]
        singles_list = [schema.load(f) for f in enhanced_files]
        if elem.nullable:
            singles_list.append(SINGLE_NULL)
        _cur_z_index[elem.body_name] = singles_list
        generated_dict[elem.z_index] = _cur_z_index
    return generated_dict


def random_metadata(_dict: Dict[int, Dict[str, List[Single]]]) -> List[Single]:
    g_image = []
    for z, list_body_part in _dict.items():
        for _, possibles in list_body_part.items():
            random_choice = random.choice(possibles)
            g_image.append(random_choice)
    return g_image

def generate_image(_list: List[Single]):
    image = Image.open(_list[0].file_uri).convert("RGBA")
    for single in _list[1:]:
        if single != SINGLE_NULL:
            tmp_image = Image.open(single.file_uri).convert("RGBA")
            image = Image.alpha_composite(image, tmp_image)

    image.save("output.png")

if __name__ == "__main__":
    run("nft.config.json")
