"use client";

import { useMemo, useState } from "react";

type Appearance = {
  body: string;
  skin: string;
  hair: string;
  eyes: string;
  accent: string;
  gearTint: string;
};

const BODIES = ["Compact", "Athletic", "Towering", "Wiry", "Stout"];
const SKINS = ["#c4a484", "#8d5524", "#f1c27d", "#6b4f3a", "#d4b8a0", "#7a9e7e", "#5c6bc0", "#b39ddb"];
const HAIRS = ["#1a1a1a", "#4a3728", "#c9a227", "#e8e8e8", "#8b0000", "#2e5a3c", "#5e35b1"];
const EYES = ["#2e7d32", "#1565c0", "#6d4c41", "#f9a825", "#c62828", "#7b1fa2", "#eceff1"];
const ACCENTS = ["#d97706", "#0ea5e9", "#22c55e", "#e11d48", "#a855f7", "#f59e0b"];

function MannequinSvg({ appearance }: { appearance: Appearance }) {
  return (
    <svg viewBox="0 0 200 320" className="w-full h-auto max-h-[320px]">
      <defs>
        <linearGradient id="stage" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stopColor="#0f172a" />
          <stop offset="100%" stopColor="#1e293b" />
        </linearGradient>
      </defs>
      <rect width="200" height="320" fill="url(#stage)" rx="12" />
      <ellipse cx="100" cy="300" rx="55" ry="10" fill="#000" opacity="0.35" />

      {/* legs */}
      <rect x="72" y="190" width="22" height="80" rx="8" fill={appearance.gearTint} />
      <rect x="106" y="190" width="22" height="80" rx="8" fill={appearance.gearTint} />
      {/* torso */}
      <rect x="68" y="110" width="64" height="90" rx="14" fill={appearance.skin} />
      <rect x="74" y="118" width="52" height="70" rx="10" fill={appearance.gearTint} opacity="0.85" />
      {/* arms */}
      <rect x="42" y="118" width="26" height="78" rx="10" fill={appearance.skin} />
      <rect x="132" y="118" width="26" height="78" rx="10" fill={appearance.skin} />
      {/* head */}
      <circle cx="100" cy="72" r="32" fill={appearance.skin} />
      <path
        d="M70 62 Q100 20 130 62 Q100 48 70 62"
        fill={appearance.hair}
      />
      <circle cx="88" cy="74" r="4" fill={appearance.eyes} />
      <circle cx="112" cy="74" r="4" fill={appearance.eyes} />
      {/* accent sash / resonance mark */}
      <path d="M78 140 L122 155 L118 168 L74 152 Z" fill={appearance.accent} opacity="0.9" />
      <circle cx="100" cy="150" r="6" fill={appearance.accent} stroke="#fff" strokeWidth="1" />
    </svg>
  );
}

export default function CharacterAppearance({
  raceName,
  value,
  onChange,
}: {
  raceName?: string;
  value?: Appearance;
  onChange?: (next: Appearance) => void;
}) {
  const defaults: Appearance = useMemo(
    () => ({
      body: "Athletic",
      skin: SKINS[0],
      hair: HAIRS[0],
      eyes: EYES[0],
      accent: ACCENTS[0],
      gearTint: "#334155",
    }),
    []
  );
  const [local, setLocal] = useState<Appearance>(value || defaults);
  const appearance = value || local;

  const set = (patch: Partial<Appearance>) => {
    const next = { ...appearance, ...patch };
    setLocal(next);
    onChange?.(next);
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center justify-between">
        <h3 className="text-white font-semibold text-sm">Appearance Stub</h3>
        <span className="text-[10px] text-amber-200/60 uppercase tracking-wide">
          {raceName || "No race"} · not a 3D client
        </span>
      </div>
      <div className="rounded-lg border border-amber-600/30 bg-slate-950/80 p-2">
        <MannequinSvg appearance={appearance} />
      </div>
      <div className="grid grid-cols-2 gap-2 text-xs">
        <label className="text-amber-100/70 space-y-1">
          Body
          <select
            className="w-full bg-input border border-border rounded px-2 py-1 text-white"
            value={appearance.body}
            onChange={(e) => set({ body: e.target.value })}
          >
            {BODIES.map((b) => (
              <option key={b}>{b}</option>
            ))}
          </select>
        </label>
        <label className="text-amber-100/70 space-y-1">
          Gear tint
          <input
            type="color"
            className="w-full h-8 bg-transparent"
            value={appearance.gearTint}
            onChange={(e) => set({ gearTint: e.target.value })}
          />
        </label>
        <label className="text-amber-100/70 space-y-1">
          Skin
          <input type="color" className="w-full h-8 bg-transparent" value={appearance.skin} onChange={(e) => set({ skin: e.target.value })} />
        </label>
        <label className="text-amber-100/70 space-y-1">
          Hair
          <input type="color" className="w-full h-8 bg-transparent" value={appearance.hair} onChange={(e) => set({ hair: e.target.value })} />
        </label>
        <label className="text-amber-100/70 space-y-1">
          Eyes
          <input type="color" className="w-full h-8 bg-transparent" value={appearance.eyes} onChange={(e) => set({ eyes: e.target.value })} />
        </label>
        <label className="text-amber-100/70 space-y-1">
          Resonance accent
          <input type="color" className="w-full h-8 bg-transparent" value={appearance.accent} onChange={(e) => set({ accent: e.target.value })} />
        </label>
      </div>
      <p className="text-[11px] text-amber-100/50 leading-relaxed">
        Workable mannequin for identity &amp; future Unity handoff. No ripped MMO meshes.
      </p>
    </div>
  );
}
