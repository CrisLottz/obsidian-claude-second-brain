"""Print a YouTube video's transcript with [mm:ss] timestamps.

Usage: python yt_transcript.py <youtube-url-or-id> [lang ...]
Requires: pip install --user youtube-transcript-api
"""
import re
import sys

try:
    from youtube_transcript_api import YouTubeTranscriptApi
except ImportError:
    sys.exit("youtube-transcript-api is not installed: python -m pip install --user youtube-transcript-api")


def video_id(arg):
    match = re.search(r"(?:v=|youtu\.be/|shorts/|embed/)([\w-]{11})", arg)
    if match:
        return match.group(1)
    if re.fullmatch(r"[\w-]{11}", arg):
        return arg
    sys.exit(f"Not a YouTube URL or video id: {arg}")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    vid = video_id(sys.argv[1])
    languages = sys.argv[2:] or ["en", "es"]
    transcript = YouTubeTranscriptApi().fetch(vid, languages=languages)
    print(f"# video_id={vid} language={transcript.language_code} url=https://www.youtube.com/watch?v={vid}")
    for snippet in transcript:
        minutes, seconds = divmod(int(snippet.start), 60)
        print(f"[{minutes:02d}:{seconds:02d}] {snippet.text}")


if __name__ == "__main__":
    main()
