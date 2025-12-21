
from agents.research_agent import create_research_agent
from agents.summarization_agent import create_summarization_agent
from shared_memory import create_shared_memory

shared_memory = create_shared_memory()

def run_pipeline(user_query):
    research_agent = create_research_agent()
    summarization_agent = create_summarization_agent()

    # Step 1: Research
    research_output = research_agent.run(topic=user_query)

    # Save to shared memory
    shared_memory.save_context(
        {"input": user_query},
        {"output": research_output}
    )

    # Step 2: Summarize
    summary_output = summarization_agent.run(
        research=research_output
    )

    return research_output, summary_output
