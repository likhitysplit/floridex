from datetime import datetime
from models import Species, Sighting
from storage import (
    species_to_dict,
    sighting_to_dict,
    species_from_dict,
    sighting_from_dict,
)

def test_species_round_trip():
    original = Species(
        common_name="White egret",
        scientific_name="Pecteilis radiata",
        victorian_meaning="purity",
        hanakotoba="my thoughts will follow you into your dreams",
    )

    as_dict = species_to_dict(original)
    reconstructed = species_from_dict(as_dict)

    assert reconstructed == original

def test_sighting_round_trip():
    species = Species(
        common_name="Rose",
        scientific_name="Rosa",
        victorian_meaning="Love",
        hanakotoba="Beauty",
    )
    original = Sighting(
        species=species,
        location="Aunt Mary's garden",
        seen_at=datetime(2026, 8, 2, 14, 30),
        notes="In full bloom",
    )

    as_dict = sighting_to_dict(original)
    reconstructed = sighting_from_dict(as_dict, {species.scientific_name: species})

    assert reconstructed == original


def test_sighting_key_matches_species_scientific_name():
    species = Species(
        common_name="Rose",
        scientific_name="Rosa",
        victorian_meaning="Love",
        hanakotoba="Beauty",
    )
    sighting = Sighting(
        species=species,
        location="garden",
        seen_at=datetime(2026, 1, 1, 12, 0),
        notes="",
    )

    as_dict = sighting_to_dict(sighting)

    assert as_dict["species"] == "Rosa"