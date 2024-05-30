<!--
    @component

    Loader component founded https://uiverse.io/mrpumps31232/strange-dragonfly-94
-->
<div class="loading-wave w-full mx-auto">
    <div class="loading-bar bg-primary-500"></div>
    <div class="loading-bar bg-secondary-500"></div>
    <div class="loading-bar bg-tertiary-500"></div>
    <div class="loading-bar bg-secondary-500"></div>
    <div class="loading-bar bg-primary-500"></div>
</div>

<style>
    .loading-wave {
        width: 300px;
        height: 100px;
        display: flex;
        justify-content: center;
        align-items: flex-end;
    }

    .loading-bar {
        width: 20px;
        height: 10px;
        margin: 0 5px;
        border-radius: 5px;
        animation: loading-wave-animation 1s ease-in-out infinite;
    }

    .loading-bar:nth-child(2) {
        animation-delay: 0.1s;
    }

    .loading-bar:nth-child(3) {
        animation-delay: 0.2s;
    }

    .loading-bar:nth-child(4) {
        animation-delay: 0.3s;
    }

    .loading-bar:nth-child(5) {
        animation-delay: 0.4s;
    }

    @keyframes loading-wave-animation {
        0% {
            height: 10px;
        }

        50% {
            height: 50px;
        }

        100% {
            height: 10px;
        }
    }
</style>