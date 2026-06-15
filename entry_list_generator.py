import argparse
import os
import sys
import random


def get_skin(car_path: str, random_skins: bool) -> str:
    """Return the name of the first skin found in <car_path>/skins/, random skin if enabled, or empty string."""
    skins_dir = os.path.join(car_path, "skins")

    if not os.path.isdir(skins_dir):
        return ""
        
    skins = sorted(
        entry for entry in os.listdir(skins_dir)
        if os.path.isdir(os.path.join(skins_dir, entry))
    )

    if random_skins:
        random.shuffle(skins)

    return skins[0] if skins else ""


def generate_entry_list(cars_dir: str, limit: int, random_cars: bool, random_skins: bool) -> str:
    """Walk the cars directory and build the entry_list.ini content."""
    if not os.path.isdir(cars_dir):
        print(f"Error: '{cars_dir}' is not a valid directory.", file=sys.stderr)
        sys.exit(1)

    car_folders = sorted(
        entry for entry in os.listdir(cars_dir)
        if os.path.isdir(os.path.join(cars_dir, entry))
    )

    car_folders = list(dict.fromkeys(car_folders))

    if not car_folders:
        print(f"No car folders found in '{cars_dir}'.", file=sys.stderr)
        sys.exit(1)

    if random_cars:
        random.shuffle(car_folders)

    if limit is not None and limit > len(car_folders):
        print(f"Warning: limit {limit} exceeds available cars ({len(car_folders)}), using all.")

    blocks = []
    for folder in car_folders:
        car_path = os.path.join(cars_dir, folder)
        skin = get_skin(car_path, random_skins)

        if not skin:
            print(f"Warning: no skin found for {folder}, skipping.")
            continue

        block = (
            f"[CAR_{len(blocks)}]\n"
            f"MODEL={folder}\n"
            f"SKIN={skin}\n"
            f"DRIVERNAME=\n"
            f"GUID=\n"
        )
        blocks.append(block)

        if limit is not None and len(blocks) >= limit:
            break

    return "\n".join(blocks)


def main():
    parser = argparse.ArgumentParser(
        description="Generate an Assetto Corsa entry_list.ini from a content/cars directory."
    )
    parser.add_argument(
        "cars_dir",
        help="Path to the Assetto Corsa content/cars directory.",
    )
    parser.add_argument(
        "-o", "--output",
        default="entry_list.ini",
        help="Output file path (default: entry_list.ini in current directory).",
    )
    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=None,
        help="Maximum number of cars to include."
    )
    parser.add_argument(
        "-rc", "--random-cars",
        action="store_true",
        help="Randomise car selection. Defaults to alphabetical order."
    )
    parser.add_argument(
        "-rs", "--random-skins",
        action="store_true",
        help="Randomise skin selection. Defaults to first alphabetically."
    )
    parser.add_argument(
        "-f", "--force", 
        action="store_true", 
        help="Overwrite output file if it exists."
    )

    args = parser.parse_args()

    output_path = os.path.abspath(args.output)

    if os.path.exists(output_path) and not args.force:
        print(f"Error: '{output_path}' already exists. Use -f to overwrite.")
        sys.exit(1)

    cars_dir = os.path.abspath(args.cars_dir)
    content = generate_entry_list(cars_dir, args.limit, args.random_cars, args.random_skins)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    car_count = content.count("[CAR_")
    print(f"Generated {car_count} entries -> {output_path}")


if __name__ == "__main__":
    main()
