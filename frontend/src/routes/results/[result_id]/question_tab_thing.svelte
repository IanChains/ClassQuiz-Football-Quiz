<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	import { QuizQuestionType } from '$lib/quiz_types';
	import { getLocalization } from '$lib/i18n';
	import type { Question } from '$lib/quiz_types';

	const { t } = getLocalization();

	export let question: Question;

	interface Answer {
		username: string;
		answer: string;
		right: boolean;
		time_taken: number;
		score: number;
	}

	export let answers: Answer[];
	// console.log(question);

	const get_answer_count_for_answer = (answer: string): number => {
		let count = 0;
		let answer_id = 0;
		if (question.type === QuizQuestionType.CHECK) {
			for (let i = 0; i < question.answers.length; i++) {
				if (answer === question.answers[i].answer) {
					answer_id = i;
					break;
				}
			}
		}
		for (let i = 0; i < answers.length; i++) {
			const a = answers[i];
			if (question.type === QuizQuestionType.CHECK) {
				console.log(a.answer.includes('2'), answer_id);
				if (a.answer.includes(String(answer_id))) {
					count++;
				}
			} else if (a.answer === answer) {
				count++;
			}
		}
		return count;
	};
</script>

<div class="flex justify-center">
	<div class="p-2 -z-10 w-10/12 rounded bg-gray-700">
		{#if question.type !== QuizQuestionType.ORDER && question.type !== QuizQuestionType.RANGE}
			<div class="flex flex-col mb-4">
				{#each question.answers as answer}
					<div class="grid grid-cols-4">
						<p>{answer.answer}</p>
						<div
							class="col-span-3 flex w-full border-l px-1 border-gray-500"
						>
							<div class="my-auto w-full mr-1">
								<span
									class="h-1 block bg-green-600 my-auto"
									style="width: {(get_answer_count_for_answer(answer.answer) /
										answers.length) *
										100}%"
								/>
							</div>
							<p>{get_answer_count_for_answer(answer.answer)}</p>
							{#if question.type !== QuizQuestionType.VOTING && question.type !== QuizQuestionType.TEXT}
								<p class="ml-1">
									{#if answer.right}✅{:else}❌{/if}
								</p>
							{/if}
						</div>
					</div>
				{/each}
			</div>
		{/if}
		<div>
			<table class="w-full text-left">
				<tr class="border-b-2 border-gray-500 text-left">
					<th class="border-r border-gray-500 p-1 mx-auto"
						>Naam Speler
					</th>
					{#if question.type !== QuizQuestionType.VOTING}
						<th class="border-r border-gray-500 p-1 mx-auto"
							>Score</th
						>
					{/if}
					<th class="border-r border-gray-500 p-1 mx-auto"
						>Antwoord Tijd
					</th>
					<th class="p-1 mx-auto">Antwoord</th>
					{#if question.type !== QuizQuestionType.VOTING}
						<th class="border-l border-gray-500 p-1 mx-auto"
							>Juist?
						</th>
					{/if}
				</tr>
				{#each answers as answer}
					<tr>
						<td class="border-r border-gray-500 p-1"
							>{answer.username}</td
						>
						{#if question.type !== QuizQuestionType.VOTING}
							<td class="border-r border-gray-500 p-1"
								>{answer.score}</td
							>
						{/if}
						<td class="border-r border-gray-500 p-1"
							>{(answer.time_taken / 1000).toFixed(3)}s
						</td>
						<td class="p-1">{answer.answer}</td>
						{#if question.type !== QuizQuestionType.VOTING}
							<td class="p-1 border-l border-gray-500">
								{#if answer.right}✅{:else}❌{/if}
							</td>
						{/if}
					</tr>
				{/each}
			</table>
		</div>
	</div>
</div>
