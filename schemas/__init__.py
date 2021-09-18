from models import BodyPart, Single
from marshmallow import Schema, fields, post_load
from utils import get_rarity, remove_ext
from os.path import join


class BodyPartSchema(Schema):
    body_name = fields.Str(required=True)
    z_index: int = fields.Int(required=True)
    nullable: bool = fields.Bool(required=True)
    folder_name: str = fields.Str(required=True)

    @post_load
    def make_model(self, data, **kwargs) -> BodyPart:
        return BodyPart(**data)


class SingleSchema(Schema):
    body_name = fields.Str(required=True)
    file_name = fields.Str(required=True)
    folder_name = fields.Str(required=True)
    z_index = fields.Int(required=True)

    @post_load
    def make_model(self, data, **kwargs) -> Single:
        file_uri = join(data.get("folder_name"), data.get("file_name"))
        single_name = remove_ext(data.get("file_name"))
        rarity = get_rarity(single_name)
        return Single(body_name=data.get("body_name"), single_name=single_name, file_uri=file_uri, rarity=rarity, z_index=data.get("z_index"))
