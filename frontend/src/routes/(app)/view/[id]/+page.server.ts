import type { PageServerLoad } from "./$types";

export const load: PageServerLoad = async ({ cookies, params }) => {
    return {"id": params.id};
}