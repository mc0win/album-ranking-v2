<script lang="ts">
	import '../app.css';
	import favicon from '$lib/assets/favicon.svg';
	import { Toaster } from '$lib/components/ui/sonner/index.js';
	import { ModeWatcher } from 'mode-watcher';
	import SunIcon from '@lucide/svelte/icons/sun';
	import MoonIcon from '@lucide/svelte/icons/moon';
	import { toggleMode } from 'mode-watcher';
	import { Button } from '$lib/components/ui/button/index.js';
	import * as NavigationMenu from '$lib/components/ui/navigation-menu/index.js';
	let { children } = $props();

	const links = [
		{
			label: 'оценить альбом',
			href: '/'
		},
		{
			label: 'добавить альбом',
			href: '/submit-album'
		},
		{
			label: 'посмотреть оценки',
			href: '/check-rankings'
		}
	];
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
</svelte:head>

<header
	class="bg-background dark:bg-input/30 flex h-20 shrink-0 items-center px-6 shadow-sm mb-4"
>
	<span class="mr-10 flex h-full items-center text-4xl font-black"
		>album ranking.</span
	>
	<NavigationMenu.Root>
		<NavigationMenu.List>
			{#each links as link}
				<NavigationMenu.Item>
					<NavigationMenu.Link
						href={link.href}
						class="flex h-full items-center bg-transparent text-xl font-medium"
						>{link.label}</NavigationMenu.Link
					>
				</NavigationMenu.Item>
			{/each}
		</NavigationMenu.List>
	</NavigationMenu.Root>
	<div class="ml-auto flex h-full items-center gap-2">
		<Button onclick={toggleMode} variant="ghost" size="icon">
			<SunIcon
				class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 !transition-all dark:-rotate-90 dark:scale-0"
			/>
			<MoonIcon
				class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 !transition-all dark:rotate-0 dark:scale-100"
			/>
		</Button>
	</div>
</header>
<Toaster />
<ModeWatcher />
{@render children?.()}
