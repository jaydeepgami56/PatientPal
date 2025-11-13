# AGENTS.md

This file provides non-obvious coding rules discovered by reading the repository.

- Agents must subclass [`utils/agent_base.py`](utils/agent_base.py:55) BaseHealthcareAgent and implement initialize(), validate_input(), process(); initialize() MUST set agent._is_initialized=True and return True or orchestrator will raise (see [`utils/orchestrator.py`](utils/orchestrator.py:256)).
- LLM interface inconsistency: `LeadAgentOrchestrator` calls llm.invoke(prompt) and expects an object with .content, while `PromptExecutor` uses llm_client.generate(... ) and expects a string. Provide an adapter implementing both interfaces or use the langchain wrapper used in tests (see [`utils/orchestrator.py`](utils/orchestrator.py:166) and [`utils/prompt_executor.py`](utils/prompt_executor.py:81).
- Prompt templates in [`utils/prompts.py`](utils/prompts.py:40) are authoritative; do NOT change headings/case/field names — regex parsers in [`utils/orchestrator.py`](utils/orchestrator.py:190) and validators depend on verbatim strings.
- Agent registration names are significant. Ensure keys in the agents dict match the exact names used by prompts/parsers (e.g., check [`agents/`](agents/:1) modules); mismatches like "Path Foundation" vs "Pathology" break routing.
- Tests are standalone scripts (not pytest). See [`test_lead_agent.py`](test_lead_agent.py:7). They require OPENAI_API_KEY in `.env` (fatal) and may warn on missing HUGGINGFACE_API_KEY.
- External interfaces use Pydantic models (RoutingDecision, AgentResponse). Avoid changing field names/structure — memory/logging/serialisation rely on .dict() shapes.
- When updating prompts, update confidence mapping and regex parsing together (see confidence_map in [`utils/orchestrator.py`](utils/orchestrator.py:214)).
- Image-only agents (Derm/CXR) MUST only be selected when image context is present — prompts and routing enforce this (see [`utils/prompts.py`](utils/prompts.py:722)).