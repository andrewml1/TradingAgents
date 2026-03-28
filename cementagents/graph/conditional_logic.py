class CementConditionalLogic:
    """Handles routing decisions for the CementAgents graph."""

    def __init__(self, max_debate_rounds: int = 2, max_risk_rounds: int = 1):
        """Initialize with configurable round limits.

        Args:
            max_debate_rounds: Maximum number of bull/bear debate rounds before
                               moving to the strategist.
            max_risk_rounds: Maximum number of risk analysis rounds before
                             moving to the manager.
        """
        self.max_debate_rounds = max_debate_rounds
        self.max_risk_rounds = max_risk_rounds

    def should_continue_debate(self, state) -> str:
        """Route: continue debate or move to strategist.

        Returns:
            "continue_debate" if more rounds are needed,
            "go_to_strategist" if max rounds reached.
        """
        rondas = state.get("rondas_debate", 0)
        if rondas >= self.max_debate_rounds:
            return "go_to_strategist"
        return "continue_debate"

    def should_continue_risk(self, state) -> str:
        """Route: continue risk analysis or move to manager.

        Returns:
            "continue_risk" if more rounds are needed,
            "go_to_manager" if max rounds reached.
        """
        rondas = state.get("rondas_riesgo", 0)
        if rondas >= self.max_risk_rounds:
            return "go_to_manager"
        return "continue_risk"
