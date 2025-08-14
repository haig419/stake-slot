import { writable, get } from 'svelte/store';
import { evaluateWays } from './evaluateWays';

const symbols = ['A', 'K', 'Q', 'J', '10', '9'];

function generateReels(count = 6, minRows = 3, maxRows = 6): string[][] {
  return Array.from({ length: count }, () => {
    const rows = Math.floor(Math.random() * (maxRows - minRows + 1)) + minRows;
    return Array.from({ length: rows }, () => symbols[Math.floor(Math.random() * symbols.length)]);
  });
}

export type SpinState = 'Idle' | 'Spinning' | 'Evaluating' | 'ShowingWin';

export interface WinDetail {
  symbol: string;
  count: number;
  payout: number;
}

export interface Highlight {
  reel: number;
  row: number;
}

export interface SpinMachineState {
  state: SpinState;
  reels: string[][];
  lastWin: { totalWin: number; wins: WinDetail[] };
  highlights: Highlight[];
}

const initialReels = generateReels();

export const spinStore = writable<SpinMachineState>({
  state: 'Idle',
  reels: initialReels,
  lastWin: { totalWin: 0, wins: [] },
  highlights: []
});

export async function spin() {
  spinStore.update(() => ({
    state: 'Spinning',
    reels: generateReels(),
    lastWin: { totalWin: 0, wins: [] },
    highlights: []
  }));
  await new Promise((resolve) => setTimeout(resolve, 900));
  spinStore.update((s) => ({ ...s, state: 'Evaluating' }));
}

export async function finishEvaluation(
  win?: { totalWin: number; wins: WinDetail[] },
  highlights?: Highlight[]
) {
  if (!win) {
    const result = evaluateWays(get(spinStore).reels);
    spinStore.update((s) => ({
      ...s,
      state: 'ShowingWin',
      lastWin: { totalWin: result.totalWin, wins: result.wins },
      highlights: result.highlights,
    }));
  } else {
    spinStore.update((s) => ({
      ...s,
      state: 'ShowingWin',
      lastWin: win,
      highlights: highlights ?? [],
    }));
  }
  await new Promise((resolve) => setTimeout(resolve, 1500));
  spinStore.update((s) => ({ ...s, state: 'Idle' }));
}
