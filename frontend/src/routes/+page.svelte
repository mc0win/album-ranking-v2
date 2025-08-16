<script lang="ts">
	import * as Tabs from '$lib/components/ui/tabs/index.js';
	import SearchForm from './search-form.svelte';
	import SunIcon from '@lucide/svelte/icons/sun';
	import MoonIcon from '@lucide/svelte/icons/moon';
	import { toggleMode } from 'mode-watcher';
	import { Button } from '$lib/components/ui/button/index.js';
</script>

<div class="flex flex-col items-center space-y-4 p-2">
	<Button onclick={toggleMode} variant="outline" size="icon" class="h-12 w-full max-w-4xl">
		<SunIcon
			class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 !transition-all dark:-rotate-90 dark:scale-0"
		/>
		<MoonIcon
			class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 !transition-all dark:rotate-0 dark:scale-100"
		/>
		<span class="sr-only">Toggle theme</span>
	</Button>
	<SearchForm />
</div>
