<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script>
	export let quiz;
</script>

<div class="flex justify-center search-card-hover">
	<a href="/view/{quiz.id}" class="h-max w-fit">
		<div class="max-w-md py-4 px-8 shadow-lg rounded-lg bg-slate-800" style="margin-top:2.5rem; margin-bottom:2.5rem;">
			<div>
				<div class="flex w-full items-center">
					<h2
						class="text-gray-200 text-3xl font-semibold pr-2"
						style="font-size: 1.5rem;"
					>
						{@html quiz.title}
					</h2>
				</div>

				{#if !quiz.license_required}
					<p
						class="text-gray-300 font-bold underline block"
						style="text-decoration-color: #F4B631; font-size:20px;"
					>
						GRATIS Quiz
					</p>
				{/if}

				<p
					class="mt-2 text-gray-300 break-all overflow-hidden text-ellipsis max-h-[4.5rem] block"
				>
					{@html quiz.description}
				</p>
			</div>
		</div>
	</a>
</div>
