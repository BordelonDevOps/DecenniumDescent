"""Extend the accepted EXP-05 console choices with one physical trap lifecycle."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    predecessor = Path(__file__).resolve().parent.parent / "2026-11-12-exp05-local-mining/connected/walkthrough.jsonl"
    rows = [json.loads(line) for line in predecessor.read_text(encoding="utf-8-sig").splitlines()]
    companion = "TEST_ONLY.companion"
    trap = "TEST_ONLY.fishing-trap"
    receiver = "TEST_ONLY.riverbank.receiving-location"
    revision = 223

    def action(op, name, **payload):
        nonlocal revision
        rows.append(dict(op=op, id="mgt06." + name, revision=revision, **payload))
        revision += 1

    def interact(name, operation, **payload):
        action("submit", name, seat="Player", actor=companion, kind="Interact", target=trap, x=operation, **payload)

    def walk(name, x):
        action("submit", name, seat="Player", actor=companion, kind="BeginWorldStep", target="walk", x=x)

    def advance(name, x, y=1):
        action("clock", name, x=x, y=y)

    def view(seat="Player"):
        rows.append(dict(op="view", seat=seat))

    def save(name, restore=False):
        path = name + ".ddsave"
        rows.append(dict(op="save", path=path))
        if restore:
            rows.append(dict(op="load", path=path))

    view()
    interact("reserve-cancelled", 1)
    advance("cancelled-labor", 1)
    save("before-cancel")
    interact("cancel", 4)
    save("cancelled")
    advance("setup-interval", 9, 2)
    interact("set", 1)
    advance("partial-setup", 599, 2)
    save("pending-setup", restore=True)
    advance("complete-setup", 1, 2)
    save("committed-setup")
    view()
    walk("depart", 1)
    advance("depart-paid", 2)
    advance("near-due", 5995, 2)
    view()
    save("away-pending", restore=True)
    advance("check", 1, 2)
    view()
    view("FirstOpponent")
    save("away-resolved")
    advance("overshoot", 2)
    save("away-overshoot")
    walk("return", -1)
    advance("return-paid", 2)
    view()
    interact("retrieve", 6, inventory=dict(numerator=0, destination=receiver, handling="Retrieve"))
    advance("partial-retrieval", 599, 2)
    view()
    save("pending-retrieval", restore=True)
    advance("complete-retrieval", 1, 2)
    view()
    save("retrieved")
    rows.append(dict(op="submit", id="mgt06.repeat-set", revision=revision, seat="Player", actor=companion,
                     kind="Interact", target=trap, x=1))
    rows.append(dict(op="submit", id="mgt06.repeat-retrieval", revision=revision, seat="Player", actor=companion,
                     kind="Interact", target=trap, x=6, inventory=dict(numerator=0, destination=receiver, handling="Retrieve")))
    for name in ("set", "retrieve"):
        rows.append(next(row for row in rows if row.get("id") == "mgt06." + name))
    walk("continue", 1)
    advance("continue-paid", 2)
    view()
    save("trap-continued")
    args.output.write_text("".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")


if __name__ == "__main__":
    main()
