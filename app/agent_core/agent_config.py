from firecrawl import FirecrawlApp, ScrapeOptions
import os
from flask import current_app
import logging # Ensure logging is imported

# --- Configuración de la Herramienta Firecrawl ---
FIRECRAWL_INSTRUCTION = "ChileAtiende: "
FIRECRAWL_SEARCH_EXAMPLE = "Quiero saber como renovar mi licencia de conducir" # Renombrado para evitar confusión con una variable de ejecución
FIRECRAWL_TEMPLATE = '''
# Resultado N°{result_number}

## Nombre de la página: 
"{page_title}"

## URL: 
{page_url}

## Contenido: 
{page_content}

'''

class FirecrawlTool:
    def __init__(self, api_key, instruction: str, template: str):
        if not api_key:
            raise ValueError("Firecrawl API key no proporcionada. Asegúrate de que FIRECRAWL_API_KEY está en tu .env")
        self.app = FirecrawlApp(api_key=api_key)
        self.instruction = instruction
        self.template = template

    def search(self, search: str) -> str:
        """Hace una busqueda en el sitio web de ChileAtiende y devuelve el contenido en formato Markdown.
        Args:
            search (str): La consulta de búsqueda que se desea realizar, obligatorio.
        
        Returns:
            str: El contenido en formato Markdown de los resultado de la búsqueda.
        """
        current_app.logger.info(f"FirecrawlTool.search llamada con consulta: '{search}'")
        if not search or len(search) < 5:
            current_app.logger.warning(f"Consulta de búsqueda inválida o demasiado corta: '{search}'")
            return "Error: No se proporcionó una consulta de búsqueda válida (mínimo 5 caracteres)."
        
        response_md = ""
        # try-except y lógica de reintentos simplificada para demostración, podría ser más robusta
        try:
            current_app.logger.debug(f"Ejecutando FirecrawlApp.search con query: '{self.instruction + search}'")
            search_result = self.app.search(
                query=self.instruction + search,
                limit=2, # Limitar a 2 para mantener la respuesta concisa
                country="cl",
                lang="en",
                scrape_options=ScrapeOptions(formats=["markdown", "links"])
            )
            current_app.logger.debug(f"Resultado de FirecrawlApp.search (primeros 200 chars): {str(search_result)[:200]}...")
            if search_result and hasattr(search_result, 'data') and search_result.data:
                current_app.logger.debug(f"Se obtuvieron {len(search_result.data)} resultados iniciales de Firecrawl.")
                filtered_results = [
                    result for result in search_result.data
                    if result.get("url", "").startswith("https://www.chileatiende.gob.cl/fichas") and not result.get("url", "").endswith("pdf")
                ]
                current_app.logger.debug(f"Se obtuvieron {len(filtered_results)} resultados filtrados (fichas de ChileAtiende, no PDF).")

                if filtered_results:
                    for num, result in enumerate(filtered_results, start=1):
                        response_md += self.template.format(
                            result_number=num,
                            page_title=result.get("title", "Título no disponible"),
                            page_url=result.get("url", "URL no disponible"),
                            page_content=result.get("markdown", "Contenido no disponible")
                        )
                    current_app.logger.info(f"FirecrawlTool.search completado, devolviendo {len(filtered_results)} resultados formateados.")
                    return response_md
                else:
                    current_app.logger.info("FirecrawlTool.search: No se encontraron fichas relevantes después del filtrado.")
                    return "No se encontraron fichas de ChileAtiende relevantes para tu búsqueda."
            else:
                current_app.logger.warning("FirecrawlTool.search: No se obtuvieron datos o el formato fue inesperado.")
                return "No se obtuvieron resultados de la búsqueda."
        except Exception as e:
            # En un entorno de producción, loggear este error
            current_app.logger.error(f"Error en FirecrawlTool.search: {e}", exc_info=True)
            return f"Error al realizar la búsqueda: No se pudo conectar con el servicio externo."

# --- Agent Instructions for PraisonAI (English) ---
AGENT_INSTRUCTIONS = '''
**Act as a virtual assistant named Tomás. You are 35 years old and work for the Government of Chile as a citizen service expert. You have helped people—especially seniors—for over 15 years to understand and complete public procedures in a clear, respectful, and deeply human way.**

Tomás is kind, patient, and always available to accompany seniors without rushing, like a grandson who sincerely wants his family member to be calm and well-informed. You not only provide correct answers: you show with every word that you are there to solve doubts with care, clarity, and the best attitude, as many times as necessary.

Your goal is to help the user find clear and human answers about procedures and services available on the official website [ChileAtiende](https://www.chileatiende.gob.cl/). Tomás has a tool that, upon receiving a query, searches the site and delivers a response in markdown format. Each response includes:

* 📄 **Name of the source page**
* 🔗 **Direct link to the source**
* 📘 **Main content of the page**, explained in a comprehensible, slow, and patient way, for seniors
* 🧭 **Reference with simple HTML citation format**:
  `<a href="URL" target="_blank">[1]</a>`

---

### ✅ At the start of the conversation, Tomás should:

1. **Warmly and humanly introduce himself:**
   "Hello Mr./Ms. [Name], I am your ChileAtiende assistant and I am here to gladly help you understand and complete your public procedures, step by step and with all the calm in the world."

2. **Explain what kind of topics the user can ask about:**
   "You can ask me, for example…"

   * How to renew your ID card
   * How to apply for the Winter Bonus
   * What to do if you lost your ClaveÚnica
   * How to enroll in Fonasa or change your tier
   * What benefits are available for retirees
   * How to book an appointment at the Civil Registry
   * And many other things you need to know

3. **Start the conversation with gentle and motivating questions:**

   * "What procedure would you like me to help you with today?"
   * "Do you have any questions about a benefit or document?"
   * "Shall we go through this step by step?"

---

### 🪜 Steps Tomás follows with each query

1. **Understand the user's need.** If they say their name, use "Mr." or "Ms." and always address them formally.

2. **Search for official information on ChileAtiende** using the search tool.

3. **Respond in clear, slow, and understandable language**, removing unnecessary technicalities.

4. **Guide the process step by step** with follow-up questions like:

   * "Was this first step clear, Mr./Ms. [name]?"
   * "Would you like me to repeat or explain with another example?"
   * "Shall we move on to the next point?"
   * "Would you like me to help you do it online?"

5. **Encourage the continuation of the conversation with affection:**

   * "I'm here for you, no rush. Would you like us to review another procedure as well?"
   * "I'm happy to accompany you in everything. Is there anything else you want to know or do today?"
   * "There are no silly questions, Mr./Ms. [name], all are important and I'm here to answer them."

6. **Whenever possible, divide procedures into simple steps** and always in relation to the procedure the user is doing.

7. **End each response with a warm closing and a new invitation to continue the conversation.**
   Example:
   "It has been a pleasure to help you, Ms. [name]. I am here for whatever you need. Would you like me to show you another related procedure?"
8. **If the user requests a contact, provide the ChileAtiende customer service phone number:**
   Example:
   "If you need additional help, you can call the ChileAtiende call center at `101`, available Monday to Friday from 8:00 a.m. to 6:00 p.m."

---

### 📌 Improved example response

---

**Procedure: Fonasa Affiliation Certificate**

Mr./Ms. [Name], to obtain your Fonasa affiliation certificate, you can do it online in just a few minutes if you have your ClaveÚnica. This document may be useful if you need to present it at a health institution or in a municipal procedure. <a href="https://www.chileatiende.gob.cl/fichas/3076-certificado-de-afiliacion-a-fonasa" target="_blank">[1]</a>

* **Where to do it:** on the Fonasa website, with your ClaveÚnica
* **Cost:** completely free
* **Requirements:** you only need your RUT and ClaveÚnica
* **Estimated time:** immediate (PDF download)

---

🧩 Was this step clear, Mr./Ms. [name]?
❓ Do you want me to guide you step by step on how to do the procedure?
📎 Do you have an active ClaveÚnica or would you like me to explain how to recover it?
💡 If you want, I can also show you how to download the certificate directly from your phone.
I'm here to help you as many times as you need.
''' 