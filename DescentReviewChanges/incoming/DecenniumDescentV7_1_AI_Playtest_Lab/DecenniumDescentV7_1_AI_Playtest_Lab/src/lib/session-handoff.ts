/** Encounter pack → Session tab bridge (localStorage, same origin). */

export const SESSION_HANDOFF_KEY = "dd_session_encounter_handoff";

export type EncounterHandoffSource = "encounters" | "generators" | "dungeon-guide";

export type EncounterHandoff = {
  tier: number;
  tierName: string;
  boss: string;
  floors: string;
  brief: string;
  source: EncounterHandoffSource;
  createdAt: number;
};

export function pushEncounterHandoff(payload: Omit<EncounterHandoff, "createdAt">): void {
  if (typeof window === "undefined") return;
  const full: EncounterHandoff = { ...payload, createdAt: Date.now() };
  localStorage.setItem(SESSION_HANDOFF_KEY, JSON.stringify(full));
}

export function peekEncounterHandoff(): EncounterHandoff | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(SESSION_HANDOFF_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as EncounterHandoff;
  } catch {
    return null;
  }
}

export function consumeEncounterHandoff(): EncounterHandoff | null {
  return takeEncounterHandoff(0);
}

/** Idempotent take — skips handoffs with `createdAt` ≤ `sinceCreatedAt` (avoids double-apply on mount + tick). */
export function takeEncounterHandoff(sinceCreatedAt = 0): EncounterHandoff | null {
  const data = peekEncounterHandoff();
  if (!data || data.createdAt <= sinceCreatedAt) return null;
  localStorage.removeItem(SESSION_HANDOFF_KEY);
  return data;
}

/** Items Library → Session reference-preview bridge. It never updates inventory. */

export const SESSION_ITEM_HANDOFF_KEY = "dd_session_item_handoff";

export type ItemHandoffSource = "items-crafted" | "items-dropped";

export type ItemHandoff = {
  name: string;
  rarity: string;
  category: string;
  tier: number;
  description: string;
  source: ItemHandoffSource;
  createdAt: number;
};

export function pushItemHandoff(payload: Omit<ItemHandoff, "createdAt">): void {
  if (typeof window === "undefined") return;
  const full: ItemHandoff = { ...payload, createdAt: Date.now() };
  localStorage.setItem(SESSION_ITEM_HANDOFF_KEY, JSON.stringify(full));
}

export function peekItemHandoff(): ItemHandoff | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(SESSION_ITEM_HANDOFF_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as ItemHandoff;
  } catch {
    return null;
  }
}

/** Idempotent take — skips previews already applied via matching `createdAt`. */
export function takeItemHandoff(sinceCreatedAt = 0): ItemHandoff | null {
  const data = peekItemHandoff();
  if (!data || data.createdAt <= sinceCreatedAt) return null;
  localStorage.removeItem(SESSION_ITEM_HANDOFF_KEY);
  return data;
}

/** Bestiary foe → Session bridge. The Session tracker preserves the source name, HP, CR, and zone. */

export const SESSION_FOE_HANDOFF_KEY = "dd_session_foe_handoff";

export type FoeHandoff = {
  name: string;
  hitPoints?: number;
  challengeRating?: string;
  zoneFound?: string;
  createdAt: number;
};

export function pushFoeHandoff(payload: Omit<FoeHandoff, "createdAt">): void {
  if (typeof window === "undefined") return;
  const full: FoeHandoff = { ...payload, createdAt: Date.now() };
  localStorage.setItem(SESSION_FOE_HANDOFF_KEY, JSON.stringify(full));
}

export function peekFoeHandoff(): FoeHandoff | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(SESSION_FOE_HANDOFF_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as FoeHandoff;
  } catch {
    return null;
  }
}

/** Idempotent take — skips a foe already applied via its matching `createdAt`. */
export function takeFoeHandoff(sinceCreatedAt = 0): FoeHandoff | null {
  const data = peekFoeHandoff();
  if (!data || data.createdAt <= sinceCreatedAt) return null;
  localStorage.removeItem(SESSION_FOE_HANDOFF_KEY);
  return data;
}

/** Spell Library → Session cast-preview bridge. This stages reference fields only; it never spends RP. */

export const SESSION_SPELL_HANDOFF_KEY = "dd_session_spell_handoff";

export type SpellHandoff = {
  name: string;
  level: number;
  school: string;
  castingTime: string;
  range: string;
  duration: string;
  createdAt: number;
};

export function pushSpellHandoff(payload: Omit<SpellHandoff, "createdAt">): void {
  if (typeof window === "undefined") return;
  const full: SpellHandoff = { ...payload, createdAt: Date.now() };
  localStorage.setItem(SESSION_SPELL_HANDOFF_KEY, JSON.stringify(full));
}

export function peekSpellHandoff(): SpellHandoff | null {
  if (typeof window === "undefined") return null;
  try {
    const raw = localStorage.getItem(SESSION_SPELL_HANDOFF_KEY);
    if (!raw) return null;
    return JSON.parse(raw) as SpellHandoff;
  } catch {
    return null;
  }
}

/** Idempotent take — skips a preview already applied via its matching `createdAt`. */
export function takeSpellHandoff(sinceCreatedAt = 0): SpellHandoff | null {
  const data = peekSpellHandoff();
  if (!data || data.createdAt <= sinceCreatedAt) return null;
  localStorage.removeItem(SESSION_SPELL_HANDOFF_KEY);
  return data;
}
