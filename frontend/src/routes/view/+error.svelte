<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import { navbarVisible } from '$lib/stores';
	import { page } from '$app/stores';
	navbarVisible.set(true);
	let status = $page.status;
</script>

<svelte:head>
	<title>Error - {status}</title>
</svelte:head>
<h1 class="text-6xl text-center">{status}</h1>

{#if status === 404}
	<p class="text-center">
		De quiz die je zocht is verdwenen of heeft zelfs nooit bestaan. Wie zal het zeggen?
	</p>
{:else}
	<p>
		Dit zou niet mogen gebeuren. Het is waarschijnlijk mijn schuld, niet de jouwe, maar misschien heb je een magische kracht om dingen kapot te maken ...
	</p>
{/if}

<div class="flex justify-center mt-8">
	<img
		class="rounded-lg"
		src="https://http.cat/{status}"
		alt="Cat representing the {status}-http error code"
	/>
</div>
