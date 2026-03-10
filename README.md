# Oxalis-Ai
** Multi-Agent Strategy Swarm**

Oxalis AI is a distributed, multi-agent AI system designed to eliminate "Architectural Paralysis." It acts as a virtual Chief Technical Architect, orchestrating a swarm of specialized AI agents to convert high-level user goals into structured, production ready execution blueprints.

Optimized for lightweight local execution, it leverages cloud native APIs to bypass local hardware limitations while delivering enterprise grade reasoning.

##  Architecture & Tech Stack

* **Frontend:** Streamlit (Reactive UI & Markdown rendering)
* **Backend:** FastAPI (Asynchronous agent orchestration)
* **Agentic Framework:** Microsoft AutoGen (AG2)
* **Inference Engine:** GitHub Models API (`gpt-4o-mini`)

The system utilizes three collaborating agents:
1.  **Planner:** Maps chronological milestones.
2.  **Retriever:** Identifies domain-specific tech stacks and resources.
3.  **Executor:** Synthesizes the dialogue into a standardized Markdown roadmap.

##  Prerequisites

* Python 3.10+
* A GitHub account with a Personal Access Token (PAT)
