from pathlib import Path

p = Path(r"C:\Github\Descent assets\DecenniumDescent-main\src\components\CharacterBuilder.tsx")
text = p.read_text(encoding="utf-8")

# imports
if "character-storage" not in text:
    text = text.replace(
        'import classDetails from "@/data/class-details";',
        '''import classDetails from "@/data/class-details";
import CharacterSheet from "@/components/CharacterSheet";
import {
  loadSavedCharacters,
  upsertCharacter,
  deleteCharacter,
  characterDisplayName,
} from "@/lib/character-storage";''',
    )

# state after selectedBackground
if "characterName" not in text:
    text = text.replace(
        'const [selectedBackground, setSelectedBackground] = useState<string>("");',
        '''const [selectedBackground, setSelectedBackground] = useState<string>("");
  const [characterName, setCharacterName] = useState<string>("");
  const [characterId, setCharacterId] = useState<string>("");
  const [characterNotes, setCharacterNotes] = useState<string>("");
  const [builderView, setBuilderView] = useState<"build" | "sheet">("build");
  const [savedCharacters, setSavedCharacters] = useState<ReturnType<typeof loadSavedCharacters>>([]);''',
    )

# refresh saved list on mount
if "setSavedCharacters(loadSavedCharacters())" not in text:
    text = text.replace(
        "  // Apply racial bonuses when race changes\n  useEffect(() => {",
        '''  useEffect(() => {
    setSavedCharacters(loadSavedCharacters());
  }, []);

  // Apply racial bonuses when race changes
  useEffect(() => {''',
    )

# payload
text = text.replace(
    """  const buildCharacterPayload = () => ({
    name: selectedRace ? `${selectedRace} ${selectedClass || "Adventurer"}` : "Unnamed Adventurer",
    race: selectedRace,
    subrace: selectedSubrace,
    class: selectedClass,
    archClass: selectedArchClass,
    resonancePoints,
    appearance,
    background: selectedBackground,
    feats: selectedFeats,
    level: currentLevel,
    xp: currentXP,
    alignment: selectedAlignment,
    abilities: abilities.map((a) => ({ name: a.name, score: a.score, modifier: a.modifier })),
    knownSpells,
    preparedSpells,
    exportedAt: new Date().toISOString(),
  });""",
    """  const buildCharacterPayload = () => ({
    id: characterId || undefined,
    name: characterName.trim() || (selectedRace ? `${selectedRace} ${selectedClass || "Adventurer"}` : "Unnamed Adventurer"),
    race: selectedRace,
    subrace: selectedSubrace,
    class: selectedClass,
    archClass: selectedArchClass,
    resonancePoints,
    appearance,
    background: selectedBackground,
    feats: selectedFeats,
    level: currentLevel,
    xp: currentXP,
    alignment: selectedAlignment,
    abilities: abilities.map((a) => ({ name: a.name, score: a.score, modifier: a.modifier })),
    knownSpells,
    preparedSpells,
    notes: characterNotes,
    exportedAt: new Date().toISOString(),
  });""",
)

# save / load / reset
text = text.replace(
    """  const saveCharacter = () => {
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
    setSelectedArchClass("");
    setResonancePoints(3);
    setSelectedBackground("");
    setSelectedFeats([]);
    setCurrentLevel(1);
    setCurrentXP(0);
    setSelectedAlignment("");
    setAbilities(defaultAbilities);
    setKnownSpells([]);
    setPreparedSpells([]);
  };""",
    """  const saveCharacter = () => {
    const saved = upsertCharacter(buildCharacterPayload());
    setCharacterId(saved.id);
    setCharacterName(saved.name || "");
    setSavedCharacters(loadSavedCharacters());
    setBuilderView("sheet");
  };

  const loadCharacter = (c: ReturnType<typeof loadSavedCharacters>[number]) => {
    setCharacterId(c.id || "");
    setCharacterName(c.name || "");
    setSelectedRace(c.race || "");
    setSelectedSubrace(c.subrace || "");
    setSelectedClass(c.class || "");
    setSelectedArchClass(c.archClass || "");
    setResonancePoints(c.resonancePoints ?? 3);
    setSelectedBackground(c.background || "");
    setSelectedFeats(c.feats || []);
    setCurrentLevel(c.level || 1);
    setCurrentXP(c.xp || 0);
    setSelectedAlignment(c.alignment || "");
    if (c.abilities?.length) setAbilities(c.abilities.map((a: { name: string; score: number; modifier: number }) => ({ ...a })));
    setKnownSpells(c.knownSpells || []);
    setPreparedSpells(c.preparedSpells || []);
    setCharacterNotes(c.notes || "");
    if (c.appearance) setAppearance(c.appearance);
    setBuilderView("build");
  };

  const removeSaved = (id: string) => {
    setSavedCharacters(deleteCharacter(id));
    if (characterId === id) setCharacterId("");
  };

  const resetCharacter = () => {
    setCharacterId("");
    setCharacterName("");
    setCharacterNotes("");
    setSelectedRace("");
    setSelectedSubrace("");
    setSelectedClass("");
    setSelectedArchClass("");
    setResonancePoints(3);
    setSelectedBackground("");
    setSelectedFeats([]);
    setCurrentLevel(1);
    setCurrentXP(0);
    setSelectedAlignment("");
    setAbilities(defaultAbilities);
    setKnownSpells([]);
    setPreparedSpells([]);
    setBuilderView("build");
  };""",
)

# UI: title row + name + view toggle
old_header = '''      {/* Title and Action Buttons */}
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-4xl font-bold text-white">Character Builder</h1>
        <div className="flex gap-2 flex-wrap">
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
        </div>
      </div>'''

new_header = '''      {/* Title and Action Buttons */}
      <div className="flex flex-col gap-4 mb-6">
        <div className="flex flex-wrap justify-between items-center gap-3">
          <h1 className="text-4xl font-bold text-white">Character Builder</h1>
          <div className="flex gap-2 flex-wrap">
            <Button variant={builderView === "build" ? "default" : "outline"} className={builderView === "build" ? "bg-amber-600" : ""} onClick={() => setBuilderView("build")}>Build</Button>
            <Button variant={builderView === "sheet" ? "default" : "outline"} className={builderView === "sheet" ? "bg-amber-600" : ""} onClick={() => setBuilderView("sheet")}>Sheet</Button>
            <Button className="amber-button" onClick={randomCharacter}><Dice1 className="w-4 h-4 mr-2" />RANDOM</Button>
            <Button className="amber-button" onClick={resetCharacter}><Plus className="w-4 h-4 mr-2" />NEW</Button>
            <Button className="amber-button" onClick={() => { navigator.clipboard.writeText(JSON.stringify(buildCharacterPayload(), null, 2)); }}><Copy className="w-4 h-4 mr-2" />COPY JSON</Button>
            <Button className="amber-button" onClick={saveCharacter}><Save className="w-4 h-4 mr-2" />SAVE</Button>
            <Button className="amber-button" onClick={exportCharacter}><Download className="w-4 h-4 mr-2" />EXPORT</Button>
          </div>
        </div>
        <div className="flex flex-wrap gap-3 items-end">
          <div className="flex-1 min-w-[200px]">
            <label className="text-xs text-amber-200/70">Character name</label>
            <Input className="bg-input border-border text-white" value={characterName} onChange={(e) => setCharacterName(e.target.value)} placeholder="Name your adventurer" />
          </div>
          <div className="min-w-[220px]">
            <label className="text-xs text-amber-200/70">Load saved</label>
            <select
              className="w-full bg-input border border-border rounded px-3 py-2 text-white"
              value=""
              onChange={(e) => {
                const c = savedCharacters.find((x) => x.id === e.target.value);
                if (c) loadCharacter(c);
              }}
            >
              <option value="">Select a saved character…</option>
              {savedCharacters.map((c) => (
                <option key={c.id} value={c.id}>{characterDisplayName(c)} (L{c.level || 1})</option>
              ))}
            </select>
          </div>
        </div>
        {savedCharacters.length > 0 && (
          <div className="flex flex-wrap gap-2">
            {savedCharacters.slice(0, 8).map((c) => (
              <div key={c.id} className="flex items-center gap-1 bg-slate-800/80 border border-amber-700/30 rounded px-2 py-1 text-xs text-amber-50">
                <button type="button" className="hover:text-amber-300" onClick={() => loadCharacter(c)}>{characterDisplayName(c)}</button>
                <button type="button" className="text-red-400 ml-1" onClick={() => removeSaved(c.id!)}>×</button>
              </div>
            ))}
          </div>
        )}
      </div>'''

if old_header in text:
    text = text.replace(old_header, new_header)
    print("header updated")
else:
    print("HEADER MISSING")

# Soften patron banner
text = text.replace(
    '''      {/* Support Banner */}
      <div className="bg-gray-600/20 border border-gray-600 rounded-lg p-4 mb-6 text-center">
        <div className="text-white mb-2">Every lone dollar you throw into our coffers is a spark of resonance, another skirmish in the Grand Weave that keeps the Old Gods snoring. Donate now and help us fend off the reset…for one more glorious day of adventuring!</div>
        <div className="text-lg text-gray-300 font-semibold mb-3">Ignite the Resonance with $1</div>
        <Button className="bg-gray-600 hover:bg-gray-700 text-white">
          Become a Patron today
        </Button>
      </div>''',
    '''      <div className="bg-amber-950/30 border border-amber-700/40 rounded-lg p-3 mb-6 text-center text-sm text-amber-100/70">
        Decennium Descent companion — build Aethel characters, then run them in Session.
      </div>''',
)

# Remove AL Illegal
text = text.replace(
    '''              <div className="flex justify-between items-center">
                <CardTitle className="text-white">Options</CardTitle>
                <Badge variant="destructive" className="text-xs">AL Illegal</Badge>
              </div>''',
    '''              <div className="flex justify-between items-center">
                <CardTitle className="text-white">Options</CardTitle>
                <Badge className="bg-amber-700/80 text-xs">Aethel</Badge>
              </div>''',
)

# Remove show info rows (multiple) - simplify
text = text.replace(
    '''                    <div className="flex items-center justify-between mb-4">
                      <span className="text-sm">Race</span>
                      <div className="flex items-center gap-2">
                        <span className="text-xs text-gray-400">show info</span>
                        <Lock className="w-4 h-4 text-gray-400" />
                        <Settings className="w-4 h-4 text-gray-400" />
                      </div>
                    </div>
''',
    '''                    <div className="mb-2 text-sm text-amber-100/70">Race</div>
''',
)

# Wrap main grid in builderView conditional - find Main Content comment
marker = "      {/* Main Content */}\n      <div className=\"grid grid-cols-12 gap-6\">"
if marker in text and "builderView === \"sheet\"" not in text.split("Main Content")[1][:200]:
    # Find end of main return content - before final closing of outer div
    # Insert sheet view before Main Content and wrap build view
    text = text.replace(
        marker,
        '''      {builderView === "sheet" ? (
        <CharacterSheet character={buildCharacterPayload()} onExport={exportCharacter} />
      ) : (
      /* Main Content */
      <div className="grid grid-cols-12 gap-6">''',
    )
    # Close the conditional before the final closing of min-h-screen div
    # The structure ends with </div></div> for grid and outer
    # Find the last occurrence carefully - after skills card closes
    closing = "      </div>\n    </div>\n  );\n}"
    if text.count("      </div>\n    </div>\n  );\n}") >= 1:
        text = text.replace(
            "      </div>\n    </div>\n  );\n}",
            "      </div>\n      )}\n    </div>\n  );\n}",
            1,
        )
        print("sheet view wrapped")
    else:
        print("close wrap failed")

# Features tab: add level list
old_feat_block = '''                        <div className="border border-amber-600/30 rounded p-3">
                          <div className="text-amber-300 font-semibold mb-1">{selectedClass}</div>
                          <p className="text-xs text-gray-300">{classes.find(c => c.name === selectedClass)?.info}</p>
                          <div className="mt-2 text-xs">
                            Hit Die: {classes.find(c => c.name === selectedClass)?.hitDie} · Spellcasting: {classes.find(c => c.name === selectedClass)?.spellcasting}
                          </div>
                        </div>'''

new_feat_block = '''                        <div className="border border-amber-600/30 rounded p-3">
                          <div className="text-amber-300 font-semibold mb-1">{selectedClass}</div>
                          <p className="text-xs text-gray-300">{classes.find(c => c.name === selectedClass)?.info}</p>
                          <div className="mt-2 text-xs">
                            Hit Die: {classes.find(c => c.name === selectedClass)?.hitDie} · Spellcasting: {classes.find(c => c.name === selectedClass)?.spellcasting}
                          </div>
                          <div className="mt-3 space-y-1 text-xs text-amber-50/80">
                            {[1,2,3,4,5].map((lvl) => (
                              <div key={lvl}>
                                <span className="text-amber-400">L{lvl}:</span>{" "}
                                {(classDetails[selectedClass as keyof typeof classDetails]?.levels?.[lvl] || ["—"]).join(", ")}
                              </div>
                            ))}
                          </div>
                        </div>'''

if old_feat_block in text:
    text = text.replace(old_feat_block, new_feat_block)
    print("features levels added")
else:
    print("features block missing")

# Wire notes textarea if it exists
if 'placeholder="Add your character notes here..."' in text and "setCharacterNotes" in text:
    # try to bind value - may already be uncontrolled
    if "value={characterNotes}" not in text:
        text = text.replace(
            'placeholder="Add your character notes here..."',
            'value={characterNotes} onChange={(e) => setCharacterNotes(e.target.value)} placeholder="Add your character notes here..."',
        )
        print("notes bound")

p.write_text(text, encoding="utf-8")
print("done", len(text))
