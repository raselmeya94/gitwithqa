# # llm_core/openai.py

# import openai
# from langchain.llms import OpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# def call_openai(api_key: str, context: str, question: str) -> str:
#     openai.api_key = api_key  # Set OpenAI API key

#     # Define prompt template for OpenAI
#     prompt_template = PromptTemplate(
#         input_variables=["context", "question"],
#         template="Given the context: {context}, answer the following question: {question}"
#     )
    
#     # Create the OpenAI LLM chain
#     openai_llm = OpenAI(model="gpt-4")  # You can adjust the model here
#     openai_chain = LLMChain(llm=openai_llm, prompt=prompt_template)
    
#     # Run the OpenAI chain with the context and question
#     return openai_chain.run(context=context, question=question)
