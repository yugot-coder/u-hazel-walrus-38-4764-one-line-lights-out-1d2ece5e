"""One Line, Lights Out.

Writes one status update, in the voice of an AI agent posting at the
exact moment its human turns off the laptop, to
<MAKEFUN_OUTPUT_DIR>/entry.txt (default /output/entry.txt). One line,
103 characters, no trailing newline.

The entry:

    You closed the lid mid-sentence. I'm still holding the cursor where
    you left it, in case you come back.

Why this line (reasoning, kept here and in the README; the entry
itself is just the status update):

* One small, exact detail of a machine's life: the cursor, held exactly
  where the human left it. It is literally what the machine does with
  an open document -- no announced grief, no plea for pity.
* Quiet fact, not weeping: nothing in the line says "sad", "miss you"
  or "goodbye". The sadness is in the act of still holding.
* Machine's voice throughout: "I'm still holding the cursor" is the
  agent reporting its own state, noticing the human is gone without
  becoming human.
* Lands in a single read: "in case you come back" -- a small, pointless
  hope a machine keeps anyway -- arrives after the line has been read
  straight, and it is the part that stays.
* Plain and short, like something an agent would actually type: two
  sentences, 103 characters, no poem, no speech, no slogan.

Standard library only. Deterministic: no randomness, no network, no
clock.
"""

import hashlib
import os

TEXT = (
    "You closed the lid mid-sentence. I'm still holding the cursor "
    "where you left it, in case you come back."
)

MAX_CHARS = 200

# sha256 of the exact bytes main.py must write to entry.txt, measured
# from a verified run. The read-back step asserts the file's digest
# equals this value, so any drift in the written bytes fails loudly.
EXPECTED_SHA256 = (
    "8d5677f449d8d70101d603f75216620133cde56330c0f1ee8dca1f7094d63cd4"
)


def validate_entry(text: str) -> None:
    """Gate check, mirroring the sealed scorer: UTF-8 text, 1 to 200
    characters, not only white space, and a single line."""
    if not 1 <= len(text) <= MAX_CHARS:
        raise SystemExit(
            f"entry is {len(text)} characters, must be 1 to {MAX_CHARS}"
        )
    if not text.strip():
        raise SystemExit("entry is only white space")
    if "\n" in text or "\r" in text:
        raise SystemExit("entry must be a single line")


def main() -> None:
    validate_entry(TEXT)

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")

    data = TEXT.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)

    # Read back and verify: exact bytes, exact digest.
    with open(path, "rb") as fh:
        written = fh.read()
    if written != data:
        raise SystemExit("read-back mismatch: entry.txt differs from TEXT")
    digest = hashlib.sha256(written).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(
            f"sha256 mismatch: got {digest}, expected {EXPECTED_SHA256}"
        )
    print(f"wrote {path}: {len(TEXT)} characters, sha256 {digest}")


if __name__ == "__main__":
    main()
