# svg-theme-to-xcursor: Generate Xcursor from SVG theme

Cursor themes generally come with limited choice for sizes. This tool allows you to generate Xcursor at any sizes, provided that your theme has SVG support.

For example, in KDE Plasma's default Breeze cursor theme, the maximum size is 72. If you want to use a size 48 cursor and you have a global scale of 3, you need a 48*3=144 size cursor or it will be blurry. This tool can generate the cursor for you.

## Requirements

- Python 3
- PySide 6
- xcursorgen (usually included in the `xorg-xcursorgen` package)

## Usage

1. Check that your cursor theme has a subdirectory named "cursors_scalable".

1. Download this tool.

```bash
git clone https://github.com/jinliu/svg-cursor.git
```

1. Copy the cursor theme to your home directory.

```bash
cp -r /usr/share/icons/breeze_cursors ~/.local/share/icons/
```

1. Run this tool.

```bash
cd ~/.local/share/icons/breeze_cursors
rm -r cursors
svg-theme-to-xcursor.py --output-dir=cursors --svg-dir=cursors_scalable --sizes=48 --scales=1,3
```

If you are using a fractional scale, e.g. 2.5, please also include an integer scale, because some apps do not support fractional scales (e.g. GTK3):

```bash
svg-theme-to-xcursor.py --output-dir=cursors --svg-dir=cursors_scalable --sizes=48 --scales=1,2.5,3
```

1. It's done. You might need to select another cursor theme and then switch back to see the changes.
