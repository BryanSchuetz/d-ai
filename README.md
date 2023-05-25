## D-AI

An AI writing assistant for DAI. Uses LangChainJS to connect a vector database of DAI primary sources to an OpenAI GPT-3 model. 

### Basically:

* Users ask a question.
* We send that query to a vector database of DAI primary sources and return a collection of near vectors.
* We hand the question and the near vectors to GPT-3 and ask it to generate an answer, given the provided context.
* We show the user the answer along with links to the source documents used as context.

![Screenshot](https://dai-assets.s3.amazonaws.com/trash/Screen%20Shot%202023-05-25%20at%202.03.56%20PM.png "Screenshot of the application in action")

### Improvements:

* Persist memory of previous questions and answers—alowing for more nuanced discovery
* Allow for an increae in returned vectors to better answer comprehensive quesitons like "How many projects do we have in Nigeria"
  * Alternatively, we can  
