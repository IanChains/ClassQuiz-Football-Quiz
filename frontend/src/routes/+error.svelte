<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import { navbarVisible } from '$lib/stores';
	import { page } from '$app/stores';
	import { getLocalization } from '$lib/i18n';

	navbarVisible.set(true);
	let status = $page.status;
	const { t } = getLocalization();
</script>

<svelte:head>
	<title>Error - {status}</title>
</svelte:head>
<h1 class="text-6xl text-center">{status}</h1>

{#if status === 404}
	<p class="text-center">
		De pagina die je zocht is verdwenen of heeft zelfs nooit bestaan. Wie zal het zeggen?
	</p>
{:else}
	<p class="text-center">
		Oei, er is iets misgegaan. Deze pagina is opgegaan in de mist!
	</p>
{/if}

<div class="flex justify-center mt-8">
	<img
		class="rounded-lg"
		src="https://http.cat/{status}"
		alt="Cat representing the {status}-http error code"
	/>
</div>
