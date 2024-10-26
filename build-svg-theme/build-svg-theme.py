#!/usr/bin/env python3

import argparse
import shutil
import json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(
                    prog='build-svg-theme',
                    description='Build an SVG theme from SVG source files')
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--config-dir', required=True)
    parser.add_argument('--svg-dir', required=True)
    parser.add_argument('--alias-file')
    parser.add_argument('--nominal-size', required=True)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    config_dir = Path(args.config_dir)
    svg_dir = Path(args.svg_dir)
    nominal_size = int(args.nominal_size)

    for config_file in sorted(config_dir.iterdir()):
        shape_name = config_file.stem
        print(f"Generate {shape_name}")

        shape_dir = output_dir / shape_name
        shape_dir.mkdir(exist_ok=False)

        metadata = []
        for line in config_file.read_text().splitlines():
            fields = line.split()
            if len(fields) < 4:
                continue
            size = int(fields[0])
            if size != nominal_size:
                continue
            hotspot_x = int(fields[1])
            hotspot_y = int(fields[2])
            path = fields[3]
            filename = Path(path).stem
            svg_file = svg_dir / f"{filename}.svg"
            shutil.copy2(svg_file, shape_dir)

            m = {
                "filename": f"{filename}.svg",
                "hotspot_x": hotspot_x,
                "hotspot_y": hotspot_y,
                "nominal_size": nominal_size,
            }
            if len(fields) > 4:
                m["delay"] = int(fields[4])
            metadata.append(m)

        metadata_file = shape_dir / "metadata.json"
        json.dump(metadata, metadata_file.open('w'))

    if args.alias_file:
        for line in Path(args.alias_file).read_text().splitlines():
            alias, target = line.split()
            if output_dir.joinpath(alias).exists():
                print(f"Skipping alias {alias} -> {target}: {alias} already exists")
            else:
                print(f"Alias {alias} -> {target}")
                (output_dir / alias).symlink_to(target)

if __name__ == '__main__':
    main()
