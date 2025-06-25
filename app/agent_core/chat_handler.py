from flask import current_app
from .agent_setup import get_agent
import logging # Ensure logging is imported, though current_app.logger is used

def handle_message(message: str, user_id: str, session_id: str) -> str:
    """Procesa el mensaje con el agente usando IDs de usuario/sesión y devuelve la respuesta en formato Markdown."""
    current_app.logger.info(f"handle_message llamado para user_id: {user_id}, session_id: {session_id}")
    current_app.logger.debug(f"Mensaje a procesar: {message}")
    agent = get_agent() # Obtiene la instancia configurada del agente
    current_app.logger.debug("Instancia del agente obtenida.")
    try:
        current_app.logger.debug(f"Llamando a agent.start con mensaje: {message}")
        result = agent.start(message)
        current_app.logger.debug(f"Resultado de agent.start (tipo: {type(result)}): {str(result)[:200]}...")
        return result
    except Exception as e:
        current_app.logger.error(f"Error en handle_message para session_id {session_id}: {e}", exc_info=True)
        return f"Lo siento, ocurrió un error al procesar tu mensaje: {str(e)}" 