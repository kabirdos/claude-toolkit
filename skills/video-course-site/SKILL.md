---
name: video-course-site
description: Build a static explainer site from a folder of course video files. Three-step pipeline — (1) transcribe videos locally with whisper.cpp, (2) generate blog posts from transcripts using parallel Claude Code agents, (3) assemble into a tabbed single-page site. Use when asked to create a course site, transcribe videos for a course, turn video lectures into blog posts, or build an explainer site from recordings. Triggers on "course site", "transcribe videos", "video to blog", "explainer site from videos".
---

# Video Course Site

Turn a folder of video files into a readable, tabbed static site where each video becomes a blog post written in the teacher's voice.

## Prerequisites

- **ffmpeg**: `brew install ffmpeg`
- **whisper.cpp**: `brew install whisper-cpp` (provides `whisper-cli`)
- **Whisper model**: Download to `~/whisper-models/ggml-large-v3-turbo.bin`

## Workflow

### Step 1: Transcribe Videos

Run the bundled transcription script:

```bash
python3 scripts/transcribe_videos.py /path/to/video/folder
```

This extracts audio, runs whisper.cpp, and produces `.json`, `.srt`, and `.txt` files in `<folder>/transcripts/`. Skips already-transcribed files.

For long-running transcription (many videos, ~1.5hrs each), run in background:

```bash
nohup caffeinate -i python3 scripts/transcribe_videos.py /path/to/folder > ~/transcribe.log 2>&1 &
```

**Known issue:** Dropbox paths with unicode characters (curly apostrophes like `'`) can break `os.listdir`. Use `os.walk` from a known ASCII parent to discover the real path.

### Step 2: Generate Blog Posts (Parallel Agents)

Dispatch one agent per transcript to generate blog posts. Posts go in `<folder>/site/posts/`.

**Important:** Write posts to a local (non-Dropbox) staging directory if the source folder is in Dropbox, since Dropbox smart sync can dehydrate newly written files to 0 bytes. Copy to Dropbox after all posts are complete.

For each transcript, dispatch an agent with instructions like:

> Read the transcript at `<folder>/transcripts/<name>.txt`. Write a blog-style HTML post (no page wrapper — just content starting with `<h2>`) that:
>
> - Is written in the teacher's voice (first person), not a summary
> - Uses `<h3>` sections to organize the teaching topics
> - Calls out student Q&A using `<blockquote>` with the question in `<strong>` tags
> - Transcribes guided meditations directly with timestamps referencing the video, using `<div class="meditation-marker">` for timestamp callouts
> - Separates teaching, Q&A, and meditation into distinct sections
> - Save to `<staging>/posts/<name>.html`

Also generate an `overview.html` that introduces the course.

### Step 3: Assemble the Site

After all posts are written, run the assembly script:

```bash
python3 scripts/assemble_site.py /path/to/video/folder
```

This reads all `.html` files from `<folder>/site/posts/`, creates tab navigation, and outputs a single `<folder>/site/index.html` with Medium-inspired typography.

## Post HTML Format

Posts are HTML fragments (no `<html>`, `<head>`, or `<body>` tags). Structure:

```html
<h2>Class Title</h2>

<h3>Topic Section</h3>
<p>Teaching content in the teacher's voice...</p>

<h3>Q&A</h3>
<blockquote>
  <p><strong>Student question here?</strong></p>
  <p>Teacher's answer...</p>
</blockquote>

<h3>Guided Meditation [starts at 1:23:45]</h3>
<div class="meditation-marker">
  Guided meditation begins at 1:23:45 in the video
</div>
<blockquote>
  <p>Direct transcription of meditation instructions...</p>
</blockquote>
```

## Rerunning on a New Course

The pipeline is idempotent — it skips completed work at each step:

1. Transcription skips videos that already have `.json` output
2. Blog generation skips transcripts that already have posts
3. Assembly rebuilds the full site from whatever posts exist

To process a new course, just point the scripts at a new folder of videos.
