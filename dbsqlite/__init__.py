from pony.orm import *

db = Database()

class ImageID(db.Entity):
    image_id = PrimaryKey(str)

db.bind(provider='sqlite', filename='database.sqlite', create_db=True)
db.generate_mapping(create_tables=True)

@db_session
def check_image(image_id: str):
    return ImageID.exists(image_id=image_id)

@db_session
def add_image(image_id: str):
    ImageID(image_id=image_id)

