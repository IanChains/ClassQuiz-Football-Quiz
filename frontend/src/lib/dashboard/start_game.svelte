<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	// import { alertModal } from '$lib/stores';
	import { captcha_enabled } from '$lib/config';
	import StartGameBackground from './start_game_background.svg';
	import { fade } from 'svelte/transition';
	import Spinner from '$lib/Spinner.svelte';
	import { onMount } from 'svelte';
	import { createTippy } from 'svelte-tippy';
	import { writable } from 'svelte/store';

	export let quiz_id;
	let captcha_selected = false;
	let selected_game_mode = 'kahoot';
	let loading = false;
	let custom_field = '';
	let licentie_key = '';
	let cqcs_enabled = false;
	let randomized_answers = false;

	const tippy = createTippy({
		arrow: true,
		animation: 'perspective-subtle',
		placement: 'top-start',
		allowHTML: true
	});

	const error_message = writable('');
	const licentie_key_write = writable('');
	const isAdmin = writable(false);

	onMount(async () => {
		try {
			const response = await fetch('/api/v1/users/admin');

			if (response.ok) {
				const result = await response.json();
				isAdmin.set(result.admin_user);
			} else {
				isAdmin.set(false);
			}
		} catch (error) {
			console.error('Error fetching admin status:', error);
		}
	});


	function ClearError(event) {
		const value = event.target.value;
		licentie_key_write.set(value);
		if (value) {
			error_message.set('');
		}
	}

	onMount(() => {
		const ls_data = localStorage.getItem('custom_field');
		custom_field = ls_data ? ls_data : '';
	});

	const start_game = async (id: string) => {
		let res;
		loading = true;
		localStorage.setItem('custom_field', custom_field);
		const cqcs_enabled_parsed = cqcs_enabled ? 'True' : 'False';
		const randomized_answers_parsed = randomized_answers ? 'True' : 'False';
		const license = $licentie_key_write
		if (captcha_enabled && captcha_selected) {
			res = await fetch(
				`/api/v1/quiz/start/${id}?captcha_enabled=True&game_mode=${selected_game_mode}&custom_field=${custom_field}&cqcs_enabled=${cqcs_enabled_parsed}&license=${license}`,
				{
					method: 'POST'
				}
			);
		} else {
			res = await fetch(
				`/api/v1/quiz/start/${id}?captcha_enabled=False&game_mode=${selected_game_mode}&custom_field=${custom_field}&cqcs_enabled=${cqcs_enabled_parsed}&randomize_answers=${randomized_answers_parsed}&license=${license}`,
				{
					method: 'POST'
				}
			);
		}

		if (res.status === 403) {
			const errorResponse = await res.json();
			error_message.set(errorResponse.detail || 'Er is iets met gegaan met de licentie code.');
			loading = false;
		} else if (res.status !== 200) {
			/*			alertModal.set({
				open: true,
				title: 'Start failed',
				body: `Failed to start game, ${await res.text()}`
			});*/
			/*alertModal.subscribe((_) => {
				window.location.assign('/account/login?returnTo=/dashboard');
			});*/
			alert('Starting game failed');
			window.location.assign('/account/login?returnTo=/dashboard');
		} else {
			const data = await res.json();
			// eslint-disable-next-line no-undef
			loading = false;
			window.location.assign(
				`/admin?token=${data.game_id}&pin=${data.game_pin}&connect=1&cqc_code=${data.cqc_code}`
			);
		}
	};

	const on_parent_click = (e: Event) => {
		if (e.target !== e.currentTarget) {
			return;
		}
		quiz_id = null;
	};
	const close_start_game_if_esc_is_pressed = (key: KeyboardEvent) => {
		if (key.code === 'Escape') {
			quiz_id = null;
		}
	};
	onMount(() => {
		document.body.addEventListener('keydown', close_start_game_if_esc_is_pressed);
	});
</script>

<div
	class="fixed top-0 left-0 flex justify-center w-screen h-screen bg-black bg-opacity-60 z-50 text-black"
	transition:fade={{ duration: 100 }}
	on:click={on_parent_click}
>
	<div
		class="w-5/6 h-5/6 bg-black m-auto rounded-lg shadow-lg p-4 flex flex-col"
		style="background-image: url({StartGameBackground}); background-color: #DFDBE5;"
	>

		<div class="grid grid-cols-2 gap-8 my-auto">
			<div
				class="rounded-lg bg-white shadow-lg cursor-pointer transition-all p-2"
				class:opacity-50={selected_game_mode !== 'kahoot'}
				on:click={() => {
					selected_game_mode = 'kahoot';
				}}
			>
				<h2 class="text-center text-2xl">Normaal</h2>
				<p>
					Vraag en antwoord worden alleen getoond op het beheerdersscherm. De spelers hebben alleen gekleurde knoppen met bijbehorende symbolen.
				</p>
			</div>
			<div
				class="rounded-lg bg-white shadow-lg cursor-pointer transition-all p-2"
				class:opacity-50={selected_game_mode !== 'normal'}
				on:click={() => {
					selected_game_mode = 'normal';
				}}
			>
				<h2 class="text-center text-2xl">Old-School</h2>
				<p>
					Vragen en afbeeldingen worden zowel op het beheerdersscherm als op het scherm van de spelers getoond.
				</p>
			</div>
		</div>

		{#if !$isAdmin}
			<div class="flex justify-center items-center my-auto">
				<label class="mr-4 font-bold" style="font-size: 18px;">Quiz Licentie Code: (incl. "QUIZ")</label>
				<input
					bind:value={licentie_key}
					on:input={ClearError}
					class="rounded-lg p-2 outline-none placeholder:italic"
					placeholder="Key/Code, die heb je gekregen hebt (Verplicht)"
					style="width: 35%"
				/>
			</div>
		{/if}

		<div class="flex justify-center items-center my-auto">
			<label class="mr-4 font-bold" style="font-size: 18px;">Aangepast Info Veld</label>
			<input
				bind:value={custom_field}
				class="rounded-lg p-2 outline-none placeholder:italic"
				style="width: 20%"
				placeholder="Email/Telefoon/Groep (Niet Verplicht)"
			/>
		</div>
		<div class="flex justify-center w-full my-auto">
			<label
				for="randomized-answers-toggle"
				class="inline-flex relative items-center cursor-pointer"
			>
				<input
					type="checkbox"
					bind:checked={randomized_answers}
					id="randomized-answers-toggle"
					class="sr-only peer"
				/>
				<span
					class="w-14 h-7 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-blue-300 dark:peer-focus:ring-blue-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-0.5 after:left-[4px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-6 after:w-6 after:transition-all dark:border-gray-600 peer-checked:bg-blue-600"
				/>
				<span class="ml-3 text-sm font-medium text-gray-900" style="font-size: 16px;">Antwoorden In Random Volgorde</span>
			</label>
		</div>

		{#if $error_message }
			<div class="flex justify-center w-full mt-auto">
				<p class="font-bold text-red-600 underline" style="font-size: 20px;">{$error_message}</p>
			</div>
		{/if}
		
		<button
			class="mt-auto mx-auto orange-red-button p-4 rounded-lg shadow-lg transition-all text-2xl"
			on:click={() => {
				if ( (!$licentie_key_write) && (!$isAdmin) ) {
					error_message.set('Gelieve een licentie code in te vullen.');
				} else {
					start_game(quiz_id);
				}
			}}
		>
			{#if loading}
				<Spinner my_20={false} />
			{:else}
				Start Spel
			{/if}
		</button>
	</div>
</div>
