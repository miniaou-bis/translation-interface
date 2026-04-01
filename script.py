import re
import tkinter as tk
import argparse

def extract_lines(html_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    title_pattern = re.compile(r'<h2\s*>\s*<b\s*>([^<]+)</b\s*>\s*<i\s*><b\s*>([^<]+)</b\s*></i\s*>\s*</h2\s*>',re.DOTALL)
    title2_pattern = re.compile(r'<h2\s*>\s*<b\s*>([^<]+)</b\s*>\s*<b\s*>\s*<i\s*>([^<]+)</i\s*>\s*</b\s*>\s*</h2\s*>',re.DOTALL)

    title3_pattern = re.compile(r'<h2\s*>\s*([^<]+)?(<i\s*>([^<]+)\s*</i\s*>)([^<]+)?</h2\s*>',re.DOTALL) ###
    mini_game = re.compile(r'<h2\s*>\s*([^<]+)</h2\s*>',re.DOTALL)

    global_pattern = re.compile(r'<p\s*>\s*<i\s*>([\s\S]*?)</i\s*>\s*</p\s*>',re.DOTALL)
    speech_pattern = re.compile(r'<p\s*>\s*<b\s*>([^<:]+):?\s*</b\s*>\s*(.*?)</p\s*>', re.DOTALL)
    choice_pattern = re.compile(r'<h2\s*>\s*Select the Phrase!\s*</h2\s*>', re.DOTALL)
    p_blocks = re.findall(r'(<h2\s*>.*?</h2\s*>|<p\s*>.*?</p\s*>)', html, re.DOTALL)

    lines = []
    for block in p_blocks:
        if choice_pattern.match(block):
            lines.append({'type': 'choice', 'text': 'Select the Phrase!', 'speaker': ''})
        elif title2_pattern.match(block) or title_pattern.match(block):
            title = title2_pattern.match(block)
            if title is None:
                title = title_pattern.match(block) 

            part1 = title.group(1).strip()
            part2 = title.group(2).strip()
            full_title = f"{part1} {part2}"
            lines.append({'type': 'choice', 'text': full_title, 'speaker': ''})
        elif title3_pattern.match(block):
            title = title3_pattern.match(block)
            
            if title.group(1) != None:
                part1 = title.group(1).strip()
                part2 = title.group(3).strip()
            else:
                part1 = title.group(3).strip()
                part2 = title.group(4).strip()
            full_title = f"{part1} {part2}"
            lines.append({'type': 'choice', 'text': full_title, 'speaker': ''})
        elif mini_game.match(block):
            title = mini_game.match(block)
            full_title = title.group(1).strip()
            lines.append({'type': 'choice', 'text': full_title, 'speaker': ''})
        else:
            global_match = global_pattern.match(block)
            speech_match = speech_pattern.match(block)
            if global_match:
                text = global_match.group(1).strip()
                lines.append({'type': 'global', 'text': text, 'speaker': ''})
            elif speech_match:
                speaker = speech_match.group(1).strip() if speech_match.group(1) else "error"
                speech = speech_match.group(2).strip()
                lines.append({'type': 'speech', 'text': speech, 'speaker': speaker})
    return lines




def show_window(lines):
    root = tk.Tk()
    root.title("Visual Novel")
    root.geometry("1000x160")
    root.configure(bg="#ffffff")

    # Speaker color map
    speaker_colors = {
        "Ringo Tsukimiya": "#FEB5BA",   # pink
        "Otoya Ittoki": "#f9837b",      # red
        "Masato Hijirikawa": "#9198fb", # blue
        "Natsuki Shinomiya": "#f4f0ac", # yellow
        "Syo Kurusu": "#ffb6d5",       # pink
        "Cecil Aijima": "#C1FEAF",     # green
        "Tokiya Ichinose": "#a18bc9",   # purple
        "Ren Jinguji": "#fbc98c",      # light orange
        "Tomochika Shibuya": "#FE79E8", # light pink
        "Shining Saotome": "#fac170",   # cream
        "Haruka Nanami": "#c0f9ec",   # cyan
        "": "#fafafa",                  # narration
    }

    speaker_label = tk.Label(root, text="", font=("Arial", 12, "bold"), fg="#22223b", bg="#f5f5f5", anchor="w", padx=20)
    speaker_label.pack(fill="x", pady=(20, 0))

    # Main frame to hold buttons and dialogue
    main_frame = tk.Frame(root, bg="#ffffff")
    main_frame.pack(expand=True, fill="both", padx=40, pady=20)

    skip_backward_btn = tk.Button(main_frame, text="⇤ Back", font=("Arial", 8), bg="#6c757d", fg="#ffffff", width=10)
    skip_backward_btn.pack(side="left", padx=(0, 10), fill="y")
    
    # Left button
    prev_btn = tk.Button(main_frame, text="← Previous", font=("Arial", 8), bg="#9a8c98", fg="#ffffff", width=10)
    prev_btn.pack(side="left", padx=(0, 10), fill="y")

    # Dialogue frame in the center
    frame = tk.Frame(main_frame, bg="#f5f5f5", bd=4, relief="ridge")
    frame.pack(side="left", expand=True, fill="both")

    text_label = tk.Label(frame, text="", wraplength=900, font=("Arial", 12), fg="#22223b", bg="#f5f5f5", justify="left", anchor="nw")
    text_label.pack(expand=True, fill="both", padx=10, pady=5)

    # Right button
    next_btn = tk.Button(main_frame, text="Next →", font=("Arial", 8), bg="#9a8c98", fg="#ffffff", width=10)
    next_btn.pack(side="left", padx=(10, 0), fill="y")

    # Skip to next section
    skip_forward_btn = tk.Button(main_frame, text="⇥ Skip", font=("Arial", 8), bg="#6c757d", fg="#ffffff", width=10)
    skip_forward_btn.pack(side="left", padx=(10, 0), fill="y")

    

    idx = [0]

    def get_colors(speaker):
        color = speaker_colors.get(speaker, "#e0e0e0")
        return color

    def update_labels():
        if 0 <= idx[0] < len(lines):
            line = lines[idx[0]]
            color = get_colors(line['speaker'])
            frame.config(bg=color)
            text_label.config(bg=color, fg="#22223b")
            speaker_label.config(bg=color, fg="#22223b")
            if line['type'] == 'speech':
                speaker_label.config(text=line['speaker'])
                text_label.config(font=("Arial", 12))  # normal font size
            elif line['type'] == 'choice':
                speaker_label.config(text="")
                text_label.config(font=("Arial", 18, "bold"))  # bigger font for choice
            else:
                speaker_label.config(text="")
                text_label.config(font=("Arial", 12))  # normal font size
            text_label.config(text=line['text'])
        elif idx[0] >= len(lines):
            speaker_label.config(text="")
            text_label.config(text="End of script.")
        else:
            speaker_label.config(text="")
            text_label.config(text="")

    def next_line():
        if idx[0] < len(lines):
            idx[0] += 1
            update_labels()
    
    def skip_to_next_choice():
        while idx[0] < len(lines) - 1:
            idx[0] += 1
            if lines[idx[0]]['type'] == 'choice':
                break
        update_labels()
    
    def skip_to_prev_choice():
        while idx[0] > 0:
            idx[0] -= 1
            if lines[idx[0]]['type'] == 'choice':
                break
        update_labels()

    def prev_line():
        if idx[0] > 0:
            idx[0] -= 1
            update_labels()

    prev_btn.config(command=prev_line)
    next_btn.config(command=next_line)
    skip_forward_btn.config(command=skip_to_next_choice)
    skip_backward_btn.config(command=skip_to_prev_choice)


    update_labels()
    root.mainloop()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visual Novel Script Viewer")
    parser.add_argument("html_path", help="Path to the HTML file containing the script")

    args = parser.parse_args()
    
    lines = extract_lines(args.html_path)
    show_window(lines)