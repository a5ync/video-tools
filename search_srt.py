#!/usr/bin/env python

import os
import re
import sys
import glob

def search_srt_files(search_directory, search_text):
    """
    Searches all .srt files in the given directory for a specific text.
    Returns timestamps and file names where matches are found.
    """
    search_text = search_text.lower()  # Case insensitive search
    srt_files = glob.glob(os.path.join(search_directory,"**", "*.srt"),recursive=True)  # Find all .srt files

    if not srt_files:
        print(f"❌ No .srt files found in '{search_directory}'.")
        return

    results = []

    for file in srt_files:
        with open(file, "r", encoding="utf-8") as f:
            lines = f.readlines()

        timestamp = None
        matched_lines = []

        for i, line in enumerate(lines):
            line_clean = line.strip().lower()

            # Match timestamp line (e.g., 00:01:23,456 --> 00:01:25,678)
            if "-->" in line:
                timestamp = line.strip()
            
            # Check if the search text is in the subtitle content
            elif search_text in line_clean:
                if timestamp:  # If a timestamp exists, store the result
                    matched_lines.append((file, timestamp, line.strip()))

        results.extend(matched_lines)

    # Print results
    if results:
        print("\n🔍 **Search Results:**")
        for file, timestamp, text in results:
            # print(f"📄 {file} | ⏱ {timestamp} | {text}")
            print(f"📄 {os.path.basename(file)} | ⏱ {timestamp} | {text}")
    else:
        print(f"❌ No matches found for '{search_text}' in '{search_directory}'.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python search_srt.py /path/to/directory 'search_text'")
        sys.exit(1)
    
    search_directory = sys.argv[1]
    search_text = sys.argv[2]

    if not os.path.isdir(search_directory):
        print(f"❌ Error: '{search_directory}' is not a valid directory.")
        sys.exit(1)

    search_srt_files(search_directory, search_text)
