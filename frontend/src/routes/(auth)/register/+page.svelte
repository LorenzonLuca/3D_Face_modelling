<script lang="ts">
    import { getToastStore, type ToastSettings } from '@skeletonlabs/skeleton';
    import type { ActionData } from './$types';
    import AuthTemplate from '$lib/components/authTemplate.svelte';

    const toastStore = getToastStore();

    export let form: ActionData;
    $: showError(form)

    function showError(form: ActionData){
        if(form?.msg){
            const t: ToastSettings = {
                message: form.msg,
                timeout: 3000,
                background: 'variant-filled-error',
            }
            toastStore.trigger(t);
        }
    }
</script>

<AuthTemplate title="Register">
    <form method="post">
        <label class="label mt-3">
            <span>Username:</span>
            <input class="input" type="text" placeholder="Username..." name="username"/>
        </label>
        <label class="label mt-3">
            <span>Password:</span>
            <input class="input" type="password" placeholder="Password..." name="password"/>
        </label>
        <label class="label mt-3">
            <span>Confirm Password:</span>
            <input class="input" type="password" placeholder=" Repeat Password..." name="password2"/>
        </label>
        <button type="submit" class="btn variant-filled-tertiary mt-6">Register</button>
    </form>
    <div class="pt-5">
        <a href="/login" class="text-primary-500">Already have an account? Login here</a>
        <br>
        <a href="/" class="text-primary-500">Continue as guest</a>
    </div>
</AuthTemplate>