from enums.rarity import Rarity
from models import BodyPart, Single
from typing import List
from dataclasses import dataclass


@dataclass
class Stat():
    rarity: Rarity
    count: int
    singles: List[Single]


class SingleStat():
    def __init__(self, body_part: str, list_singles: List[Single]) -> None:
        self.body_part = body_part
        self.singles = list_singles
        self.stats: List[Stat] = self.__generate_stat()

    def __generate_stat(self) -> List[Stat]:
        _dict = {}
        for single in self.singles:
            cur_rarity_list = _dict.get(single.rarity, [])
            cur_rarity_list.append(single)
            _dict[single.rarity] = cur_rarity_list
        return [Stat(rarity=rar, count=len(singles), singles=singles) for rar, singles in _dict.items()]

    def __str__(self) -> str:
        _list = [f"({stat.rarity.name}): {stat.count}" for stat in self.stats]
        return f"[{self.body_part}] {', '.join(_list)}"

    def __repr__(self) -> str:
        _list = [f"({stat.rarity.name}): {stat.count}" for stat in self.stats]
        return f"[{self.body_part}] {', '.join(_list)}"