<script lang="ts">

  export let reels: string[][] = [];
  export let reelGap: number = 8;
  export let maxRows: number = 7;
  export let cellSize: number = 84;

  const symbols = ['A', 'K', 'Q', 'J', '10', '9'];

  function randomReels(count = 6) {
    return Array.from({ length: count }, () => {
      const rows = Math.floor(Math.random() * 4) + 3; // 3-6
      return Array.from({ length: rows }, () => symbols[Math.floor(Math.random() * symbols.length)]);
    });
  }

  if (!reels || reels.length === 0) {
    reels = randomReels();
  }
</script>

<div
  class="grid"
  style="--cellSize:{cellSize}px; --gap:{reelGap}px; --maxRows:{maxRows}; grid-template-columns:repeat({reels.length}, 1fr);"
>
  {#each reels as reel}
    <div class="reel">
      {#each reel as symbol}
        <div class="cell">{symbol}</div>
      {/each}
    </div>
  {/each}
</div>

<style>
  .grid {
    display: grid;
    column-gap: var(--gap);
    height: calc(var(--cellSize) * var(--maxRows) + var(--gap) * (var(--maxRows) - 1));
    padding: var(--gap);
    background: #f9f9f9;
    border: 1px solid #ccc;
    border-radius: 6px;
  }
  .reel {
    display: flex;
    flex-direction: column;
    gap: var(--gap);
    align-items: center;
  }
  .cell {
    width: var(--cellSize);
    height: var(--cellSize);
    display: flex;
    align-items: center;
    justify-content: center;
    border: 1px solid #ddd;
    border-radius: 4px;
    background: white;
    font-family: sans-serif;
    font-size: 1.25rem;
    color: #333;
    transition: background 0.2s;
  }
  .cell:hover {
    background: #f0f0f0;
  }
</style>


  // TODO: implement Variable Ways grid component
</script>

<div>VariableWaysGrid placeholder</div>
