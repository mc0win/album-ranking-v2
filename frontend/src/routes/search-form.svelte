<script lang="ts">
	import { defaults, superForm } from 'sveltekit-superforms';
	import { zod4 } from 'sveltekit-superforms/adapters';
	import * as Form from '$lib/components/ui/form/index.js';
	import * as Select from '$lib/components/ui/select/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { searchSchema } from './schema';

	const sources = [
		{
			value: 'discogs-master',
			label: 'Discogs (master)',
			placeholder: 'https://www.discogs.com/master/2129-Boards-Of-Canada-Geogaddi'
		},
		{
			value: 'discogs-release',
			label: 'Discogs (release)',
			placeholder:
				'https://www.discogs.com/release/21697099-Have-A-Nice-Life-Deathconsciousness'
		},
		{
			value: 'spotify',
			label: 'Spotify',
			placeholder: 'https://open.spotify.com/album/6NtqlXVVPSnSUo9Ebg6QQR'
		}
	];

	const form = superForm(defaults(zod4(searchSchema)), {
		validators: zod4(searchSchema),
		SPA: true
	});

	const { form: formData, enhance } = form;
</script>

<form method="POST" use:enhance class="flex w-full max-w-4xl flex-col space-y-4">
	<Form.Field {form} name="source">
		<Form.Control>
			{#snippet children({ props })}
				<Form.Label>Откуда брать</Form.Label>
				<Select.Root type="single" {...props} bind:value={$formData.source}>
					<Select.Trigger class="w-full" {...props}
						>{sources.find((source) => source.value === $formData.source)
							?.label}</Select.Trigger
					>
					<Select.Content>
						{#each sources as source (source.value)}
							<Select.Item value={source.value} label={source.label}
								>{source.label}</Select.Item
							>
						{/each}
					</Select.Content>
				</Select.Root>
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Field {form} name="link">
		<Form.Control>
			{#snippet children({ props })}
				<Form.Label>Ссылка на альбом</Form.Label>
				<Input
					{...props}
					bind:value={$formData.link}
					placeholder={sources.find((source) => source.value === $formData.source)
						?.placeholder}
				/>
			{/snippet}
		</Form.Control>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Button class="h-14" variant="outline">Добавить в круг</Form.Button>
</form>
