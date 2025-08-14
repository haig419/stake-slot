import { writable, get } from 'svelte/store';
import { evaluateVariableWays } from '@stake/math-sdk';

const symbols = ['A', 'K', 'Q', 'J', '10', '9'];

function generateReels(count = 6, minRows = 3, maxRows = 6): string[][] {
  return Array.from({ length: count }, () => {
    const rows = Math.floor(Math.random() * (maxRows - minRows + 1)) + minRows;
    return Array.from({ length: rows }, () => symbols[Math.floor(Math.random() * symbols.length)]);
  });
}

function evaluateWays(reels: string[][]) {
  const board = reels.map((reel) => reel.map((symbol) => ({ symbol })));
  const result = evaluateVariableWays({ board } as any);
  return {
    totalWin: result.totalWin ?? 0,
    wins: (result.wins ?? []).map((w: any) => ({
      symbol: w.symbol,
      count: w.count,
      payout: w.payout,
    })),
  };
}

export type SpinState = 'Idle' | 'Spinning' | 'Evaluating' | 'ShowingWin';

export interface WinDetail {
  symbol: string;
  count: number;
  payout: number;
}

export interface SpinMachineState {
  state: SpinState;
  reels: string[][];
  lastWin: { totalWin: number; wins: WinDetail[] };
}

const initialReels = generateReels();

export const spinStore = writable<SpinMachineState>({
  state: 'Idle',
  reels: initialReels,
  lastWin: { totalWin: 0, wins: [] }
});

export async function spin() {
  spinStore.update(() => ({
    state: 'Spinning',
    reels: generateReels(),
    lastWin: { totalWin: 0, wins: [] }
  }));
  await new Promise((resolve) => setTimeout(resolve, 900));
  spinStore.update((s) => ({ ...s, state: 'Evaluating' }));
}

export async function finishEvaluation(win?: { totalWin: number; wins: WinDetail[] }) {
  const result = win ?? evaluateWays(get(spinStore).reels);
  spinStore.update((s) => ({ ...s, state: 'ShowingWin', lastWin: result }));
  await new Promise((resolve) => setTimeout(resolve, 1500));
  spinStore.update((s) => ({ ...s, state: 'Idle' }));
}
