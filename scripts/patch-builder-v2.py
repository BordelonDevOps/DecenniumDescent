from pathlib import Path

p = Path(r"C:\Github\Descent assets\DecenniumDescent-main\src\components\CharacterBuilder.tsx")
text = p.read_text(encoding="utf-8")

# imports
if "CharacterAppearance" not in text:
    text = text.replace(
        'import featsData from "@/data/feats";',
        'import featsData from "@/data/feats";\nimport prestigePaths from "@/data/prestige";\nimport CharacterAppearance from "@/components/CharacterAppearance";',
    )

# state for arch + appearance + resonance
if "selectedArchClass" not in text:
    text = text.replace(
        'const [selectedClass, setSelectedClass] = useState<string>("");',
        'const [selectedClass, setSelectedClass] = useState<string>("");\n  const [selectedArchClass, setSelectedArchClass] = useState<string>("");\n  const [resonancePoints, setResonancePoints] = useState<number>(3);\n  const [appearance, setAppearance] = useState({\n    body: "Athletic",\n    skin: "#c4a484",\n    hair: "#1a1a1a",\n    eyes: "#1565c0",\n    accent: "#d97706",\n    gearTint: "#334155",\n  });',
    )

# export payload extras
text = text.replace(
    "    class: selectedClass,\n    background: selectedBackground,",
    "    class: selectedClass,\n    archClass: selectedArchClass,\n    resonancePoints,\n    appearance,\n    background: selectedBackground,",
)

# reset extras
text = text.replace(
    'setSelectedClass("");\n    setSelectedBackground("");',
    'setSelectedClass("");\n    setSelectedArchClass("");\n    setResonancePoints(3);\n    setSelectedBackground("");',
)

# features tab replacement
old_features = '''                {/* Features Tab */}
                <TabsContent value="features" className="space-y-4">
                  <div className="space-y-4">
                    <h3 className="text-white font-semibold text-center">Class Features</h3>
                    <div className="text-center text-gray-400">
                      Class features and abilities will be displayed here.
                    </div>
                  </div>
                </TabsContent>'''

new_features = '''                {/* Features Tab */}
                <TabsContent value="features" className="space-y-4">
                  <div className="space-y-4">
                    <h3 className="text-white font-semibold text-center">Class & Prestige</h3>
                    {!selectedClass ? (
                      <div className="text-center text-gray-400 text-sm">Select a class to see features and arch paths.</div>
                    ) : (
                      <div className="space-y-3 text-sm text-amber-50/80">
                        <div className="border border-amber-600/30 rounded p-3">
                          <div className="text-amber-300 font-semibold mb-1">{selectedClass}</div>
                          <p className="text-xs text-gray-300">{classes.find(c => c.name === selectedClass)?.info}</p>
                          <div className="mt-2 text-xs">
                            Hit Die: {classes.find(c => c.name === selectedClass)?.hitDie} · Spellcasting: {classes.find(c => c.name === selectedClass)?.spellcasting}
                          </div>
                        </div>
                        <div>
                          <div className="text-amber-200 font-medium mb-2">Arch / Prestige Path</div>
                          <select
                            className="w-full bg-input border border-border rounded px-3 py-2 text-white mb-2"
                            value={selectedArchClass}
                            onChange={(e) => setSelectedArchClass(e.target.value)}
                          >
                            <option value="">None yet</option>
                            {(classes.find(c => c.name === selectedClass)?.archClasses || []).map((a) => (
                              <option key={a} value={a}>{a}</option>
                            ))}
                          </select>
                          {selectedArchClass && prestigePaths.filter((p) => p.name === selectedArchClass).map((p) => (
                            <div key={p.name} className="border border-orange-600/40 rounded p-3 space-y-1 text-xs">
                              <div className="text-orange-300 font-semibold">{p.name}</div>
                              <p>{p.summary}</p>
                              <div><span className="text-blue-300">Entrance:</span> {p.entrance}</div>
                              <div><span className="text-green-300">Hallmarks:</span> {p.hallmarks.join(" · ")}</div>
                            </div>
                          ))}
                        </div>
                        <div className="border border-purple-600/40 rounded p-3">
                          <div className="flex justify-between items-center mb-2">
                            <span className="text-purple-300 font-medium">Resonance Points</span>
                            <span className="text-white font-bold">{resonancePoints}</span>
                          </div>
                          <input
                            type="range"
                            min={0}
                            max={12}
                            value={resonancePoints}
                            onChange={(e) => setResonancePoints(Number(e.target.value))}
                            className="w-full"
                          />
                          <p className="text-[11px] text-gray-400 mt-1">Spend RP to push the Weave — MMO-feel resource for table play.</p>
                        </div>
                      </div>
                    )}
                  </div>
                </TabsContent>'''

if old_features in text:
    text = text.replace(old_features, new_features)
    print("features tab updated")
else:
    print("features tab not found")

# Insert appearance panel into right column - find Ability Scores card start-ish
marker = '<CardTitle className="text-white">Ability Scores</CardTitle>'
appearance_block = '''<div className="mb-4">
              <CharacterAppearance raceName={selectedRace} value={appearance} onChange={setAppearance} />
            </div>
            <CardTitle className="text-white">Ability Scores</CardTitle>'''

# CardTitle is inside CardHeader - need careful insert before the Ability Scores card
# Look for right column Ability Scores
ability_card = '''        {/* Right Panel - Ability Scores */}
        <div className="col-span-4">
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="text-white">Ability Scores</CardTitle>'''

ability_card_new = '''        {/* Right Panel - Appearance + Ability Scores */}
        <div className="col-span-4 space-y-4">
          <Card className="glass-card">
            <CardHeader className="pb-2">
              <CardTitle className="text-white text-base">Look</CardTitle>
            </CardHeader>
            <CardContent>
              <CharacterAppearance raceName={selectedRace} value={appearance} onChange={setAppearance} />
            </CardContent>
          </Card>
          <Card className="glass-card">
            <CardHeader>
              <CardTitle className="text-white">Ability Scores</CardTitle>'''

if ability_card in text:
    text = text.replace(ability_card, ability_card_new)
    print("appearance card inserted")
else:
    print("ability card marker missing")

# class tab: add arch select after class select
old_class_select_tail = '''                    <div className="text-xs text-red-400 mt-2">1 remaining</div>

                    <div className="mt-4 space-y-3">
                      {classes.map((cls) => ('''

new_class_select_tail = '''                    <div className="text-xs text-red-400 mt-2">1 remaining</div>

                    {selectedClass && (
                      <div className="mt-3">
                        <div className="text-sm mb-1">Arch Class</div>
                        <select
                          className="w-full bg-input border border-border rounded px-3 py-2 text-white"
                          value={selectedArchClass}
                          onChange={(e) => setSelectedArchClass(e.target.value)}
                        >
                          <option value="">optional</option>
                          {(classes.find((c) => c.name === selectedClass)?.archClasses || []).map((a) => (
                            <option key={a} value={a}>{a}</option>
                          ))}
                        </select>
                      </div>
                    )}

                    <div className="mt-4 space-y-3">
                      {classes.map((cls) => ('''

if old_class_select_tail in text:
    text = text.replace(old_class_select_tail, new_class_select_tail)
    print("arch select on class tab")
else:
    print("class select tail missing")

p.write_text(text, encoding="utf-8")
print("character builder patched")
