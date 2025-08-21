<script lang="ts">
	import { ScrollArea } from '$lib/components/ui/scroll-area/index.js';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import AlbumCard from './AlbumCard.svelte';
	let { data } = $props();
</script>

{#await data}
	<Skeleton class="w-4xl bg-background dark:bg-input/30 h-[800px] rounded-lg p-4" />
{:then data}
	{#await data.albums then albums}
		{#if !(typeof albums === 'string')}
			<ScrollArea class="w-4xl h-[800px] rounded-md border p-8">
				<div
					role="grid"
					class="grid grid-cols-4 items-center gap-20 p-10"
				>
					{#each albums as album, i}
						{console.log(album)}
						<AlbumCard id={i} data={album} />
					{/each}
				</div>
			</ScrollArea>
		{:else}
			<p class="w-full max-w-4xl text-center text-gray-500 select-none">{albums}</p>
		{/if}
	{/await}
{/await}
