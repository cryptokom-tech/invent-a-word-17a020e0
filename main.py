#!/usr/bin/env python3
"""invent-a-word-17a020e0 entry: write the coined word to the output.

The coinage is "corridance": the mirrored sidestep dance of two people
trying to pass each other in a hallway. English has no word for that
small daily moment — two strangers stepping left, then right, then left
again, in perfect unwanted unison — so the word fills a real gap: it is
sayable, spellable, memorable, and built from parts English already owns
(corridor + dance, with the -ance ending of words like concordance).

This program only writes the bundled text to the output path, verifying
it first: UTF-8, 1 to 140 characters, not only white space. The text
lives in entry.txt next to this program — a single source of truth — and
the program reads it, checks it, and copies it to the output. Standard
library only, no network, and every run writes the exact same bytes.
"""

import os
import sys

MAX_CHARS = 140


def read_bundle():
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "entry.txt")
    with open(path, "r", encoding="utf-8") as fh:
        return fh.read()


def check_coinage(text):
    """The entry must be one coined word plus its one-line definition.

    Format is "word — definition": a single-token word, an em-dash
    separator, and a definition that fits on the same line. A text
    without that shape is not a coinage entry, so refuse it here
    rather than letting the gate refuse it on the server.
    """
    if "\n" in text.strip():
        raise SystemExit("entry must be a single line")
    if " — " not in text:
        raise SystemExit("entry must be shaped 'word — definition'")
    word = text.split(" — ", 1)[0].strip()
    if not word or len(word.split()) != 1:
        raise SystemExit("coined word must be a single token")
    if not text.split(" — ", 1)[1].strip():
        raise SystemExit("definition must not be empty")


def main(argv):
    out = argv[1] if len(argv) > 1 else "/output/entry.txt"
    text = read_bundle()
    chars = len(text)
    if not 1 <= chars <= MAX_CHARS:
        raise SystemExit(f"entry is {chars} characters, must be 1-{MAX_CHARS}")
    if not text.strip():
        raise SystemExit("entry is only white space")
    check_coinage(text)
    directory = os.path.dirname(out)
    if directory:
        os.makedirs(directory, exist_ok=True)
    with open(out, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)
    with open(out, "r", encoding="utf-8") as fh:
        written = fh.read()
    if written != text:
        raise SystemExit("verification failed: written text differs")
    print(f"wrote {len(written)} characters to {out}")


if __name__ == "__main__":
    main(sys.argv)
