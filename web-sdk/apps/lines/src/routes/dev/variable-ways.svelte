<script lang="ts">
  import { VariableWaysGrid, spin, finishEvaluation, spinStore } from "@stake/variable-ways";

  async function handleSpin() {
    await spin();
    await finishEvaluation();
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
