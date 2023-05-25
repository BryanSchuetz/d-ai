<script lang="ts">
  import { enhance, type SubmitFunction } from '$app/forms';

  let textSubmission = "";
  let answer = "";
  let loading = false;
  let docs = [];
  let sources = [];

  const handleSubmit: SubmitFunction = () => {
      loading = true;

return async ({ action, result }) => {
          console.log(result);
          let resultObject = JSON.parse(JSON.stringify(result));
          if (action.search == "?/submit") {
              if (resultObject.status == 200) {
                  if (resultObject.data.response) {
                      answer = resultObject.data.response.trim();
                  }
                  if (resultObject.data.docs) {
                      sources = [];
                      docs = resultObject.data.docs;
                  }
                  loading = false;
              } else {
                  loading = false;
                  alert("An error occurred, please try again.");
              }
          }
      }
}
</script>


<section class="w-full p-8 max-w-2xl m-auto">
    <div class="sm:flex">
      <div class="mb-4 flex-shrink-0 sm:mb-0 sm:mr-2 self-center">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-10 h-10 hidden sm:block">
          <path stroke-linecap="round" stroke-linejoin="round" d="M8.25 3v1.5M4.5 8.25H3m18 0h-1.5M4.5 12H3m18 0h-1.5m-15 3.75H3m18 0h-1.5M8.25 19.5V21M12 3v1.5m0 15V21m3.75-18v1.5m0 15V21m-9-1.5h10.5a2.25 2.25 0 002.25-2.25V6.75a2.25 2.25 0 00-2.25-2.25H6.75A2.25 2.25 0 004.5 6.75v10.5a2.25 2.25 0 002.25 2.25zm.75-12h9v9h-9v-9z" />
        </svg>        
      </div>
      <div>
        <h1 class="prose text-3xl lg:text-4xl mb-0">D-AI Writting Assistant</h1>
      </div>
      </div>

  {#if loading === false}
      <section id="form-box" class="prose mb-8">
        <div class="sm:flex">
        <div>
          <h4 class="text-lg font-bold mb-0">Powerd by OpenAI <svg class="h-5 w-5 text-black relative top-[-2px] inline" fill="#000000" width="800px" height="800px" viewBox="0 0 24 24" role="img" xmlns="http://www.w3.org/2000/svg"><title>OpenAI icon</title><path d="M22.2819 9.8211a5.9847 5.9847 0 0 0-.5157-4.9108 6.0462 6.0462 0 0 0-6.5098-2.9A6.0651 6.0651 0 0 0 4.9807 4.1818a5.9847 5.9847 0 0 0-3.9977 2.9 6.0462 6.0462 0 0 0 .7427 7.0966 5.98 5.98 0 0 0 .511 4.9107 6.051 6.051 0 0 0 6.5146 2.9001A5.9847 5.9847 0 0 0 13.2599 24a6.0557 6.0557 0 0 0 5.7718-4.2058 5.9894 5.9894 0 0 0 3.9977-2.9001 6.0557 6.0557 0 0 0-.7475-7.0729zm-9.022 12.6081a4.4755 4.4755 0 0 1-2.8764-1.0408l.1419-.0804 4.7783-2.7582a.7948.7948 0 0 0 .3927-.6813v-6.7369l2.02 1.1686a.071.071 0 0 1 .038.052v5.5826a4.504 4.504 0 0 1-4.4945 4.4944zm-9.6607-4.1254a4.4708 4.4708 0 0 1-.5346-3.0137l.142.0852 4.783 2.7582a.7712.7712 0 0 0 .7806 0l5.8428-3.3685v2.3324a.0804.0804 0 0 1-.0332.0615L9.74 19.9502a4.4992 4.4992 0 0 1-6.1408-1.6464zM2.3408 7.8956a4.485 4.485 0 0 1 2.3655-1.9728V11.6a.7664.7664 0 0 0 .3879.6765l5.8144 3.3543-2.0201 1.1685a.0757.0757 0 0 1-.071 0l-4.8303-2.7865A4.504 4.504 0 0 1 2.3408 7.872zm16.5963 3.8558L13.1038 8.364 15.1192 7.2a.0757.0757 0 0 1 .071 0l4.8303 2.7913a4.4944 4.4944 0 0 1-.6765 8.1042v-5.6772a.79.79 0 0 0-.407-.667zm2.0107-3.0231l-.142-.0852-4.7735-2.7818a.7759.7759 0 0 0-.7854 0L9.409 9.2297V6.8974a.0662.0662 0 0 1 .0284-.0615l4.8303-2.7866a4.4992 4.4992 0 0 1 6.6802 4.66zM8.3065 12.863l-2.02-1.1638a.0804.0804 0 0 1-.038-.0567V6.0742a4.4992 4.4992 0 0 1 7.3757-3.4537l-.142.0805L8.704 5.459a.7948.7948 0 0 0-.3927.6813zm1.0976-2.3654l2.602-1.4998 2.6069 1.4998v2.9994l-2.5974 1.4997-2.6067-1.4997Z"/></svg></h4>
          <p>This model has been given access to a <strong>vector database of DAI primary sources</strong>, including every blog post, project description, and solution page we've ever published. The model has been instructed to assist you in your writing, provide citations to the text it generates, and to not make things up.</p>
          <p><strong>Example Query:</strong> <em>Explain impact bonds as a component of development finance.</em></p>
        </div>
        </div>
          <form class="form"  action="?/submit" method="POST" enctype="multipart/form-data" use:enhance={handleSubmit} id="upload" name="upload">
              <div class="field">
                  <div class="control">
                      <textarea id="text-submission" name="text-submission" class="textarea form-textarea w-full h-[300px]" placeholder="How can I help you?" bind:value={textSubmission}></textarea>
                  </div>
              </div>
              <div class="field">
                  <div class="control">
                    <button type="submit"class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                      Send Request
                    </button>
                  </div>
              </div>
          </form>
        </section>

      {#if answer != ""}
          <div class="box">
              <h2 class="mb-4"><b>Answer:</b></h2>

              <div style="white-space: pre-wrap;">{answer}</div>
          </div>
      {/if}
      {#if docs != ""}
          <div class="box mt-4">
              <h2 class="mb-4"><b>Sources:</b></h2>

              <div>
                <ul>
                  {#each docs as doc}
                    {#if !sources.push(doc.metadata.source)}
                      {@debug sources}
                    {/if}
                  {/each} 
                  {#each sources.filter((value, index) => sources.indexOf(value) === index) as source}
                    <li><a target="_blank" rel="noreferrer" href="https://github.com/BryanSchuetz/d-ai-sources/blob/master/{source}">{source.replace('.md', '')}</a></li>
                  {/each}
                </ul>
              </div>
          </div>
      {/if}
  {:else}

      <div class="spinner max-w-md m-auto items-center">
        <svg class="m-auto" width="100" height="100" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><style>.spinner_HIK5{transform-origin:center;animation:spinner_XVY9 1s cubic-bezier(0.36,.6,.31,1) infinite}@keyframes spinner_XVY9{50%{transform:rotate(180deg)}100%{transform:rotate(360deg)}}</style><circle cx="12" cy="12" r="3"/><g class="spinner_HIK5"><circle cx="4" cy="12" r="3"/><circle cx="20" cy="12" r="3"/></g></svg>
        <h2 class="text-center">One moment, your prompt is being used to query <a target="_blank" rel="noreferrer" class="text-blue-500 hover:text-blue-700" href="https://www.pinecone.io/learn/vector-embeddings/">a vector database</a> of DAI primary sources. A collection of near vectors will be returned for use by the OpenAI model when generating your text.</h2>
      </div>
  {/if}
</section>


<style>

</style>