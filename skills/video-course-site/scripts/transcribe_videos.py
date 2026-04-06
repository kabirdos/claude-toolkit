#!/usr/bin/env python3
"""Transcribe all video files in a folder using whisper.cpp.

Usage:
  python3 transcribe_videos.py /path/to/video/folder

Requires: ffmpeg, whisper-cli (Homebrew), whisper model at ~/whisper-models/ggml-large-v3-turbo.bin

Outputs into <folder>/transcripts/:
  - .json  (whisper JSON with timestamps)
  - .srt   (subtitle format)
  - .txt   (timestamped plain text)
"""
import os
import sys
import subprocess
import json

sys.stdout.reconfigure(line_buffering=True)

MODEL = os.path.expanduser("~/whisper-models/ggml-large-v3-turbo.bin")
VIDEO_EXTS = ('.mp4', '.mkv', '.mov', '.webm', '.avi')

def find_videos(folder):
    return sorted(f for f in os.listdir(folder)
                  if any(f.lower().endswith(e) for e in VIDEO_EXTS))

def transcribe(folder):
    outdir = os.path.join(folder, "transcripts")
    os.makedirs(outdir, exist_ok=True)

    videos = find_videos(folder)
    print(f"Found {len(videos)} videos to transcribe")

    for vid in videos:
        base = os.path.splitext(vid)[0]
        vidpath = os.path.join(folder, vid)
        wav = os.path.join(outdir, f"{base}.wav")
        json_out = os.path.join(outdir, f"{base}.json")

        if os.path.exists(json_out) and os.path.getsize(json_out) > 0:
            print(f"SKIP: {base} (already transcribed)")
            continue

        print(f"\n=== Processing: {base} ===")

        print("  Extracting audio...")
        result = subprocess.run([
            "ffmpeg", "-y", "-i", vidpath,
            "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", wav
        ], capture_output=True, text=True)

        if not os.path.exists(wav):
            print(f"  ERROR: Failed to extract audio")
            print(f"  {result.stderr[-500:]}")
            continue

        print(f"  Audio: {os.path.getsize(wav)/1e6:.0f} MB")

        print("  Transcribing...")
        out_prefix = os.path.join(outdir, base)
        result = subprocess.run([
            "/opt/homebrew/bin/whisper-cli", "-m", MODEL, "-f", wav,
            "-oj", "-of", out_prefix, "--no-prints"
        ], capture_output=True, text=True)

        if os.path.exists(json_out):
            print(f"  JSON: {os.path.getsize(json_out)/1e3:.0f} KB")
        else:
            print(f"  ERROR: Whisper failed")
            if os.path.exists(wav):
                os.remove(wav)
            continue

        # Generate SRT
        subprocess.run([
            "/opt/homebrew/bin/whisper-cli", "-m", MODEL, "-f", wav,
            "-osrt", "-of", out_prefix, "--no-prints"
        ], capture_output=True, text=True)

        os.remove(wav)
        print(f"  Done: {base}")

    # Export timestamped text files from JSON
    print("\nExporting text transcripts...")
    for f in sorted(os.listdir(outdir)):
        if f.endswith('.json'):
            base = f.replace('.json', '')
            txt_path = os.path.join(outdir, base + '.txt')
            if os.path.exists(txt_path) and os.path.getsize(txt_path) > 0:
                continue
            with open(os.path.join(outdir, f)) as fh:
                data = json.load(fh)
            with open(txt_path, 'w') as out:
                for seg in data['transcription']:
                    ts = seg['timestamps']['from']
                    out.write(f'[{ts}] {seg["text"].strip()}\n')
            print(f"  {base}.txt")

    print("\n=== Transcription complete ===")
    jsons = [f for f in os.listdir(outdir) if f.endswith('.json')]
    txts = [f for f in os.listdir(outdir) if f.endswith('.txt')]
    print(f"  {len(jsons)} JSON transcripts, {len(txts)} text files")
    print(f"  Transcripts are in: {outdir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 transcribe_videos.py /path/to/video/folder")
        sys.exit(1)
    folder = os.path.abspath(sys.argv[1])
    if not os.path.isdir(folder):
        print(f"Error: {folder} is not a directory")
        sys.exit(1)
    transcribe(folder)
