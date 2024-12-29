<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import QRCode from 'qrcode';
	import Spinner from '$lib/Spinner.svelte';
	import { getLocalization } from '$lib/i18n';

	const { t } = getLocalization();

	export let totp_data: { url: string; secret: string } | undefined;

	const get_image_url = async () => {
		return await QRCode.toDataURL(totp_data.url);
	};
</script>

<div class="w-screen h-screen fixed top-0 left-0 p-48 z-30 bg-black bg-opacity-50">
	<div class="w-full h-full">
		<button
			class="bg-gray-900 px-2 py-1 rounded-t-lg hover:bg-gray-300 transition"
			on:click={() => {
				totp_data = undefined;
			}}
			>Sluiten
		</button>
		<div class="bg-gray-700 rounded-b-lg rounded-tr-lg w-full h-full">
			<div class="grid grid-cols-3 w-full h-full">
				<div class="flex flex-col justify-center w-full h-5/6">
					<span class="m-auto" />
					<div class="h-5/6 flex">
						<p class="my-auto ml-auto">
							Scan deze QR-code om de 2FA in te stellen.
						</p>
					</div>
					<div class="flex">
						<p class="my-auto ml-auto">
							Voer dit in als de 'secret' als u de QR-code niet kunt scannen.
						</p>
					</div>
				</div>
				<div class="flex flex-col justify-start w-full h-5/6">
					<h2 class="text-2xl m-auto">2FA Setup</h2>
					{#await get_image_url()}
						<Spinner my_20={false} />
					{:then data}
						<div class="m-auto h-5/6 object-contain w-full">
							<img
								src={data}
								alt="QR-Code for Totp-setup"
								class="w-full h-full object-contain"
							/>
						</div>
					{/await}
					<p class="m-auto select-all font-mono">{totp_data.secret}</p>
				</div>
				<div class="flex justify-center h-5/6 w-full">
					<p class="m-auto text-3xl p-4">
						Vergeet niet je herstelcode/backupcode op te slaan!
					</p>
				</div>
			</div>
		</div>
	</div>
</div>
