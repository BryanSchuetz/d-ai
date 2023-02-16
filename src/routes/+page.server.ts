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
            model: "davinci:ft-tinyquark-2023-02-16-19-24-41",
            prompt: `${textPrompt}\n\n###\n\n`,
            temperature: 0.4,
            max_tokens: 800,
            frequency_penalty: 0.25,
            presence_penalty: 0,
            stop: ["###"],
        });

        return {
            response: textResponse.data.choices[0].text,
        }
    }
}