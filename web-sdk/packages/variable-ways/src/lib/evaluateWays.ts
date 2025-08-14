import type { WinDetail, Highlight } from './spinMachine';

export interface EvaluateResult {
  totalWin: number;
  wins: WinDetail[];
  highlights: Highlight[];
}

export function evaluateWays(reels: string[][]): EvaluateResult {
  if (!reels.length || !reels[0].length) {
    return { totalWin: 0, wins: [], highlights: [] };
  }
  const target = reels[0][0];
  const highlights: Highlight[] = [];
  let count = 0;
  for (let r = 0; r < reels.length; r++) {
    const row = reels[r].findIndex((s) => s === target);
    if (row === -1) break;
    highlights.push({ reel: r, row });
    count++;
  }
  if (count >= 3) {
    return {
      totalWin: count * 1,
      wins: [{ symbol: target, count, payout: count * 1 }],
      highlights,
    };
  }
  return { totalWin: 0, wins: [], highlights: [] };
}
