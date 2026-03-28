from langchain_core.callbacks.base import BaseCallbackHandler

# Importación diferida para evitar importación circular
_dashboard_buffer = None


def _get_buffer():
    global _dashboard_buffer
    if _dashboard_buffer is None:
        from cementagents.ui.dashboard import message_buffer
        _dashboard_buffer = message_buffer
    return _dashboard_buffer


def set_active_node(node_name: str):
    """Llamar al inicio de cada nodo para actualizar el estado en el dashboard."""
    _get_buffer().set_agent_active(node_name)


class StreamingTraceCallback(BaseCallbackHandler):
    """Alimenta el dashboard con tokens en tiempo real y eventos LLM."""

    def on_llm_start(self, serialized, prompts, **kwargs):
        pass  # El header ya lo muestra set_active_node

    def on_llm_new_token(self, token: str, **kwargs):
        _get_buffer().add_token(token)

    def on_llm_end(self, response, **kwargs):
        _get_buffer().flush_tokens()

    def on_llm_error(self, error, **kwargs):
        _get_buffer().add_message("Error", str(error)[:200])
