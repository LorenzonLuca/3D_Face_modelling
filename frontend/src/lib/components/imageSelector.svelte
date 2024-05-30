<!--
    @component

    Component for select image choosing from webcam or upload image

    Parameter:
    
    - waitingImg: boolean that define if page is waiting for message from backend
    - token: token of authentication of user
-->
<script lang="ts">
    import {
        FileDropzone,
        getModalStore,
        getToastStore,
        type ModalSettings,
        type ToastSettings,
    } from "@skeletonlabs/skeleton";
    import Icon from "@iconify/svelte";
    import Camera from "$lib/components/camera.svelte";
    import { onMount } from "svelte";
    import { eventOk, ioStore } from "$lib/stores";

    const modalStore = getModalStore();
    const toastStore = getToastStore();

    let responseOk: string = "";
    eventOk.subscribe((value) => {
        responseOk = value;
    });
    let io: any;
    ioStore.subscribe((value) =>{
        io = value;
    })

    export let waitingImg: boolean;
    export let token: string | undefined;
    let files: FileList;
    let openCamera: boolean = false;
    let img: string | undefined = undefined;
    let width: number;
    let height: number;

    onMount(() => {
        io.off();
        io.on("image", (res: any) => {
            if (res.status === responseOk) {
                waitingImg = true;
            } else {
                const t: ToastSettings = {
                    message:
                        "Error while sending the image to the server. Retry",
                    timeout: 3000,
                    background: "variant-filled-error",
                };
                toastStore.trigger(t);
            }
        });
    });

    function loadImage(e: Event): void {
        if (validateFile(files[files.length - 1])) {
            imageToBase64(files[files.length - 1], (imgBase64: any) => {
                img = imgBase64;
            });
        }
    }

    function saveImageSize(): void {
        var i = new Image();
        i.onload = function () {
            width = i.width;
            height = i.height;
        };
        if (img === undefined) {
            return;
        }
        i.src = img;
    }

    function validateFile(file: any): boolean {
        const imageTypes = ["image/jpeg", "image/png"];
        return file && imageTypes.includes(file["type"]);
    }

    function imageToBase64(img: any, callback: Function): void {
        const reader = new FileReader();
        reader.addEventListener("load", () => callback(reader.result));
        reader.readAsDataURL(img);
    }

    function openWebCam(e: Event): void {
        openCamera = true;
    }

    function changeImage(e: Event): void {
        const confirm: ModalSettings = {
            type: "confirm",
            title: "Change photo",
            body: "Are you sure you want to change the image?",
            response: (r: boolean) => {
                if (r) {
                    img = undefined;
                    width = 0;
                    height = 0;
                }
            },
        };
        modalStore.trigger(confirm);
    }

    function elaborateImage(e: Event): void {
        const data = {
            img: img,
            auth: token !== undefined ? token : "",
        };
        io.emit("process_image", data);
    }

    $: if (img !== undefined) {
        saveImageSize();
    }
</script>

<div class="h-full p-4 lg:p-10 ">
    {#if openCamera}
        <Camera bind:openCamera bind:img />
    {:else if img !== undefined}
        <!-- svelte-ignore a11y-img-redundant-alt -->
        <div class="w-full h-full flex justify-center items-center">
            <div class="flex-col card w-full p-8 lg:w-2/3">
                {#if width > height}
                    <img
                        src={img}
                        alt="Image to send"
                        class="mx-auto mb-5"
                    />
                {:else}
                    <img
                        src={img}
                        alt="Image to send"
                        class="mx-auto mb-5 sm:w-1/3"
                    />
                {/if}
                <button
                    class="w-full flex justify-center p-2 mb-5 bg-success-500 hover:bg-success-700"
                    on:click={elaborateImage}
                >
                    <p class="text-xl">Elaborate</p>
                </button>
                <button
                    class="w-full flex justify-center p-2 variant-ghost-error hover:bg-error-500"
                    on:click={changeImage}
                >
                    <p class="text-xl">Change Image</p>
                </button>
            </div>
        </div>
    {:else}
        <div class="w-full h-full flex flex-wrap flex-cols items-center">
            <div class="w-full h-3/4 lg:h-full sm:columns-2">
                <div class="h-full sm:pr-6">
                    <FileDropzone
                        name="img"
                        bind:files
                        on:change={loadImage}
                        class="h-full"
                    >
                        <svelte:fragment slot="lead">
                            <Icon
                                icon="mdi:file-image-plus-outline"
                                width="100"
                                class="inline"
                            />
                        </svelte:fragment>
                        <svelte:fragment slot="message"
                            >Upload a file or drag and drop</svelte:fragment
                        >
                        <svelte:fragment slot="meta"
                            >PNG,JPG allowed</svelte:fragment
                        >
                    </FileDropzone>
                </div>
                <div class="h-full pl-6 hidden sm:block">
                    <button on:click={openWebCam} class="h-full w-full">
                        <div
                            class="h-full flex items-center justify-center border-2 border-solid border-gray-500 rounded-container-token bg-surface-700 transition hover:brightness-105"
                        >
                            <div class="flex-col">
                                <Icon icon="mdi:camera-outline" width="100" />
                                <p>Take photo</p>
                            </div>
                        </div>
                    </button>
                </div>
            </div>
            {#if token != undefined}
                <div class="block lg:hidden w-full text-center py-2">
                    <a href="/history" class="btn variant-filled-tertiary w-full"
                        >History</a
                    >
                </div>
            {/if}
        </div>
    {/if}
</div>
