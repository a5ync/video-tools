#!/usr/bin/env python

import json
import sys

def seconds_to_srt_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,MS)"""
    millisec = int((seconds % 1) * 1000)
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{millisec:03}"

def convert_transcribe_json_to_srt(json_file, srt_file):
    """Convert Amazon Transcribe JSON to SRT format"""
    with open(json_file, 'r') as f:
        data = json.load(f)

    items = data['results']['items']
    srt_output = []
    index = 1
    chunk = []
    start_time = None

    for item in items:
        if "start_time" in item:
            if not start_time:
                start_time = float(item["start_time"])
            chunk.append(item["alternatives"][0]["content"])
            end_time = float(item["end_time"])
        
        # Group into sentences of around 10 words or when punctuation is found
        if len(chunk) >= 10 or item["type"] == "punctuation":
            if start_time and chunk:
                srt_output.append(f"{index}\n{seconds_to_srt_time(start_time)} --> {seconds_to_srt_time(end_time)}\n{' '.join(chunk)}\n")
                index += 1
                chunk = []
                start_time = None

    with open(srt_file, 'w') as f:
        f.writelines("\n".join(srt_output))

    print(f"SRT file saved: {srt_file}")

# Run script
if len(sys.argv) != 3:
    print("Usage: python convert_transcribe_json_to_srt.py transcript.json output.srt")
else:
    convert_transcribe_json_to_srt(sys.argv[1], sys.argv[2])
