<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import { getLocalization } from '$lib/i18n';

	const { t } = getLocalization();
	export let scores: {
		[key: string]: string;
	};
	export let custom_field: {
		[key: string]: string;
	};

	let usernames = Object.keys(scores);
	console.log(custom_field);
</script>

<div class="w-full">
	<div class="flex justify-center w-full">
		<table class="w-11/12 m-auto">
			<tr class="border-b-2 border-gray-500 text-left">
				<th class="border-r border-gray-500 p-1 mx-auto"
					>Naam Speler
				</th>
				<th class="p-1 mx-auto">Speler Score</th>
				{#if Object.keys(custom_field).length !== 0}
					<th class="border-l border-gray-500 p-1 mx-auto"
						>Aangepast Veld
					</th>
				{/if}
			</tr>
			{#each usernames as uname}
				<tr class="text-left">
					<td class="border-r border-gray-500 p-1">{uname}</td>
					<td class="p-1">{scores[uname]}</td>
					{#if custom_field[uname]}
						<td class="border-l border-gray-500 p-1"
							>{custom_field[uname]}</td
						>
					{/if}
				</tr>
			{/each}
		</table>
	</div>
</div>
