import prestigePaths from "@/data/prestige";
import { missingPrestigeFeats } from "@/lib/prestige-utils";

export type ChargenWarning = {
  id: string;
  message: string;
  severity: "required" | "advisory";
};

export type ChargenSnapshot = {
  class?: string;
  level?: number;
  oracleMystery?: string;
  oracleCurse?: string;
  sacredOath?: string;
  druidCircle?: string;
  archClass?: string;
  heroPath?: string;
  feats?: string[];
};

/** Surfaces missing required subclass picks and prestige feat gaps for playtest review. */
export function getChargenWarnings(char: ChargenSnapshot): ChargenWarning[] {
  const warnings: ChargenWarning[] = [];
  const level = char.level ?? 1;
  const cls = char.class || "";

  if (!cls) {
    warnings.push({ id: "class", message: "Choose a base class from the 17-class canon roster.", severity: "required" });
    return warnings;
  }

  if (cls === "Oracle") {
    if (!char.oracleMystery) {
      warnings.push({
        id: "oracle-mystery",
        message: "Oracle requires a Mystery at level 1 (Revelation Caster path).",
        severity: "required",
      });
    }
    if (!char.oracleCurse) {
      warnings.push({
        id: "oracle-curse",
        message: "Oracle requires an Oracle's Curse at level 1.",
        severity: "required",
      });
    }
  }

  if (cls === "Paladin") {
    if (level >= 3 && !char.sacredOath) {
      warnings.push({
        id: "paladin-oath",
        message: "Paladin requires a Sacred Oath at level 3.",
        severity: "required",
      });
    } else if (level < 3 && !char.sacredOath) {
      warnings.push({
        id: "paladin-oath-soon",
        message: "Sacred Oath is chosen at level 3 — pick before L3 playtest scenes.",
        severity: "advisory",
      });
    }
  }

  if (cls === "Druid") {
    if (level >= 2 && !char.druidCircle) {
      warnings.push({
        id: "druid-circle",
        message: "Druid requires a Circle at level 2 (Shapeshifting).",
        severity: "required",
      });
    } else if (level < 2 && !char.druidCircle) {
      warnings.push({
        id: "druid-circle-soon",
        message: "Druid Circle is chosen at level 2 — pick before Shapeshifting unlocks.",
        severity: "advisory",
      });
    }
  }

  if (level >= 10 && !char.heroPath) {
    warnings.push({
      id: "hero-path",
      message: "Choose a Hero Path at level 10; it defines the class's late-game philosophy and mechanics.",
      severity: "required",
    });
  }

  if (char.archClass) {
    const prestige = prestigePaths.find((p) => p.name === char.archClass);
    if (prestige) {
      if (level < 10) {
        warnings.push({
          id: "prestige-level",
          message: `${char.archClass} prestige paths normally unlock at level 10+.`,
          severity: "advisory",
        });
      }
      const missing = missingPrestigeFeats(prestige.requirements, char.feats);
      if (missing.length) {
        warnings.push({
          id: `prestige-feats-${char.archClass}`,
          message: `Prestige feat prerequisites not on sheet: ${missing.join(", ")}`,
          severity: "advisory",
        });
      }
    }
  }

  return warnings;
}

export function hasRequiredChargenGaps(char: ChargenSnapshot): boolean {
  return getChargenWarnings(char).some((w) => w.severity === "required");
}
