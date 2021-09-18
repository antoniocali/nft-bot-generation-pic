from dataclasses import dataclass
from enums.rarity import Rarity

@dataclass
class BodyPart():
    body_name: str
    z_index: int
    nullable: bool
    folder_name: str


@dataclass
class Single():
    body_name: str
    single_name: str
    file_uri: str
    rarity: Rarity
    z_index: int


SINGLE_NULL = Single("","","", Rarity.NORMAL, -1)    