/** Pure reference helpers for the staged Bard draft; not connected to saved characters. */
export type BardState = {
  crescendo: number;
  lastPerformance: string | null;
  gainedThisTurn: number;
  rp: number;
  dissonance: number;
};

export type BardCard = {
  id: string;
  band: string;
  path: string | null;
  kind: string;
  minimumClassLevel: number;
  acquisition: string;
  tags: string[];
  resourceCost: { rp: number; maintenanceRp: number; crescendo: string };
};

export function songDice(bardLevel: number): number {
  if (!Number.isInteger(bardLevel) || bardLevel < 1 || bardLevel > 20) throw new Error('Bard level must be 1–20');
  return bardLevel >= 17 ? 4 : bardLevel >= 11 ? 3 : bardLevel >= 5 ? 2 : 1;
}

export function canSelectBardFeature(card: BardCard, bardLevel: number, heroPath: string | null, known: ReadonlySet<string>, bands: readonly string[]): boolean {
  return card.acquisition === 'selection'
    && card.minimumClassLevel <= bardLevel
    && !known.has(card.id)
    && bands.includes(card.band)
    && (card.path === null || (bardLevel >= 10 && card.path === heroPath));
}

// Call only after validating known feature, level, target, voice, action and recharge.
export function startBardPerformance(state: BardState, card: BardCard, options: { ownTurn?: boolean; accelerated?: boolean } = {}): { state: BardState; spent: number; enhanced: boolean } {
  if (!card.tags.includes('performance')) throw new Error('Only a started Bard Performance uses this helper');
  if (!Number.isInteger(state.crescendo) || state.crescendo < 0 || state.crescendo > 5) throw new Error('Invalid Crescendo');
  if (state.rp < card.resourceCost.rp) throw new Error('Insufficient RP; no costs or stacks spent');
  const minimum = card.resourceCost.crescendo === 'spend-all-minimum-3' ? 3 : card.resourceCost.crescendo === 'spend-all-minimum-5' ? 5 : 0;
  if (state.crescendo < minimum) throw new Error('Insufficient Crescendo; no costs spent');
  const spent = minimum > 0 || state.crescendo === 5 ? state.crescendo : 0;
  const enhanced = spent === 5;
  const next = { ...state, rp: state.rp - card.resourceCost.rp, lastPerformance: card.id };
  if (spent) {
    next.crescendo = 0;
    if (enhanced) next.dissonance = Math.max(0, state.dissonance - 2);
  } else if (options.ownTurn !== false && state.lastPerformance !== card.id) {
    // The caller may authorize accelerated gain only when an explicit card's conditions hold.
    const ceiling = options.accelerated ? 2 : 1;
    const gain = Math.max(0, Math.min(ceiling - state.gainedThisTurn, 5 - state.crescendo));
    next.crescendo += gain;
    next.gainedThisTurn += gain;
  }
  return { state: next, spent, enhanced };
}

export function beginBardTurn(state: BardState): BardState {
  return { ...state, gainedThisTurn: 0 };
}

export function breakBardRhythm(state: BardState, cause: 'damage' | 'silence' | 'incapacitated' | 'concentration' | 'encounter-end', fluidTempo = false): BardState {
  if (cause === 'damage' && fluidTempo) return { ...state };
  // RP and Dissonance survive encounter boundaries; this is not a free rest.
  return { ...state, crescendo: 0, lastPerformance: null };
}

export function copiedEchoAmount(originalUnmodifiedDice: number, fractions: readonly number[]): number {
  if (!Number.isInteger(originalUnmodifiedDice) || originalUnmodifiedDice < 0 || fractions.some(x => !Number.isFinite(x) || x < 0)) throw new Error('Invalid Echo amount');
  const fraction = Math.min(1, fractions.reduce((sum,x) => sum+x,0));
  if (!originalUnmodifiedDice || !fraction) return 0;
  return Math.min(Math.floor(originalUnmodifiedDice), Math.max(1, Math.floor(originalUnmodifiedDice * fraction)));
}

export function shortenBardRecharge(counter: number, alreadyResetThisRound: boolean, amount: number | 'reset'): { counter: number; resetUsed: boolean } {
  if (alreadyResetThisRound || counter <= 0) return { counter, resetUsed: alreadyResetThisRound };
  if (amount !== 'reset' && (!Number.isFinite(amount) || amount <= 0)) throw new Error('Positive shortening required');
  return { counter: amount === 'reset' ? 0 : Math.max(0, counter-amount), resetUsed: true };
}
