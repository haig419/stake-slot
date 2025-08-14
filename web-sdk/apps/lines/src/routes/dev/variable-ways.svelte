<script lang="ts">
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
</style>

</script>

<VariableWaysGrid />

