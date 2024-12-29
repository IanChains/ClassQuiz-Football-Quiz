<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import { getLocalization } from '$lib/i18n';
	import { navbarVisible } from '$lib/stores';

	navbarVisible.set(true);

	const { t } = getLocalization();

	let isSubmitting = false;

	const submit = async () => {
		isSubmitting = true;
		const res = await fetch('/api/v1/users/forgot-password', {
			method: 'POST',
			headers: {
				'Content-Type': 'application/json'
			},
			body: JSON.stringify({
				email: email
			})
		});
		if (res.status === 200) {
			alert('E-mail is verzonden! Controleer je mailbox. Heb je geen mail ontvangen? Neem dan contact op met info@ian-chains.it');
			return;
		} else if (res.status === 404) {
			alert('We hebben de gebruiker niet gevonden.');
		}
		else {
			alert('Er is een fout opgetreden. Neem contact op met info@ian-chains.it');
		}
		isSubmitting = false;
	};

	let email = '';
</script>

<svelte:head>
	<title>Wachtwoord Resetten</title>
</svelte:head>

<div class="flex items-center justify-center h-full px-4">
	<div>
		<div
			class="w-full max-w-sm mx-auto overflow-hidden rounded-lg shadow-md bg-gray-800"
		>
			<div class="px-6 py-4">
				<h2 class="text-3xl font-bold text-center text-white">
					Football Is Life Quiz
				</h2>

				<p class="mt-1 text-center text-gray-400">
					Wachtwoord Resetten
				</p>

				<form on:submit|preventDefault={submit}>
					<div class="w-full mt-4">
						<div class="bg-gray-800 p-4 rounded-lg">
							<div class="relative bg-inherit w-full">
								<input
									id="email"
									bind:value={email}
									name="email"
									type="email"
									class="w-full peer bg-transparent h-10 rounded-lg text-white placeholder-transparent ring-2 px-2 ring-gray-500 focus:ring-sky-600 focus:outline-none focus:border-rose-600"
									placeholder="E-mailadres"
								/>
								<label
									for="email"
									class="absolute cursor-text left-0 -top-3 text-sm text-white bg-inherit mx-1 px-1 peer-placeholder-shown:text-base peer-placeholder-shown:text-gray-500 peer-placeholder-shown:top-2 peer-focus:-top-3 peer-focus:text-sky-600 peer-focus:text-sm transition-all"
								>
									E-mailadres
								</label>
							</div>
						</div>

						<div class="flex items-center justify-between mt-4 gap-2">
							<a
								href="/account/login"
								class="text-sm text-gray-200 hover:text-gray-500"
								>Heb je al een account?</a
							>

							<button
								class="px-4 py-2 leading-5 text-white transition-colors duration-200 transform bg-gray-700 rounded hover:bg-gray-600 focus:outline-none disabled:cursor-not-allowed disabled:opacity-50"
								disabled={email === ''}
								type="submit"
							>
								{#if isSubmitting}
									<svg class="h-4 w-4 animate-spin mx-auto" viewBox="3 3 18 18">
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
									Verstuur!
								{/if}
							</button>
						</div>
					</div>
				</form>
			</div>

			<div
				class="flex items-center justify-center py-4 text-center bg-gray-700"
			>
				<span class="text-sm text-gray-200"
					>Heb je nog geen account?
				</span>

				<a
					href="/account/register"
					class="mx-2 text-sm font-bold text-blue-400 hover:underline"
					>Registreren</a
				>
			</div>
		</div>
	</div>
</div>
