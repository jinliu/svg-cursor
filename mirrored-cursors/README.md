# Mirrored Cursors

## Installation

1. Download [breeze_cursors.mirrored.tar.gz](https://github.com/jinliu/svg-cursor/raw/refs/heads/main/mirrored-cursors/breeze_cursors.mirrored.tar.gz). Then extract it to `~/.local/share/icons/`

2. Genenerate Xcursor files from the SVG files:

   ```bash
   cd ~/.local/share/icons/breeze_cursors.mirrored
   kcursorgen --svg-theme-to-xcursor --svg-dir=cursors_scalable --xcursor-dir=cursors --sizes=36 --scales=1,2.5,3
   ```

   Note: You can adjust the `--sizes` and `--scales` options as needed. Scales must include 1, your
   current scale factor, and the rounded up scale factor if your current scale factor is not an integer.

## Building

The `mirror` script should work with any SVG cursor theme. To build the mirrored version of Breeze Dark, run:

```bash
cd mirrored-cursors
rm -r breeze_cursors.mirrored
mkdir -p breeze_cursors.mirrored/cursors_scalable
./mirror breeze_cursors/cursors_scalable breeze_cursors.mirrored/cursors_scalable --mirror-list=mirror-list.txt
```
