import argparse
from datetime import datetime

from models import Species, Sighting
from storage import load_storage, save_storage

DATA_FILE = "floridex.json"

def cmd_add_species(args: argparse.Namespace) -> None:
    species_list, sightings_list = load_storage(DATA_FILE)

    for existing in species_list:
        if existing.scientific_name == args.scientific:
            print(f"species '{args.scientific}' already exists.")
            return

    new_species = Species(
        common_name=args.common,
        scientific_name=args.scientific,
        victorian_meaning=args.victorian,
        hanakotoba=args.hanakotoba,
    )
    species_list.append(new_species)

    save_storage(DATA_FILE, species_list, sightings_list)

    print(f"added: {new_species.common_name} ({new_species.scientific_name})")

def cmd_add_sighting(args: argparse.Namespace) -> None:
    species_list, sightings_list = load_storage(DATA_FILE)
    species_by_key = {s.scientific_name: s for s in species_list}

    if args.species not in species_by_key:
        print(f"Unknown species '{args.species}'. Add it first with `add-species`.")
        return

    new_sighting = Sighting(
        species=species_by_key[args.species],
        location=args.location,
        seen_at=datetime.now(),
        notes=args.notes,
    )
    sightings_list.append(new_sighting)
    save_storage(DATA_FILE, species_list, sightings_list)
    print(f"recorded: {new_sighting.species.common_name} at {new_sighting.location}.")

def cmd_list_sightings(args: argparse.Namespace) -> None:
    _species_list, sightings_list = load_storage(DATA_FILE)
    if not sightings_list:
        print("no sightings yet. try `add-sighting`.")
        return

    for sighting in sightings_list:
        when = sighting.seen_at.strftime(DATE_FORMAT_DISPLAY)
        print(f"[{when}] {sighting.species.common_name} at {sighting.location} — {sighting.notes}")


def cmd_dex(args: argparse.Namespace) -> None:
    species_list, sightings_list = load_storage(DATA_FILE)
    if not species_list:
        print("your dex is empty. try `add-species`.")
        return

    counts: dict[str, int] = {}
    for sighting in sightings_list:
        key = sighting.species.scientific_name
        counts[key] = counts.get(key, 0) + 1

    print(f"Your dex — {len(species_list)} species collected")
    print("-" * 40)
    for species in species_list:
        seen_count = counts.get(species.scientific_name, 0)
        print(f"{species.common_name} ({species.scientific_name}) — seen {seen_count}x")
        print(f"  Victorian: {species.victorian_meaning}")
        print(f"  Hanakotoba: {species.hanakotoba}")


DATE_FORMAT_DISPLAY = "%Y-%m-%d %H:%M"

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="floridex", description="Your flower pokédex.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_species = subparsers.add_parser("add-species", help="Add a new species to your dex.")
    p_species.add_argument("--common", required=True, help="Common name (e.g. 'Rose')")
    p_species.add_argument("--scientific", required=True, help="Scientific name (e.g. 'Rosa')")
    p_species.add_argument("--victorian", required=True, help="Victorian meaning")
    p_species.add_argument("--hanakotoba", required=True, help="Japanese flower meaning")
    p_species.set_defaults(func=cmd_add_species)

    p_sighting = subparsers.add_parser("add-sighting", help="Record a sighting.")
    p_sighting.add_argument("--species", required=True, help="Scientific name of the species")
    p_sighting.add_argument("--location", required=True, help="Where you saw it")
    p_sighting.add_argument("--notes", default="", help="Notes about the sighting")
    p_sighting.set_defaults(func=cmd_add_sighting)

    p_list = subparsers.add_parser("list-sightings", help="Show all sightings.")
    p_list.set_defaults(func=cmd_list_sightings)

    p_dex = subparsers.add_parser("dex", help="Show your collected species.")
    p_dex.set_defaults(func=cmd_dex)

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
