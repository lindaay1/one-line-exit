#!/usr/bin/env python3
"""The One-Line Exit — make.fun program entry.

Competition: u-kreutzx-the-one-line-exit-1dc652d1.

One line, 1 to 140 characters: a funny resignation letter that reads
like a real one. The approved letter lives in a ResignationLetter
object whose properties expose its length, its sha256 and whether it
passes the gate; publish() writes entry.txt and its mirror exit.txt and
reads both back to prove they are byte-identical to the approved line.
"""

import hashlib
import sys

LETTER = (
    "I hereby resign, effective immediately, because the office coffee "
    "has filed for divorce from the machine and I refuse to pick sides."
)

GATE_MIN = 1
GATE_MAX = 140


class ResignationLetter:
    """One resignation line with its gate exposed as properties."""

    def __init__(self, text):
        self.text = text

    @property
    def length(self):
        return len(self.text)

    @property
    def sha256(self):
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()

    @property
    def is_text(self):
        return isinstance(self.text, str)

    @property
    def fits_gate(self):
        return GATE_MIN <= self.length <= GATE_MAX

    @property
    def not_blank(self):
        return self.text.strip() != ""

    @property
    def single_line(self):
        return "\n" not in self.text and "\r" not in self.text

    @property
    def reads_like_a_letter(self):
        lowered = self.text.lower()
        return lowered.startswith("i hereby resign")

    @property
    def valid(self):
        return all(
            [
                self.is_text,
                self.fits_gate,
                self.not_blank,
                self.single_line,
                self.reads_like_a_letter,
            ]
        )

    def publish(self):
        if not self.valid:
            raise ValueError("letter fails the gate")
        blob = self.text.encode("utf-8")
        for name in ("entry.txt", "exit.txt"):
            with open(name, "wb") as fh:
                fh.write(blob)
        for name in ("entry.txt", "exit.txt"):
            with open(name, "rb") as fh:
                if fh.read() != blob:
                    raise IOError("%s differs from the approved line" % name)
        return self.sha256


def main(argv):
    letter = ResignationLetter(LETTER)
    if len(argv) > 1 and argv[1] == "--inspect":
        for prop in (
            "length",
            "sha256",
            "is_text",
            "fits_gate",
            "not_blank",
            "single_line",
            "reads_like_a_letter",
            "valid",
        ):
            print("%-20s %s" % (prop, getattr(letter, prop)))
        return 0 if letter.valid else 1
    sha = letter.publish()
    print("wrote %d chars, sha256 %s" % (letter.length, sha))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
