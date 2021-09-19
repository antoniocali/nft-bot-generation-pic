from models import Single
from services.metadata import Metadata
from dbsqlite import check_image, add_image
from utils import get_hash
import random
from typing import List, Tuple

class ImagesService:
    def __init__(self, metadata: Metadata) -> None:
        self.metadata = metadata
    
    def new_nft(self) -> Tuple[List[Single], str]:
        g_image = []
        for _, list_body_part in self.metadata.indexed.items():
            for _, possibles in list_body_part.items():
                random_choice = random.choice(possibles)
                g_image.append(random_choice)
        id_image = get_hash(g_image)
        if check_image(id_image):
            return self.new_nft()
        else:
            add_image(id_image)
            return (g_image, id_image)
