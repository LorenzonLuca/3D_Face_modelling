<script lang="ts">
    import type { PageData } from "./$types";
    import Elaboration from "$lib/components/elaboration.svelte";
    import { goto } from "$app/navigation";

    export let data: PageData;

    const history = data.history;

    let img = "";
    let mesh = "";
    let name = "";

    function setValues(id: any) {
        let index = Number(id);
        const value = history[index];
        img = "data:image/jpeg;base64," + value.img;
        mesh = "data:content/type;base64," + value.mesh;
        name = value.mesh_name;
    }

    $: setValues(data.id);
</script>

<div class="w-full h-full">
    <Elaboration {img} {mesh} {name} />
</div>
