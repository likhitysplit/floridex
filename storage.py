import json
from datetime import datetime
from pathlib import Path

from models import Species, Sighting


DATE_FORMAT = "%Y-%m-%d %H:%M"


def species_to_dict(species: Species) -> dict:
    return {
        "common_name": species.common_name,
        "scientific_name": species.scientific_name,
        "victorian_meaning": species.victorian_meaning,
        "hanakotoba": species.hanakotoba,
    }


def species_from_dict(data: dict) -> Species:
    return Species(
        common_name=data["common_name"],
        scientific_name=data["scientific_name"],
        victorian_meaning=data["victorian_meaning"],
        hanakotoba=data["hanakotoba"],
    )


def sighting_to_dict(sighting: Sighting) -> dict:
    return {
        "species": sighting.species.scientific_name,
        "location": sighting.location,
        "seen_at": sighting.seen_at.strftime(DATE_FORMAT),
        "notes": sighting.notes,
    }


def sighting_from_dict(data: dict, species_by_key: dict[str, Species]) -> Sighting:
    return Sighting(
        species=species_by_key[data["species"]],
        location=data["location"],
        seen_at=datetime.strptime(data["seen_at"], DATE_FORMAT),
        notes=data["notes"],
    )


def save_storage(
    filename: str,
    species_list: list[Species],
    sightings_list: list[Sighting],
) -> None:
    storage = {
        "species": [species_to_dict(s) for s in species_list],
        "sightings": [sighting_to_dict(s) for s in sightings_list],
    }
    with open(filename, "w") as f:
        json.dump(storage, f, indent=2)


def load_storage(filename: str) -> tuple[list[Species], list[Sighting]]:
    if not Path(filename).exists():
        return [], []

    with open(filename, "r") as f:
        data = json.load(f)

    species_list = [species_from_dict(s) for s in data["species"]]
    species_by_key = {s.scientific_name: s for s in species_list}
    sightings_list = [
        sighting_from_dict(s, species_by_key) for s in data["sightings"]
    ]

    return species_list, sightings_list