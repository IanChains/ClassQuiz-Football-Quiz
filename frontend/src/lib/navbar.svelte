<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import '@fontsource/marck-script/index.css';
	import { getLocalization } from '$lib/i18n';
	import { signedIn, pathname } from '$lib/stores';
	import { createTippy } from 'svelte-tippy';
	import { browser } from '$app/environment';
	import { beforeNavigate } from '$app/navigation';
	import { draw, slide } from 'svelte/transition';

	import logo from '$lib/logo.png';

	const tippy = createTippy({
		arrow: true,
		animation: 'perspective-subtle',
		placement: 'bottom'
	});

	const { t } = getLocalization();

	let menuIsClosed = true;
	const toggleMenu = () => {
		menuIsClosed = !menuIsClosed;
	};

	beforeNavigate(() => {
		menuIsClosed = true; // Closes menu to let the user see the page beneath
	});

	let darkMode = false;
	if (browser) {
		darkMode =
			localStorage.theme === 'dark' ||
			(!('theme' in localStorage) &&
				window.matchMedia('(prefers-color-scheme: dark)').matches);
	}

	const switchDarkMode = () => {
		!darkMode ? localStorage.setItem('theme', 'dark') : localStorage.setItem('theme', 'light');
		window.location.reload();
	};
</script>

<nav class="w-screen px-4 lg:px-10 py-2 fixed backdrop-blur-2xl bg-white/70 shadow-md z-30 top-0">
	<!-- Desktop navbar -->
	<div class="hidden lg:flex lg:items-center lg:flex-row lg:justify-between">

		<div class="lg:flex lg:items-center lg:flex-row gap-1">
			<img style="max-height: 50px" src={logo}/>
			<a
				href="/"
				class="font-black tracking-tight text-xl lg:text-2xl text-black link-hover px-3 lg:px-5"
				>Football Is Life Quiz</a
			>
			<a class="btn-nav border-2 rounded" href="/play">Play</a>
			<a class="btn-nav" href="https://footballislife.be">Meer Info</a>
			{#if $signedIn}
				<a class="btn-nav" href="/dashboard">Dashboard</a>
			{/if}
		</div>
		<div class="lg:flex lg:items-center lg:flex-row gap-1">
			{#if $signedIn}
				<a class="btn-nav" href="/api/v1/users/logout">Uitloggen</a>
			{:else}
				{#if !import.meta.env.VITE_REGISTRATION_DISABLED}
					<a class="btn-nav" href="/account/register">Registreren</a>
				{/if}

				<a class="btn-nav" href="/account/login?returnTo={$pathname}">Inloggen</a>
			{/if}
		</div>
	</div>

	<!-- Mobile navbar -->
	<div class="lg:hidden">
		<!-- Navbar header -->
		<div class="flex items-center justify-between">
			<img style="max-height: 50px" src={logo}/>
			<a href="/"
				class="font-black tracking-tight text-xl lg:text-2xl text-black link-hover px-3 lg:px-5"
				>Football Is Life Quiz</a
			>
			<a class="btn-nav flex" href="/play">Play</a>

			<!-- Dark/Light mode toggle + Open/Close menu -->
			<div class="flex items-center">

				{#if menuIsClosed}
					<button
						class="px-3"
						id="open-menu"
						on:click={toggleMenu}
						aria-label="Open navbar"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							viewBox="0 0 24 24"
							fill="none"
							stroke="#000000"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
						>
							<path d="M3 6h18M3 12h18M3 18h18" />
						</svg>
					</button>
				{:else}
					<button
						class="px-3"
						id="close-menu"
						on:click={toggleMenu}
						aria-label="Close navbar"
					>
						<svg
							xmlns="http://www.w3.org/2000/svg"
							width="24"
							height="24"
							viewBox="0 0 24 24"
							fill="none"
							stroke="#000000"
							stroke-width="2"
							stroke-linecap="round"
							stroke-linejoin="round"
							><path in:draw={{ duration: 300 }} d="M18 6 6 18" /><path
								in:draw={{ duration: 300 }}
								d="m6 6 12 12"
							/></svg
						>
					</button>
				{/if}
			</div>
		</div>

		<!-- Navbar content -->
		{#if !menuIsClosed}
			<div class="flex flex-col" transition:slide={{ duration: 400 }}>
				<a class="btn-nav" href="https://footballislife.be">Meer Info</a>
				{#if $signedIn}
					<a class="btn-nav" href="/dashboard">Dashboard</a>
				{/if}

				<hr class="my-1 border" />
				{#if $signedIn}
					<a class="btn-nav" href="/api/v1/users/logout">Uitloggen</a>
				{:else}
					{#if !import.meta.env.VITE_REGISTRATION_DISABLED}
						<a class="btn-nav" href="/account/register">Registreren</a>
					{/if}

					<a class="btn-nav" href="/account/login?returnTo={$pathname}"
						>Inloggen</a
					>
				{/if}
			</div>
		{/if}
	</div>
</nav>

<style lang="scss">
	.btn-nav {
		@apply text-lg font-medium px-3 text-gray-600 hover:text-green-600 py-1.5 transition-all duration-300;
	}

</style>
