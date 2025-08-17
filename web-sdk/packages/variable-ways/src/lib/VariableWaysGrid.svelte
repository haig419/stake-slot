<script lang="ts">
  export let reels: string[][] = [];
  export let reelGap: number = 8;
  export let maxRows: number = 7;
  export let cellSize: number = 84;
  export let highlights: Array<{ reel: number; row: number }> = [];

  const symbols = ["A", "K", "Q", "J", "10", "9"];

  function randomReels(count = 6) {
    return Array.from({ length: count }, () => {
      const rows = Math.floor(Math.random() * 4) + 3; // 3–6
      return Array.from({ length: rows }, () => symbols[Math.floor(Math.random() * symbols.length)]);
    });
  }

  if (!reels || reels.length === 0) {
    reels = randomReels();
  }

  function isWinCell(r: number, row: number) {
    return highlights.some((h) => h.reel === r && h.row === row);
  }
</script>

<div
  class="grid"
  style="--cellSize:{cellSize}px; --gap:{reelGap}px; --maxRows:{maxRows}; grid-template-columns: repeat({reels.length}, 1fr);"
>
  {#each reels as reel, r}
    <div class="reel">
      {#each reel as symbol, row}
        <div class="cell" class:win={isWinCell(r, row)}>{symbol}</div>
      {/each}
    </div>
  {/each}
</div>

<style>
  .grid {
    display: grid;
    gap: var(--gap);
    padding: calc(var(--cellSize) * 0.25);
    border: 1px solid #ccc;
    border-radius: 10px;
    background: #fff;
  }
  .reel {
    display: flex;
    flex-direction: column;
    gap: var(--gap);
  }
  .cell {
    width: var(--cellSize);
    height: var(--cellSize);
    display: grid;
    place-items: center;
    border: 1px solid #a0a0a0;
    border-radius: 10px;
    background: #fafafa;
    font-family: system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
    font-size: 1.1rem;
    color: #333;
    transition: background 0.2s;
  }
  .cell:hover {
    background: #f0f0f0;
  }
  .cell.win {
    outline: 2px solid var(--win-outline, #55ff99);
    animation: flash 300ms ease-in-out 3;
  }
  @keyframes flash {
    0%, 100% { filter: none; }
    50% { filter: brightness(1.5); }
  }
</style>
