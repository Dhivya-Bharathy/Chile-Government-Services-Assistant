from flask import current_app
from praisonaiagents import Agent
from .agent_config import (
    FirecrawlTool,
    FIRECRAWL_INSTRUCTION,
    FIRECRAWL_TEMPLATE,
    AGENT_INSTRUCTIONS
)

_agent = None

def get_agent():
    """Inicializa y/o devuelve la instancia del Agente PraisonAI configurado."""
    global _agent
    current_app.logger.debug("get_agent llamado.")
    if _agent is None:
        current_app.logger.info("Inicializando nueva instancia del Agente PraisonAI.")
        firecrawl_api_key = current_app.config.get('FIRECRAWL_API_KEY')
        if not firecrawl_api_key:
            current_app.logger.warning("FIRECRAWL_API_KEY no configurada en .env. La herramienta Firecrawl no funcionará.")
        else:
            current_app.logger.debug("FIRECRAWL_API_KEY encontrada.")
        # Inicializar la herramienta Firecrawl
        current_app.logger.info("Inicializando FirecrawlTool.")
        firecrawl_tool = FirecrawlTool(
            api_key=firecrawl_api_key,
            instruction=FIRECRAWL_INSTRUCTION,
            template=FIRECRAWL_TEMPLATE
        )
        tools_list = [firecrawl_tool.search]
        current_app.logger.debug(f"Herramientas configuradas para el agente: {[tool.__name__ for tool in tools_list]}")
        # Crear el Agente PraisonAI
        _agent = Agent(
            instructions=AGENT_INSTRUCTIONS,
            tools=tools_list
        )
        current_app.logger.info("Agente PraisonAI inicializado exitosamente.")
    else:
        current_app.logger.debug("Usando instancia de Agente PraisonAI existente.")
    return _agent 