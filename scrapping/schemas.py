from datetime import datetime
from pydantic import BaseModel, TypeAdapter

from utils import get_time_delta


class Interval(BaseModel):
    start: datetime
    end: datetime

    def __eq__(self, other):
        if type(other) is Interval:
            range = 60 * 60 * 12  # 12 часов
            return (
                abs(get_time_delta(self.start, other.start)) < range
                and abs(get_time_delta(self.end, other.end)) < range
            )

        raise ValueError()


class Banner(BaseModel):
    image_url: str
    characters: list[str] = []


class BannerGroup(BaseModel):
    index: int = 0

    banners: list[Banner] = []

    is_limited: bool
    is_fest: bool
    is_prediction: bool = False

    interval: Interval

    @property
    def characters(self):
        return [name for banner in self.banners for name in banner.characters]
    
    def check_exact_characters(self, other: "BannerGroup"):
        """Возвращает True, если обе группы содержат одинаковых персонажей"""
        
        return all(ch in other.characters for ch in self.characters) and all(ch in self.characters for ch in other.characters)
    
    def check_includes_characters(self, other: "BannerGroup"):
        """Возвращает True, если все персонажи из other содержаться в этой группе"""
        
        return all(ch in self.characters for ch in other.characters)
    
    
banner_groups_adapter = TypeAdapter(list[BannerGroup])