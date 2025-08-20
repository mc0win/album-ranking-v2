<script lang="ts">
	import { ScrollArea } from '$lib/components/ui/scroll-area/index.js';
	import { Skeleton } from '$lib/components/ui/skeleton';
	import AlbumCard from './AlbumCard.svelte';
	let { data } = $props();
</script>

{#await data}
	<Skeleton class="w-4xl h-[800px] rounded-lg p-4 " />
{:then data}
	<ScrollArea class="w-4xl h-[800px] rounded-md border p-4">
		{#each data.albums as album, i}
			<AlbumCard data={album} />
		{/each}
	</ScrollArea>
{/await}
