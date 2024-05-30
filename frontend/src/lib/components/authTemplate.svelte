<!--
    @component

    Template for auth pages (login & register)

    Parameter:
    
    - title: title of the page section
-->
<script lang="ts">
    export let title: string;
</script>


<div class="w-full h-full flex items-center">
    <div class="card bg-initial mx-auto py-12 px-5 md:px-10 lg:px-30 w-5/6 md:w-2/3 lg:w-1/2 ">
        <h2 class="text-xl mb-6">{title}</h2>
        <slot />
    </div> 
</div>