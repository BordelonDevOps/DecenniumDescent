"""Split First Song extract into firstSongSections in cosmology-lore.json."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXTRACT = os.path.join(ROOT, "The_Cosmology_of_Decennium_Descent_EXTRACT.txt")
JSON_PATH = os.path.join(ROOT, "src", "data", "cosmology-lore.json")

NUM_MAP = {
    "1": "I",
    "I": "I",
    "One": "I",
    "II": "II",
    "2": "II",
    "Two": "II",
    "III": "III",
    "3": "III",
    "Three": "III",
    "IV": "IV",
    "4": "IV",
    "Four": "IV",
    "V": "V",
    "5": "V",
    "Five": "V",
    "VI": "VI",
    "6": "VI",
    "Six": "VI",
    "VII": "VII",
    "7": "VII",
    "Seven": "VII",
    "VIII": "VIII",
    "8": "VIII",
    "Eight": "VIII",
    "IX": "IX",
    "9": "IX",
    "Nine": "IX",
    "X": "X",
    "10": "X",
    "Ten": "X",
    "XI": "XI",
    "11": "XI",
    "Eleven": "XI",
    "XII": "XII",
    "12": "XII",
    "Twelve": "XII",
}

DRAFT_IDS = frozenset({"IX", "X", "XI", "XII"})


def chapter_id(header: str) -> str | None:
    m = re.search(
        r"Chapter\s+([IVXLC\d]+|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve)",
        header,
    )
    if not m:
        return None
    return NUM_MAP.get(m.group(1), m.group(1))


def main() -> None:
    with open(EXTRACT, encoding="utf-8") as f:
        text = f.read()

    pattern = re.compile(
        r"^(Chapter (?:[IVXLC\d]+|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten|Eleven|Twelve)[^\n]*)",
        re.MULTILINE,
    )
    matches = list(pattern.finditer(text))

    sections = []
    for i, m in enumerate(matches):
        header = m.group(1).strip()
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        cid = chapter_id(header)
        if not cid:
            continue
        sec: dict = {"id": cid, "title": header, "body": body}
        if cid in DRAFT_IDS:
            sec["draft"] = True
            sec["draftNote"] = (
                "Split from The_Cosmology_of_Decennium_Descent_EXTRACT.txt; "
                "author review pending."
            )
        sections.append(sec)

    with open(JSON_PATH, encoding="utf-8") as f:
        cos = json.load(f)

    cos["firstSongSections"] = sections
    cos["firstSongChapters"] = [s["title"] for s in sections]

    ch1 = next((s for s in sections if s["id"] == "I"), None)
    if ch1:
        excerpt = ch1["body"][:2400]
        cos["firstSong"] = ch1["title"] + "\n" + excerpt + (
            "…" if len(ch1["body"]) > 2400 else ""
        )

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(cos, f, indent=2, ensure_ascii=False)

    print(f"Wrote {len(sections)} firstSongSections to cosmology-lore.json")


if __name__ == "__main__":
    main()
