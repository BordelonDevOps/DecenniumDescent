"use client";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Printer, Download } from "lucide-react";
import { characterDisplayName } from "@/lib/character-storage";
import classDetails, { classPathBlocks, sortedClassLevels } from "@/data/class-details";
import { getOathById } from "@/data/paladin-oaths";
import { getHeroFormsForCircle, hasDraftHeroFormsForCircle, DRUID_CIRCLES } from "@/data/druid-shapeshifting";
import { getMysteryById } from "@/data/oracle-mysteries";
import { getCurseById, ORACLE_CURSE_BOON_LEVELS } from "@/data/oracle-curses";
import prestigePaths from "@/data/prestige";
import { getBackgroundByName } from "@/data/backgrounds";
import { getSpellDisplayName, getSpellByKey } from "@/data/spell-utils";
import featsData from "@/data/feats";
import ClassPathDisplay from "@/components/ClassPathDisplay";
import LevelFeatureList from "@/components/LevelFeatureList";
import ClassCeilingCapsCallout from "@/components/ClassCeilingCapsCallout";
import ChargenWarnings from "@/components/ChargenWarnings";
import PrestigeRequirements from "@/components/PrestigeRequirements";
import ReputationPanel from "@/components/ReputationPanel";
import { isSpellcasterClass } from "@/data/spell-utils";
import { computeSpellCost, multiclassRpBreakdown, resolveMaxRp } from "@/data/resonance-economy";
import { races } from "@/data/races";

type Ability = { name: string; score: number; modifier: number | string };
type Appearance = {
  body?: string;
  skin?: string;
  hair?: string;
  eyes?: string;
  accent?: string;
  gearTint?: string;
};

export type SheetCharacter = {
  id?: string;
  name?: string;
  race?: string;
  subrace?: string;
  class?: string;
  archClass?: string;
  background?: string;
  alignment?: string;
  level?: number;
  xp?: number;
  resonancePoints?: number;
  feats?: string[];
  abilities?: Ability[];
  knownSpells?: string[];
  preparedSpells?: string[];
  sacredOath?: string;
  druidCircle?: string;
  oracleMystery?: string;
  oracleCurse?: string;
  appearance?: Appearance;
  notes?: string;
  reputation?: Record<string, number>;
  secondaryClass?: string;
  secondaryLevel?: number;
};

function DraftBadge({ className }: { className?: string }) {
  return (
    <Badge
      variant="outline"
      className={`text-[9px] px-1.5 py-0 border-amber-500/50 text-amber-300/90 bg-amber-950/30 print:border-gray-400 print:text-gray-700 print:bg-transparent ${className ?? ""}`}
    >
      Draft
    </Badge>
  );
}

export default function CharacterSheet({
  character,
  onExport,
}: {
  character: SheetCharacter | null;
  onExport?: () => void;
}) {
  if (!character) {
    return (
      <Card className="bg-slate-900/70 border-amber-600/30">
        <CardContent className="py-10 text-center text-amber-100/50 text-sm">
          Save or load a character to open the sheet.
        </CardContent>
      </Card>
    );
  }

  const name = characterDisplayName(character);
  const detail = character.class
    ? classDetails[character.class as keyof typeof classDetails]
    : null;
  const prestige = prestigePaths.find((p) => p.name === character.archClass);
  const oath = character.sacredOath ? getOathById(character.sacredOath) : null;
  const druidCircleLabel = character.druidCircle
    ? DRUID_CIRCLES.find((c) => c.id === character.druidCircle)?.label
    : null;
  const oracleMystery = character.oracleMystery ? getMysteryById(character.oracleMystery) : null;
  const oracleCurse = character.oracleCurse ? getCurseById(character.oracleCurse) : null;
  const heroForms = character.druidCircle ? getHeroFormsForCircle(character.druidCircle) : null;
  const hasDraftHeroForms = character.druidCircle ? hasDraftHeroFormsForCircle(character.druidCircle) : false;
  const featureLevels = character.class ? sortedClassLevels(character.class) : [];
  const bg = character.background ? getBackgroundByName(character.background) : null;
  const selectedFeats = (character.feats || []).map((name) => ({
    name,
    draft: Boolean(featsData.find((feat) => feat.name === name)?.draft),
  }));
  const knownLabels = (character.knownSpells || []).map(getSpellDisplayName);
  const preparedLabels = (character.preparedSpells || []).map(getSpellDisplayName);
  const resonanceMax = resolveMaxRp(character.class || "", character.level || 1, character.reputation, character);
  const multiclassBreakdown = multiclassRpBreakdown(resonanceMax);
  const spellCostCtx = {
    className: character.class || "",
    alignment: character.alignment,
    reputation: character.reputation,
  };
  const preparedWithCost = (character.preparedSpells || []).map((key) => {
    const spell = getSpellByKey(key);
    const cost = spell ? computeSpellCost(spell, spellCostCtx) : null;
    const label = getSpellDisplayName(key);
    return cost != null && cost > 0 ? `${label} (${cost} RP)` : label;
  });
  const raceData = character.race
    ? races.find((r) => r.name === character.race || r.id === character.race)
    : null;
  const isUmbrin = character.race === "Umbrin" || raceData?.id === "umbrin";
  const umbrinBlurb = raceData?.info
    ? raceData.info.length > 220
      ? `${raceData.info.slice(0, 220)}…`
      : raceData.info
    : null;

  const printSheet = () => window.print();

  const identityTags: { key: string; label: string }[] = [];
  if (character.secondaryClass) {
    identityTags.push({
      key: "secondary",
      label: `${character.secondaryClass} L${character.secondaryLevel ?? 1}`,
    });
  }
  if (oath) identityTags.push({ key: "oath", label: `Oath: ${oath.name}` });
  if (druidCircleLabel) identityTags.push({ key: "circle", label: `Circle: ${druidCircleLabel}` });
  if (oracleMystery) {
    identityTags.push({ key: "mystery", label: `Mystery: ${oracleMystery.name}` });
  }
  if (oracleCurse) identityTags.push({ key: "curse", label: `Curse: ${oracleCurse.name}` });

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap gap-2 print:hidden">
        <Button onClick={printSheet} className="bg-amber-600 hover:bg-amber-500">
          <Printer className="w-4 h-4 mr-2" /> Print sheet
        </Button>
        {onExport && (
          <Button variant="outline" onClick={onExport}>
            <Download className="w-4 h-4 mr-2" /> Export JSON
          </Button>
        )}
      </div>

      <Card className="bg-slate-950 border-amber-600/40 print:border-black print:shadow-none" id="aethel-character-sheet">
        <CardHeader className="border-b border-amber-700/30">
          <div className="flex flex-wrap justify-between gap-3">
            <div>
              <CardTitle className="text-2xl text-amber-300 print:text-black">{name}</CardTitle>
              <p className="text-sm text-amber-100/70 print:text-gray-700 mt-1">
                Level {character.level || 1} {character.race}
                {character.subrace ? ` (${character.subrace})` : ""} ·{" "}
                {character.secondaryClass
                  ? `${character.class || "—"} L${character.level || 1} + ${character.secondaryClass} L${character.secondaryLevel ?? 1}`
                  : character.class || "—"}
                {character.archClass ? ` → ${character.archClass}` : ""}
              </p>
              {identityTags.length > 0 && (
                <p className="text-xs text-amber-100/60 print:text-gray-700 mt-1.5 flex flex-wrap gap-x-3 gap-y-0.5">
                  {identityTags.map((tag) => (
                    <span key={tag.key}>{tag.label}</span>
                  ))}
                </p>
              )}
            </div>
            <div className="flex flex-wrap gap-2">
              <Badge variant="outline" className={!character.alignment ? "text-amber-100/60 print:text-gray-600" : undefined}>
                {character.alignment || "Ethos not recorded"}
              </Badge>
              {character.background && <Badge className="bg-slate-700">{character.background}</Badge>}
              <Badge className="bg-purple-800" title={multiclassBreakdown?.summary}>
                RP {character.resonancePoints ?? 3}
                {resonanceMax.maxRp > 0 ? ` / ${resonanceMax.maxRp}${resonanceMax.draft ? " (draft)" : ""}` : ""}
              </Badge>
              <Badge variant="outline">XP {character.xp ?? 0}</Badge>
            </div>
          </div>
        </CardHeader>
        <CardContent className="pt-4 space-y-5 text-sm">
          <ChargenWarnings character={character} />
          {multiclassBreakdown && (
            <div className="border border-purple-700/40 rounded-lg p-3 bg-purple-950/20 text-xs text-amber-50/80 print:text-gray-800 print:border-gray-400 print:break-inside-avoid">
              <div className="flex items-center gap-1.5 mb-1">
                <span className="text-purple-300 font-medium print:text-black">Multiclass Resonance merge</span>
                <Badge variant="outline" className="text-[10px] border-purple-500/50 text-purple-200 print:text-black print:border-black">
                  Canon
                </Badge>
              </div>
              <ul className="list-disc pl-4 space-y-0.5">
                {multiclassBreakdown.lines.map((line) => (
                  <li key={line}>{line}</li>
                ))}
              </ul>
            </div>
          )}
          {character.secondaryClass && !multiclassBreakdown && (
            <div className="border border-amber-700/30 rounded-lg p-3 bg-black/20 text-xs text-amber-100/70 print:text-gray-800 print:border-gray-400 print:break-inside-avoid">
              <strong className="text-amber-200 print:text-black">
                Secondary class recorded: {character.secondaryClass} L{character.secondaryLevel ?? 1}.
              </strong>{" "}
              It does not add a second Weave pool; the listed RP maximum uses the eligible class pool only.
            </div>
          )}
          {isUmbrin && raceData && (
            <div className="umbrin-lore-card border border-violet-700/40 rounded-lg p-3 bg-violet-950/20 text-xs text-amber-50/80 print:text-gray-800 print:border-gray-400">
              <div className="umbrin-lore-title text-violet-300 font-medium print:text-black mb-1">Umbrin — The Murk</div>
              {umbrinBlurb && <p className="mb-1 print:text-gray-700">{umbrinBlurb}</p>}
              <p className="print:text-gray-700">
                <strong>Languages:</strong> {raceData.languages.join(", ")}
                {raceData.languages.includes("Murkish") && (
                  <span className="text-violet-200/70 print:text-gray-600">
                    {" "}
                    — Murkish is the under-tongue of exile politics and Murk cult rites.
                  </span>
                )}
              </p>
            </div>
          )}
          <div className="border border-amber-700/30 rounded-lg p-3 bg-black/20 text-xs text-amber-50/80 print:text-gray-800 print:border-gray-400">
            <h3 className="text-amber-300 font-semibold print:text-black mb-1">People & traits</h3>
            {raceData ? (
              <>
                <p>
                  <strong>{raceData.name}</strong>
                  {character.subrace ? ` · ${character.subrace}` : ""}
                </p>
                <p className="mt-1">
                  <strong>Traits:</strong> {raceData.traits.length ? raceData.traits.join(", ") : "None recorded"}
                </p>
              </>
            ) : (
              <p>
                {character.race
                  ? `${character.race} is recorded, but its sourced trait summary is unavailable.`
                  : "No people recorded — choose a people in Character Builder to show its sourced traits."}
              </p>
            )}
          </div>
          <div className="grid grid-cols-2 md:grid-cols-6 gap-2">
            {(character.abilities || []).map((a) => (
              <div key={a.name} className="border border-amber-700/30 rounded p-2 text-center print:border-gray-400">
                <div className="text-[10px] uppercase text-amber-200/70 print:text-gray-600">{a.name.slice(0, 3)}</div>
                <div className="text-xl font-bold text-white print:text-black">{a.score}</div>
                <div className="text-amber-300 print:text-gray-800">
                  {typeof a.modifier === "number" ? (a.modifier >= 0 ? `+${a.modifier}` : a.modifier) : a.modifier}
                </div>
              </div>
            ))}
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h3 className="text-amber-300 font-semibold print:text-black">Combat & tools</h3>
              <p className="text-amber-50/80 print:text-gray-800 text-xs">
                <strong>Armor:</strong> {(detail?.armor || []).join(", ") || "—"}
              </p>
              <p className="text-amber-50/80 print:text-gray-800 text-xs">
                <strong>Weapons:</strong> {(detail?.weapons || []).join(", ") || "—"}
              </p>
              <p className="text-amber-50/80 print:text-gray-800 text-xs">
                <strong>Skills:</strong> {(detail?.skills || []).join(", ") || "—"}
              </p>
              <ul className="list-disc pl-4 text-xs text-amber-50/80 print:text-gray-800">
                {(detail?.combat || []).map((c) => (
                  <li key={c}>{c}</li>
                ))}
              </ul>
            </div>
            <div className="space-y-2">
              <h3 className="text-amber-300 font-semibold print:text-black">
                Class features{featureLevels.length ? ` (${featureLevels[0]}–${featureLevels[featureLevels.length - 1]})` : ""}
              </h3>
              <LevelFeatureList
                levels={detail?.levels as Record<number, (string | { text: string; draft?: boolean; source?: string })[]> | undefined}
              />
              <ClassCeilingCapsCallout className={character.class} compact />
              <ClassPathDisplay
                archPaths={character.class ? classPathBlocks(character.class).archPaths : []}
                heroPaths={character.class ? classPathBlocks(character.class).heroPaths : []}
                showEmptyHeroPaths={Boolean(character.class)}
              />
              {prestige && (
                <div className="border border-orange-600/40 rounded p-2 mt-2 text-xs">
                  <div className="text-orange-300 font-medium print:text-black">{prestige.name}</div>
                  <p className="print:text-gray-800">{prestige.summary}</p>
                  <p className="mt-1 text-amber-100/60 print:text-gray-700">
                    Recorded path intent only — this selection does not grant prerequisites or features.
                  </p>
                  {prestige.hallmarks.length > 0 && (
                    <ul className="mt-1 list-disc pl-4 print:text-gray-700 space-y-0.5">
                      {prestige.hallmarks.map((h, index) => (
                        <li key={h}>
                          {prestige.draftHallmarkIndices.includes(index) && (
                            <DraftBadge className="mr-1 align-middle" />
                          )}
                          {h}
                        </li>
                      ))}
                    </ul>
                  )}
                  {prestige.capstone && (
                    <p className="mt-1 print:text-gray-700">
                      <strong>Capstone:</strong>{" "}
                      {prestige.draftCapstone && (
                        <DraftBadge className="mr-1 align-middle" />
                      )}
                      {prestige.capstone}
                    </p>
                  )}
                  <div className="mt-2">
                    <PrestigeRequirements
                      prestige={prestige}
                      selectedFeats={character.feats}
                      compact
                    />
                  </div>
                </div>
              )}
              {character.class === "Paladin" && !oath && (
                <div className="border border-red-600/40 rounded p-2 mt-2 text-xs text-red-300/90 print:text-gray-800 flex flex-wrap items-center gap-2">
                  <span>
                    No Sacred Oath recorded{(character.level ?? 1) >= 3 ? " (required at L3)" : " (chosen at L3)"}.
                  </span>
                  <DraftBadge />
                  <span className="text-amber-200/70 print:text-gray-600">Choose in Character Builder</span>
                </div>
              )}
              {character.class === "Druid" && !druidCircleLabel && (
                <div className="border border-red-600/40 rounded p-2 mt-2 text-xs text-red-300/90 print:text-gray-800">
                  Druid Circle not selected{(character.level ?? 1) >= 2 ? " (required at L2)" : " (chosen at L2)"}.
                </div>
              )}
              {character.class === "Oracle" && !oracleMystery && (
                <div className="border border-red-600/40 rounded p-2 mt-2 text-xs text-red-300/90 print:text-gray-800 flex flex-wrap items-center gap-2">
                  <span>No Oracle Mystery recorded (required at L1).</span>
                  <DraftBadge />
                  <span className="text-amber-200/70 print:text-gray-600">Choose in Character Builder</span>
                </div>
              )}
              {character.class === "Oracle" && !oracleCurse && (
                <div className="border border-red-600/40 rounded p-2 mt-2 text-xs text-red-300/90 print:text-gray-800 flex flex-wrap items-center gap-2">
                  <span>No Oracle&apos;s Curse recorded (required at L1).</span>
                  <DraftBadge />
                  <span className="text-amber-200/70 print:text-gray-600">Choose in Character Builder</span>
                </div>
              )}
              {oath && (
                <div className="border border-amber-600/40 rounded p-2 mt-2 text-xs">
                  <div className="text-amber-300 font-medium print:text-black flex flex-wrap items-center gap-2">
                    <span>{oath.name}</span>
                    {oath.draft && <DraftBadge />}
                  </div>
                  <p className="print:text-gray-800">{oath.theme}</p>
                  {(character.level ?? 1) >= 11 && (
                    <p className="mt-1 print:text-gray-700"><strong>Signature (L11):</strong> {oath.signaturePower}</p>
                  )}
                  {oath.revelationSpells
                    .filter((s) => (character.level ?? 1) >= s.level)
                    .map((s) => (
                      <p key={s.level} className="mt-1 print:text-gray-700">
                        <strong>L{s.level} Revelation:</strong> {s.spell}
                      </p>
                    ))}
                  {oath.finalOathGift && (character.level ?? 1) >= 20 && (
                    <p className="mt-1 print:text-gray-700 flex flex-wrap items-center gap-2">
                      <span>
                        <strong>Final Oath Gift (L20):</strong> {oath.finalOathGift}
                      </span>
                      {oath.finalOathGiftDraft && <DraftBadge />}
                    </p>
                  )}
                </div>
              )}
              {druidCircleLabel && (
                <div className="border border-green-600/40 rounded p-2 mt-2 text-xs">
                  <div className="text-green-300 font-medium print:text-black flex flex-wrap items-center gap-2">
                    <span>{druidCircleLabel}</span>
                    {hasDraftHeroForms && <DraftBadge />}
                  </div>
                  {(character.level ?? 1) >= 10 && heroForms && (
                    <p className="mt-1 print:text-gray-700">
                      <strong>Hero forms:</strong>{" "}
                      {heroForms.forms.map((f: { name: string; draft?: boolean }) => `${f.name}${f.draft ? " (draft)" : ""}`).join(", ")}
                    </p>
                  )}
                </div>
              )}
              {oracleMystery && (
                <div className="border border-violet-600/40 rounded p-2 mt-2 text-xs">
                  <div className="text-violet-300 font-medium print:text-black flex flex-wrap items-center gap-2">
                    <span>Mystery of {oracleMystery.name}</span>
                    {oracleMystery.draft && <DraftBadge />}
                  </div>
                  <p className="print:text-gray-800">{oracleMystery.theme}</p>
                  {oracleMystery.patron && (
                    <p className="mt-1 print:text-gray-700"><strong>Patron:</strong> {oracleMystery.patron}</p>
                  )}
                  {oracleMystery.prophecyTrigger && (
                    <p className="mt-1 print:text-gray-700"><strong>Prophecy trigger:</strong> {oracleMystery.prophecyTrigger}</p>
                  )}
                  {oracleMystery.level1 && (character.level ?? 1) >= 1 && (
                    <p className="mt-1 print:text-gray-700"><strong>L1:</strong> {oracleMystery.level1.name}</p>
                  )}
                  {oracleMystery.tierIII && (character.level ?? 1) >= 9 && (
                    <p className="mt-1 print:text-gray-700">
                      <strong>Tier III:</strong> {oracleMystery.tierIII.name}
                    </p>
                  )}
                  {oracleMystery.finalRevelation && (character.level ?? 1) >= 20 && (
                    <p className="mt-1 print:text-gray-700">
                      <strong>Final Revelation:</strong> {oracleMystery.finalRevelation.name}
                    </p>
                  )}
                </div>
              )}
              {oracleCurse && (
                <div className="border border-violet-600/40 rounded p-2 mt-2 text-xs">
                  <div className="text-violet-300 font-medium print:text-black flex flex-wrap items-center gap-2">
                    <span>Curse — {oracleCurse.name}</span>
                    {oracleCurse.draft && <DraftBadge />}
                  </div>
                  <p className="print:text-gray-800">{oracleCurse.blurb}</p>
                  {ORACLE_CURSE_BOON_LEVELS.filter((lvl) => (character.level ?? 1) >= lvl).map((lvl) => {
                    const boon = oracleCurse.boons.find((b) => b.level === lvl);
                    if (!boon) return null;
                    return (
                      <p key={lvl} className="mt-1 print:text-gray-700">
                        <strong>L{lvl} Boon:</strong> {boon.description}
                      </p>
                    );
                  })}
                </div>
              )}
            </div>
          </div>

          <div className="grid md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <h3 className="text-amber-300 font-semibold print:text-black">Background</h3>
              {bg ? (
                <div className="text-xs text-amber-50/80 print:text-gray-800 space-y-1 border border-amber-700/30 rounded p-2">
                  <p className="font-medium text-amber-200 print:text-black">{bg.name}</p>
                  <p>{bg.description}</p>
                  <p><strong>Skills:</strong> {bg.skillProficiencies.join(", ")}</p>
                  {bg.toolProficiencies.length > 0 && (
                    <p><strong>Tools:</strong> {bg.toolProficiencies.join(", ")}</p>
                  )}
                  <p><strong>{bg.feature}:</strong> {bg.featureDescription}</p>
                </div>
              ) : (
                <p className="text-xs text-amber-50/80 print:text-gray-800">{character.background || "None selected"}</p>
              )}
            </div>
            <div className="space-y-2">
              <h3 className="text-amber-300 font-semibold print:text-black">Feats</h3>
              {selectedFeats.length ? (
                <div className="flex flex-wrap gap-x-2 gap-y-1 text-xs text-amber-50/80 print:text-gray-800">
                  {selectedFeats.map((feat) => (
                    <span key={feat.name} className="inline-flex items-center gap-1">
                      {feat.name}
                      {feat.draft && <DraftBadge />}
                    </span>
                  ))}
                </div>
              ) : (
                <p className="text-xs text-amber-50/80 print:text-gray-800">None selected</p>
              )}
            </div>
          </div>

          <div className="space-y-2">
            <h3 className="text-amber-300 font-semibold print:text-black">Reputation</h3>
            {bg?.startingReputation && (
              <p className="text-[10px] text-amber-200/50 print:text-gray-600">
                Background start: {bg.startingReputation}
              </p>
            )}
            <ReputationPanel
              scores={character.reputation || {}}
              onChange={() => {}}
              mode="compact"
              readOnly
            />
          </div>

          <div>
            <h3 className="text-amber-300 font-semibold print:text-black mb-1">Spells & revelations</h3>
            {character.class === "Oracle" ? (
              <p className="text-xs text-violet-200/80 print:text-gray-800">
                Revelation Caster — see Mystery and Oracle&apos;s Curse above. Oracles do not use Weave known/prepared lists.
              </p>
            ) : (
              <>
                <p className="text-xs text-amber-50/80 print:text-gray-800">
                  <strong>Known ({knownLabels.length}):</strong> {knownLabels.length ? knownLabels.join(", ") : "—"}
                </p>
                <p className="text-xs text-amber-50/80 print:text-gray-800 mt-1">
                  <strong>Prepared ({preparedLabels.length}):</strong>{" "}
                  {preparedWithCost.length ? preparedWithCost.join(", ") : "—"}
                </p>
                {character.class && !isSpellcasterClass(character.class) && knownLabels.length === 0 && (
                  <p className="text-xs text-amber-200/50 mt-1 print:text-gray-600">
                    {character.class} is not a primary Weave caster — spell lists optional.
                  </p>
                )}
              </>
            )}
          </div>

          {character.appearance && (
            <div className="text-xs text-amber-100/60 print:text-gray-600">
              Look: {character.appearance.body || "Athletic"} frame · resonance accent {character.appearance.accent || "—"}
            </div>
          )}
          {character.notes && (
            <div>
              <h3 className="text-amber-300 font-semibold print:text-black mb-1">Notes</h3>
              <p className="text-xs whitespace-pre-wrap text-amber-50/80 print:text-gray-800">{character.notes}</p>
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
