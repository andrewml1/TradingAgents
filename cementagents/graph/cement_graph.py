import os
from datetime import date
from typing import Dict, Any, Optional

from cementagents.default_config import DEFAULT_CONFIG, PROVIDER_DEFAULTS
from cementagents.agents.utils.agent_states import ZonaState
from cementagents.agents.utils.memory import ZonaMemory
from cementagents.agents.analysts.data_analyst import create_data_analyst
from cementagents.agents.researchers.bull_researcher import create_bull_researcher
from cementagents.agents.researchers.bear_researcher import create_bear_researcher
from cementagents.agents.debate.debate_moderator import create_debate_moderator
from cementagents.agents.strategist.strategist import create_strategist
from cementagents.agents.risk_mgmt.risk_analyst import create_risk_analyst
from cementagents.agents.managers.manager import create_manager
from cementagents.graph.conditional_logic import CementConditionalLogic
from cementagents.graph.setup import CementGraphSetup
from cementagents.graph.propagation import CementPropagator
from cementagents.dataflows.mock_data import get_zona_data


class CementAgentsGraph:
    """Main orchestrator for the CementAgents multi-agent system.

    Manages the full analysis pipeline for Colombia's cement market zones,
    including debate, strategy, risk analysis, and final decision-making.
    """

    @staticmethod
    def _create_llm(provider: str, model: str):
        """Instantiate the correct LangChain chat model for the given provider."""
        if provider == "openai":
            from langchain_openai import ChatOpenAI
            return ChatOpenAI(model=model, max_tokens=4096)
        elif provider == "anthropic":
            from langchain_anthropic import ChatAnthropic
            return ChatAnthropic(model=model, max_tokens=4096)
        else:
            raise ValueError(
                f"Proveedor '{provider}' no soportado. Usa 'anthropic' o 'openai'."
            )

    def __init__(self, config: Dict[str, Any] = None):
        """Initialize the CementAgents graph and all sub-components.

        Args:
            config: Configuration dictionary. Falls back to DEFAULT_CONFIG if None.
        """
        self.config = config or DEFAULT_CONFIG.copy()

        # Initialize LLM clients
        provider = self.config.get("llm_provider", "anthropic")
        provider_defaults = PROVIDER_DEFAULTS.get(provider, PROVIDER_DEFAULTS["anthropic"])
        deep_model = self.config.get("deep_think_llm") or provider_defaults["deep_think_llm"]
        quick_model = self.config.get("quick_think_llm") or provider_defaults["quick_think_llm"]

        self.deep_llm = self._create_llm(provider, deep_model)
        self.quick_llm = self._create_llm(provider, quick_model)

        # Initialize shared memories
        self.bull_memory = ZonaMemory(self.quick_llm)
        self.bear_memory = ZonaMemory(self.quick_llm)
        self.strategist_memory = ZonaMemory(self.quick_llm)
        self.manager_memory = ZonaMemory(self.deep_llm)

        # Determine dataflow function
        if self.config.get("use_mock_data", True):
            self.dataflow_fn = get_zona_data
        else:
            # Placeholder for real data integration
            # Users can replace this with a real API call function
            self.dataflow_fn = get_zona_data

        # Build agent nodes
        analyst_node = create_data_analyst(self.quick_llm, self.dataflow_fn)
        bull_node = create_bull_researcher(self.quick_llm, self.bull_memory)
        bear_node = create_bear_researcher(self.quick_llm, self.bear_memory)
        moderator_node = create_debate_moderator(self.deep_llm)
        strategist_node = create_strategist(self.deep_llm, self.strategist_memory)
        risk_node = create_risk_analyst(self.deep_llm)
        manager_node = create_manager(self.deep_llm, self.manager_memory)

        # Build conditional routing logic
        self.conditional_logic = CementConditionalLogic(
            max_debate_rounds=self.config.get("max_debate_rounds", 2),
            max_risk_rounds=self.config.get("max_risk_discuss_rounds", 1),
        )

        # Build graph
        self.graph_setup = CementGraphSetup(
            analyst_node=analyst_node,
            bull_node=bull_node,
            bear_node=bear_node,
            moderator_node=moderator_node,
            strategist_node=strategist_node,
            risk_node=risk_node,
            manager_node=manager_node,
            conditional_logic=self.conditional_logic,
        )
        self.graph = self.graph_setup.setup_graph()
        self.propagator = CementPropagator()

    def _build_initial_state(
        self, zona: str, perfil_riesgo: str, fecha: str
    ) -> ZonaState:
        """Build the initial ZonaState for a graph run.

        Args:
            zona: Zone name.
            perfil_riesgo: Risk profile (Agresivo|Neutral|Conservador).
            fecha: Analysis date string.

        Returns:
            Initialized ZonaState dictionary.
        """
        return ZonaState(
            zona=zona,
            fecha_analisis=fecha,
            datos_consolidados="",
            argumentos_bullish=[],
            argumentos_bearish=[],
            historial_debate=[],
            veredicto="NEUTRAL",
            confianza=0.5,
            rondas_debate=0,
            propuesta_estratega="",
            historial_riesgo=[],
            propuesta_ajustada="",
            scorecard_riesgo="",
            rondas_riesgo=0,
            decision_final="",
            acciones_autorizadas="",
            justificacion="",
            perfil_riesgo_zona=perfil_riesgo,
        )

    def analyze_zona(
        self,
        zona: str,
        perfil_riesgo: Optional[str] = None,
        fecha: Optional[str] = None,
    ) -> dict:
        """Run the full analysis pipeline for a single zona.

        Args:
            zona: Zone name to analyze.
            perfil_riesgo: Risk profile override. Falls back to config value.
            fecha: Analysis date string. Defaults to today.

        Returns:
            Dictionary with all output fields including decision_final,
            veredicto, confianza, propuesta_ajustada, scorecard_riesgo,
            acciones_autorizadas, and justificacion.
        """
        if perfil_riesgo is None:
            perfil_riesgo = self.config.get("risk_profile", "Neutral")

        if fecha is None:
            fecha = str(date.today())

        init_state = self._build_initial_state(zona, perfil_riesgo, fecha)

        graph_config = {
            "recursion_limit": 50,
        }

        final_state = self.graph.invoke(
            init_state,
            config=graph_config,
        )

        return self.propagator.extract_results(final_state)

    def analyze_all_zonas(
        self,
        perfil_riesgo: Optional[str] = None,
        fecha: Optional[str] = None,
    ) -> Dict[str, dict]:
        """Run analysis for all configured zonas.

        Args:
            perfil_riesgo: Risk profile override. Falls back to config value.
            fecha: Analysis date string. Defaults to today.

        Returns:
            Dictionary mapping zona name -> analysis results dict.
        """
        if perfil_riesgo is None:
            perfil_riesgo = self.config.get("risk_profile", "Neutral")

        if fecha is None:
            fecha = str(date.today())

        results = {}
        for zona in self.config.get("zonas", []):
            results[zona] = self.analyze_zona(
                zona, perfil_riesgo=perfil_riesgo, fecha=fecha
            )
        return results
