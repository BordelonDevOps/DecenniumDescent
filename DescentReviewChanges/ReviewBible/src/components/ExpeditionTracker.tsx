"use client";

import { useEffect, useMemo, useState } from "react";
import { Caravan, Clock3, Package, Plus, ShieldAlert, TentTree, Trash2 } from "lucide-react";
import { Button } from "./ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Input } from "./ui/input";
import rules from "@/data/gameplay-loop.json";
import {
  complicationSeverity,
  extractionPressureIncrease,
  pressureTriggersComplication,
  routeProgressForWatch,
  extractionTestDue,
} from "@/lib/gameplay-loop";

type TeamId = "combat" | "recon" | "research" | "resource" | "support" | "rest";
type Phase = "Preparation" | "Descent" | "Objective" | "Extraction" | "Haven";
type MappingState = "Unknown" | "Sketched" | "Mapped" | "Secured";

type Member = {
  id: string;
  name: string;
  team: TeamId;
  activity: string;
  load: number;
  capacity: number;
  strain: number;
  wounds: number;
  status: string;
  restDebtDueIn: number | null;
};

type CargoLot = {
  id: string;
  name: string;
  load: number;
  extractionClass: number;
  priority: number;
  value: number;
  tags: string;
};

type ExpeditionState = {
  phase: Phase;
  openingHour: number;
  routeName: string;
  routeProgress: number;
  routeLength: number;
  mapping: MappingState;
  routeCapacity: number;
  routeSustenance: number;
  pressure: number;
  supplies: number;
  treasury: number;
  camp: string;
  objective: string;
  abortConditions: string;
  grossCargoTarget: number;
  netExpeditionTarget: number;
  trueProfitTarget: number;
  primarySuccessMetric: "Gross" | "Net" | "True Profit";
  lastExtractionTestProgress: number;
  attentionActive: boolean;
  members: Member[];
  cargo: CargoLot[];
  log: string[];
};

const STORAGE_KEY = "dd_expedition_loop_v2";
const TEAM_IDS: TeamId[] = ["combat", "recon", "research", "resource", "support", "rest"];
const PHASES: Phase[] = ["Preparation", "Descent", "Objective", "Extraction", "Haven"];
const MAPPING: MappingState[] = ["Unknown", "Sketched", "Mapped", "Secured"];

const teamById = new Map(rules.expedition.teams.map((team) => [team.id, team]));

function uid() {
  return Math.random().toString(36).slice(2, 10);
}

function initialState(): ExpeditionState {
  return {
    phase: "Preparation",
    openingHour: 0,
    routeName: "Surface Gate to first secured camp",
    routeProgress: 0,
    routeLength: 6,
    mapping: "Mapped",
    routeCapacity: 60,
    routeSustenance: 2,
    pressure: 1,
    supplies: 72,
    treasury: 500,
    camp: "Temporary Camp",
    objective: "Reach the objective, recover profitable cargo, and return before an abort condition is met.",
    abortConditions: "Supply below two days; two Critical characters; transport Integrity 0; Horn reached without a secured return route.",
    grossCargoTarget: 3000,
    netExpeditionTarget: 2000,
    trueProfitTarget: 1000,
    primarySuccessMetric: "True Profit",
    lastExtractionTestProgress: -1,
    attentionActive: false,
    members: [],
    cargo: [],
    log: ["Expedition record created."],
  };
}

function normalizeState(raw: Partial<ExpeditionState>): ExpeditionState {
  const base = initialState();
  const importedMembers = Array.isArray(raw.members) ? raw.members : [];
  const rosterTruncated = importedMembers.length > 12;
  const members = importedMembers.slice(0, 12).map((member) => {
    const legacy = member as Member & { watchesWithoutRest?: number };
    const migratedDebt = legacy.restDebtDueIn == null && Number(legacy.watchesWithoutRest) > 0
      ? Math.max(0, 3 - Math.floor(Number(legacy.watchesWithoutRest)))
      : legacy.restDebtDueIn;
    return {
      ...member,
      restDebtDueIn: migratedDebt == null ? null : Math.max(0, Math.min(2, Number(migratedDebt) || 0)),
    };
  });
  const importedLog = Array.isArray(raw.log) ? raw.log.slice(0, 100) : base.log;
  return {
    ...base,
    ...raw,
    members,
    cargo: Array.isArray(raw.cargo) ? raw.cargo : [],
    log: rosterTruncated ? ["Imported roster exceeded the canonical maximum of 12; excess entries were rejected.", ...importedLog].slice(0, 100) : importedLog,
  };
}

export default function ExpeditionTracker() {
  const [state, setState] = useState<ExpeditionState>(() => initialState());
  const [newMemberName, setNewMemberName] = useState("");
  const [newCargoName, setNewCargoName] = useState("");

  useEffect(() => {
    try {
      const saved = window.localStorage.getItem(STORAGE_KEY);
      if (saved) setState(normalizeState(JSON.parse(saved) as Partial<ExpeditionState>));
    } catch {
      setState(initialState());
    }
  }, []);

  useEffect(() => {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  }, [state]);

  const rosterLoad = useMemo(() => state.members.reduce((sum, member) => sum + member.load, 0), [state.members]);
  const rosterCapacity = useMemo(() => state.members.reduce((sum, member) => sum + member.capacity, 0), [state.members]);
  const cargoLoad = useMemo(() => state.cargo.reduce((sum, lot) => sum + lot.load, 0), [state.cargo]);
  const convoyLoad = rosterLoad + cargoLoad;
  const highestExtractionClass = useMemo(
    () => state.cargo.reduce((max, lot) => Math.max(max, lot.extractionClass), 0),
    [state.cargo],
  );
  const dailySupply = state.members.length;
  const day = Math.floor(state.openingHour / 24) + 1;
  const watchNumber = Math.floor(state.openingHour / 8) + 1;
  const hornRemaining = Math.max(0, rules.opening.hornHour - state.openingHour);
  const openingRemaining = Math.max(0, rules.opening.hours - state.openingHour);

  const update = (patch: Partial<ExpeditionState>) => setState((current) => ({ ...current, ...patch }));
  const appendLog = (line: string) =>
    setState((current) => ({ ...current, log: [`H${current.openingHour}: ${line}`, ...current.log].slice(0, 100) }));

  const addMember = () => {
    const name = newMemberName.trim();
    if (!name || state.members.length >= 12) return;
    const activity = teamById.get("combat")?.activities[0] ?? "Advance";
    setState((current) => ({
      ...current,
      members: [...current.members, { id: uid(), name, team: "combat", activity, load: 0, capacity: 10, strain: 0, wounds: 0, status: "Ready", restDebtDueIn: null }],
      log: [`H${current.openingHour}: ${name} joined the Expedition.`, ...current.log].slice(0, 100),
    }));
    setNewMemberName("");
  };

  const addCargo = () => {
    const name = newCargoName.trim();
    if (!name) return;
    setState((current) => ({
      ...current,
      cargo: [...current.cargo, { id: uid(), name, load: 1, extractionClass: 1, priority: 3, value: 0, tags: "" }],
      log: [`H${current.openingHour}: Cargo added — ${name}.`, ...current.log].slice(0, 100),
    }));
    setNewCargoName("");
  };

  const assignRestDebt = (memberId: string) => {
    setState((current) => ({
      ...current,
      members: current.members.map((member) => {
        if (member.id !== memberId) return member;
        const alreadyOwes = member.restDebtDueIn !== null;
        return {
          ...member,
          restDebtDueIn: 2,
          strain: Math.min(6, member.strain + (alreadyOwes ? 1 : 0)),
        };
      }),
      log: [`H${current.openingHour}: Rest Debt assigned; it must be cleared within the next two Watches.`, ...current.log].slice(0, 100),
    }));
  };

  const resolveWatch = () => {
    const active = state.members.filter((member) => member.team !== "rest");
    const resting = state.members.filter((member) => member.team === "rest");
    const supplySpent = state.members.length / 3;
    const nextSupplies = Math.max(0, state.supplies - supplySpent);
    const overRouteCapacity = convoyLoad > state.routeCapacity;
    const progress = routeProgressForWatch(state.mapping, overRouteCapacity);
    const reconCount = active.filter((member) => member.team === "recon").length;
    const supportCount = active.filter((member) => member.team === "support").length;
    const carriesAttention = state.cargo.some((lot) => /(?:^|[,;\s])attention(?:$|[,;\s])/i.test(lot.tags));
    const attentionIncrease = carriesAttention && !state.attentionActive && state.phase !== "Preparation" && state.phase !== "Haven" ? 1 : 0;
    const basePressure = Math.max(
      0,
      Math.min(6, state.pressure + (overRouteCapacity ? 1 : 0) + attentionIncrease - (reconCount > 0 ? 1 : 0)),
    );
    const roll = 1 + Math.floor(Math.random() * 6);
    const event = pressureTriggersComplication(basePressure, roll);
    const severity = complicationSeverity(basePressure, roll);
    const nextHour = Math.min(rules.opening.hours, state.openingHour + rules.modes.expedition.watchHours);
    const extractionDirection = state.phase === "Extraction" ? -1 : 1;
    const nextProgress = Math.max(0, Math.min(state.routeLength, state.routeProgress + progress * extractionDirection));
    const insufficient = nextSupplies <= 0 && state.members.length > 0;
    const atExit = state.phase === "Extraction" ? nextProgress === 0 : nextProgress === state.routeLength;
    const testDue = state.phase === "Extraction" && extractionTestDue({
      mapping: state.mapping,
      progress: nextProgress,
      length: state.routeLength,
      lastTestProgress: state.lastExtractionTestProgress,
      atExit,
      severeComplication: severity === "severe",
    });

    setState((current) => ({
      ...current,
      openingHour: nextHour,
      supplies: nextSupplies,
      routeProgress: nextProgress,
      attentionActive: carriesAttention,
      lastExtractionTestProgress: testDue ? nextProgress : current.lastExtractionTestProgress,
      pressure: event ? Math.min(6, basePressure + (severity === "severe" ? 1 : 0)) : basePressure,
      members: current.members.map((member) => {
        if (member.team === "rest") {
          return {
            ...member,
            restDebtDueIn: null,
            strain: Math.min(6, Math.max(0, member.strain + (insufficient ? 1 : 0) - (supportCount > 0 ? 1 : 0))),
          };
        }
        if (member.restDebtDueIn === null) {
          return { ...member, strain: Math.min(6, member.strain + (insufficient ? 1 : 0)) };
        }
        if (member.restDebtDueIn > 1) {
          return {
            ...member,
            restDebtDueIn: member.restDebtDueIn - 1,
            strain: Math.min(6, member.strain + (insufficient ? 1 : 0)),
          };
        }
        if (member.restDebtDueIn === 1) {
          return {
            ...member,
            restDebtDueIn: 0,
            strain: Math.min(6, member.strain + (insufficient ? 1 : 0) + 1),
          };
        }
        return { ...member, strain: Math.min(6, member.strain + (insufficient ? 1 : 0)) };
      }),
      log: [
        ...(testDue ? [`H${nextHour}: Extraction Test due at Progress ${nextProgress} (${state.mapping} route).`] : []),
        ...(attentionIncrease ? [`H${nextHour}: Attention cargo exposed; Pressure +1.`] : []),
        `H${nextHour}: Watch resolved — ${active.length} active, ${resting.length} resting, ${progress} route Progress, Pressure ${basePressure}, d6 ${roll}${event ? ` (${severity} complication)` : " (clear)"}.`,
        ...current.log,
      ].slice(0, 100),
    }));
  };

  const beginExtraction = () => {
    const increase = extractionPressureIncrease(highestExtractionClass);
    setState((current) => ({
      ...current,
      phase: "Extraction",
      lastExtractionTestProgress: -1,
      pressure: Math.min(6, current.pressure + increase),
      log: [`H${current.openingHour}: Extraction declared. Highest Extraction Class ${highestExtractionClass}; Pressure +${increase}.`, ...current.log].slice(0, 100),
    }));
  };

  const arriveHaven = () => {
    setState((current) => ({
      ...current,
      phase: "Haven",
      routeProgress: 0,
      pressure: 0,
      attentionActive: false,
      members: current.members.map((member) => ({ ...member, strain: 0, restDebtDueIn: null, status: member.status === "Missing" ? "Missing" : "Recovering" })),
      log: [`H${current.openingHour}: Expedition entered Haven resolution. Quarantine and provenance filing begin.`, ...current.log].slice(0, 100),
    }));
  };

  return (
    <div className="space-y-6 p-6">
      <div className="text-center space-y-2">
        <h2 className="text-3xl font-bold text-amber-400">Expedition Loop</h2>
        <p className="text-amber-200/80 max-w-3xl mx-auto">
          Plan the company, assign each Watch, manage Pressure and cargo, extract, and resolve the Haven.
        </p>
      </div>

      <Card className="bg-slate-900/70 border-amber-600/30">
        <CardContent className="pt-4 text-sm text-slate-200">
          <strong className="text-amber-300">Quick loop:</strong> objective → finance → roster → load → Watches → encounter → cargo → extraction → Haven → advancement. Tier I Haven returns may use Inspection → Appraisal → Sale → Sponsor → Recovery when no dispute or crisis requires the full procedure.
        </CardContent>
      </Card>

      <div className="grid gap-4 md:grid-cols-4">
        <Card className="bg-slate-900/70 border-amber-600/30"><CardHeader><CardTitle className="text-sm flex gap-2"><Clock3 className="w-4 h-4" /> Opening</CardTitle></CardHeader><CardContent className="space-y-1 text-sm"><div>Hour {state.openingHour} · Day {day} · Watch {watchNumber}</div><div>Horn in {hornRemaining} h</div><div>Seal in {openingRemaining} h</div></CardContent></Card>
        <Card className="bg-slate-900/70 border-amber-600/30"><CardHeader><CardTitle className="text-sm flex gap-2"><ShieldAlert className="w-4 h-4" /> Pressure</CardTitle></CardHeader><CardContent><div className="text-3xl font-bold text-red-300">{state.pressure}</div><div className="text-xs text-slate-300">{rules.pressure.states[String(state.pressure) as keyof typeof rules.pressure.states]}</div></CardContent></Card>
        <Card className="bg-slate-900/70 border-amber-600/30"><CardHeader><CardTitle className="text-sm flex gap-2"><Package className="w-4 h-4" /> Convoy</CardTitle></CardHeader><CardContent className="text-sm"><div>{convoyLoad} / {Math.min(rosterCapacity || 0, state.routeCapacity)} Load</div><div>{state.supplies.toFixed(1)} Supply · {dailySupply}/day</div><div>Highest Extraction Class {highestExtractionClass}</div></CardContent></Card>
        <Card className="bg-slate-900/70 border-amber-600/30"><CardHeader><CardTitle className="text-sm flex gap-2"><TentTree className="w-4 h-4" /> Position</CardTitle></CardHeader><CardContent className="text-sm"><div>{state.routeName}</div><div>Progress {state.routeProgress}/{state.routeLength}</div><div>{state.mapping} · {state.camp}</div></CardContent></Card>
      </div>

      <Card className="bg-slate-900/70 border-amber-600/30">
        <CardHeader><CardTitle>Expedition State</CardTitle></CardHeader>
        <CardContent className="grid gap-3 md:grid-cols-3">
          <label className="text-xs text-slate-300">Phase<select value={state.phase} onChange={(event) => update({ phase: event.target.value as Phase })} className="mt-1 w-full rounded border border-amber-700/40 bg-slate-950 p-2 text-sm">{PHASES.map((phase) => <option key={phase}>{phase}</option>)}</select></label>
          <label className="text-xs text-slate-300">Mapping<select value={state.mapping} onChange={(event) => update({ mapping: event.target.value as MappingState })} className="mt-1 w-full rounded border border-amber-700/40 bg-slate-950 p-2 text-sm">{MAPPING.map((mapping) => <option key={mapping}>{mapping}</option>)}</select></label>
          <label className="text-xs text-slate-300">Camp<Input value={state.camp} onChange={(event) => update({ camp: event.target.value })} className="mt-1" /></label>
          <label className="text-xs text-slate-300 md:col-span-2">Route<Input value={state.routeName} onChange={(event) => update({ routeName: event.target.value })} className="mt-1" /></label>
          <label className="text-xs text-slate-300">Treasury<Input type="number" value={state.treasury} onChange={(event) => update({ treasury: Number(event.target.value) || 0 })} className="mt-1" /></label>
          <label className="text-xs text-slate-300 md:col-span-2">Primary objective<textarea value={state.objective} onChange={(event) => update({ objective: event.target.value })} className="mt-1 min-h-20 w-full rounded border border-amber-700/40 bg-slate-950 p-2 text-sm" /></label>
          <label className="text-xs text-slate-300">Abort conditions<textarea value={state.abortConditions} onChange={(event) => update({ abortConditions: event.target.value })} className="mt-1 min-h-20 w-full rounded border border-amber-700/40 bg-slate-950 p-2 text-sm" /></label>
          <label className="text-xs text-slate-300">Pressure<Input type="number" min={0} max={6} value={state.pressure} onChange={(event) => update({ pressure: Math.max(0, Math.min(6, Number(event.target.value) || 0)) })} className="mt-1" /></label>
          <label className="text-xs text-slate-300">Supply<Input type="number" min={0} step="0.5" value={state.supplies} onChange={(event) => update({ supplies: Math.max(0, Number(event.target.value) || 0) })} className="mt-1" /></label>
          <label className="text-xs text-slate-300">Route capacity<Input type="number" min={0} value={state.routeCapacity} onChange={(event) => update({ routeCapacity: Math.max(0, Number(event.target.value) || 0) })} className="mt-1" /></label>
          <label className="text-xs text-slate-300">Route length<Input type="number" min={1} value={state.routeLength} onChange={(event) => update({ routeLength: Math.max(1, Number(event.target.value) || 1) })} className="mt-1" /></label>
          <label className="text-xs text-slate-300">Route progress<Input type="number" min={0} max={state.routeLength} value={state.routeProgress} onChange={(event) => update({ routeProgress: Math.max(0, Math.min(state.routeLength, Number(event.target.value) || 0)) })} className="mt-1" /></label>
          <label className="text-xs text-slate-300">Route Sustenance (0–4)<Input type="number" min={0} max={4} value={state.routeSustenance} onChange={(event) => update({ routeSustenance: Math.max(0, Math.min(4, Number(event.target.value) || 0)) })} className="mt-1" /></label>
          <label className="text-xs text-slate-300">Gross cargo target<Input type="number" min={0} value={state.grossCargoTarget} onChange={(event) => update({ grossCargoTarget: Math.max(0, Number(event.target.value) || 0) })} className="mt-1" /></label>
          <label className="text-xs text-slate-300">Net expedition target<Input type="number" min={0} value={state.netExpeditionTarget} onChange={(event) => update({ netExpeditionTarget: Math.max(0, Number(event.target.value) || 0) })} className="mt-1" /></label>
          <label className="text-xs text-slate-300">True profit target<Input type="number" min={0} value={state.trueProfitTarget} onChange={(event) => update({ trueProfitTarget: Math.max(0, Number(event.target.value) || 0) })} className="mt-1" /></label>
          <label className="text-xs text-slate-300">Primary success metric<select value={state.primarySuccessMetric} onChange={(event) => update({ primarySuccessMetric: event.target.value as ExpeditionState["primarySuccessMetric"] })} className="mt-1 w-full rounded border border-amber-700/40 bg-slate-950 p-2 text-sm"><option>Gross</option><option>Net</option><option>True Profit</option></select></label>
        </CardContent>
      </Card>

      <Card className="bg-slate-900/70 border-amber-600/30">
        <CardHeader><CardTitle>Roster — {state.members.length}/12</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <div className="flex gap-2"><Input placeholder="Character or specialist" value={newMemberName} onChange={(event) => setNewMemberName(event.target.value)} onKeyDown={(event) => event.key === "Enter" && addMember()} /><Button onClick={addMember} disabled={state.members.length >= 12}><Plus className="w-4 h-4" /></Button></div>
          <div className="space-y-2">
            {state.members.map((member) => {
              const activities = teamById.get(member.team)?.activities ?? [];
              return <div key={member.id} className="grid gap-2 rounded border border-slate-700 bg-slate-950/50 p-2 md:grid-cols-[1.2fr_1fr_1.1fr_75px_75px_90px_120px_40px]">
                <Input value={member.name} onChange={(event) => setState((current) => ({ ...current, members: current.members.map((item) => item.id === member.id ? { ...item, name: event.target.value } : item) }))} />
                <select value={member.team} onChange={(event) => { const team = event.target.value as TeamId; const activity = teamById.get(team)?.activities[0] ?? ""; setState((current) => ({ ...current, members: current.members.map((item) => item.id === member.id ? { ...item, team, activity } : item) })); }} className="rounded border border-amber-700/40 bg-slate-950 p-2 text-sm">{TEAM_IDS.map((id) => <option key={id} value={id}>{teamById.get(id)?.name ?? id}</option>)}</select>
                <select value={member.activity} onChange={(event) => setState((current) => ({ ...current, members: current.members.map((item) => item.id === member.id ? { ...item, activity: event.target.value } : item) }))} className="rounded border border-amber-700/40 bg-slate-950 p-2 text-sm">{activities.map((activity) => <option key={activity}>{activity}</option>)}</select>
                <Input aria-label="Load" type="number" min={0} value={member.load} onChange={(event) => setState((current) => ({ ...current, members: current.members.map((item) => item.id === member.id ? { ...item, load: Math.max(0, Number(event.target.value) || 0) } : item) }))} />
                <Input aria-label="Capacity" type="number" min={1} value={member.capacity} onChange={(event) => setState((current) => ({ ...current, members: current.members.map((item) => item.id === member.id ? { ...item, capacity: Math.max(1, Number(event.target.value) || 1) } : item) }))} />
                <div className="flex gap-1"><Input aria-label="Strain" type="number" min={0} max={6} value={member.strain} onChange={(event) => setState((current) => ({ ...current, members: current.members.map((item) => item.id === member.id ? { ...item, strain: Math.max(0, Math.min(6, Number(event.target.value) || 0)) } : item) }))} /><Input aria-label="Wounds" type="number" min={0} max={3} value={member.wounds} onChange={(event) => setState((current) => ({ ...current, members: current.members.map((item) => item.id === member.id ? { ...item, wounds: Math.max(0, Math.min(3, Number(event.target.value) || 0)) } : item) }))} /></div>
                <Button
                  type="button"
                  variant="outline"
                  className="h-auto min-h-9 whitespace-normal px-2 py-1 text-[10px]"
                  title="Assign when this character works through or loses a scheduled Rest Watch"
                  onClick={() => assignRestDebt(member.id)}
                >
                  {member.restDebtDueIn === null ? "Assign Rest Debt" : member.restDebtDueIn === 0 ? "Rest Debt overdue" : `Rest due in ${member.restDebtDueIn} Watch${member.restDebtDueIn === 1 ? "" : "es"}`}
                </Button>
                <Button variant="outline" onClick={() => setState((current) => ({ ...current, members: current.members.filter((item) => item.id !== member.id) }))}><Trash2 className="w-4 h-4" /></Button>
              </div>;
            })}
          </div>
          <p className="text-xs text-slate-400">Columns: name, team, activity, carried Load, capacity, Strain/Wounds, and the two-Watch Rest Debt countdown. Assign debt only when a scheduled Rest Watch is lost or interrupted.</p>
        </CardContent>
      </Card>

      <Card className="bg-slate-900/70 border-amber-600/30">
        <CardHeader><CardTitle>Cargo Manifest</CardTitle></CardHeader>
        <CardContent className="space-y-3">
          <div className="flex gap-2"><Input placeholder="Cargo lot" value={newCargoName} onChange={(event) => setNewCargoName(event.target.value)} onKeyDown={(event) => event.key === "Enter" && addCargo()} /><Button onClick={addCargo}><Plus className="w-4 h-4" /></Button></div>
          {state.cargo.map((lot) => <div key={lot.id} className="grid gap-2 rounded border border-slate-700 bg-slate-950/50 p-2 md:grid-cols-[1.5fr_90px_90px_90px_110px_1fr_40px]">
            <Input value={lot.name} onChange={(event) => setState((current) => ({ ...current, cargo: current.cargo.map((item) => item.id === lot.id ? { ...item, name: event.target.value } : item) }))} />
            <Input aria-label="Load" type="number" min={0} value={lot.load} onChange={(event) => setState((current) => ({ ...current, cargo: current.cargo.map((item) => item.id === lot.id ? { ...item, load: Math.max(0, Number(event.target.value) || 0) } : item) }))} />
            <Input aria-label="Extraction Class" type="number" min={0} max={6} value={lot.extractionClass} onChange={(event) => setState((current) => ({ ...current, cargo: current.cargo.map((item) => item.id === lot.id ? { ...item, extractionClass: Math.max(0, Math.min(6, Number(event.target.value) || 0)) } : item) }))} />
            <Input aria-label="Priority" type="number" min={1} max={5} value={lot.priority} onChange={(event) => setState((current) => ({ ...current, cargo: current.cargo.map((item) => item.id === lot.id ? { ...item, priority: Math.max(1, Math.min(5, Number(event.target.value) || 1)) } : item) }))} />
            <Input aria-label="Value" type="number" min={0} value={lot.value} onChange={(event) => setState((current) => ({ ...current, cargo: current.cargo.map((item) => item.id === lot.id ? { ...item, value: Math.max(0, Number(event.target.value) || 0) } : item) }))} />
            <Input placeholder="Tags" value={lot.tags} onChange={(event) => setState((current) => ({ ...current, cargo: current.cargo.map((item) => item.id === lot.id ? { ...item, tags: event.target.value } : item) }))} />
            <Button variant="outline" onClick={() => setState((current) => ({ ...current, cargo: current.cargo.filter((item) => item.id !== lot.id) }))}><Trash2 className="w-4 h-4" /></Button>
          </div>)}
          <p className="text-xs text-slate-400">Columns: name, Load, Extraction Class, priority, base value, tags.</p>
        </CardContent>
      </Card>

      <Card className="bg-slate-900/70 border-amber-600/30">
        <CardHeader><CardTitle className="flex items-center gap-2"><Caravan className="w-5 h-5" /> Resolve the loop</CardTitle></CardHeader>
        <CardContent className="flex flex-wrap gap-2">
          <Button onClick={resolveWatch}>Resolve 8-hour Watch</Button>
          <Button variant="outline" onClick={beginExtraction}>Declare Extraction</Button>
          <Button variant="outline" onClick={arriveHaven}>Enter Haven Resolution</Button>
          <Button variant="outline" onClick={() => { setState(initialState()); appendLog("Expedition reset."); }}>Reset</Button>
        </CardContent>
      </Card>

      <Card className="bg-slate-900/70 border-amber-600/30">
        <CardHeader><CardTitle>Expedition Log</CardTitle></CardHeader>
        <CardContent className="space-y-1 text-sm text-slate-300 max-h-80 overflow-y-auto">
          {state.log.map((line, index) => <div key={`${line}-${index}`} className="border-b border-slate-800 py-1">{line}</div>)}
        </CardContent>
      </Card>
    </div>
  );
}
