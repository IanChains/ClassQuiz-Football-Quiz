<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import type { PageData } from './$types';
	import { getLocalization } from '$lib/i18n';

	export let data: PageData;

	let showresults = false;
	let checkedQuizzes = new Set<string>();
	let scores: Record<string, number> = {};
	let usernames: string[] = [];

	function handleScoreButtonClick() {
		if (checkedQuizzes.size < 2) {
			alert("Je moet minimaal 2 vakjes aanduiden!");
			return;
		}

		scores = {};
		usernames = [];

		checkedQuizzes.forEach(quizId => {
			const result = data.results.find(r => r.id === quizId);
			if (result) {
				for (const [username, score] of Object.entries(result.player_scores)) {
					const numericScore = parseInt(score);
					if (!scores[username]) {
						scores[username] = 0;
						usernames.push(username);
					}
					scores[username] += numericScore;
				}
			}
		});

		showresults = true;
		
	}

	function toggleCheckbox(quizId: string, checked: boolean) {
		if (checked) {
			checkedQuizzes.add(quizId);
		} else {
			checkedQuizzes.delete(quizId);
		}
	}
</script>

<svelte:head>
	<title>Quiz Results</title>
</svelte:head>

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
						<th class="mx-auto p-1" style="max-width:50px">
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
								<input type="checkbox" class="mx-auto flex" style="height:20px;width:20px;" id="totale_result" name="totale_result" value={result.id} on:change={e => toggleCheckbox(result.id, e.target.checked)}>
							</td>
						</tr>
					{/each}
				</table>
				{#if showresults}
					<div class="w-full" style="margin-top:175px;">
						<div class="flex justify-center w-full">
							<h2 class="font-bold mb-6" style="font-size:3rem">Totale Scores (Gekozen Quizzen):</h2>
							<table class="w-11/12 m-auto">
								<tr class="border-b-2 border-gray-500 text-left">
									<th class="border-r border-gray-500 p-1 mx-auto"
										>Naam Speler
									</th>
									<th class="p-1 mx-auto">Speler Score</th>
								</tr>
								{#each usernames as uname}
									<tr class="text-left">
										<td class="border-r border-gray-500 p-1">{uname}</td>
										<td class="p-1">{scores[uname]}</td>
									</tr>
								{/each}
							</table>
						</div>
					</div>
				{/if}
			{/if}
		</div>
	</div>
</div>
