<script lang="ts">
	import Sortable from 'sortablejs';
	import { onMount } from 'svelte';
	import type { Track } from './schemas';

	const useSortable = (getter: () => HTMLElement | null, options?: Sortable.Options) => {
		$effect(() => {
			const sortableEl = getter();
			const sortable = sortableEl ? Sortable.create(sortableEl, options) : null;
			return () => sortable;
		});
	};

	let { data, value = $bindable([]), prop } = $props();

	let sortable = $state<HTMLElement | null>(null);

	async function getTracks() {
		return data;
	}
	onMount(() => {
		getTracks().then((tracks) => {
			value = tracks.map((track: Track) => track.id);
		});

		useSortable(() => sortable, {
			onEnd(evt) {
				let ids = [];
				const children = evt.target.children;
				let i = 1;
				for (let item of children) {
					const string_id = item.getAttribute('data-id');
					ids.push(parseInt(!(string_id === null) ? string_id : ''));
					item.children[0].innerHTML = i.toString();
					i++;
				}
				value = ids;
			}
		});
	});
</script>

<input class="invisible hidden" bind:value {...prop} />
{#await data}
	<div></div>
{:then tracks}
	<div class="pb-2 pt-2">
		<div class="border-accent-foreground rounded-lg border">
			<div bind:this={sortable}>
				{#each tracks as track, i}
					<div
						data-id={i}
						class="border-accent-foreground flex h-12 cursor-grab [&:not(:last-child)]:border-b"
					>
						<div
							class="border-accent-foreground flex h-12 w-12 items-center justify-center border-r text-xl"
						>
							{i + 1}
						</div>
						<div class="flex items-center pl-4">
							{track.track_name}
						</div>
					</div>
				{/each}
			</div>
		</div>
	</div>
{/await}
