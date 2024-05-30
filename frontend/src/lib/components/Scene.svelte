<!--
    @component

    Scene for show 3dmodel created using Threlte (Three.js)

	Parameter:
	
     - b64mesh: 3d model to show in base64 
     - dezoom: boolean used for know if user is using mobile device or not. In case it change the default zoom position
-->
<script lang="ts">
	import { T } from "@threlte/core";
	import { OrbitControls, useGltf } from "@threlte/extras";
	export let b64Mesh: string;
	export let dezoom: boolean;
</script>

<!-- Orthographic camera -->
<T.OrthographicCamera
	position={[0, 0, 10]}
	zoom={dezoom ? 75 : 150}
	makeDefault
>
	<!-- Controls -->
	<OrbitControls enableDamping />
</T.OrthographicCamera>

<!-- Main light -->
<T.PointLight intensity={100} position={[0, 3.5, 8]} color="#ffffff" />

{#await useGltf(b64Mesh) then model}
	<T is={model.scene} position.y={-0.2} />
{/await}
