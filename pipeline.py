from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain
from langchain_core.messages import HumanMessage

def run_research_pipeline(topic : str) -> dict:
 
    state = {}

    # Step 1: Search Agent
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50+"\n")

    search_agent = build_search_agent()
    search_result = search_agent.invoke(
        {"messages": [HumanMessage(content=f"Find recent, reliable and detailed information about: {topic}")]},
        config={"recursion_limit": 25}
    )
    state['search_result'] = search_result['messages'][-1].content

    print("\n search result ", state['search_result'])

    # Step 2: Reader Agent
    print("\n"+" ="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke(
        {
            "messages": [('user',
                          f"Based on the following search results about '{topic}', "
                          f"pick the most relevant URL and scrape it for deeper content.\n\n"
                          f"Search Results:\n{state['search_result'][:800]}"
            )]
        },
        config={"recursion_limit": 25}
    )

    state['scrape_content'] = reader_result['messages'][-1].content

    print("\nscraped content: \n", state['scrape_content'])

    # Step 3: Writer Chain
    print("\n"+" ="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n{state['search_result']}\n\n"
        f"DETAILED SCRAPED CONTENT : \n{state['scrape_content']}"
    )

    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n Final Report: \n", state['report'])

    # Step 4: Critic Chain
    print("\n"+" ="*50)
    print("step 4 - Critic is reviewing the report ...")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report": state['report']
    })

    print("\n Critic report: \n", state['feedback'])

    return state


if __name__ == "__main__":
    topic = input("\nEnter a research topic: ")
    run_research_pipeline(topic)