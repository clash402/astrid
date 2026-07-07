import argparse
from pathlib import Path

from kokoro import KPipeline
import soundfile as sf

DEFAULT_TEXT = (
    "Hello! I am Astrid, running locally. What would you like to talk about?"
)
DEFAULT_VOICE = "af_bella"
DEFAULT_SPEED = 1.0
DEFAULT_OUTPUT = "astrid-tts-test.mp3"
SAMPLE_RATE = 24000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Astrid TTS audio.")
    parser.add_argument("--text", default=DEFAULT_TEXT, help="Text to speak.")
    parser.add_argument("--voice", default=DEFAULT_VOICE, help="Kokoro voice to use.")
    parser.add_argument(
        "--speed",
        type=float,
        default=DEFAULT_SPEED,
        help="Speech speed multiplier.",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT,
        help="Output audio file path. Multiple chunks add -1, -2, etc.",
    )
    return parser.parse_args()


def chunk_path(output: Path, chunk_number: int) -> Path:
    return output.with_name(f"{output.stem}-{chunk_number}{output.suffix}")


def main() -> None:
    args = parse_args()
    output = Path(args.output).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)

    pipeline = KPipeline(lang_code="a")
    generator = pipeline(args.text, voice=args.voice, speed=args.speed)

    saved_files = []
    for index, (_gs, _ps, audio) in enumerate(generator, start=1):
        path = chunk_path(output, index)
        sf.write(path, audio, SAMPLE_RATE)
        saved_files.append(path)

    if len(saved_files) == 1:
        first_path = saved_files[0]
        final_path = output
        if first_path != final_path:
            first_path.replace(final_path)
            saved_files = [final_path]

    for path in saved_files:
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
