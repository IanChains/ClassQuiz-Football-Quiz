<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import { getLocalization } from '$lib/i18n';

	const { t } = getLocalization();
	export let backup_code;

	let already_downloaded = false;

	const download_code = (force = false) => {
		if (already_downloaded && !force) {
			return;
		}
		const el = document.createElement('a');
		el.setAttribute('href', `data:text/plain;charset=utf-8,${backup_code}`);
		el.setAttribute('download', 'ClassQuiz-Backup-Code.txt');
		el.style.display = 'none';
		document.body.appendChild(el);
		el.click();
		document.body.removeChild(el);
		already_downloaded = true;
	};
</script>

<div class="w-screen h-screen fixed top-0 left-0 p-48 z-30 bg-black bg-opacity-50">
	<div class="w-full h-full">
		<button
			class="bg-gray-900 px-2 py-1 rounded-t-lg hover:bg-gray-300 transition"
			on:click={() => {
				backup_code = undefined;
			}}
			>Sluiten
		</button>
		<div
			class="bg-gray-700 rounded-b-lg rounded-tr-lg w-full h-full flex flex-col"
		>
			<h2 class="text-3xl m-auto">Jouw Back-Up Code:</h2>
			<p
				class="select-all font-mono text-xl m-auto"
				on:click={() => {
					download_code(false);
				}}
			>
				{backup_code}
			</p>
			<p class="m-auto">Bewaar deze code ergens veilig, deel deze met niemand!</p>
			<button
				on:click={() => {
					download_code(true);
				}}
				class="m-auto p-2 orange-red-button rounded-lg"
				>Download Back-Up Code
			</button>
		</div>
	</div>
</div>
