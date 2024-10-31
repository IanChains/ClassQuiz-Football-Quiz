<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import { getLocalization } from '$lib/i18n';
	import { navbarVisible } from '$lib/stores';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	navbarVisible.set(true);

	const { t } = getLocalization();
	let url_input = '';
	let file_input: File[];

	let url_valid = false;
	let kahoot_regex = /^https:\/\/create\.kahoot\.it\/details\/([a-zA-Z-\d]{36})\/?$/;
	let is_loading = false;

	$: url_valid = kahoot_regex.test(url_input);

	const submit = async () => {
		if (!url_valid) {
			return;
		}
		is_loading = true;
		const regex_res = kahoot_regex.exec(url_input);
		const res = await fetch(`/api/v1/quiz/import/${regex_res[1]}`, {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			}
		});

		if (res.status === 200) {
			window.location.href = '/dashboard';
		} else if (res.status === 400) {
			/*			alertModal.set({
				open: true,
				title: 'Import failed',
				body: "This quiz isn't (yet) supported!"
			});*/
			alert("This quiz isn't (yet) supported!");
		} else if (res.status === 403) {
			/*			alertModal.set({
				open: true,
				title: 'Import failed',
				body: 'Unknown error while importing the quiz!'
			});*/
			alert('Quiz is probably private!');
		} else {
			alert(`Kahoot replied with ${res.status}`);
		}
		is_loading = false;
	};

	const file_submit = async () => {
		is_loading = true;
		const formdata = new FormData();
		formdata.append('file', file_input[0]);
		let res;
		if (file_input[0].name.includes('.xlsx')) {
			res = await fetch('/api/v1/quiz/excel-import', {
				method: 'POST',
				body: formdata
			});
		} else if (file_input[0].name.includes('.cqa')) {
			res = await fetch('/api/v1/eximport/', {
				method: 'POST',
				body: formdata
			});
		} else {
			alert('Wrong file type');
			is_loading = false;
			return;
		}

		if (res.status === 200) {
			window.location.href = '/dashboard';
		} else {
			/*			alertModal.set({
				open: true,
				title: 'Import failed',
				body: 'Something went wrong!'
			});*/
			alert('Er is iets mis gegaan.');
		}
		is_loading = false;
	};

	$: console.log(file_input);

	onMount(() => {
		let url_from_path = $page.url.searchParams.get('url');
		if (url_from_path === '') {
			url_from_path = null;
		}
		url_input = url_from_path ?? '';
	});
</script>

<svelte:head>
	<title>Import Quiz</title>
</svelte:head>

<!--{#if is_loading}
	<svg class='h-8 w-8 animate-spin mx-auto my-20' viewBox='3 3 18 18'>
		<path
			class='fill-black'
			d='M12 5C8.13401 5 5 8.13401 5 12C5 15.866 8.13401 19 12 19C15.866 19 19 15.866 19 12C19 8.13401 15.866 5 12 5ZM3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12Z'
		/>
		<path
			class='fill-blue-100'
			d='M16.9497 7.05015C14.2161 4.31648 9.78392 4.31648 7.05025 7.05015C6.65973 7.44067 6.02656 7.44067 5.63604 7.05015C5.24551 6.65962 5.24551 6.02646 5.63604 5.63593C9.15076 2.12121 14.8492 2.12121 18.364 5.63593C18.7545 6.02646 18.7545 6.65962 18.364 7.05015C17.9734 7.44067 17.3403 7.44067 16.9497 7.05015Z'
		/>
	</svg>
{:else}-->

<!--	<form on:submit|preventDefault={submit}>
		<input type='text' class="text-black w-2/5" bind:value={url_input} />
		<button type='submit' disabled={!url_valid}>Submit</button>
	</form>-->
<div class="flex items-center justify-center h-full px-4">
	<div>
		<span class="p-4" />

		<div
			class="lg:w-[64rem] lg:max-w-[64rem] w-screen max-w-screen mx-auto overflow-hidden bg-white rounded-lg shadow-md dark:bg-gray-800"
		>
			<div class="px-6 py-4">
				<h2 class="text-3xl font-bold text-center text-gray-700 dark:text-white">
					Quiz Importeren
				</h2>

				<!--				<h3 class="mt-1 text-xl font-medium text-center text-gray-600 dark:text-gray-200">
									Welcome Back
								</h3>-->

				<!--				<p class="mt-1 text-center text-gray-500 dark:text-gray-400">
									Login or create account
								</p>-->
				<div class="grid">
					<form on:submit|preventDefault={file_submit}>
						<div class="w-full mt-4 h-full flex flex-col">
							<h2 class="text-center text-2xl">Een Football Quiz Importeren</h2>
							<div class="dark:bg-gray-800 bg-white p-4 rounded-lg">
								<div class="relative bg-inherit w-full">
									<input
										id="file"
										bind:files={file_input}
										name="file"
										type="file"
										accept=".cqa,.xlsx"
										class="w-full peer bg-transparent h-10 rounded-lg py-1.5 text-gray-700 dark:text-white placeholder-transparent ring-2 px-2 ring-gray-500 focus:ring-sky-600 focus:outline-none focus:border-rose-600"
										class:ring-red-700={!file_input}
										class:ring-green-600={file_input}
									/>
									<p class="text-sm">Upload een football quiz bestand met de extensie .cqa of .xlsx</p>
								</div>
								<p class="mt-2">
									Je kan hier een football quiz importeren.
									Het bestand die je hier upload moet afkomstig zijn van een geëxporteerde quiz.
									Of een bestand die je van ons (Football Is Life Quiz) of de webmaster (Ian-Chains IT) hebt gekregen.
								</p>
							</div>

							<div class="flex items-center justify-center mt-auto">
								<span />

								<button
									class="px-4 py-2 leading-5 text-white transition-colors duration-200 transform bg-gray-700 rounded hover:bg-gray-600 focus:outline-none disabled:cursor-not-allowed disabled:opacity-50"
									disabled={!file_input || is_loading}
									type="submit"
								>
									{#if is_loading}
										<svg
											class="h-4 w-4 animate-spin mx-auto"
											viewBox="3 3 18 18"
										>
											<path
												class="fill-black"
												d="M12 5C8.13401 5 5 8.13401 5 12C5 15.866 8.13401 19 12 19C15.866 19 19 15.866 19 12C19 8.13401 15.866 5 12 5ZM3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12Z"
											/>
											<path
												class="fill-blue-100"
												d="M16.9497 7.05015C14.2161 4.31648 9.78392 4.31648 7.05025 7.05015C6.65973 7.44067 6.02656 7.44067 5.63604 7.05015C5.24551 6.65962 5.24551 6.02646 5.63604 5.63593C9.15076 2.12121 14.8492 2.12121 18.364 5.63593C18.7545 6.02646 18.7545 6.65962 18.364 7.05015C17.9734 7.44067 17.3403 7.44067 16.9497 7.05015Z"
											/>
										</svg>
									{:else}
										Quiz Importeren
									{/if}
								</button>
							</div>
						</div>
					</form>
				</div>
			</div>
			<div class="flex items-center justify-center py-4 text-center bg-gray-50 dark:bg-gray-700 mt-4">
				<span class="text-sm text-gray-600 dark:text-gray-200">Vragen? -></span>
				<a	href="mailto:football.is.life.quiz@gmail.com"	class="ml-2 mr-4 text-sm font-bold text-blue-500 dark:text-blue-400 hover:underline transition-all">football.is.life.quiz@gmail.com</a>

				<span class="text-sm text-gray-600 dark:text-gray-200 ml-4">IT hulp nodig? -></span>
				<a	href="mailto:info@ian-chains.it"	class="mx-2 text-sm font-bold text-blue-500 dark:text-blue-400 hover:underline transition-all">info@ian-chains.it</a>
			</div>
		</div>
	</div>
</div>
<!--{/if}-->
