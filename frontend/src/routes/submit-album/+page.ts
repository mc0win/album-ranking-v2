import { superValidate } from "sveltekit-superforms"
import type { PageLoad } from "../$types"
import { zod4 } from "sveltekit-superforms/adapters"
import { submitSchema } from "../schemas"


export const load: PageLoad = async ({}) => {
    const submitForm = await superValidate(zod4(submitSchema))
    return {
        submitForm
    }
}