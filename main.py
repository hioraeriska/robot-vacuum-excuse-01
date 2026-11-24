"""The Robot Vacuum's Best Excuse — make.fun entry.

Writes one line to /output/entry.txt: the funniest excuse a robot
vacuum could offer for missing a spot, at most 140 characters.
Deterministic: the same line every run, no trailing newline.
"""

import os
import tempfile


LINE = "The dust bunny under your bed offered me a bribe. I accepted. We are friends now."


def resolve_output_dir() -> str:
    """Return the directory the entry must be written to."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR", "").strip()
    return out or "/output"


def main() -> None:
    # The gate accepts 1 to 140 characters; refuse to write anything
    # outside it rather than submitting an invalid entry.
    if not (1 <= len(LINE) <= 140):
        raise ValueError(f"entry is {len(LINE)} chars, must be 1-140")
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    # Atomic write: write to a temp file in the same directory, then
    # os.replace() it into place, so a crashed run never leaves a
    # half-written entry.txt behind.
    fd, tmp_path = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(LINE)
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


if __name__ == "__main__":
    main()
