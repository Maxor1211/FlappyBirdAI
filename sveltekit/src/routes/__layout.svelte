<script>
	import "../app.css";
	import "flowbite/dist/flowbite.css";
	import { Icon } from "@steeze-ui/svelte-icon";
	import { Moon, Sun } from "@steeze-ui/heroicons";
	import { Code } from "@steeze-ui/iconic-free";

	let light_visible;

	// Change the icons inside the button based on previous settings
	if (
		localStorage.getItem("color-theme") === "dark" ||
		(!("color-theme" in localStorage) && window.matchMedia("(prefers-color-scheme: dark)").matches)
	)
		light_visible = true;
	else light_visible = false;

	function toggle_dark_mode() {
		// toggle icons inside button
		light_visible = light_visible ? false : true;

		// if set via local storage previously
		if (localStorage.getItem("color-theme")) {
			if (localStorage.getItem("color-theme") === "light") {
				document.documentElement.classList.add("dark");
				localStorage.setItem("color-theme", "dark");
			} else {
				document.documentElement.classList.remove("dark");
				localStorage.setItem("color-theme", "light");
			}

			// if NOT set via local storage previously
		} else {
			if (document.documentElement.classList.contains("dark")) {
				document.documentElement.classList.remove("dark");
				localStorage.setItem("color-theme", "light");
			} else {
				document.documentElement.classList.add("dark");
				localStorage.setItem("color-theme", "dark");
			}
		}
	}
</script>

<svelte:head>
	<title>is it real.ml</title>
    <meta name="description" content="Check if an article is real using machine learning models — By Yaseen AlMannaee" />
	<link rel="preconnect" href="https://fonts.googleapis.com" />
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
	<link
		href="https://fonts.googleapis.com/css2?family=Lemon&display=swap"
		rel="stylesheet" />
</svelte:head>

<div class="flex flex-col h-screen justify-between">
	<header class="mx-auto text-center mt-16 mb-10 md:mt-8">
		<a href="/" class="text-gray-900 dark:text-white group relative">
			<span class="tracking-tight text-sm italic absolute bottom-0 -right-4">.ml</span>
			<span class="logotype font-['Lemon'] p-1 text-6xl group-hover:underline">is it real</span>
		</a>
		<br />
		<button
			on:click={toggle_dark_mode}
			type="button"
			class="text-slate-900 dark:text-slate-50 hover:bg-gray-100 
		dark:hover:bg-gray-700 rounded-lg text-sm p-1px absolute right-2 top-2">
			<Icon src={Moon} theme="solid" class={light_visible ? "h-8" : "hidden h-8"} />
			<Icon src={Sun} theme="solid" class={light_visible ? "hidden h-8" : "h-8"} />
		</button>
		<a
			href="https://www.github.com/y-almannaee/is-it-real"
			class="text-slate-900 dark:text-slate-50 hover:bg-gray-100 
		dark:hover:bg-gray-700 rounded-lg text-sm p-1px absolute right-11 top-2"
			><Icon src={Code} theme="solid" class="h-8" />
			<span class="flex absolute top-0.5 right-0.5 h-2 w-2">
				<span
					class="animate-ping absolute inline-flex h-full w-full rounded-full bg-rose-400 dark:bg-sky-400 opacity-75" />
				<span class="relative inline-flex rounded-full h-2 w-2 bg-rose-600 dark:bg-sky-500" />
			</span>
		</a>
	</header>

	<main class="mb-auto">
		<slot />
	</main>

	<footer class="p-4 mx-auto md:flex md:items-center md:justify-between md:p-6">
		<span class="text-sm text-gray-500 sm:text-center dark:text-gray-400">
			© 2022 <a
				href="https://yaseen.ae"
				class="font-semibold text-gray-700 dark:text-gray-300 hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
				>Yaseen AlMannaee</a>
			<br /> Built with
			<a
				class="font-semibold text-gray-700 dark:text-gray-300 hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
				href="https://kit.svelte.dev">SvelteKit</a
			> and 
			<a
				class="font-semibold text-gray-700 dark:text-gray-300 hover:underline decoration-rose-700 dark:decoration-sky-500 decoration-2"
				href="https://tailwindcss.com">TailwindCSS</a
			>
		</span>
		<!-- <ul class="flex flex-wrap items-center mt-3 text-sm text-gray-500 dark:text-gray-400 sm:mt-0">
				<li>
					<a href="#" class="mr-4 hover:underline md:mr-6 ">About</a>
				</li>
				<li>
					<a href="#" class="mr-4 hover:underline md:mr-6">Privacy Policy</a>
				</li>
				<li>
					<a href="#" class="mr-4 hover:underline md:mr-6">Licensing</a>
				</li>
				<li>
					<a href="#" class="hover:underline">Contact</a>
				</li>
			</ul> -->
	</footer>
</div>
