<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import { onMount } from 'svelte';
	import { writable } from 'svelte/store';
	import '@fontsource/marck-script/index.css';
	import { signedIn, pathname } from '$lib/stores';
	import { beforeNavigate } from '$app/navigation';
	import { draw, slide } from 'svelte/transition';

	import logo from '$lib/logo.png';

	let menuIsClosed = true;
	const toggleMenu = () => {
		menuIsClosed = !menuIsClosed;
	};

	beforeNavigate(() => {
		menuIsClosed = true; // Closes menu to let the user see the page beneath
	});

	const isAdmin = writable(false);

	let maintenance = false;

	onMount(async () => {
		try {
			const response = await fetch('/api/v1/users/admin');

			if (response.status === 502) {
				maintenance = true;
				isAdmin.set(false);
			} else if (response.ok) {
				const result = await response.json();
				isAdmin.set(result.admin_user);
			} else {
				isAdmin.set(false);
			}
		} catch (error) {
			console.error('Error fetching admin status:', error);
		}
	});
</script>

<nav class="px-4 lg:px-10 py-2 fixed backdrop-blur-2xl custom-dark-blue-bg shadow-md z-30 top-0" style="width:100%">
	<!-- Desktop navbar -->
	<div class="hidden lg:flex lg:items-center lg:flex-row lg:justify-between">

		<div class="lg:flex lg:items-center lg:flex-row gap-1">
			<img style="max-height: 50px" src={logo}/>
			<a
				href="/"
				class="font-black tracking-tight text-xl lg:text-2xl custom-bright-orange custom-bright-red-hover px-3 lg:px-5 duration-300"
				>Football Is Life Quiz</a
			>
			{#if maintenance}
			<a class="btn-nav custom-nav-btn underline" href="/" style="color: red; font-weight:bold;">Quiz Site in onderhoud!</a>
			{:else}
			<a class="btn-nav border-2 rounded custom-nav-btn" href="/play">Play</a>
			<a class="btn-nav custom-nav-btn" href="/search">Quiz Zoeken</a>
			<a class="btn-nav custom-nav-btn" href="https://footballislife.be">Meer Info</a>
				{#if $signedIn}
					{#if $isAdmin}
						<a class="btn-nav-admin custom-nav-btn-admin" href="/dashboard-admin">Admin Dashboard</a>
					{:else}
						<a class="btn-nav custom-nav-btn" href="/dashboard">Dashboard</a>
					{/if}
				{/if}
			{/if}
		</div>
		<div class="lg:flex lg:items-center lg:flex-row gap-1">
			{#if !maintenance}
				{#if $signedIn}
					<a class="btn-nav custom-nav-btn" href="/api/v1/users/logout">Uitloggen</a>
				{:else}
					{#if !import.meta.env.VITE_REGISTRATION_DISABLED}
						<a class="btn-nav custom-nav-btn" href="/account/register">Registreren</a>
					{/if}

					<a class="btn-nav custom-nav-btn" href="/account/login?returnTo={$pathname}">Inloggen</a>
				{/if}
			{/if}
		</div>
	</div>

	<!-- Mobile navbar -->
	<div class="lg:hidden">
		<!-- Navbar header -->
		<div class="flex items-center justify-between">
			<img style="max-height: 50px" src={logo}/>
			<a href="/"
				class="font-black tracking-tight text-xl lg:text-2xl custom-bright-orange custom-bright-red-hover px-3 lg:px-5 duration-300"
				>Football Is Life Quiz</a
			>
			{#if !maintenance}
				<a class="btn-nav flex" href="/play">Play</a>
			{/if}

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
							stroke="#FFFFFF"
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
							stroke="#FFFFFF"
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
				{#if maintenance}
					<a class="btn-nav custom-nav-btn underline" href="/" style="color: red; font-weight:bold;">Site in onderhoud!</a>
				{:else}
					<a class="btn-nav custom-nav-btn" href="/search">Quiz Zoeken</a>
					<a class="btn-nav custom-nav-btn" href="https://footballislife.be">Meer Info</a>
						{#if $signedIn}
							{#if $isAdmin}
								<a class="btn-nav-admin custom-nav-btn-admin" href="/dashboard-admin">Admin Dashboard</a>
							{:else}
								<a class="btn-nav custom-nav-btn" href="/dashboard">Dashboard</a>
							{/if}
						{/if}
				{/if}

				{#if !maintenance}
					<hr class="my-1 border" />
					{#if $signedIn}
						<a class="btn-nav custom-nav-btn" href="/api/v1/users/logout">Uitloggen</a>
					{:else}
						{#if !import.meta.env.VITE_REGISTRATION_DISABLED}
							<a class="btn-nav custom-nav-btn" href="/account/register">Registreren</a>
						{/if}

						<a class="btn-nav custom-nav-btn" href="/account/login?returnTo={$pathname}"
							>Inloggen</a
						>
					{/if}
				{/if}
			</div>
		{/if}
	</div>
</nav>

<style lang="scss">
	.btn-nav {
		@apply text-lg font-medium px-3 py-1.5 transition-all duration-300;
	}
	.btn-nav-admin {
		@apply text-lg font-medium px-3 py-1.5 transition-all duration-300;
	}

</style>
