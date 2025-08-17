import { writable, get, type Writable } from "svelte/store";
import { evaluateWays } from "./evaluateWays";

export type State = "Idle" | "Spinning" | "Evaluating" | "ShowingWin";

export type Highlight = { reel: number; row: number };
export type WinDetail = { symbol: string; count: number; payout: number };

export interface SpinState {
  state: State;
  reels: string[][];
  lastWin: { totalWin: number; wins: WinDetail[] };
  highlights: Highlight[];
}

const symbols = ["A", "K", "Q", "J", "10", "9"];

function randomReels(reelCount = 6, minRows = 3, maxRows = 6): string[][] {
  return Array.from({ length: reelCount }, () =>
    Array.from(
      { length: Math.floor(Math.random() * (maxRows - minRows + 1)) + minRows },
      () => symbols[Math.floor(Math.random() * symbols.length)]
    )
  );
}

function createSpinStore(): Writable<SpinState> {
  return writable<SpinState>({
    state: "Idle",
    reels: randomReels(),
    lastWin: { totalWin: 0, wins: [] },
    highlights: [],
  });
}

export const spinStore = createSpinStore();

export async function spin(): Promise<void> {
  spinStore.update((s) => ({
    ...s,
    state: "Spinning",
    reels: randomReels(),
    lastWin: { totalWin: 0, wins: [] },
    highlights: [],
  }));
  // simulate reel spin time
  await new Promise((r) => setTimeout(r, 900));
  spinStore.update((s) => ({ ...s, state: "Evaluating" }));
}

export async function finishEvaluation(
  win?: { totalWin: number; wins: WinDetail[] },
  highlights?: Highlight[]
): Promise<void> {
  const reels = get(spinStore).reels;
  const result = win ?? evaluateWays(reels);
  spinStore.update((s) => ({
    ...s,
    state: "ShowingWin",
    lastWin: { totalWin: result.totalWin, wins: result.wins },
    highlights: highlights ?? ("highlights" in result ? (result as any).highlights : []),
  }));
  await new Promise((r) => setTimeout(r, 1500));
  spinStore.update((s) => ({ ...s, state: "Idle" }));
}
