#!/usr/bin/env python3

import argparse
import json
import math
import tempfile
import subprocess
from pathlib import Path
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtGui import QImage, QPainter
from PySide6.QtCore import QRectF, QPointF

def main():
    parser = argparse.ArgumentParser(
                    prog='svg-theme-to-xcursor',
                    description='Generate XCursor from an SVG theme')
    parser.add_argument('--output-dir', required=True)
    parser.add_argument('--svg-dir', required=True)
    parser.add_argument('--sizes', required=True)
    parser.add_argument('--scales', required=True)
    args = parser.parse_args()

    sizes = list(map(int, args.sizes.split(',')))
    scales = list(map(float, args.scales.split(',')))
    desired_sizes = {}

    for scale in scales:
        alignment = round(scale)

        if alignment != scale:
            alignment = 1

        for size in sizes:
            scaled_size = round(size * scale)
            if not scaled_size in desired_sizes:
                desired_sizes[scaled_size] = alignment
            else:
                desired_sizes[scaled_size] = math.lcm(desired_sizes[scaled_size], alignment);

    print("Desired sizes:")
    for size, alignment in sorted(desired_sizes.items()):
        print(f"\t{size} alignment {alignment}")

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    svg_dir = Path(args.svg_dir)

    with tempfile.TemporaryDirectory() as tmp_dir:
        for shape_dir in sorted(svg_dir.iterdir()):
            if not shape_dir.is_dir() or shape_dir.is_symlink():
                continue

            shape_name = shape_dir.stem
            print(f"Generate {shape_name}")

            metadata = json.load(Path(shape_dir / "metadata.json").open())

            shape_tmp_dir = Path(tmp_dir) / shape_name
            shape_tmp_dir.mkdir(exist_ok=False)
            for size, _ in desired_sizes.items():
                (shape_tmp_dir / str(size)).mkdir(exist_ok=False)

            with (shape_tmp_dir / "config").open('w') as config_file:
                for m in metadata:
                    filename = m["filename"]
                    hotspot_x = m["hotspot_x"]
                    hotspot_y = m["hotspot_y"]
                    nominal_size = m["nominal_size"]
                    delay = m.get("delay", 0)

                    svg_renderer = QSvgRenderer(str(shape_dir /  filename))
                    svg_size = svg_renderer.defaultSize()

                    for size, alignment in desired_sizes.items():
                        scale = size / nominal_size
                        image_size = svg_size * scale
                        aligned_image_size = (image_size.width() + (alignment - image_size.width() % alignment) % alignment, image_size.width() + (alignment - image_size.width() % alignment) % alignment)

                        image = QImage(aligned_image_size[0], aligned_image_size[1], QImage.Format_ARGB32)
                        image.fill(0)

                        painter = QPainter()
                        painter.begin(image)
                        svg_renderer.render(painter, QRectF(QPointF(0, 0), image_size))
                        painter.end()

                        pngname = Path(str(size)) / Path(filename).with_suffix(".png")
                        image.save(str(shape_tmp_dir / pngname))

                        hotspot_x_scaled = math.floor(hotspot_x * scale + 0.01)
                        hotspot_y_scaled = math.floor(hotspot_y * scale + 0.01)

                        config_file.write(f"{size} {hotspot_x_scaled} {hotspot_y_scaled} {pngname} {delay}\n")

                config_file.close()
                subprocess.run(["xcursorgen", "--prefix", str(shape_tmp_dir), str(shape_tmp_dir / "config"), str(output_dir / shape_name)])
    
    for alias in sorted(svg_dir.iterdir()):
        if not alias.is_symlink():
            continue

        print(f"Alias {alias.name} => {alias.resolve().name}")
        output_dir.joinpath(alias.name).symlink_to(alias.resolve().name)

if __name__ == '__main__':
    main()
