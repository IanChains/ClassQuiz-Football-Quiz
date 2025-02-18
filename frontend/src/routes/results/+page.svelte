<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import type { PageData } from './$types';
	import { getLocalization } from '$lib/i18n';

	export let data: PageData;

	let checkedCount = 0;

	function handleScoreButtonClick() {
		const checkboxes = document.querySelectorAll('input[name="totale_result"]');
		checkedCount = Array.from(checkboxes).filter(checkbox => checkbox.checked).length;

		if (checkedCount === 0) {
			alert("Je moet een aantal vakjes aanduiden!");
		} else {
			alert(`Je hebt ${checkedCount} vakjes aangeduid!`);
		}
	}
</script>

<div class="w-full">
	<div class="flex justify-center w-full">
		<div class="w-11/12 m-auto">
			{#if data.results.length === 0}
				<p class="text-center text-3xl mt-8">Er zijn nog geen resultaten gevonden ...</p>
			{:else}
				<table class="w-full">
					<tr class="border-b-2 border-gray-500 text-left">
						<th class="border-r border-gray-500 p-1 mx-auto"
							>Quiz Titel
						</th>
						<th class="border-r border-gray-500 p-1 mx-auto"
							>Datum Gespeeld
						</th>
						<th class="border-r border-gray-500 p-1 mx-auto"
							>Aantal Speler
						</th>
						<th class="border-r border-gray-500 p-1 mx-auto">Notitie</th>
						<th class="mx-auto p-1">
							<button type="button" class="mx-auto p-1" id="totale_score_button" on:click={handleScoreButtonClick}>Totale Score (Click Me!)</button>
						</th>
					</tr>
					{#each data.results as result}
						<tr class="text-left">
							<td class="border-r border-gray-500 p-1"
								><a href="/results/{result.id}" class="underline text-lg"
									>{result.title}</a
								></td
							>
							<td class="border-r border-gray-500 p-1"
								>{new Date(result.timestamp).toLocaleString()}</td
							>
							<td class="border-r border-gray-500 p-1"
								>{Object.keys(result.player_scores).length}</td
							>
							<td class="border-r border-gray-500 p-1">
								{#if result.note}
									{result.note}
								{:else}
									‎ 
								{/if}
							</td>
							<td class="p-1">
								<input type="checkbox" class="mx-auto flex" style="height:20px;width:20px;" id="totale_result" name="totale_result" value="checked">
							</td>
						</tr>
					{/each}
				</table>
			{/if}
		</div>
	</div>
</div>
