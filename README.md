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

## Troubleshooting
- If the window doesn't appear, ensure Tkinter is installed and you're running with a graphical session.
- For parsing issues, print `html` or `p_blocks` in `extract_lines` to inspect matched blocks.

License: (add your preferred license)
