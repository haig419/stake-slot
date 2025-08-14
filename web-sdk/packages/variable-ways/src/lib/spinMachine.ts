import { writable, get } from 'svelte/store';

const symbols = ['A', 'K', 'Q', 'J', '10', '9'];

function generateReels(count = 6, minRows = 3, maxRows = 6): string[][] {
  return Array.from({ length: count }, () => {
    const rows = Math.floor(Math.random() * (maxRows - minRows + 1)) + minRows;
    return Array.from({ length: rows }, () => symbols[Math.floor(Math.random() * symbols.length)]);
  });
}

function evaluateWays(reels: string[][]) {
  const target = reels[0]?.[0];
  if (!target) return { totalWin: 0, wins: [] };
  let count = 0;
  for (const reel of reels) {
    if (reel.includes(target)) count++;
    else break;
  }
  if (count >= 3) {
    const payout = count * 2;
    return { totalWin: payout, wins: [{ symbol: target, count, payout }] };
  }
  return { totalWin: 0, wins: [] };
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
