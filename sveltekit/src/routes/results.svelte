<script lang="ts">
	import { onMount } from "svelte";

	let data;
	let results = {
		title: "Article title",
		request_url:
			"https://nytimes.com/2022/03/26/us/politics/donald-trump-age-68-dies-at-night.html",
		result: { 0: 0, 1: 0, 2: 0, 3: 0 },
		request: [
			{
				id: 0,
				req_name: "dtree",
				disp_name: "Decision Tree",
				options: { criterion: "entropy", max_depth: 5, min_samples_leaf: 4 },
				active: true
			},
			{
				id: 1,
				req_name: "nb",
				disp_name: "Naive Bayes",
				options: { alpha: 0.5, type: "multinomial" },
				active: true,
				disabled: true
			},
			{
				id: 2,
				req_name: "knn",
				disp_name: "K-Nearest Neighbours",
				options: { k_neighbours: 4, weight: "uniform", power: 2 },
				active: true,
				disabled: true
			},
			{
				id: 3,
				req_name: "svm",
				disp_name: "Support Vector Machine",
				options: {},
				active: true,
				disabled: true
			}
		],
		stats: {}
	};
	onMount(() => {
		try {
			data = window.location && window.location.hash && atob(window.location.hash.substring(1));
			data = JSON.parse(data);
		} catch {
			data = false;
		}
		console.log(data);
	});
</script>

{#if data}
	<div class="mx-auto text-center block sm:w-full md:w-2/3 lg:w-2/4 mt-6 text-slate-800 dark:text-slate-200">
		<div class="font-serif font-bold text-3xl uppercase center w-full">
			{results.title}
		</div>
		<div
			class="font-sans text-lg lowercase truncate italic hover:underline text-sky-600 dark:text-sky-400">
			<a href={results.request_url}>{results.request_url}</a>
		</div>
		<div class="grid grid-cols-2 md:grid-cols-4 mt-6 gap-x-4">
			{#each results.request as cfer (cfer.id)}
				{#if cfer.active}
					<div class="bg-slate-100/20 dark:bg-slate-800/20 rounded-lg px-2 py-1 shadow-md">
						<div class:text-rose-500={!results.result[cfer.id]} class-text-green-500={results.result[cfer.id]}
						class="font-bold text-2xl md:text-4xl">
							{results.result[cfer.id] ? "TRUE" : "FAKE"}
						</div>
						<div>
							{cfer.disp_name}
						</div>
						<div>
							{cfer.options}
						</div>
					</div>
				{/if}
			{/each}
		</div>
	</div>
{:else}
	<div class="mx-auto text-center block w-fit mt-12 text-slate-800 dark:text-slate-200">
		<div class="italic text-lg font-bold">Checking results...</div>
		<div>If loading persists make sure the link is correct.</div>
	</div>
{/if}
