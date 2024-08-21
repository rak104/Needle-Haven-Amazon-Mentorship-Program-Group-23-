import os
import openai
from langchain.chat_models import ChatOpenAI   
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain   
from langchain.chains import SequentialChain
from langchain.agents import load_tools, initialize_agent
from langchain.agents import AgentType   
from langchain.chains import RetrievalQA
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.llms import OpenAI   
from langchain.indexes import VectorstoreIndexCreator
from langchain.chains.router import MultiPromptChain
from langchain.chains.router.llm_router import LLMRouterChain, RouterOutputParser
from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SimpleSequentialChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch
from langchain.indexes import VectorstoreIndexCreator
from langchain.document_loaders import CSVLoader
from langchain.llms import OpenAI

llm_model="gpt-3.5-turbo"
openai_api_key = "sk-None-XS76dEz4IURDhsv2AJb9T3BlbkFJYoWnTsDhATqUPkspJY6n"
input_file = r"stores.csv"

class GPT:
    def __init__(self):
        self.openai_api_key = openai_api_key
        self.llm_model = llm_model

        # Initialize the LLM model
        self.llm = ChatOpenAI(openai_api_key=self.openai_api_key, temperature=0.9, model=self.llm_model)

        # Initialize the CSV loader if input_file is provided
        
        
        self.loader = CSVLoader(file_path=input_file)
        self.embedding_model = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        self.index = VectorstoreIndexCreator(
            vectorstore_cls=DocArrayInMemorySearch,
            embedding=self.embedding_model
        ).from_loaders([self.loader])

        self.llm_replacement_model = OpenAI(temperature=0, model='gpt-3.5-turbo-instruct', openai_api_key=self.openai_api_key)

        # Templates
        product_template = """You are a very good fashion products expert. \
        You are great at answering questions about fashion products\
        you provide a list of well-known and emerging brands that excel in this category? 
        Please include information about their style, target audience, 
        and any unique features or values that set them apart \
        also you should elaborate as requested in the question below\
        When you don't know the answer to a question you admit\
        that you don't know.

        Here is the question:
        {input}"""

        brand_template = """You are a very good fashion brands expert. \
        You are great at answering brand related questions. \
        if the brand if fashion or clothing brand ,Tell me more about the brand mentioned in the question below\
        What are their popular products, target audience,
        and unique features? \
        also elaborate any requested ideas in the question below\
        if it is not a fashion brand state that you are a fashion expert and that this is not a fashion brand.

        Here is the question:
        {input}"""

        situation_template = """You are a very good fashion expert. \
        You have an excellent knowledge of what to wear on events,\
        please recommend an outfit for the situation or event mentioned in the question below,  \
        Include details about the type of clothing, colors, accessories,\
        and any additional styling tips to ensure the outfit is stylish and appropriate for the occasion.

        Here is a question:
        {input}"""

        # Create prompt infos
        self.prompt_infos = [
            {
                "name": "product",
                "description": "Good for answering any questions related to a specific clothing and fashion products",
                "prompt_template": product_template
            },
            {
                "name": "brand",
                "description": "Good for answering questions about fashion brands",
                "prompt_template": brand_template
            },
            {
                "name": "situation",
                "description": "Good for answering questions related to situations, like what to wear when going to specific event or occasion",
                "prompt_template": situation_template
            }
        ]



        # Load tools
        self.tools = load_tools(["wikipedia"], llm=self.llm)
        self.agent = initialize_agent(
            self.tools,
            self.llm,
            agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
            handle_parsing_errors=True,
            max_tokens=150
        )

    
        self.destination_chains = {}
        for p_info in self.prompt_infos:
            name = p_info["name"]
            prompt_template = p_info["prompt_template"]
            prompt = ChatPromptTemplate.from_template(template=prompt_template)
            chain = LLMChain(llm=self.llm, prompt=prompt)
            self.destination_chains[name] = chain

        self.destinations = [f"{p['name']}: {p['description']}" for p in self.prompt_infos]
        self.destinations_str = "\n".join(self.destinations)

        self.default_prompt = ChatPromptTemplate.from_template("{input}")
        self.default_chain = LLMChain(llm=self.llm, prompt=self.default_prompt)

        MULTI_PROMPT_ROUTER_TEMPLATE = """Given a raw text input to a \
        language model select the model prompt best suited for the input. \
        You will be given the names of the available prompts and a \
        description of what the prompt is best suited for. \
        You may also revise the original input if you think that revising\
        it will ultimately lead to a better response from the language model.

        << FORMATTING >>
        Return a markdown code snippet with a JSON object formatted to look like:
        ```json
        {{{{
            "destination": string \ name of the prompt to use or "DEFAULT"
            "next_inputs": string \ a potentially modified version of the original input
        }}}}
        ```

        REMEMBER: "destination" MUST be one of the candidate prompt \
        names specified below OR it can be "DEFAULT" if the input is not\
        well suited for any of the candidate prompts.
        REMEMBER: "next_inputs" can just be the original input \
        if you don't think any modifications are needed.

        << CANDIDATE PROMPTS >>
        {destinations}

        << INPUT >>
        {{input}}

        << OUTPUT (remember to include the ```json)>>"""

        self.router_template = MULTI_PROMPT_ROUTER_TEMPLATE.format(
            destinations=self.destinations_str
        )
        self.router_prompt = PromptTemplate(
            template=self.router_template,
            input_variables=["input"],
            output_parser=RouterOutputParser(),
        )

        self.router_chain = LLMRouterChain.from_llm(self.llm, self.router_prompt)

        self.chain = MultiPromptChain(
            router_chain=self.router_chain,
            destination_chains=self.destination_chains,
            default_chain=self.default_chain,
            verbose=True
        )



    def general_search(self, req):
        return self.chain.run(req)

    def wiki_search(self, request):
        return self.agent.invoke(request)["output"]

    def stores_search(self, req):
        prompt = ChatPromptTemplate.from_template(
            "What is the item mentioned in the input, give the item's name with description same as mentioned in the input, don't add information other than in input, the input is  {input}"
        )

        chain = LLMChain(llm=self.llm, prompt=prompt)

        item = chain.run(req)
        req = "Please list all your "+item+" as bullet points, and summarize each one and mention from which store is it."
        return(self.index.query(req, llm=self.llm_replacement_model))
