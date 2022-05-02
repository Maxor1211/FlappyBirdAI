<script lang="ts">
	import { onMount } from "svelte";
	import { Icon } from "@steeze-ui/svelte-icon";
	import { InformationCircle } from "@steeze-ui/heroicons";

	let data;
	let results = {
		title: "Article title",
		request_url:
			"https://nytimes.com/2022/03/26/us/politics/donald-trump-age-68-dies-at-night.html",
		result: { 0: 1, 1: 0, 2: 0, 3: 0 },
		request: [
			{
				id: 0,
				req_name: "dtree",
				disp_name: "Decision Tree",
				options: {
					criterion: "entropy",
					max_depth: 5,
					min_samples_split: 1000,
					min_samples_leaf: 4
				},
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
			data = window.location && window.location.hash && decodeURIComponent(atob(window.location.hash.substring(1)));
			data = JSON.parse(data);
		} catch {
			data = false;
		}
		results = data;
		data = true;
	});
</script>

{#if data}
	<div
		class="mx-auto text-center block sm:w-full md:w-2/3 lg:w-2/4 mt-6 text-slate-800 dark:text-slate-200">
		<div class="font-serif font-bold text-3xl uppercase center w-full">
			{results.title}
		</div>
		<div
			class="font-sans text-lg lowercase truncate italic hover:underline text-sky-600 dark:text-sky-400">
			<a href={results.request_url}>{results.request_url}</a>
		</div>
		<div class="flex justify-center mt-6 gap-x-4">
			{#each results.request as cfer (cfer.id)}
				{#if cfer.active}
					<div
						class="flex flex-col bg-slate-100/20 dark:bg-slate-800/20 rounded-lg basis-52 px-2 py-1 shadow-xl dark:shadow-slate-500/10">
						<div
							class="font-bold text-2xl md:text-4xl {results.result[cfer.id]
								? 'text-green-600'
								: 'text-rose-500'}">
							{results.result[cfer.id] ? "REAL" : "FAKE"}
						</div>
						<div>
							{cfer.disp_name}
						</div>
						<div class="mt-auto mb-0 group relative">
							<Icon
								src={InformationCircle}
								class="mt-4 mb-2 w-6 h-6 mx-auto text-sky-600/40 dark:text-sky-300/40" />
							<div
								class="invisible opacity-0 transition-all duration-300 group group-hover:visible hover:visible
							group-hover:opacity-100 hover:opacity-100 top-14 left-1/2 -translate-x-1/2 absolute bg-slate-50 dark:bg-slate-600 shadow-md w-56 rounded-md ">
								<div
									class="rotate-45 w-4 h-4 bg-slate-50 dark:bg-slate-600 relative z-10 -top-2 mx-auto" />
								<div>
									{#if cfer.id === 0}
										<p class="capitalize">{cfer.options.criterion}</p>
										<p>Max depth: {cfer.options.max_depth}</p>
										<p>Min. Samples Split: {cfer.options.min_samples_split}</p>
										<p>Min. Samples Leaf: {cfer.options.min_samples_leaf}</p>
									{:else if cfer.id === 1}
										<p>Alpha: {cfer.options.alpha}</p>
										<p class="capitalize">{cfer.options.type}</p>
									{:else if cfer.id === 2}
										<p>k Neighbours: {cfer.options.k_neighbours}</p>
										<p class="capitalize">{cfer.options.weight}</p>
										<p>Power: {cfer.options.power}</p>
									{:else if cfer.id === 3}
										<!--SVM-->
									{/if}
								</div>
							</div>
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
