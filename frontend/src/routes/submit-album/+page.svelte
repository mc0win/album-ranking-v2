<script lang="ts">
	import SubmitForm from '../components/SubmitForm.svelte';
	import type { PageProps } from './$types';

	let { data }: PageProps = $props();
</script>

<div class="flex flex-col items-center space-y-4 p-2">
	<SubmitForm {data} />
</div>
