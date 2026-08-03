from dataclasses import dataclass
from datetime import datetime
import json

# dataclasses
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

# methods
def species_to_dict(species: Species) -> dict:
    return {
        "common_name": species.common_name,
        "scientific_name": species.scientific_name,
        "victorian_meaning": species.victorian_meaning,
        "hanakotoba": species.hanakotoba,
    }

def sighting_to_dict(sighting: Sighting) -> dict:
    return {
        "species": sighting.species.scientific_name,
        "location": sighting.location,
        "seen_at": sighting.seen_at.strftime("%Y-%m-%d %H:%M"),
        "notes": sighting.notes,
    }

def build_storage(species_list: list[Species], sightings_list: list[Sighting]) -> dict: 
    return {
        "species": [species_to_dict(s) for s in species_list],
        "sightings": [sighting_to_dict(s) for s in sightings_list],
    }

def species_from_dict(data: dict) -> Species:
    return Species(
        common_name=data["common_name"],
        scientific_name=data["scientific_name"],
        victorian_meaning=data["victorian_meaning"],
        hanakotoba=data["hanakotoba"],
    )

def sightings_from_dict(data: dict, species_by_key: dict[str, Species]) -> Sighting:
    return Sighting(
        species=species_by_key[data["species"]],
        location=data["location"],
        seen_at=datetime.strptime(data["seen_at"], "%Y-%m-%d %H:%M"),
        notes=data["notes"],
    )

def load_storage(file_name: str) -> tuple[list[Species], list[Sighting]]:
    with open(file_name, "r") as f:
        data = json.load(f);

    species_list = [species_from_dict(s) for s in data["species"]]
    species_by_key = {s.scientific_name: s for s in species_list}
    sightings_list = [sightings_from_dict(s, species_by_key) for s in data["sightings"]]

    return species_list, sightings_list

# main
white_egret = Species(
    common_name="white egret",
    scientific_name="pecteilis radiata",
    victorian_meaning="purity, grace, resilience",
    hanakotoba="my thoughts will follow you into your dreams.",
)

first_sighting = Sighting(
    species=white_egret,
    location="in the lost library",
    seen_at=datetime.now(),
    notes="very interesting shape, hauntingly beautiful."
)

second_sighting = Sighting(
    species=white_egret,
    location="in basil's garden",
    seen_at=datetime.now(),
    notes="i wonder how basil's doing.",
)
print(sighting_to_dict(second_sighting))

all_species = [white_egret]
all_sightings = [first_sighting, second_sighting]

storage = build_storage(all_species, all_sightings)

with open("floridex.json", "w") as f:
    json.dump(storage, f, indent=2)

print("wrote floridex.json.")

print()
print("--- reading it back ---")
loaded_species, loaded_sightings = load_storage("floridex.json")

for species in loaded_species:
    print(species)

for sighting in loaded_sightings:
    print(sighting)