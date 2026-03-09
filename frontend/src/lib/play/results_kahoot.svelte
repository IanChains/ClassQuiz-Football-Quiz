<!--
SPDX-FileCopyrightText: 2023 Marlon W (Mawoka)

SPDX-License-Identifier: MPL-2.0
-->

<script lang="ts">
	export let scores;

	export let question_results: Array<{
		username: string;
		answer: string;
		right: boolean;
		time_taken: number;
		score: number;
	}>;

	function sortObjectbyValue(obj) {
		const ret = {};
		Object.keys(obj)
			.sort((a, b) => obj[b] - obj[a])
			.forEach((s) => (ret[s] = obj[s]));
		return ret;
	}

	export let username;
	let score_by_username = {};

	if (JSON.stringify(scores) === '{}') {
		for (const i of question_results) {
			scores[i.username] = 0;
		}
	}

	$: console.log(score_by_username, scores, 'dieter');
	for (const i of question_results) {
		score_by_username[i.username] = i.score;
	}

	$: scores = sortObjectbyValue(scores);

	const do_sth = () => {
		for (const i of Object.keys(score_by_username)) {
			scores[i] = (score_by_username[i] ?? 0) + (scores[i] ?? 0);
		}
		scores = scores;
	};

	do_sth();

	const get_user_rank = (username: string, scores_obj) => {
		const sortedScores = Object.entries(scores_obj);
		const rank = sortedScores.findIndex(([user]) => user === username) + 1;
    	return rank > 0 ? rank : null;
	};

	$: user_rank = get_user_rank(username, scores);
	$: console.log(`Your place: ${user_rank}`);
</script>

<div>
	<div class="flex justify-center h-screen">
		<div class="m-auto flex flex-col">
			<p class="p-4 bg-black bg-opacity-40 rounded-lg text-2xl">
				+{score_by_username[username] ?? '0'}
			</p>
			<p>Totale Score: {scores[username] ?? '0'}</p>
			<p>Jouw positie: {user_rank ?? 'Onbekend'}</p>
		</div>
	</div>
</div>
