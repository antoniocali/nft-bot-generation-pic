import enum


class Rarity(enum.IntEnum):
    NORMAL = 1
    RARE = 2
    SR = 3


RARITY_DICTIONARY = {
    "_sr": Rarity.SR,
    "sr_": Rarity.SR,
    "r_": Rarity.RARE,
    "_r": Rarity.RARE
}
