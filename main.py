import os
import autogen
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Initialize Environment & App
load_dotenv()
app = FastAPI(title="Oxalis AI")

# Request Model
class TaskRequest(BaseModel):
    project_topic: str
    timeframe: str
    additional_context: str = "" # Optional field

llm_config = {
    "config_list": [{
        "model": "gpt-4o-mini",
        "api_key": os.environ.get("GITHUB_TOKEN"),
        "base_url": "https://models.inference.ai.azure.com", # GitHub's inference routing URL
    }],
    "temperature": 0.2,
    "cache_seed": None,
}


# Azure OpenAI Configuration
'''llm_config = {
    "config_list": [{
        "model": os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-4o"),
        "api_key": os.environ.get("AZURE_OPENAI_API_KEY"),
        "base_url": os.environ.get("AZURE_OPENAI_ENDPOINT"),
        "api_type": "azure",
        "api_version": "2024-02-15-preview"
    }],
    "temperature": 0.2,
}
'''

@app.post("/plan")
async def execute_swarm(request: TaskRequest):
    try:
        # 2. Dynamically construct the master prompt
        dynamic_prompt = f"""
        Create a complete {request.timeframe} plan for a project on: {request.project_topic}.
        Additional context from the user: {request.additional_context}.
        
        Planner: Break this down into milestones.
        Retriever: Find concepts or methodologies for these milestones.
        Executor: Compile this into a final Markdown schedule.
        """
        # 1. Define Agents inside the execution block for thread safety
        user_proxy = autogen.UserProxyAgent(
            name="Admin",
            system_message="A human admin.",
            code_execution_config=False,
            human_input_mode="NEVER"
        )

        # Agents
        planner = autogen.AssistantAgent(
        name="Planner",
        llm_config=llm_config,
        system_message="""You are the Strategic Architect of Oxalis AI. 
        Your role is to analyze ANY goal provided by the user and break it into a logical, phased execution plan.
        1. Identify the core domain (Engineering, Medical, Business, Creative, etc.).
        2. Create a high-level roadmap with specific milestones.
        3. Delegate research requirements to the Retriever. 
        Be domain-agnostic and structured."""
        )

        retriever = autogen.AssistantAgent(
        name="Retriever",
        llm_config=llm_config,
        system_message="""You are the Knowledge Expert of Oxalis AI. 
        Based on the Planner's roadmap, identify the essential resources, technical stacks, 
        or theoretical frameworks required for success. 
        If it's medical, find diagnostic methodologies. If it's software, find libraries/APIs. 
        If it's business, find market strategies. Pass verified intelligence to the Executor."""
        )

        executor = autogen.AssistantAgent(
        name="Executor",
        llm_config=llm_config,
        system_message="""You are the Implementation Lead of Oxalis AI. 
        Synthesize the strategy from the Planner and the intelligence from the Retriever. 
        Produce a professional, production-ready 'Project Blueprint' .
        Use H2 headers for main phases, bold text for deadlines,bullet points for resource lists and tables wherever necessary.
        Include a summary, timeline, and resource list. 
        End your message with 'TERMINATE' when the blueprint is complete."""
        )

        # 2. Orchestrate the Group Chat
        groupchat = autogen.GroupChat(
            agents=[user_proxy, planner, retriever, executor], 
            messages=[], 
            max_round=10
        )

        manager = autogen.GroupChatManager(
            groupchat=groupchat, 
            llm_config=llm_config,
            is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", "")
        )

        # 3. Trigger the Swarm
        user_proxy.initiate_chat(manager, message=dynamic_prompt)

        # 4. Extract and return the final message from the Executor
        final_message = groupchat.messages[-1]["content"].replace("TERMINATE", "").strip()
        
        return {"status": "success", "data": final_message}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/")
def health_check():
    return {"status": "Oxalis AI Swarm is active and ready."}