<script lang="ts">
    import History from "$lib/components/history.svelte";
    import Icon from '@iconify/svelte';
    import type { PageData } from "./$types";
    import { goto } from "$app/navigation";

    export let data: PageData;

    function backToHome(){
        goto('/')
    }
</script>

<div class="h-full p-2">
    <button class="flex items-center justify-center mt-2" on:click={backToHome}>
        <Icon icon="mdi:arrow-back" width=45/>
        <div class="h-full items-center">
            <p>Back to Homepage</p>
        </div>
    </button>
    <History history={data?.history} authenticated={data.logged} />
</div>
