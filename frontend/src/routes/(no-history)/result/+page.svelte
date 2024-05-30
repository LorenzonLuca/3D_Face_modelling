<script lang="ts">
    import {
        resultElaborationImg,
        resultElaborationMesh,
        meshName,
    } from "$lib/stores";
    import Elaboration from "$lib/components/elaboration.svelte";
    import { goto } from "$app/navigation";

    let resultImg: string;
    let resultMesh: string;
    let nameMesh: string;
    resultElaborationImg.subscribe((value) => {
        resultImg = value;
    });
    resultElaborationMesh.subscribe((value) => {
        resultMesh = value;
    });
    meshName.subscribe((value) => {
        nameMesh = value;
    });

    function checkValues(img: string, mesh: string) {
        try {
            if (img == "" || mesh == "") {
                goto("/");
            }
        } catch (err) {}
    }

    $: checkValues(resultImg, resultMesh);
</script>

<Elaboration img={resultImg} mesh={resultMesh} name={nameMesh} />
