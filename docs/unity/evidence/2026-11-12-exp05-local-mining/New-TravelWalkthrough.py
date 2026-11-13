"""Insert a paid finite-site approach and revisit into the accepted public input history."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    prior = Path(__file__).resolve().parent.parent / "2026-11-12-exp04-public-observation/connected/walkthrough.jsonl"
    inputs = [json.loads(line) for line in prior.read_text(encoding="utf-8-sig").splitlines()]
    companion = "TEST_ONLY.companion"
    mining_index = next(i for i, row in enumerate(inputs) if row.get("kind") == "StartMining")
    rows = inputs[:mining_index]
    revision = 15

    def command(op, name, **payload):
        nonlocal revision
        rows.append(dict(op=op, id="exp05." + name, revision=revision, **payload))
        revision += 1

    def step(name, x, y):
        command("submit", name, seat="Player", actor=companion, kind="BeginWorldStep", target="walk", x=x, y=y)

    def advance(name, x, y=1):
        command("clock", name, x=x, y=y)

    def view(seat="Player"):
        rows.append(dict(op="view", seat=seat))

    def save(name):
        rows.append(dict(op="save", path=name))

    step("depart", 1, 0)
    advance("depart-paid", 2)
    step("beyond-reach", 0, 1)
    advance("beyond-reach-paid", 2)
    view()
    step("return-near", 0, -1)
    advance("return-near-paid", 2)
    step("approach", -1, 0)
    advance("fraction", 1, 2)
    view()
    view("FirstOpponent")
    save("partial-edge.ddsave")
    rows.append(dict(op="load", path="partial-edge.ddsave"))
    view()
    advance("arrival", 2)
    save("arrived.ddsave")
    shift = revision - 15

    # Later command targets whose identifiers are derived from the committed revision.
    dynamic = ("charter.attempt", "formula", "manufacture.order", "exploration.hide", "exploration.search")

    def adjust_target(target):
        if target in ("inventory.31.intake", "inventory.35.lot"):
            fields = target.split(".")
            fields[1] = str(int(fields[1]) + shift)
            return ".".join(fields)
        for prefix in dynamic:
            if target.startswith(prefix + "."):
                rest = target[len(prefix) + 1:].split(".")
                rest[0] = str(int(rest[0]) + shift)
                return prefix + "." + ".".join(rest)
        if target.startswith("world.fixed-calendar.start."):
            return target.rsplit(".", 1)[0] + "." + str(int(target.rsplit(".", 1)[1]) + 8)
        if target.startswith("world.fixed-calendar.activity."):
            return target.rsplit(".", 1)[0] + "." + str(int(target.rsplit(".", 1)[1]) + 4)
        return target

    for row in inputs[mining_index:]:
        if "revision" in row:
            row["revision"] += shift
        if "target" in row:
            row["target"] = adjust_target(row["target"])
        # Pay the missing active labor and advance through the next companion
        # interval refresh before handling the vessel.
        if row.get("id") == "i-96":
            row["x"] = 26789
            row["y"] = 2
        rows.append(row)

    revision = 208 + shift
    # The companion ends the prior route at (3,2), next to the already-known deposit.
    step("revisit-depart", 1, 0)
    advance("revisit-depart-paid", 6)
    view()
    save("away-from-site.ddsave")
    rows.append(dict(op="load", path="away-from-site.ddsave"))
    step("revisit-return", -1, 0)
    advance("revisit-return-paid", 6)
    view()
    rejected = dict(inputs[mining_index], id="exp05.repeat-mining", revision=revision)
    rows.append(rejected)
    step("continue", 0, 1)
    advance("continue-paid", 6)
    view()
    save("travel-continued.ddsave")

    args.output.write_text("".join(json.dumps(row, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")


if __name__ == "__main__":
    main()
