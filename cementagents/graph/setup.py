from langgraph.graph import StateGraph, END, START
from cementagents.agents.utils.agent_states import ZonaState
from cementagents.graph.conditional_logic import CementConditionalLogic


class CementGraphSetup:
    """Builds and compiles the LangGraph StateGraph for CementAgents."""

    def __init__(
        self,
        analyst_node,
        bull_node,
        bear_node,
        moderator_node,
        strategist_node,
        risk_node,
        manager_node,
        conditional_logic: CementConditionalLogic,
    ):
        """Store all agent node functions and routing logic.

        Args:
            analyst_node: Data analyst node function.
            bull_node: Bullish researcher node function.
            bear_node: Bearish researcher node function.
            moderator_node: Debate moderator node function.
            strategist_node: Strategist (commercial strategy) node function.
            risk_node: Risk analyst node function.
            manager_node: Manager (final decision) node function.
            conditional_logic: CementConditionalLogic instance for routing.
        """
        self.analyst_node = analyst_node
        self.bull_node = bull_node
        self.bear_node = bear_node
        self.moderator_node = moderator_node
        self.strategist_node = strategist_node
        self.risk_node = risk_node
        self.manager_node = manager_node
        self.conditional_logic = conditional_logic

    def setup_graph(self):
        """Build and compile the StateGraph.

        Node flow:
            START -> analyst
            analyst -> bull_researcher (parallel start)
            analyst -> bear_researcher (parallel start)
            bull_researcher -> debate_moderator
            bear_researcher -> debate_moderator
            debate_moderator -> [continue_debate -> bull_researcher | go_to_strategist -> strategist]
            strategist -> risk_analyst
            risk_analyst -> [continue_risk -> risk_analyst | go_to_manager -> manager]
            manager -> END

        Returns:
            Compiled LangGraph application.
        """
        workflow = StateGraph(ZonaState)

        # Register all nodes
        workflow.add_node("analyst", self.analyst_node)
        workflow.add_node("bull_researcher", self.bull_node)
        workflow.add_node("bear_researcher", self.bear_node)
        workflow.add_node("debate_moderator", self.moderator_node)
        workflow.add_node("strategist", self.strategist_node)
        workflow.add_node("risk_analyst", self.risk_node)
        workflow.add_node("manager", self.manager_node)

        # Entry point
        workflow.add_edge(START, "analyst")

        # Analyst fans out to both researchers in parallel
        workflow.add_edge("analyst", "bull_researcher")
        workflow.add_edge("analyst", "bear_researcher")

        # Both researchers converge at the moderator
        workflow.add_edge("bull_researcher", "debate_moderator")
        workflow.add_edge("bear_researcher", "debate_moderator")

        # Moderator routes: more debate rounds or move to strategist
        workflow.add_conditional_edges(
            "debate_moderator",
            self.conditional_logic.should_continue_debate,
            {
                "continue_debate": "bull_researcher",
                "go_to_strategist": "strategist",
            },
        )

        # Strategist feeds into risk analyst
        workflow.add_edge("strategist", "risk_analyst")

        # Risk analyst routes: more risk rounds or move to manager
        workflow.add_conditional_edges(
            "risk_analyst",
            self.conditional_logic.should_continue_risk,
            {
                "continue_risk": "risk_analyst",
                "go_to_manager": "manager",
            },
        )

        # Manager is the terminal node
        workflow.add_edge("manager", END)

        return workflow.compile()
