<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import { createTippy } from 'svelte-tippy';
	import StartGamePopup from '$lib/dashboard/start_game.svelte';
	import { onMount } from 'svelte';
	import BrownButton from '$lib/components/buttons/brown.svelte';
	import RatingComponent from '$lib/view_quiz/RatingComponent.svelte';

	const default_colors = ['#D6EDC9', '#B07156', '#7F7057', '#4E6E58'];

	const tippy = createTippy({
		arrow: true,
		animation: 'perspective-subtle',
		placement: 'right'
	});

	let start_game = null;
	const close_start_game_if_esc_is_pressed = (key: KeyboardEvent) => {
		if (key.code === 'Escape') {
			start_game = null;
		}
	};
	onMount(() => {
		document.body.addEventListener('keydown', close_start_game_if_esc_is_pressed);
	});

	export let data;
	let { quiz, logged_in, admin_user }: { quiz: QuizData; logged_in: boolean; admin_user: boolean; } = data;

	interface QuizData {
		id: string;
		public: boolean;
		title: string;
		description: string;
		created_at: string;
		updated_at: string;
		user_id: string;
		imported_from_kahoot?: boolean;
		cover_image?: string,
		kahoot_id?: string;
		mod_rating?: number;
	}


	function copyToClipboard() {
        navigator.clipboard.writeText(quiz.id)
            .then(() => {
                alert("Quiz ID gekopieerd naar plakbord.");
            })
            .catch(err => {
                console.error("Failed to copy: ", err);
            });
        }
</script>

<svelte:head>
	<title>ClassQuiz - View {quiz.title}</title>
</svelte:head>

<div class="flex flex-col w-full h-full">
	<h1 class="text-4xl text-center mt-4">{@html quiz.title}</h1>
	<div class="text-center my-2">
		<p>{@html quiz.description}</p>
	</div>
	{#if quiz.cover_image}
		<div class="flex justify-center align-middle items-center">
			<div class="h-[15vh] m-auto w-auto my-3">
				<img
					class="max-h-full max-w-full block"
					src="/api/v1/storage/download/{quiz.cover_image}"
					alt="Not provided"
				/>
			</div>
		</div>
	{/if}
	<div class="flex justify-center flex-row gap-2 my-4">
		<RatingComponent bind:quiz />
	</div>
	<div class="flex flex-col justify-center">
		<div class="mx-auto flex flex-col gap-2 justify-center w-fit">
			{#if logged_in}
				<div class="w-full my-4">
					<BrownButton
						on:click={() => {
							start_game = quiz.id;
						}}
						flex={true}
					>
						<!-- heroicons/legacy-outline/Play -->
						<svg
							class="w-5 h-5"
							aria-hidden="true"
							fill="none"
							stroke="currentColor"
							stroke-width="2"
							viewBox="0 0 24 24"
							xmlns="http://www.w3.org/2000/svg"
						>
							<path
								d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
							<path
								d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
								stroke-linecap="round"
								stroke-linejoin="round"
							/>
						</svg>
					</BrownButton>
				</div>
			{:else}
				<div use:tippy={{ content: 'Je moet ingelogd zijn om de Quiz te starten!' }}>
					<div class="w-full my-4">
						<BrownButton disabled={true} flex={true}>
							<!-- heroicons/legacy-outline/Play -->
							<svg
								class="w-5 h-5"
								aria-hidden="true"
								fill="none"
								stroke="currentColor"
								stroke-width="2"
								viewBox="0 0 24 24"
								xmlns="http://www.w3.org/2000/svg"
							>
								<path
									d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
								<path
									d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
									stroke-linecap="round"
									stroke-linejoin="round"
								/>
							</svg>
						</BrownButton>
					</div>
				</div>
			{/if}
			
			{#if admin_user}
				<div class="text-center my-2">
					<p>Quiz ID (Click to Copy):</p>
					<p on:click={copyToClipboard}>{@html quiz.id}</p>
				</div>
			{/if}
			
		</div>
	</div>

	<section class="mt-auto mb-4">
		<p class="mt-6 mx-auto max-w-[70%] text-sm dark:text-gray-200 text-center">
			Omdat er hier nog een beetje plaats vrij is, wil ik jou graag bedanken voor het gebruiken van deze Quiz Site.
			<br>Deze Quiz Site is mogelijk gemaakt door het Open Source Project <a href="https://classquiz.de/" class="underline" target="_blank">ClassQuiz</a>!
			<br>Graag wil ik <a href="https://mawoka.eu/" class="underline" target="_blank">Mawoka</a> en <a href="https://classquiz.de/docs/attribution" class="underline" target="_blank">zijn team</a> bedanken voor het maken van ClassQuiz!
			<br>Ik wens jou een fijne dag toe! ♥ WebMaster <a href="https://ian-chains.it" class="underline" target="_blank">Ian-Chains IT</a> ♥
		</p>
	</section>

</div>

{#if start_game !== null}
	<StartGamePopup bind:quiz_id={start_game} />
{/if}