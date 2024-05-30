<script lang="ts">
	import '../../app.postcss';
	import { AppShell, AppBar, Toast} from '@skeletonlabs/skeleton';
	import { initializeStores } from '@skeletonlabs/skeleton';

	initializeStores();

</script>

<Toast />

<AppShell>
	<svelte:fragment slot="header">
		<AppBar>
			<svelte:fragment slot="lead">
				<h1 class="text-3xl"><a href="/">3D Face Modelling</a></h1>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
	<slot />
	<svelte:fragment slot="pageFooter">
		<AppBar>
			<svelte:fragment slot="lead">
				<p class="text-xs">Copyright Luca Lorenzon</p>
			</svelte:fragment>
		</AppBar>
	</svelte:fragment>
</AppShell>