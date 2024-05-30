<script lang="ts">
	import '../../app.postcss';
	import { AppShell, AppBar, Modal, initializeStores, Toast} from '@skeletonlabs/skeleton';
	import History from "$lib/components/history.svelte";
    import type { LayoutData } from './$types';
	import { enhance } from "$app/forms";
	import { selectedIndexHistory } from '$lib/stores';

	initializeStores();

	export let data: LayoutData;
	
	function resetHistory(){
        selectedIndexHistory.update((v) => undefined)
	}
</script>

<Modal />
<Toast />

<AppShell>
	<svelte:fragment slot="pageHeader">
		<AppBar class="lg:border-r-2 lg:border-surface-700">
			<svelte:fragment slot="lead">
				<h1 class="text-3xl"><a href="/" on:click={resetHistory}>3D Face Modelling</a></h1>
			</svelte:fragment>
			<svelte:fragment slot="trail">
				{#if data.username}
					<p class="text-xl">{data.username}</p>
					<!-- <Logout /> -->
					<form method="post" action="?/logout" use:enhance>
						<button class="text-sm text-error-500" type="submit">Logout</button>
					</form>
				{:else}
					<button><a href="/login" class="text-xl">Login</a></button>
					<button><a href="/register" class="text-xl">Register</a></button>
				{/if}
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<div class="lg:border-r-2 lg:border-surface-700 h-full">
		<slot />
	</div>
	<svelte:fragment slot="sidebarRight">
		<div class="hidden lg:block h-full">
			<History history={data?.history} authenticated={data.logged} />
		</div>
	</svelte:fragment>
	<svelte:fragment slot="pageFooter">
		<AppBar>
			<svelte:fragment slot="lead">
				<p class="text-xs">Copyright Luca Lorenzon</p>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
</AppShell>