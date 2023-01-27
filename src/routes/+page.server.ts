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
            model: "text-davinci-003",
            prompt: `
            Here is an example of a DAI Global project description:

            Project: Worldwide—Digital Frontiers
            Client: U.S. Agency for International Development

            Across the developing world, digital technologies are accelerating change at every level of society—from mobile solutions that serve rural women’s savings groups in Tanzania to data-driven decision-making tools for natural resource planning in Honduras. The challenge is that, to date, these solutions have not matched the pace and scale of the problems they address.
            
            Digital Frontiers is a $74.4 million buy-in mechanism available to bureaus and missions of the U.S. Agency for International Development (USAID). We work closely with USAID’s Global Development Lab (GDL), the Center for Digital Development (CDD), USAID Missions, the private sector, and international and local development organizations to identify successful and sustainable digital development approaches and scale their impact globally.
            
            Digital Frontiers helps USAID have greater impact across its development portfolio by advancing digital tools and approaches in the areas of digital finance, digital inclusion, ICT for development, geospatial, and digital knowledge and insights.

            
            Write a new DAI Global project description based on the following project: ${textPrompt}.`,
            temperature: 0.6,
            max_tokens: 2048,
        });


        return {
            response: textResponse.data.choices[0].text,
        }
    }
}