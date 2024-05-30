<script lang="ts">
	import { AppShell } from "@skeletonlabs/skeleton";
	import type { PageData } from "./$types";
	import ImageSelector from "$lib/components/imageSelector.svelte";
	import { goto } from "$app/navigation";

	export let data: PageData;
	let waitingImg: boolean = false;

	$: if (waitingImg) {
		goto("/running");
	}
</script>

<AppShell>
	<ImageSelector
		bind:waitingImg
		token={data.logged ? data.token : undefined}
	/>
</AppShell>
