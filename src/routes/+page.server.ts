import { Configuration, OpenAIApi } from 'openai';
import { OPENAI_KEY } from '$env/static/private';
import type { Actions } from './$types';

export const actions: Actions = {
    submit: async ({ request } : any) => {
        const promptFormData = await request.formData();
        const textPrompt = promptFormData.get('text-submission') as string;
        const configuration = new Configuration({
            apiKey: OPENAI_KEY,
        });

        const openai = new OpenAIApi(configuration);

        const textResponse = await openai.createCompletion({
            model: "davinci:ft-tinyquark-2023-01-28-20-01-11",
            prompt: textPrompt,
            temperature: 0.4,
            max_tokens: 600,
            top_p: 1,
            frequency_penalty: 0.25,
            presence_penalty: 0,
        });

        return {
            response: textResponse.data.choices[0].text,
        }
    }
}