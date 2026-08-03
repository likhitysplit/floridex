from dataclasses import dataclass
from datetime import datetime


@dataclass
class Species:
    common_name: str
    scientific_name: str
    victorian_meaning: str
    hanakotoba: str


@dataclass
class Sighting:
    species: Species
    location: str
    seen_at: datetime
    notes: str