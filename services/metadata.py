from typing import List, Dict, Any, Tuple
from models import SINGLE_NULL, Single, BodyPart
from models.stats import SingleStat
from schemas import BodyPartSchema, SingleSchema
from utils import get_files, get_path, get_rarity, remove_ext, join

class Metadata:
    def __init__(self, input_folder: str, input_data: List[Dict[str, Any]]) -> None:
        self.input_folder = input_folder
        self.body_parts = self.__get_body_parts(input_data)
        self.single_parts = self.__gen_dict_single(self.body_parts)
        self.stats = self.__create_stats(self.single_parts)
        self.indexed = self.__z_indexed_dictionary(self.single_parts)

    def __get_body_parts(self, _json: List[Dict[str, Any]]) -> List[BodyPart]:
        schema = BodyPartSchema()
        return [schema.load(item) for item in _json]

    def __gen_dict_single(self, stacks: List[BodyPart]) -> Dict[Tuple[str, int], List[Single]]:
        generated_dict = {}
        schema = SingleSchema()
        input_folder_name = get_path(self.input_folder)
        for elem in stacks:
            folder_name = join(input_folder_name, elem.folder_name)
            all_files = get_files(folder_name)
            enhanced_files = [{"body_name": elem.body_name, "file_name": f,
                                "folder_name": folder_name} for f in all_files]
            singles_list = [schema.load(f) for f in enhanced_files]
            if elem.nullable:
                singles_list.append(SINGLE_NULL)
            generated_dict[(elem.body_name, elem.z_index)] = singles_list
        return generated_dict

    def __create_stats(self, stacks: Dict[Tuple[str, int], List[Single]]) -> List[SingleStat]:
        schema = SingleSchema()
        return [SingleStat(body_part, singles) for (body_part, _), singles in stacks.items()]

    def __z_indexed_dictionary(self, stacks: Dict[Tuple[str, int], List[Single]]) -> Dict[int, Dict[str, List[Single]]]:
        generated_dict = {}
        for (body_part, z_index), singles in stacks.items():
            z_indexed = generated_dict.get(z_index, {})
            z_indexed[body_part] = singles
            generated_dict[z_index] = z_indexed
        return generated_dict