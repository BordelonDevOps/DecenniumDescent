from pathlib import Path

p = Path(r"C:\Github\Descent assets\DecenniumDescent-main\src\components\CharacterBuilder.tsx")
text = p.read_text(encoding="utf-8")

if 'from "@/data/feats"' not in text:
    text = text.replace(
        'from "@/data/spells";',
        'from "@/data/spells";\nimport featsData from "@/data/feats";',
    )

start = text.index("  const feats = [")
end = text.index("const classes = [")
replacement = "const feats = featsData;\n\n"
text = text[:start] + replacement + text[end:]

# Improve applyRacialBonuses for Human / OR cases
old_asi = '''  const applyRacialBonuses = (abilities: typeof defaultAbilities, race: (typeof races)[number] | null | undefined) => {
    if (!race || !race.abilityScoreIncrease) return abilities;
    
    const bonuses = race.abilityScoreIncrease.split(', ');
    const updatedAbilities = [...abilities];
    
    bonuses.forEach((bonus: string) => {
      const [abilityName, modifier] = bonus.split(' ');
      const abilityIndex = updatedAbilities.findIndex(a => a.name === abilityName);
      if (abilityIndex !== -1) {
        const bonusValue = parseInt(modifier.replace('+', ''));
        updatedAbilities[abilityIndex] = {
          ...updatedAbilities[abilityIndex],
          score: updatedAbilities[abilityIndex].score + bonusValue
        };
      }
    });
    
    return updateAbilityModifiers(updatedAbilities);
  };'''

new_asi = '''  const applyRacialBonuses = (abilities: typeof defaultAbilities, race: (typeof races)[number] | null | undefined) => {
    if (!race || !race.abilityScoreIncrease) return abilities;

    const asi = race.abilityScoreIncrease;
    const updatedAbilities = abilities.map((a) => ({ ...a }));

    // Human (and similar): all scores +1
    if (/All ability scores \\+1/i.test(asi)) {
      return updateAbilityModifiers(
        updatedAbilities.map((a) => ({ ...a, score: a.score + 1 }))
      );
    }

    // Skip ambiguous OR choices — leave scores unchanged until player picks
    if (/\\bOR\\b/i.test(asi)) {
      return updateAbilityModifiers(updatedAbilities);
    }

    for (const part of asi.split(/,/)) {
      const m = part.trim().match(/([A-Za-z]+)\\s*\\+(\\d+)/);
      if (!m) continue;
      const abilityIndex = updatedAbilities.findIndex((a) => a.name === m[1]);
      if (abilityIndex === -1) continue;
      updatedAbilities[abilityIndex] = {
        ...updatedAbilities[abilityIndex],
        score: updatedAbilities[abilityIndex].score + Number(m[2]),
      };
    }

    return updateAbilityModifiers(updatedAbilities);
  };'''

if old_asi in text:
    text = text.replace(old_asi, new_asi)
    print("ASI helper updated")
else:
    print("ASI helper pattern not found — skipping")

# Wire action buttons
old_buttons = '''        <div className="flex gap-2">
          <Button className="amber-button">
            <Dice1 className="w-4 h-4 mr-2" />
            RANDOM
          </Button>
          <Button className="amber-button">
            <Plus className="w-4 h-4 mr-2" />
            NEW
          </Button>
          <Button className="amber-button">
            <Copy className="w-4 h-4 mr-2" />
            CLONE
          </Button>
          <Button className="amber-button">
            <Save className="w-4 h-4 mr-2" />
            SAVE NEW CHARACTER
          </Button>
          <Button className="amber-button">
            <Download className="w-4 h-4 mr-2" />
            EXPORT
          </Button>
        </div>'''

# Insert helper functions before return in component — find unique marker
marker = "  return (\n    <div className=\"min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-gray-900 p-6\">"
helpers = '''
  const buildCharacterPayload = () => ({
    name: selectedRace ? `${selectedRace} ${selectedClass || "Adventurer"}` : "Unnamed Adventurer",
    race: selectedRace,
    subrace: selectedSubrace,
    class: selectedClass,
    background: selectedBackground,
    feats: selectedFeats,
    level: currentLevel,
    xp: currentXP,
    alignment: selectedAlignment,
    abilities: abilities.map((a) => ({ name: a.name, score: a.score, modifier: a.modifier })),
    knownSpells,
    preparedSpells,
    exportedAt: new Date().toISOString(),
  });

  const exportCharacter = () => {
    const payload = buildCharacterPayload();
    const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${payload.name.replace(/\\s+/g, "_").toLowerCase() || "character"}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const saveCharacter = () => {
    const payload = buildCharacterPayload();
    const key = "dd_characters";
    const existing = JSON.parse(localStorage.getItem(key) || "[]");
    existing.push(payload);
    localStorage.setItem(key, JSON.stringify(existing));
    alert(`Saved locally (${existing.length} character(s) in this browser).`);
  };

  const resetCharacter = () => {
    setSelectedRace("");
    setSelectedSubrace("");
    setSelectedClass("");
    setSelectedBackground("");
    setSelectedFeats([]);
    setCurrentLevel(1);
    setCurrentXP(0);
    setSelectedAlignment("");
    setAbilities(defaultAbilities);
    setKnownSpells([]);
    setPreparedSpells([]);
  };

  const randomCharacter = () => {
    const race = races[Math.floor(Math.random() * races.length)];
    const cls = classes[Math.floor(Math.random() * classes.length)];
    setSelectedRace(race.name);
    setSelectedSubrace(race.subraces?.[0] || "");
    setSelectedClass(cls.name);
    const featPool = feats.slice(0, Math.min(40, feats.length));
    const pick = featPool[Math.floor(Math.random() * featPool.length)];
    setSelectedFeats(pick ? [pick.name] : []);
  };

'''

if marker in text and "buildCharacterPayload" not in text:
    text = text.replace(marker, helpers + marker)
    print("helpers inserted")

new_buttons = '''        <div className="flex gap-2 flex-wrap">
          <Button className="amber-button" onClick={randomCharacter}>
            <Dice1 className="w-4 h-4 mr-2" />
            RANDOM
          </Button>
          <Button className="amber-button" onClick={resetCharacter}>
            <Plus className="w-4 h-4 mr-2" />
            NEW
          </Button>
          <Button className="amber-button" onClick={() => { navigator.clipboard.writeText(JSON.stringify(buildCharacterPayload(), null, 2)); alert("Character JSON copied."); }}>
            <Copy className="w-4 h-4 mr-2" />
            CLONE
          </Button>
          <Button className="amber-button" onClick={saveCharacter}>
            <Save className="w-4 h-4 mr-2" />
            SAVE NEW CHARACTER
          </Button>
          <Button className="amber-button" onClick={exportCharacter}>
            <Download className="w-4 h-4 mr-2" />
            EXPORT
          </Button>
        </div>'''

if old_buttons in text:
    text = text.replace(old_buttons, new_buttons)
    print("buttons wired")
else:
    print("buttons block not found")

p.write_text(text, encoding="utf-8")
print("done")
