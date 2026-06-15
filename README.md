# AC Entry List Generator

A command-line tool that generates an `entry_list.ini` file for an Assetto Corsa server by scanning your local `content/cars` directory.

## Requirements

- Python 3.6+

## Usage

```bash
python entry_list_generator.py <cars_dir> [options]
```

### Arguments

| Argument | Description |
|---|---|
| `cars_dir` | **(Required)** Path to your Assetto Corsa `content/cars` directory |

### Options

| Flag | Description |
|---|---|
| `-o`, `--output` | Output file path. Defaults to `entry_list.ini` in the current directory |
| `-l`, `--limit` | Maximum number of cars to include |
| `-rc`, `--random-cars` | Randomise which cars are selected (default: alphabetical) |
| `-rs`, `--random-skins` | Randomise skin selection per car (default: first alphabetically) |
| `-f`, `--force` | Overwrite output file if it already exists |

## Examples

**All cars, alphabetical order:**
```bash
python entry_list_generator.py ~/assettocorsa/content/cars/
```

**Limit to 20 cars, save to server folder:**
```bash
python entry_list_generator.py ~/assettocorsa/content/cars/ -l 20 -o ~/ac_server/cfg/entry_list.ini
```

**Random selection of 30 cars with random skins:**
```bash
python entry_list_generator.py ~/assettocorsa/content/cars/ -l 30 -rc -rs
```

**Overwrite an existing entry list:**
```bash
python entry_list_generator.py ~/assettocorsa/content/cars/ -f
```

**Windows:**
```bash
python entry_list_generator.py "C:\Program Files (x86)\Steam\steamapps\common\assettocorsa\content\cars"
```

## Output format

```ini
[CAR_0]
MODEL=ferrari_458_gt3
SKIN=livery_1
DRIVERNAME=
GUID=

[CAR_1]
MODEL=ks_bmw_m4
SKIN=00_default
DRIVERNAME=
GUID=
```
