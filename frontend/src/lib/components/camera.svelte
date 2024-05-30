<!--
    @component

    Webcam component

    Parameter:
    
    - openCamera: boolean variable for start/stop webcam recording
    - img: image result of webcam
-->
<script lang="ts">
    import Icon from "@iconify/svelte";
    import Loader from "./loader.svelte";
    export let openCamera: boolean;
    export let img: string | undefined;

    let videoSource: any = null;
    let loading = false;
    let stream: any = null;
    let webcamError: boolean = false;
    let webcamErrorMsg: string = "";

    async function obtenerVideoCamera(): Promise<void> {
        try {
            loading = true;
            stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 1920 },
                    height: { ideal: 1080 },
                },
            });
            videoSource.srcObject = stream;
            videoSource.play();
            loading = false;
        } catch (error: any) {
            webcamErrorMsg = error.message;
            webcamError = true;
            loading = false;
        }
    }

    function capturePhoto(): void {
        const canvas = document.createElement("canvas");
        canvas.width = videoSource.videoWidth;
        canvas.height = videoSource.videoHeight;
        canvas.getContext("2d")!.drawImage(videoSource, 0, 0, canvas.width, canvas.height);
        img = canvas.toDataURL("image/jpeg");
        closeStream();
    }

    function closeStream(): void {
        if (stream) {
            stream.getTracks().forEach(function (track: any) {
                track.stop();
            });
        }
        openCamera = false;
    }

    $: if (openCamera) {
        obtenerVideoCamera();
    }
</script>

<div class="w-full h-full flex justify-center">
    <div class="w-full">
        <!-- svelte-ignore a11y-media-has-caption -->
        <div class="flex justify-center">
            <div class="flex-col card p-8 w-content w-2/3">
                {#if !loading}
                    <button
                        class="flex items-center justify-center mb-5"
                        on:click={closeStream}
                    >
                        <Icon icon="mdi:arrow-back" width="45" />
                        <div class="h-full items-center">
                            <p>Back to Homepage</p>
                        </div>
                    </button>
                {:else}
                    <Loader />
                {/if}
                {#if !loading && webcamError}
                    <div class="card variant-filled-error p-5 mb-5">
                        <h2 class="text-2xl">Error to access webcam:</h2>
                        <p>{webcamErrorMsg}</p>
                    </div>
                {:else}
                    <video bind:this={videoSource} class="mb-5" />
                {/if}
                {#if !loading && !webcamError}
                    <div class="w-full">
                        <button
                            class="w-full flex justify-center p-2 bg-success-500 hover:bg-success-700"
                            on:click={capturePhoto}
                        >
                            <Icon icon="mdi:camera-outline" width="45" />
                        </button>
                    </div>
                {/if}
            </div>
        </div>
    </div>
</div>
