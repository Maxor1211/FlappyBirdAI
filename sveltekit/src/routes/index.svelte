<script lang="ts">
	import { Icon } from "@steeze-ui/svelte-icon";
	import { Search, EmojiSad, Close, Settings } from "@steeze-ui/iconic-free";

	let	request_url = "",
		disabled = false,
		modal = 52,
		hidden = true;

	const classifiers = [
		{ id: 0, req_name: "dtree", disp_name: "Decision Tree", active: true },
		{ id: 1, req_name: "nb", disp_name: "Naive Bayes", active: false },
		{ id: 2, req_name: "knn", disp_name: "K-Nearest Neighbours", active: false },
		{ id: 3, req_name: "svm", disp_name: "Support Vector Machine", active: false, disabled: true }
	];

	async function get_result() {
		let classifier = [];
		for(const cfer of classifiers) {
			if(cfer.active)
			classifier.push(cfer.req_name);
		}
		const url = `/api/${classifier.join(',')}/${encodeURIComponent(request_url)}`;
		console.log(url);
		const res = await fetch(url);
		const res_json = await res.json();
		if (res.ok) {
			return res_json;
		} else {
			throw new Error(res_json);
		}
	}

	let promise = get_result();

	function handle_new_req() {
		promise = get_result();
	}
</script>

<label class="relative text-gray-400 focus-within:text-gray-600 block mx-auto w-5/6 md:w-2/3">
	<input
		bind:value="{request_url}"
		on:click="{()=>{request_url=""}}"
		placeholder="Enter a news article URL..."
		class="form-input rounded-xl appearance-none w-full focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 placeholder:italic placeholder:text-slate-400 focus:placeholder:text-gray-600" />
	<Icon
		src={Search}
		class="w-8 h-8 pointer-events-none absolute top-1/2 transform -translate-y-1/2 right-3" />
</label>

<div
	class:hidden
	tabindex="-1"
	aria-hidden={hidden}
	class="bg-slate-900/10 overflow-y-auto overflow-x-hidden fixed top-0 right-0 left-0 transition-opacity duration-700 opacity-{Math.floor(
		-1.92307692 * modal + 100
	)} z-50 w-full md:inset-0 h-modal md:h-full justify-center items-center"
	on:click|self={() => {
		modal = 52;
		setTimeout(() => {
			hidden = true;
		}, 700);
	}}>
	<div
		class="relative p-4 mx-auto mt-16 will-change-transform transition-transform translate-y-{modal} duration-1000 w-full max-w-md h-full md:h-auto">
		<div class="relative px-6 py-6 lg:px-8 xl:py-8 bg-white rounded-lg shadow dark:bg-gray-700">
			<div class="flex justify-end mb-4">
				<h3 class="text-xl font-medium text-gray-900 dark:text-white w-fit">
					Modify machine learning settings
				</h3>
				<button
					type="button"
					class="w-8 h-8 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-800 dark:hover:text-white"
					on:click={() => {
						modal = 52;
						setTimeout(() => {
							hidden = true;
						}, 700);
					}}>
					<Icon src={Close} class="h-5 w-5" />
				</button>
			</div>
			<form class="mb-4 space-y-6" action="#">
				<div class="grid grid-cols-1 gap-2">
					{#each classifiers as cfer (cfer.id)}
						<div class:opacity-20={cfer.disabled}>
							<label class="text-gray-500 dark:text-gray-400 text-lg select-none">
								<input
									disabled={cfer.disabled}
									type="checkbox"
									class="form-checkbox text-rose-600 dark:text-sky-600 appearance-none rounded-full h-6 w-6
									disabled:cursor-not-allowed mr-1 hover:ring-4"
									value=""
									bind:checked="{cfer.active}" />
								{cfer.disp_name}
							</label>
						</div>
					{/each}
				</div>
			</form>
		</div>
	</div>
</div>

<div class="mx-auto w-fit mt-6 flex flex-row gap-2">
	<button
		class="text-white bg-gradient-to-br dark:from-sky-500 dark:via-sky-600 dark:to-sky-700 
	from-red-400 via-rose-600 to-rose-700 font-bold
	disabled:from-slate-500 disabled:via-slate-600 disabled:to-slate-700
	dark:disabled:from-slate-500 dark:disabled:via-slate-600 dark:disabled:to-slate-700
	will-change-transform
	hover:scale-110 transition ease-in-out delay-150 duration-500 
	disabled:hover:scale-100 disabled:cursor-not-allowed 
	focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800
	rounded-lg px-2 py-2 text-center"
		type="button"
		on:click={() => {
			hidden = false;
			setTimeout(() => {
				modal = 0;
			}, 50);
		}}>
		<Icon src={Settings} class="h-8" />
	</button>

	<button
		type="button"
		{disabled}
		class="text-white bg-gradient-to-br dark:from-sky-500 dark:via-sky-600 dark:to-sky-700 
	from-red-400 via-rose-600 to-rose-700 font-bold
	disabled:from-slate-500 disabled:via-slate-600 disabled:to-slate-700
	dark:disabled:from-slate-500 dark:disabled:via-slate-600 dark:disabled:to-slate-700
	will-change-transform
	hover:scale-110 transition ease-in-out delay-150 duration-500 
	disabled:hover:scale-100 disabled:cursor-not-allowed 
	focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800
	rounded-lg text-lg px-5 py-2.5 text-center"
	on:click={get_result}>Check</button>
</div>

{#await promise}
	<div class="mx-auto w-fit mt-6">
		<svg
			role="status"
			class="inline w-8 h-8 text-gray-200 animate-spin dark:text-gray-600 fill-rose-600 dark:fill-blue-600"
			viewBox="0 0 100 101"
			fill="none"
			xmlns="http://www.w3.org/2000/svg">
			<path
				d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
				fill="currentColor" />
			<path
				d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
				fill="currentFill" />
		</svg>
	</div>
{:then result}
	<p>Result</p>
{:catch error}
	{#if error.message.includes("JSON")}
		<br />
	{:else}
		<div
			class="flex p-2 mt-8 w-4/5 mx-auto md:w-1/3 text-red-700 bg-red-100 rounded-lg dark:bg-red-200 dark:text-red-800"
			role="alert">
			<Icon src={EmojiSad} class="inline flex-shrink-0 mr-3 -mt-0.5 w-8 h-8" />
			<div>
				<span class="font-medium">Error: {error.message}</span><br /> Check your URL, or try again later.
			</div>
		</div>
	{/if}
{/await}
<br class="translate-y-52 opacity-0 opacity-100" />
