<script lang="ts" module>
import { defineMeta } from '@storybook/addon-svelte-csf';

import { VariableWaysGrid } from '@stake/variable-ways';

const { Story } = defineMeta({
    title: 'VariableWays/VariableWaysGrid',
    component: VariableWaysGrid,
    parameters: {

        docs: { description: { component: 'Spin flow uses a placeholder evaluator and highlights wins.' } }
    },

        docs: { description: { component: 'Spin uses Math SDK ways evaluation for accurate results.' } }
    },


import { VariableWaysGrid } from '@stake/variable-ways';


const { Story } = defineMeta({
    title: 'VariableWays/VariableWaysGrid',
    component: VariableWaysGrid,


    args: {
        reelCount: 6,
        minRows: 3,
        maxRows: 6,
        cellSize: 80,
        gap: 8,
    },
    argTypes: {
        reelCount: { control: { type: 'number', min: 3, max: 8 } },
        minRows: { control: { type: 'number', min: 2, max: 7 } },
        maxRows: { control: { type: 'number', min: 3, max: 9 } },
        cellSize: { control: { type: 'number', min: 48, max: 128 } },
        gap: { control: { type: 'number', min: 0, max: 16 } },
    },
});
</script>

<script lang="ts">
import { onMount } from 'svelte';

import { VariableWaysGrid, spin, finishEvaluation, spinStore } from '@stake/variable-ways';
import { evaluateWays } from '@stake/variable-ways';


import { VariableWaysGrid, spin, finishEvaluation, spinStore } from '@stake/variable-ways';



import { VariableWaysGrid, spin, finishEvaluation, spinStore } from '@stake/variable-ways';

import { VariableWaysGrid } from '@stake/variable-ways';



const SYMBOLS = ['A', 'K', 'Q', 'J', '10', '9'];

export let reelCount: number;
export let minRows: number;
export let maxRows: number;
export let cellSize: number;
export let gap: number;



let reels: string[][] = [];
  


function generateReels(reelsCount: number, min: number, max: number): string[][] {
    return Array.from({ length: reelsCount }, () => {
        const rows = Math.floor(Math.random() * (max - min + 1)) + min;
        return Array.from({ length: rows }, () => SYMBOLS[Math.floor(Math.random() * SYMBOLS.length)]);
    });
}

function randomize(args = { reelCount, minRows, maxRows }) {



    const r = generateReels(args.reelCount, args.minRows, args.maxRows);
    spinStore.update((s) => ({ ...s, reels: r }));
}

async function handleSpin() {
    await spin();

    const result = evaluateWays($spinStore.reels);
    await finishEvaluation({ totalWin: result.totalWin, wins: result.wins }, result.highlights);

    await finishEvaluation();


    reels = generateReels(args.reelCount, args.minRows, args.maxRows);



}

onMount(() => {
    randomize();
});
</script>

{#snippet template(args)}
<div style="display:flex; flex-direction:column; gap:8px; padding:16px;">

    <div style="display:flex; gap:8px; align-items:center;">
        <button on:click={() => randomize(args)}>Randomize</button>
        <button on:click={handleSpin}>Spin</button>
        <span>State: {$spinStore.state}</span>


    <div style="display:flex; gap:8px; align-items:center;">
        <button on:click={() => randomize(args)}>Randomize</button>
        <button on:click={handleSpin}>Spin</button>

        {#if $spinStore.lastWin.totalWin > 0}
            <span>Win: {$spinStore.lastWin.totalWin}</span>
        {/if}
    </div>

    <VariableWaysGrid reels={$spinStore.reels} highlights={$spinStore.highlights} cellSize={args.cellSize} reelGap={args.gap} />

    <VariableWaysGrid reels={$spinStore.reels} cellSize={args.cellSize} reelGap={args.gap} />


    <button on:click={() => randomize(args)}>Randomize</button>
    <VariableWaysGrid reels={reels} cellSize={args.cellSize} reelGap={args.gap} />



</div>
{/snippet}

<Story name="Playground" {template} />

<Story name="SixReelsVariableHeights">
    {#snippet template()}
        {@const reels = generateReels(6, 3, 6)}
        <div style="padding:16px;">
            <VariableWaysGrid {reels} cellSize={80} reelGap={8} />
        </div>
    {/snippet}
</Story>

<Story name="AllMinHeights">
    {#snippet template()}
        {@const reels = generateReels(6, 3, 3)}
        <div style="padding:16px;">
            <VariableWaysGrid {reels} cellSize={80} reelGap={8} />
        </div>
    {/snippet}
</Story>

<Story name="AllMaxHeights">
    {#snippet template()}
        {@const reels = generateReels(6, 6, 6)}
        <div style="padding:16px;">
            <VariableWaysGrid {reels} cellSize={80} reelGap={8} />
        </div>
    {/snippet}
</Story>

<Story name="DeterministicCase">
    {#snippet template()}
        {@const reels = [
            ['A', 'K', 'Q'],
            ['J', '10', '9', 'A'],
            ['K', 'Q', 'J', '10'],
            ['Q', 'J', '10', '9', 'A'],
            ['9', 'A', 'K'],
            ['10', '9', 'A', 'K'],
        ]}
        <div style="padding:16px;">
            <VariableWaysGrid {reels} cellSize={80} reelGap={8} />
        </div>
    {/snippet}
</Story>
