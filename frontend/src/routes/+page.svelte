<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import { navbarVisible } from '$lib/stores';
	import { getLocalization } from '$lib/i18n';
	import Footer from '$lib/footer.svelte';

	/*	import LandingPromo from '$lib/landing/landing-promo.svelte';*/


	const { t } = getLocalization();

	navbarVisible.set(true);

	/*	interface StatsData {
		quiz_count: number;
		user_count: number;
	}*/

	/*	const getStats = async (): Promise<StatsData> => {
			const response = await fetch('/api/v1/stats/combined');
			return await response.json();
		};*/

	// eslint-disable-next-line no-unused-vars
	enum SelectedCreateThing {
		// eslint-disable-next-line no-unused-vars
		Create,
		// eslint-disable-next-line no-unused-vars
		Find,
		// eslint-disable-next-line no-unused-vars
		Import
	}

	// eslint-disable-next-line no-unused-vars
	enum SelectedPlayThing {
		// eslint-disable-next-line no-unused-vars
		Select,
		// eslint-disable-next-line no-unused-vars
		Results,
		// eslint-disable-next-line no-unused-vars
		Winners
	}

	let selected_create_thing = SelectedCreateThing.Create;
	let selected_play_thing = SelectedPlayThing.Select;

	/*	<li>No;
		Tracking < /li>
		< li > Self - hostable < /li>
		< li > German;
		Server < /li>
		< li > user - friendly < /li>
		< li > Completely;
		free < /li>
		< li > Quiz - results;
		are;
		downloadable < /li>;*/

	const classquiz_reasons = [
		{
			headline: $t('index_page.no_player_limit'),
			content: $t('index_page.no_player_limit_content')
		},
		{
			headline: $t('index_page.no_tracking'),
			content: $t('index_page.no_tracking_content')
		},
		{
			headline: $t('index_page.self_hostable'),
			content: $t('index_page.self_hostable_content')
		},
		{
			headline: $t('index_page.german_server'),
			content: $t('index_page.german_server_content')
		},
		{
			headline: $t('index_page.user_friendly'),
			content: $t('index_page.user_friendly_content')
		},
		{
			headline: $t('index_page.completely_free'),
			content: $t('index_page.completely_free_content')
		},
		{
			headline: $t('index_page.quiz_results_downloadable'),
			content: $t('index_page.quiz_results_downloadable_content')
		},
		{
			headline: $t('index_page.multilingual'),
			content: $t('index_page.multilingual_content')
		},
		{
			headline: $t('index_page.dark_mode'),
			content: $t('index_page.dark_mode_content')
		},
		{
			headline: $t('index_page.download_quizzes'),
			content: $t('index_page.download_quizzes_content')
		},
		{
			headline: $t('index_page.community_driven'),
			content: $t('index_page.community_driven_content')
		}
	];
	let selected_classquiz_reason = 0;
</script>

<svelte:head>
	<title>Quiz Football Is Life</title>
	<meta name="description" content="Dit is de quiz site van Football Is Life!"/>
	<title>Quiz Football Is Life</title>
	<meta
		name="description"
		content="Dit is de quiz site van Football Is Life!"
	/>

	<meta property="og:url" content="https://quiz.footballislife.be/" />
	<meta property="og:type" content="website" />
	<meta property="og:title" content="Quiz Football Is Life" />
	<meta
		property="og:description"
		content="Dit is de quiz site van Football Is Life!"
	/>
	<meta property="og:image" content=$lib/logo.png />
	<meta name="apple-mobile-web-app-title" content="Quiz Football Is Life" />
	<meta name="application-name" content="Quiz Football Is Life" />
</svelte:head>

<!--<div class="min-h-screen flex flex-col">
	<section class="pb-40">
		<div class="pt-12 text-center">
			<h1 class="sm:text-8xl text-6xl mt-6 marck-script">ClassQuiz</h1>
			<p class="text-xl mt-4">{$t('index_page.slogan')}</p>
		</div>
	</section>

	<section id="features" class="mt-8">
		<div class="text-center snap-y">
			<h1 class="sm:text-6xl text-4xl">{$t('words.features')}</h1>
			<p class="text-xl pt-4">
				{$t('index_page.features_description.1')}
				<br />
				{$t('index_page.features_description.2')}
				<br />
				{$t('index_page.features_description.3')}
			</p>
		</div>
	</section>
	<section class="py-8">
		<h1 class="sm:text-6xl text-4xl text-center break-words">
			{$t('words.screenshot', { count: 2 })}
		</h1>
		<div>
			<LandingPromo />
		</div>
	</section>

	<section>
		<h1 class="sm:text-6xl text-4xl text-center">Testimonials</h1>
		{#await import('$lib/landing/testimonials.svelte') then testimonials}
			<svelte:component this={testimonials.default} />
		{/await}
	</section>

	<section id="stats">
		<div class="text-center pb-20 pt-10 snap-y">
			<h1 class="sm:text-6xl text-4xl">{$t('words.stats')}</h1>
			<p class="text-xl pt-4">
				{#await getStats() then stats}
					{$t('index_page.stats', {
						user_count: stats.user_count,
						quiz_count: stats.quiz_count
					})}
				{/await}
			</p>
		</div>
	</section>
</div>-->
<div class="min-h-screen flex flex-col">
	<section class="pb-40">
		<div class="pt-12 text-center">
			<h1 class="sm:text-8xl text-6xl mt-6">Football Is Life Quiz</h1>
			<p class="text-xl mt-4">Voetbal wie houdt daar nu niet van?!</p>
		</div>
	</section>
	<section>
		<h2 class="text-center text-5xl mb-6">De partner voor uw voetbalquiz op maat!</h2>
	</section>

	
</div>

<Footer />

<style>
	.why-classquiz::-webkit-scrollbar {
		height: 0.8rem;
		margin-bottom: 5rem;
	}

	.why-classquiz::-webkit-scrollbar-track {
		box-shadow: inset 0 0 10px 10px transparent;
		border: solid 3px transparent;
	}

	.why-classquiz::-webkit-scrollbar-thumb {
		box-shadow: inset 0 0 10px 10px #374151;
		border: solid 3px transparent;
		border-radius: 15px;
	}

	.why-classquiz::-webkit-scrollbar-thumb:hover {
		box-shadow: inset 0 0 10px 10px #555;
		border: solid 3px transparent;
	}
</style>
