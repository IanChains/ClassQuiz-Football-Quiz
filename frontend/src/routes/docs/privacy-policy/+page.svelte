<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import { onMount } from 'svelte';
	import '$lib/hljs.css';

	onMount(async () => {
		const { default: hljs } = await import('highlight.js/lib/common');
		hljs.highlightAll();
	});
</script>

<svelte:head>
	<title>Privacy policy - Quiz Football Is Life</title>
	<meta
		name="description"
		content="Privacy Policy of Football Is Life Quiz!"
	/>
</svelte:head>

<article
	class="prose prose-sm sm:prose lg:prose-lg xl:prose-xl mx-auto mt-10 prose-slate px-4 dark:prose-invert"
>
	<h1>Privacy Policy</h1>

	<h2>Wat wordt hoe lang opgeslagen en waarom?</h2>
	<table>
		<thead>
			<tr>
				<th>Wat?</th>
				<th>Waarom?</th>
				<th>Hoe lang?</th>
				<th>Waar?</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td> Het IP-adres van de gebruiker</td>
				<td>
					<ul>
						<li>Misbruik voorkomen</li>
						<li>Gebruikerssessies aanbieden</li>
						<li>Voor Ontwikkelingen & Debuggen</li>
					</ul>
				</td>
				<td> Voor een zeer lange tijd</td>
				<td> Op de main, developer & backup server, beheerd door: Ian-Chains IT</td>
			</tr>
			<tr>
				<td> De gegevens die de gebruiker invoert (quizzen, e-mail, gebruikersnaam ...)</td>
				<td> Zelfverklarend</td>
				<td> Maximaal 90 dagen na verwijdering van je account</td>
				<td> Op de main & backup server, beheerd door: Ian-Chains IT</td>
			</tr>
			<tr>
				<td>De <b>gehashed</b> wachtwoord van de gebruiker</td>
				<td>Zelfverklarend</td>
				<td>Maximaal 90 dagen na verwijdering van je account</td>
				<td>Op de main & backup server, beheerd door: Ian-Chains IT</td>
			</tr>
			<tr>
				<td> Analytics & Marketing Data: Google Analytics (P-adres, bezochte pagina's, tijd op de site, apparaat- en browsergegevens ...)</td>
				<ul>
					<li>Om websiteverkeer te analyseren</li>
					<li>Marketing & Promotie doeleinden</li>
					<li>Om de gebruikerservaring te verbeteren</li>
					<li>Om inzicht te krijgen in prestaties en gebruikspatronen</li>
				</ul>
				<td> Standaard 14 maanden met maximaal 26 maanden</td>
				<td> Op de servers van Google</td>
			</tr>
		</tbody>
	</table>

	<h2>Cookies</h2>
	<p>
		Cookies worden gebruikt om toegangstokens, gebruikerssessies en voorkeuren op te slaan. Ze verlopen na een
		jaar. Cookies worden ook door Google Analytics gebruikt om gebruikersgedrag bij te houden.
	</p>

	<h2>Account & Data verwijdering</h2>
	<p>
		Aanvragen voor account & data verwijdering kunnen worden gestuurd naar: <a href="mailto:webmaster@footballislife.be">webmaster@footballislife.be</a>
		Vermeld alsjeblieft het e-mailadres waarmee je je hebt geregistreerd op Football Is Life Quiz en, indien mogelijk, een bewijs dat je de eigenaar bent van het account of de data, door bijvoorbeeld het e-mailadres te schrijven dat is gekoppeld aan je Football Is Life Quiz-account.
	</p>

	<h2>Tracking</h2>
	<p>
		This site uses a self-hosted GlitchTip (sentry) instance for error-logging. An opt-out is
		not available at the moment. This website also uses
		<a href="https://plausible.io/">Plausible</a> to log usage-data, but this is also running on
		the same server as ClassQuiz itself.
	</p>

</article>
