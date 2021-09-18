from enums.rarity import Rarity, RARITY_DICTIONARY
from os.path import abspath, isfile, join
from os import listdir
from typing import List
from models import Single


def remove_ext(filename: str) -> str:
    last_dot = filename.rindex(".")
    return filename[:last_dot]


def get_rarity(filename: str) -> Rarity:
    for substr_key, rarity in RARITY_DICTIONARY.items():
        if filename.startswith(substr_key) or filename.endswith(substr_key):
            return rarity
    return Rarity.NORMAL


def get_path(folder: str) -> str:
    return abspath(folder)


def get_files(folder: str) -> List[str]:
    return [f for f in listdir(folder) if isfile(join(folder, f))]

def get_hash(singles: List[Single]) -> str:
    id_pic = ",".join([f"{elem.body_name}:{elem.single_name}" for elem in singles])
    return str(hash(id_pic))
