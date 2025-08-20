<script lang="ts">
	import { Skeleton } from '$lib/components/ui/skeleton';
	let { data } = $props();
</script>

<div class="border-muted shadow-card h-[300px] w-[300px]">
	{#await data.albums}
		<Skeleton class="h-full w-full rounded-lg p-4 " />
	{:then album}
		<img alt={album.name} src={album.cover} class="h-full w-full rounded-lg p-4" />
	{/await}
</div>
