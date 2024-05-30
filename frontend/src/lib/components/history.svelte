<!--
    @component

    History section

    Parameter:
    
    - history: array of element to put inside the history
    - authenticated: boolean value for know if the user is authenticated inside the website
-->
<script lang="ts">
    import { goto } from "$app/navigation";
    import { selectedIndexHistory } from "$lib/stores";

    export let history: any[] = [];
    export let authenticated: boolean = false;
    let selectedIndex: number | undefined;
    selectedIndexHistory.subscribe((value) => {
        selectedIndex = value;
    });

    let errorMsg: string | undefined = undefined;
    $: if (!authenticated) {
        errorMsg = "Log in for save values in your history";
    } else if (history.length == 0) {
        errorMsg = "There aren't values in your history";
    }

    function convertDate(date: Date){
        const d = new Date(date);
        
        return `${String(d.getDate()).padStart(2,'0')}.${String(d.getMonth()+1).padStart(2,'0')}.${d.getFullYear()} - 
        ${String(d.getHours()-1).padStart(2,'0')}:${String(d.getMinutes()).padStart(2,'0')}`;
    }

    function selectElement(index: number){
        goto(`/view/${index}`);
        selectedIndexHistory.update((v) => index)
    }
</script>

<div class="p-5 h-screen">
    <h1 class="text-5xl p-10 text-center">History</h1>
    {#if errorMsg === undefined}
        <div class="p-2 flex flex-col flex-wrap overflow-auto items-center">
            {#each history as el, index}
                <button on:click={() => selectElement(index)} class={selectedIndex != index ? "" : "rounded-md p-2 variant-ghost-secondary"}>
                    <div class="w-fit py-2 grid grid-rows-4 items-center justify-center">
                        <img src={`data:image/jpeg;base64,${el.img}`} alt={`element ${el.id}`} width="200" class="row-span-3">
                        <h1>{convertDate(el.date)}</h1>
                    </div>
                </button>
            {/each}
        </div>
    {:else}
        <div class="p-10">
            <p class="text-error-500">{errorMsg}</p>
        </div>
    {/if}
</div>
