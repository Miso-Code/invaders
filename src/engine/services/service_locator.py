from src.engine.services.images_service import ImagesService
from src.engine.services.score_service import ScoreService
from src.engine.services.sounds_service import SoundsService
from src.engine.services.text_service import TextService


class ServiceLocator:
    images_service = ImagesService()
    sounds_service = SoundsService()
    text_service = TextService()
    score_service = ScoreService(0)
