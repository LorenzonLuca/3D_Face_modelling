<script lang="ts">
	import '../../app.postcss';
	import { AppShell, AppBar, Modal, initializeStores, Toast} from '@skeletonlabs/skeleton';
	import History from "$lib/components/history.svelte";
    import type { LayoutData } from './$types';
	import { enhance } from "$app/forms";

	initializeStores();

	export let data: LayoutData;
</script>

<Modal />
<Toast />

<AppShell>
	<svelte:fragment slot="pageHeader">
		<AppBar>
			<svelte:fragment slot="lead">
				<h1 class="text-3xl"><a href="/">3D Face Modelling</a></h1>
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
	<slot />
</AppShell>