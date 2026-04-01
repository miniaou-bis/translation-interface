# Translation interface

A small utility script that extracts dialogue blocks from HTML files and presents them in a simple visual-novel style Tkinter viewer.

## Contents
- `script.py` — Parses HTML (titles, speeches, narration, choices) and shows a Tkinter UI to step through lines with speaker color backgrounds.

## Requirements
- Python 3.8+
- Tkinter (usually included with standard Python installers)

## Quick start

Run:
   ```
   python script.py <html_file_path>
   ```

## Notes & customization
- HTML parsing relies on regex patterns in `extract_lines` — adjust those patterns if your HTML structure differs.
- Speaker background colors are defined in the `speaker_colors` dict in `script.py`. Edit or extend this mapping to change appearance.
- The UI currently uses a hardcoded window size and basic buttons (Previous, Next, Skip). Modify `show_window` to change layout or behavior.

## Source & attribution
This tool was used for translating "Uta no Prince-sama: Repeat Love". The HTML used as input in this repository was taken from:
https://shiningwonderland.tumblr.com/directory-repeat

## Permissions
Ensure you have the right to use or redistribute any original content. This tool reads local HTML files; do not republish copyrighted material or claim others' translations as your own without permission.

## Troubleshooting
- If the window doesn't appear, ensure Tkinter is installed and you're running with a graphical session.
- For parsing issues, print `html` or `p_blocks` in `extract_lines` to inspect matched blocks.
