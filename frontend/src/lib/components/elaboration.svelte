<!--
    @component

    Template for show elaboration result

    Parameter:
    
    - img: image to show in base64
    - mesh: 3d model to show in base64
    - name: name of the file of 3d model for download
-->
<script lang="ts">
    import { Canvas } from "@threlte/core";
    import Scene from "$lib/components/Scene.svelte";
    import { goto } from "$app/navigation";
    import { selectedIndexHistory } from "$lib/stores";

    export let img: string;
    export let mesh: string;
    export let name: string = "mesh";

    let width: number;
    let height: number;

    function getSize(img: string) {
        try {
            var i = new Image();
            i.onload = function () {
                width = i.width;
                height = i.height;
            };
            i.src = img;
        } catch (err) {}
    }

    $: getSize(img);

    function donwloadModel() {
        var a = document.createElement("a");
        a.href = mesh;
        let fileName = name + ".glb";
        a.download = fileName;
        a.click();
    }

    function homePage() {
        goto("/");
        selectedIndexHistory.update((v) => undefined);
    }

    function history() {
        goto("/history");
        selectedIndexHistory.update((v) => undefined);
    }

    let innerWidth = 0;

    $: condition = innerWidth <= 768;
</script>

<svelte:window bind:innerWidth />

<div class="w-full h-full flex flex-wrap flex-cols items-center px-10">
    <div class="w-full md:w-1/3">
        {#if width > height}
            <img src={img} alt="Result" class="mx-auto mb-5" />
        {:else}
            <img src={img} alt="Result" class="mx-auto mb-5 w-3/5" />
        {/if}
    </div>
    <div class="w-full md:w-2/3 h-2/5 md:h-4/5">
        <Canvas>
            <Scene b64Mesh={mesh} dezoom={condition} />
        </Canvas>
    </div>
    <button on:click={donwloadModel} class="btn variant-filled-tertiary w-full"
        >Download 3D Object</button
    >
    <div class="w-full columns-2 lg:columns-1">
        <button on:click={homePage} class="btn variant-soft-tertiary w-full"
            >Homepage</button
        >
        <button
            on:click={history}
            class="btn variant-soft-tertiary w-full block lg:hidden"
            >History</button
        >
    </div>
</div>
