<script lang="ts">
    import { ProgressBar, getToastStore, type ToastSettings } from "@skeletonlabs/skeleton";
    import { onMount } from "svelte";
    import { eventOk, resultElaborationImg, resultElaborationMesh, meshName, ioStore } from "$lib/stores";
    import { goto } from "$app/navigation";

    let responseOk: string = "";
    eventOk.subscribe((value) =>{
        responseOk = value;
    })
    let io: any;
    ioStore.subscribe((value) =>{
        io = value;
    })
    const toastStore = getToastStore();

    let progressValue: number | undefined = undefined;
    let queueFinished: boolean = false;
    let queueIndex: number;

    onMount(() =>{
        io.on('queue_number', (res: any) => {
            const i = Number(res.index)
            queueIndex = i;
            if(i == 0 && !queueFinished){
                queueFinished = true;
            }
        })
        io.on('status_elaboration', (res: any) => {
            if(res.status == responseOk){
                const status = Number(res.value);
                progressValue = status;  
                if(status == 100){
                    resultElaborationImg.update((v) => "data:image/jpeg;base64," + res.img)
                    resultElaborationMesh.update((v) => "data:content/type;base64," + res.mesh)
                    meshName.update((v) => res.mesh_name)
                    goto("/result");
                }
            }else{
                let msg = 'Error while elaborating image.'
                if(res.msg == "NO-FACE"){
                    msg += "Cannot find a face inside the image."
                }else if (res.msg == "INVALID-VALUES"){
                    msg += "Cannot elaborate this image, retry again."
                }
                
                const t: ToastSettings = {
                    message: msg,
                    timeout: 5000,
                    background: 'variant-filled-error',
                }
                toastStore.trigger(t);
                goto('/');
            }  
        })
    })

</script>

<div class="w-full h-full flex items-center justify-center">
    <div class="flex-col w-2/3">
        <h1 class="text-2xl py-4">
        {#if queueIndex == undefined}
            Waiting
        {:else if queueFinished}
            Loading
        {:else}
            Users in queue: {queueIndex}
        {/if}
        </h1>
        <ProgressBar value={progressValue} meter='bg-primary-500' max={100}/> 
    </div>     
</div>