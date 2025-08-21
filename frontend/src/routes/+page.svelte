<script lang="ts">
	import SunIcon from '@lucide/svelte/icons/sun';
	import MoonIcon from '@lucide/svelte/icons/moon';
	import { toggleMode } from 'mode-watcher';
	import * as Tabs from '$lib/components/ui/tabs/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import RankingForm from './components/RankingForm.svelte';
	import SubmitForm from './components/SubmitForm.svelte';
	import type { PageProps } from './$types';
	import WatchPage from './components/WatchPage.svelte';

	let { data }: PageProps = $props();
</script>

<div class="flex flex-col items-center space-y-4 p-2">
	<Button onclick={toggleMode} variant="outline" size="icon" class="w-full max-w-4xl">
		<SunIcon
			class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 !transition-all dark:-rotate-90 dark:scale-0"
		/>
		<MoonIcon
			class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 !transition-all dark:rotate-0 dark:scale-100"
		/>
		<span class="sr-only">Toggle theme</span>
	</Button>
	<div class="flex w-full max-w-4xl justify-evenly space-x-4">
		<Tabs.Root value="ranking" class="relative w-full">
			<Tabs.List class="bg-background dark:bg-input/30 w-full shadow-sm">
				<Tabs.Trigger value="ranking" class="w-1/3">Оценить альбом</Tabs.Trigger>
				<Tabs.Trigger value="submit" class="w-1/3">Добавить альбом</Tabs.Trigger>
				<Tabs.Trigger value="watch" class="w-1/3">Посмотреть оценки</Tabs.Trigger>
			</Tabs.List>
			<Tabs.Content value="ranking">
				<RankingForm {data} />
			</Tabs.Content>
			<Tabs.Content value="submit">
				<SubmitForm {data} />
			</Tabs.Content>
			<Tabs.Content value="watch">
				<WatchPage {data} />
			</Tabs.Content>
		</Tabs.Root>
	</div>
</div>
