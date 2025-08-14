<script lang="ts">

  import { VariableWaysGrid, spin, finishEvaluation, spinStore } from "@stake/variable-ways";

  async function handleSpin() {
    await spin();

    await finishEvaluation();


    await finishEvaluation();

    await finishEvaluation({ totalWin: 0, wins: [] });


  }
</script>

<div class="dev">
  <div class="controls">
    <button on:click={handleSpin}>Spin</button>
    <span>State: {$spinStore.state}</span>
  </div>
  <VariableWaysGrid reels={$spinStore.reels} />
  {#if $spinStore.lastWin.totalWin > 0}

    <div class="wins">
      <div>Total Win: {$spinStore.lastWin.totalWin}</div>
      <ul>
        {#each $spinStore.lastWin.wins as w}
          <li>{w.symbol} x{w.count} = {w.payout}</li>
        {/each}
      </ul>
    </div>
  {/if}

    <div>Total Win: {$spinStore.lastWin.totalWin}</div>
  {/if}


  import { VariableWaysGrid } from "@stake/variable-ways";

  const symbols = ['A', 'K', 'Q', 'J', '10', '9'];
  let reels: string[][] = [];

  function randomize() {
    const reelCount = 6;
    reels = Array.from({ length: reelCount }, () => {
      const rows = Math.floor(Math.random() * 4) + 3; // 3-6
      return Array.from({ length: rows }, () => symbols[Math.floor(Math.random() * symbols.length)]);
    });
  }

  randomize();
</script>

<div class="dev">
  <button on:click={randomize}>Randomize</button>
  <VariableWaysGrid {reels} />



</div>

<style>
  .dev {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    padding: 1rem;
  }


  .controls {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
</style>


</style>

</script>

<VariableWaysGrid />


