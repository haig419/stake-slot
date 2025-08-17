<script lang="ts">
  import { VariableWaysGrid, spin, finishEvaluation, spinStore, evaluateWays } from "@stake/variable-ways";

  async function handleSpin() {
    await spin(); // sets state -> Spinning, randomizes reels, then Evaluating
    const result = evaluateWays($spinStore.reels); // placeholder evaluator for now
    await finishEvaluation({ totalWin: result.totalWin, wins: result.wins }, result.highlights);
  }
</script>

<div class="dev">
  <div class="hud">
    <button on:click={handleSpin} disabled={$spinStore.state === 'Spinning'}>Spin</button>
    <span>State: {$spinStore.state}</span>
    <span>Last win: {$spinStore.lastWin.totalWin}</span>
  </div>

  <VariableWaysGrid reels={$spinStore.reels} highlights={$spinStore.highlights} />

  {#if $spinStore.lastWin.totalWin > 0}
    <div class="wins">
      <div>Total Win: {$spinStore.lastWin.totalWin}</div>
      <ul>
        {#each $spinStore.lastWin.wins as w}
          <li>{w.symbol} × {w.count} = {w.payout}</li>
        {/each}
      </ul>
    </div>
  {/if}
</div>

<style>
  .dev { display: flex; flex-direction: column; gap: 1rem; padding: 1rem; }
  .hud { display: flex; align-items: center; gap: 1rem; }
  .wins { padding: 0.5rem 0; }
</style>
