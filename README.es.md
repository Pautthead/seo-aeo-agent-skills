# Skills de SEO + AEO + GEO para agentes de IA

Skills respaldadas por evidencia para Claude Code, Codex, Cursor, OpenCode, **Grok Build**, Gemini CLI, Cline, Hermes y ~75 hosts más. Cada regla de puntuación se remonta a una fuente fechada. **Sin claves de API, sin servidores MCP, sin suscripción.**

```bash
npx skills add Pautthead/seo-aeo-agent-skills
```

> **Fuentes verificadas por última vez el 2026-10-19.** Estas estadísticas caducan en semanas. Cada estadística de este README enlaza a su fuente primaria; la tabla de verificación está en [`docs/SOURCE-VERIFICATION.md`](docs/SOURCE-VERIFICATION.md).

[![Licencia: Apache-2.0](https://img.shields.io/badge/licencia-Apache--2.0-blue.svg)](LICENSE)
[![Instalación](https://img.shields.io/badge/instalar-npx%20skills-8a2be2.svg)](https://www.npmjs.com/package/skills)
[![Claves de API](https://img.shields.io/badge/claves%20de%20API-ninguna%20requerida-brightgreen.svg)](skills/)
[![Skills](https://img.shields.io/badge/skills-4-orange.svg)](skills/)
[![Release](https://img.shields.io/badge/release-v1.1.0-informational.svg)](https://github.com/Pautthead/seo-aeo-agent-skills/releases)

---

## Inicio rápido

```bash
npx skills add Pautthead/seo-aeo-agent-skills
```

Pídele al agente:

> Ejecuta `aeo-bot-access-audit` sobre https://fluyeporlaweb.com

Una ejecución real del 2026-10-20, acortada. Los cuatro informes completos están en [`examples/`](examples/).

```
# Bot Access Audit — fluyeporlaweb.com
Date: 2026-10-20 · Method: keyless (curl)

Verdict (esa ejecución): OPEN — 100/100
robots.txt 200, User-agent: * Allow: /. Edge: 16 user-agents × 5 páginas, todas 200,
los mismos bytes que el navegador. Sin cf-mitigated, sin challenge.

Repuntuado con la regla 11 (esta versión): 95/100, sigue OPEN.
ClaudeBot está permitido y Claude-SearchBot no tiene grupo: −5 una vez.
El 95 es la regla nueva aplicada a ese hecho. La ejecución del 2026-10-20 imprimió 100.
```

| Skill | Ejemplo |
|---|---|
| `seo-data-contract` | [examples/seo-data-contract-fluyeporlaweb.md](examples/seo-data-contract-fluyeporlaweb.md) |
| `aeo-bot-access-audit` | [examples/aeo-bot-access-audit-fluyeporlaweb.md](examples/aeo-bot-access-audit-fluyeporlaweb.md) |
| `aeo-citability-audit` | [examples/aeo-citability-audit-fluyeporlaweb.md](examples/aeo-citability-audit-fluyeporlaweb.md) |
| `information-gain-analysis` | [examples/information-gain-analysis-fluyeporlaweb.md](examples/information-gain-analysis-fluyeporlaweb.md) |

## Las cuatro skills

| Skill | La pregunta que responde | ¿Necesita claves? |
|---|---|---|
| [`seo-data-contract`](skills/seo-data-contract/SKILL.md) | ¿Son estos datos lo bastante frescos y fiables como para actuar sobre ellos? | No |
| [`aeo-bot-access-audit`](skills/aeo-bot-access-audit/SKILL.md) | ¿Pueden los bots de IA llegar realmente a este sitio? | No (solo `curl`) |
| [`aeo-citability-audit`](skills/aeo-citability-audit/SKILL.md) | ¿Sobreviviría esta página a ser extraída y citada? | No |
| [`information-gain-analysis`](skills/information-gain-analysis/SKILL.md) | ¿Qué sabe esta página que el SERP no sabe? | No |

Estas skills puntúan las mismas páginas para un segundo trabajo: que sean **extraídas, citadas y atribuidas** dentro de una respuesta sintetizada.

---

## Una ejecución real

`aeo-bot-access-audit` contra `ahrefs.com/blog/llmstxt-study/`, ejecutado el 2026-10-19. Reproducible con los comandos de la skill:

```
$ curl -sI -A "Mozilla/5.0 ...; compatible; OAI-SearchBot/1.4; +https://openai.com/searchbot" <url>
OAI-SearchBot/1.4    HTTP 200
Claude-SearchBot     HTTP 200
PerplexityBot        HTTP 200
GPTBot/1.4           HTTP 200

$ curl -s <origin>/robots.txt
User-agent: *
Disallow: /article
Disallow: /site-explorer/ajax/
...
```

**Hallazgo:** los cuatro bots de IA llegan al edge y reciben `200`. El `robots.txt` no menciona ningún bot de IA —el comodín los cubre—, así que no se bloquea nada. Pero **no hay ninguna directiva `Sitemap:`**, ni política alguna basada en tokens nombrados. El sitio es accesible para los bots de recuperación de IA y no ha tomado ninguna decisión deliberada al respecto.

Esa distinción es el objetivo de la skill. Un `robots.txt` limpio no prueba nada por sí solo: Cloudflare, Akamai y AWS WAF aplican sus reglas *antes* de que tu origen llegue a parsear un archivo robots. La comprobación en el edge es la única que significa algo.

---

## Por qué existe esto

Tres modos de fallo, todos estructurales más que ingeniosos.

**1. Datos obsoletos en silencio.** La queja estructural más citada del SEO agéntico. De [r/AiAutomations, 2026-09-07](https://www.reddit.com/r/AiAutomations/comments/1w9h1sv/an_seo_agent_kept_working_for_two_weeks_after_its/):

> *«En analook dot com, un token OAuth de GSC caducó y el agente siguió usando datos de Search Console en caché durante dos semanas. Las posiciones cambiaban mientras que sus decisiones seguían basándose en la vista antigua… El flujo puede ejecutarse con éxito contra una entrada que ya no debería considerarse fiable.»*

El flujo termina con código 0. El informe parece correcto. Cada número que contiene es un hecho del pasado formulado en presente.

**2. Salida segura pero irreproducible.** De [r/SEO_Xpert, 2026-07-10](https://www.reddit.com/r/SEO_Xpert/comments/1ush4r6/my_experience_with_using_ai_claude_codecodex_for/): un agente propuso ~150 enlaces internos con total confianza; ~20 eran utilizables. La misma página, en una sesión nueva, produjo recomendaciones distintas. Nada en la salida te decía qué elementos procedían de datos y cuáles de las prioridades del modelo.

**3. Técnicas que nunca compensaron.** `llms.txt` se ha vendido, documentado y desplegado durante todo el año como palanca de visibilidad en IA. Seis estudios de 2026 no encuentran relación entre publicar el archivo y obtener más citas o más rastreo. [La tabla de evidencias está más abajo](#lo-que-estas-skills-se-niegan-a-hacer).

---

## Las cuatro skills en detalle

### `seo-data-contract` — frescura y procedencia antes del análisis

Cada número de SEO que usa un agente es una afirmación sobre el pasado. Esto obliga a envolver ese número en un sobre fechado y con fuente antes de escribir una sola palabra de análisis, y rechaza el análisis de plano cuando la entrada ya no es fiable.

Tres preguntas, todas obligatorias:

1. **¿Puede autenticarse ahora mismo?** Una respuesta en caché no es una comprobación de autenticación.
2. **¿Cuándo fue el último éxito de una recuperación?** No la última actualización del proveedor — la última extracción correcta del propio agente.
3. **¿Cuál es la fecha más reciente representada *dentro* de los datos?** No la hora de la descarga. Una consulta ejecutada hoy a las 14:03 puede devolver filas cuyo último día completo es de hace tres semanas.

Después, una clasificación determinista — `fresh · aging · stale · expired · unknown · observed` — calculada como una resta frente a la latencia esperada de la fuente. Una credencial `expired` o `revoked` sobre datos envejecidos hace que la clase baje como mínimo a `stale`: los datos no están solo viejos, están congelados, y no hay camino de vuelta a `fresh`. `unavailable` deliberadamente no fuerza ese descenso, porque un usuario que pega una exportación de GSC nunca tuvo una credencial que perder, y rechazarla rompería la vía sin claves sobre la que está construido este repositorio.

Gestiona explícitamente el caso dominante en el mundo real: *el usuario acaba de escribir un número en el chat*.

### `aeo-bot-access-audit` — ¿pueden los bots leerte de verdad?

Es lo que más se les escapa a los profesionales, y todo lo demás del repositorio depende de si el bot de recuperación recibió bytes de vuelta. Siete pasos, todos con `curl`:

- Lee `robots.txt` como una especificación, no como una intuición.
- Clasifica cada token `User-agent:` por finalidad — **entrenamiento vs. recuperación vs. solicitado por el usuario**. Bloquear `GPTBot` no bloquea la Búsqueda de ChatGPT (`OAI-SearchBot` sí). La mayoría de los sitios lo tienen al revés.
- Ejecuta las cuatro trampas documentadas de `robots.txt`, incluidas rutas críticas de render bloqueadas bajo `/assets/` o `/wp-content/`, que parecen un bloqueo y se comportan como un éxito parcial.
- **Verifica en el edge, bot por bot, con la cadena UA publicada exacta.** Un 200 desde tu IP con una UA suplantada te dice que el edge no bloquea esa cadena. No demuestra lo que recibe el bot real — el bot real llega desde otra red, puede llevar otra versión y puede estar filtrado por reputación de IP. Para Anthropic no existe ninguna cadena UA publicada; verifica la identidad contra la lista de IPs publicada.
- Confirma el descubrimiento del sitemap mediante la directiva `Sitemap:`.
- Lee el control de vista previa (`nosnippet`), que es una decisión distinta con economía opuesta.

**La política entrenamiento-vs.-recuperación puntúa cero a propósito.** No existe consenso profesional, al menos una tabla de rastreadores de 2026 muy copiada es sencillamente incorrecta al respecto, y es tu decisión, no un hallazgo.

### `aeo-citability-audit` — puntuada para un segundo modo de consumo

20 comprobaciones deterministas, 5 puntos cada una, en tres grupos:

| Grupo | Comprobaciones | Puntos | Qué mide |
|---|---|---|---|
| Extructibilidad | X-01…X-08 | 40 | Posición de la respuesta, renderizado en servidor frente a inyectado por JS, jerarquía de encabezados, marcado semántico, bloques autocontenidos, presencia de listas/tablas, `<html lang>` |
| Merecimiento de cita | W-01…W-07 | 35 | Densidad de hechos con fuente, cobertura de los hechos en los que coinciden las páginas citadas, citas atribuidas, referencias externas, tablas comparativas, definiciones citables, precio visible + fecha visible |
| Integridad de entidad y página | E-01…E-05 | 25 | Consistencia de nombres, clúster temático, superficie de confianza, control de vista previa, frescura legible por máquina |

**Multilingüe, y honesto al respecto.** El recuento de palabras se basa en caracteres por idioma (tabla `chars/token` para 11 familias de idiomas), las comprobaciones de posición se basan en caracteres en lugar de palabras, y las etapas léxicas de X-05, W-03 y W-06 incluyen léxicos para **en, nl, es, pt, it, fr, de**. En cualquier otro idioma esos tres devuelven **N/A**, nunca una puntuación fallida. El principal scorer de citabilidad del mercado es solo inglés y por expresiones regulares —un bug documentado en su propio rastreador de incidencias—, y el informe siempre lista las comprobaciones N/A por su ID. Un informe que dice 95/100 con dos N/A silenciosos es peor que uno que dice 90/95.

La auditoría imprime esta línea siempre que puntúa por encima de 70 sin ningún N/A: *«nada está mal en la página»*. No «vas a ser citado». El factor mejor situado de Shepard es la accesibilidad de URL, con 9,5; la posición de búsqueda es el segundo, con 9,4, y esta auditoría no puede medirlo sin datos de pago.

### `information-gain-analysis` — por qué te citan o te recortan

La patente de Google **US11354342B2** describe un asistente que responde desde la fuente 1 con los hechos A+B, luego desde la fuente 2 con el hecho C *únicamente*, eliminando el solapamiento. La lectura que hace Ahrefs de ella es la frase sobre la que está construido este repositorio:

> *«En una lista ordenada, aunque seas el cuarto sitio que dice lo mismo, sigues estando en el SERP… Pero en una respuesta sintetizada **no** hay una posición cuatro. O aportas la información que aún no se ha dicho, o tu contenido se recorta.»*

La skill construye un registro de hechos a partir de las páginas que hoy posicionan, lo resta del tuyo y devuelve una **lista de trabajo** priorizada de hechos que nadie más tiene — cada uno con una vía concreta para obtenerlo. Un hecho no producible es un deseo, no un hallazgo.

Dos reglas rigen la puntuación:

1. **La posición aporta cero puntos.** El estudio de On-Page.ai sobre 150 páginas en top-3 encontró la posición *sin relación* con la puntuación dentro del top 3, mientras que las páginas con 15+ puntos de datos únicos promediaban 62,1 frente a 40,2 de las páginas con 0–1. Puntuar aquí la posición blanquearía una señal probadamente buena dentro de una etiqueta llamada ganancia de información. (Investigación de proveedor (*vendor research*): On-Page.ai vende un producto de puntuación y este Information Gain Score es su propia métrica.)
2. **El recuento es determinista; el juicio de significado no.** «¿Este número informa o es relleno?» es un juicio sobre el significado. La skill lo informa como juicio, nunca como medición, e incluye un bloque de divulgación obligatorio.

---

## Instalación

```bash
# Detecta automáticamente los agentes instalados
npx skills add Pautthead/seo-aeo-agent-skills

# Lista explícita de hosts. Nombra Claude Code explícitamente: ejecutar el
# instalador desde dentro de una sesión de agente puede escribir solo en
# .agents/skills/, que Claude Code no lee.
npx skills add Pautthead/seo-aeo-agent-skills -a claude-code -a opencode -a codex -a grok
```

Marketplace de plugins de Claude Code:

```
/plugin marketplace add Pautthead/seo-aeo-agent-skills
/plugin install seo-aeo@seo-aeo-agent-skills
```

O copia `skills/<name>/` a mano al directorio de tu host:

| Host | `--agent` | Ruta del proyecto | Ruta global |
|---|---|---|---|
| Claude Code | `claude-code` | `.claude/skills/` | `~/.claude/skills/` |
| OpenCode | `opencode` | `.agents/skills/` | `~/.config/opencode/skills/` |
| Codex | `codex` | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `cursor` | `.agents/skills/` | `~/.cursor/skills/` |
| **Grok Build (xAI)** | `grok` | `.grok/skills/` | `~/.grok/skills/` |
| Hermes Agent | `hermes-agent` | `.hermes/skills/` | `~/.hermes/skills/` |
| OpenClaw | `openclaw` | `skills/` | `~/.openclaw/skills/` |
| Gemini CLI | `gemini-cli` | `.agents/skills/` | `~/.gemini/skills/` |
| Cline | `cline` | `.agents/skills/` | `~/.agents/skills/` |
| OpenHands | `openhands` | `.openhands/skills/` | `~/.openhands/skills/` |
| Goose | `goose` | `.goose/skills/` | `~/.config/goose/skills/` |
| Crush | `crush` | `.crush/skills/` | `~/.config/crush/skills/` |
| Amp | `amp` | `.agents/skills/` | `~/.config/agents/skills/` |
| Warp | `warp` | `.agents/skills/` | `~/.agents/skills/` |
| Kiro CLI | `kiro-cli` | `.kiro/skills/` | `~/.kiro/skills/` |

`.agents/skills/` es la ubicación de proyecto portátil de facto — Codex, Cursor, Cline, Amp, Warp y OpenCode la leen de forma nativa, así que no hace falta ningún enlace simbólico. OpenCode además lee `.opencode/skills/`, `.claude/skills/` y `.agents/skills/`, subiendo desde el directorio de trabajo hasta la raíz del worktree. Grok Build lee `.grok/skills/` y *también* escanea `.agents/skills/` en cada nivel, y respeta `GROK_HOME`.

Eso es un subconjunto de los ~80 agentes que admite la CLI `skills`. Cualquier host que sepa leer `SKILL.md` puede usarlas.

---

## Lo que estas skills se niegan a hacer

Consulta esta sección si has venido a evaluarnos. Alrededor del 80% del GEO es SEO corriente. Un servicio que no lo dice vende una disciplina aparte que la evidencia no sostiene ([Jeremy Moser, vía Digiday, 2026-03-10](https://digiday.com/media/geo-hype-busted-experts-call-it-more-seo-than-new-discipline/)).

### `llms.txt` no te consigue citas en las respuestas de IA

Seis estudios de 2026. Ninguno encuentra relación entre publicar `llms.txt` y obtener más citas o más rastreo. Dos son mediciones independientes (Ahrefs, Arsentev), tres son investigación de proveedor (SE Ranking, Otterly.AI, CueScout) y una es editorial (Search Engine Land). Tres de los seis miden descargas del archivo, no citas.

| Estudio | Fecha | N | Resultado | Tipo |
|---|---|---|---|---|
| [Ahrefs](https://ahrefs.com/blog/llmstxt-study/) | 2026-06-15 | 137.210 dominios | El 28% publica uno; el **97% no recibió ninguna petición**; *«Ningún bot de IA va a buscar archivos llms.txt que no existen»* | medido |
| [SE Ranking](https://seranking.com/blog/llms-txt/) | 2026-10-15 | ~300.000 dominios | 10,13% de adopción; su modelo se volvió **más** preciso cuando se eliminó la variable — *«Los LLMs.txt podrían introducir hoy más ruido que valor»* | investigación de proveedor (*vendor research*) |
| [Otterly.AI](https://otterly.ai/blog/the-llms-txt-experiment/) | 2026-02-05 | 62.100 visitas de bots de IA / 90 días | 84 peticiones llegaron a `/llms.txt` (~0,1%); sin correlación positiva con la actividad de rastreo de IA | investigación de proveedor (*vendor research*) |
| [Search Engine Land](https://searchengineland.com/does-llms-txt-matter-467740) | 2026-01-20 | 10 sitios, antes/después | 8 sin cambios; los sitios que publicaron **contenido funcional nuevo** crecieron, los que solo documentaron contenido existente no crecieron nada | editorial |
| [CueScout](https://cuescout.com/blog/does-llms-txt-work) | 2026-10-15 | 537 sitios SaaS, 80 respuestas de AI Mode | 24,3% citados *con* él frente a 21,8% *sin* él (p=0,53); **ninguno de los 708 enlaces citados señalaba a un archivo llms.txt** | investigación de proveedor (*vendor research*) |
| [Arsentev, log de origen](https://doi.org/10.5281/zenodo.23018429) | 2026-09-28 | 345.808 peticiones / 15 días | **Cero** peticiones con token de rastreador a `/llms.txt`; robots.txt recibió 698, sitemap.xml recibió 282 | medido |

**El matiz.** «No funciona» se pasa. De los archivos que se descargan, la mayor parte del tráfico no es una herramienta de IA: Ahrefs sitúa a los agentes de IA en el 10,5% de las peticiones y en el quinto puesto global. Los bots de IA con nombre llegan al 19,5% solo al sumar las cuatro categorías. La frase de Mueller sobre la «muleta temporal», que Ahrefs extiende a este archivo, iba sobre la documentación de desarrolladores en markdown de Google. El resultado nulo de CueScout es la versión corta: nada que se cita apunta al archivo. Para ChatGPT, Perplexity o AI Overviews, Ahrefs llama al archivo «en gran medida decorativo». Presupuesta cero frente al tráfico.

La propia documentación de Google, en una sección titulada *«Mythbusting generative AI search: what you don't need to do»*, dentro del punto **«LLMS.txt files and other "special" markup»**:

> *«No necesitas crear nuevos archivos legibles por máquina, archivos de texto para IA, marcado ni Markdown para aparecer en Google Search (incluidas sus capacidades de IA generativa), porque Google Search no los usa.»*
>
> *«No hay ningún problema en que decidas crear y mantener archivos LLMS.txt (u otros similares) para otros servicios o sistemas que usan esos archivos. Hacerlo no perjudicará ni mejorará la visibilidad ni el posicionamiento de tu sitio en Google Search, porque Google Search los ignora.»*
> — [Google Search Central, «Optimizing your website for generative AI features on Google Search»](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide)

Los avisos propios de Ahrefs viajan junto a la cifra: el 28% de adopción es una **cota superior** (su base de clientes se inclina hacia lo técnico), y *«cada cifra de este estudio es, por tanto, un techo del consumo real de llms.txt»*.

**Lo que recomendamos en su lugar.** Espejos en Markdown. Con un índice más espejos `.md` presentes, el coste de ingesta de los agentes bajó a ~123K tokens / ~10 llamadas a herramientas frente a ~240K / ~20 sin ellos ([a14y](https://a14y.dev/research/llms-txt-linking/) - estudio de un proveedor sobre su propia herramienta; n=5 por brazo, un solo sitio, así que direccional). La calidad de las respuestas se mantuvo. *«El coste es la ingesta, no la generación»*. Y fíjate en lo que **no** funcionó ahí: se probaron tres formatos de enlace — `<link rel="llms-txt">`, `<link rel="alternate" type="text/markdown">`, un enlace visible «For agents» en el pie — y **los tres obtuvieron 0/5 de adopción**. El único brazo que se movió fue una línea en el prompt.

### El schema FAQPage no es una palanca de GEO

Shepard puntúa los datos estructurados con 5,6 y es cuidadoso en ambos sentidos: los LLM *«no suelen ingerir schema como parte de su entrenamiento»* y hay *«evidencia limitada de que al menos puedan ver el schema al buscar»* — pero *«prácticamente todos los estudios que analizan el schema y las citas de IA encuentran una relación positiva. El efecto suele ser pequeño, pero es asombrosamente consistente entre estudios»*.

Citamos ambas mitades porque citar solo la negativa tergiversa la fuente. La conclusión no cambia: el schema merece la pena por los resultados enriquecidos y la claridad de entidad, no como táctica GEO. Google además dejó de mostrar resultados enriquecidos de FAQ para la mayoría de sitios hace tiempo, mientras que varias skills de 2026 siguen recomendando automáticamente añadir FAQPage.

### Nada de publicación automatizada en foros o en Reddit

Reddit eliminó las cuatro comunidades de subreddit que **OtterlyAI** había creado para su propio experimento de engagement GEO de 60 días, por incumplimiento de la Regla 2 de la Content Policy de Reddit ([OtterlyAI, 2026-10-01](https://otterly.ai/blog/reddit-geo-2026/)) — el autoinforme de un proveedor sobre su propio experimento fallido, y la razón por la que el sector automatizó Reddit desde el principio. **Mide Reddit. Nunca publiques en él.**

### Ninguna promesa de visibilidad en IA en menos de 60 días

Ninguna fuente pública fiable ofrece una ventana de aumento de citas. Una cifra de «60–120 días» circula ampliamente; no se pudo rastrear hasta una fuente primaria y se ha eliminado de este repositorio en lugar de suavizarla. Lo que sí se sostiene: los cambios on-page se mueven en semanas, los cambios en citas de terceros se mueven mucho más despacio. Si alguien te cita una ventana precisa, pídele el estudio.

### Ninguna afirmación de que el GEO es una disciplina aparte

> *«El 80 por ciento del GEO es buen SEO fundamental. Si un servicio de GEO no te dice abiertamente que el éxito en la visibilidad de IA es un 80 por ciento de buen SEO fundamental, te están vendiendo aceite de serpiente.»*
> — Jeremy Moser (uSERP), vía Digiday, 2026-03-10

### Y la regla que está por encima de todo lo anterior

**No produzcas un hallazgo que la técnica no pueda detectar de verdad.** Si una comprobación es N/A — idioma no soportado, campo ausente, fuente inalcanzable — infórmala como *no puntuada*. Nunca como aprobado, nunca como suspenso.

Una asimetría que conviene conocer: los recuperadores que resumen (`web_fetch` y similares) **eliminan las etiquetas `<script>`**, así que una página recuperada así realmente no se puede comprobar en busca de JSON-LD. Pero **`curl` devuelve bytes en bruto**, así que ahí tienes que hacer grep del cuerpo buscando `"@type"` e informar de lo que hay de verdad. No conviertas una comprobación resoluble en un N/A permanente.

---

## Datos de pago opcionales — DataForSEO

Nada de este repositorio requiere nada de esto. Las cuatro skills se completan sin credenciales. Esta sección existe porque una carencia — datos de posición en el SERP, para los dos factores mejor puntuados — no tiene equivalente gratuito, y porque aquí los precios tienen una trampa que conviene conocer.

Este enlace es un enlace de afiliado: podemos obtener una comisión si te registras. DataForSEO aparece porque son los datos masivos de SERP/keywords más baratos que encontramos, no porque sea necesario. No es un aval de la calidad de sus datos: la advertencia de frescura de abajo es real y es suya.

Precios comprobados el 2026-10-19 en [dataforseo.com/pricing](https://dataforseo.com/pricing). El precio de un proveedor cambia sin aviso; verifícalo antes de presupuestar.

| Endpoint | Precio | Notas |
|---|---|---|
| `dataforseo_labs/google/*/live` | **$0.012/tarea + $0.00012/ítem** | Por defecto. Solo live, sin cola. Máx. 700 keywords/tarea, 1.000 ítems/respuesta, 2.000 llamadas/min, 30 concurrentes |
| `historical_rank_overview/live` | $0.12/tarea + $0.0012/ítem | Desbloquea la posición de búsqueda y el fan-out rank en la auditoría de citabilidad |
| `historical_serps/live` | $0.00012/SERP | |
| `search_intent/live` | $0.012/tarea + $0.00012/keyword | |
| SERP API (cifra principal) | **$2.00 / 1k live** · $1.20 / 1k priority · $0.60 / 1k standard | Mira la trampa |

> **Trampa de precios.** La tarifa principal de **$0.60/1k** es la cola *standard*, que tarda unos **5 minutos**. Para un agente interactivo no es un producto equivalente, así que **$2.00/1k live es la comparación honesta**. Cotizamos $2.00 en todas partes.

**El refresco de la base de datos es de 30 a 90 días.** Nunca presentes la salida de Labs como tiempo real.

**Servidor MCP oficial — el servidor es gratuito, tú pagas las tarifas de API:**

- Remoto: `https://mcp.dataforseo.com/v3/mcp` con `Authorization: Basic base64(login:password)`
- Local: `npx -y dataforseo-mcp-server` con `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD`
- Código: [github.com/dataforseo/mcp-server-typescript](https://github.com/dataforseo/mcp-server-typescript)

**Trampa de autenticación:** solo HTTP Basic, y las credenciales vienen del login de **API** en `app.dataforseo.com/api-access`. Usar el login del panel es el fallo de autenticación más habitual.

**Primeros pasos:** crédito de prueba de $1, recarga mínima de $50. → [fluyeporlaweb.com/go/dataforseo](https://fluyeporlaweb.com/go/dataforseo/) (enlace de afiliado).

---

## Cómo funciona la puntuación

Cuatro reglas, aplicadas a todas las skills:

1. **Análisis determinista, reescritura por LLM.** Los scorers, las listas de verificación y los parsers son reglas reproducibles que el agente aplica, no juicios que improvisa. El riesgo de alucinación pertenece a la capa que produce prosa, no a la que produce números.
2. **Cada umbral numérico está etiquetado por tipo.** Es o bien una medición con una fuente trazable, o explícitamente un juicio. El 9,5 de Cyrus Shepard para la accesibilidad de URLs es una **puntuación de correlación asignada a mano, no una medición** — sus propias palabras: *«Asigné cada puntuación a mano según esos criterios, usando IA para ayudar a ajustar los números finales… No son factores de clasificación confirmados. Correlación no es causal.»* Los usamos para ordenar, nunca como tamaños de efecto. La tabla `chars/token` de la skill de citabilidad está etiquetada como juicio.
3. **Los tipos de fuente están etiquetados.** `measured` (Ahrefs, arXiv, Zenodo) · `vendor research` (SE Ranking, CueScout, OtterlyAI, Muck Rack, On-Page.ai, Indig/Omnia) · `editorial` (Search Engine Land) · `vendor docs` (OpenAI, Perplexity, Google). Una cifra de marketing de un proveedor nunca se disfraza de hecho.
4. **Documenta tus propios límites, y hazlo en serio.** Cada skill incluye una sección `Known limitations` que se copia literalmente al informe.

### Lo que esta regla ya nos ha costado

La revisión encontró una **cita fabricada** atribuida a Danny Sullivan — *«No hay ningún beneficio en crear un archivo llms.txt para el SEO.»* No está en ninguna fuente. Nos llegó por medio de una pasada de investigación y se quedó en el README hasta que alguien fue a buscarla. Ha desaparecido, sustituida por la propia documentación de Google, que es una cita más sólida que la cita de segunda mano que intentábamos usar.

También eliminados: una estadística atribuida a un informe comunitario con nombre propio en una fecha concreta y sin nada detrás; un número equivocado (2.135 peticiones a robots.txt) pegado a un estudio real; una métrica mal etiquetada (98% de exactitud para lo que es 97,0 de macro-F1); dos URL que en silencio resuelvían a páginas índice de blog; una fuente que no se pudo encontrar en absoluto; y números de versión de User-Agent que estaban mal en comandos pensados para copiar y pegar.

Cada uno está registrado en [`docs/SOURCE-VERIFICATION.md`](docs/SOURCE-VERIFICATION.md) y en [`docs/METHODOLOGY-BRIEF.md`](docs/METHODOLOGY-BRIEF.md) §1.9c para que la siguiente persona que contribuya no los reintroduzca.

---

## Hoja de ruta

Carencias documentadas, desde [`docs/METHODOLOGY-BRIEF.md`](docs/METHODOLOGY-BRIEF.md) §5. **Ninguna está en v1.**

| Previsto | Por qué es una carencia real |
|---|---|
| **Validador de schema JSON-LD** contra resultados enriquecidos | Muchas skills generan datos estructurados. Casi ninguna los valida. |
| **Mapeador del grafo de enlaces internos** | *«Muchas skills lo mencionan, ninguna mapea realmente un grafo de enlaces.»* Directamente relevante para el fallo de 150 propuestas y 20 utilizables. |
| **Análisis de hueco de keywords** | La cobertura competitiva actualmente exige una exportación de pago. |
| **Coincidencia de intención / tipo de página del SERP** | Factor top-6 en la ordenación de Shepard. La auditoría de citabilidad lo aproxima; nada lo puntúa bien. |
| **Triaje de la decadencia de contenidos** | Distingue la decadencia de tráfico de la de posiciones y de la obsolescencia. Requiere GSC. |
| **Tracker de experimentos GEO** | Una variable, 7–21 días, tres motores. Nada en el mercado resiste cambiar cinco cosas a la vez. |
| **Deriva SEO como GitHub Action pre-merge** | El fallo de datos obsoletos detectado antes del merge en lugar de después de una revisión trimestral. |
| **SEO específico por framework** para Next.js, Astro, Nuxt | El output de render y los metadatos difieren lo suficiente como para que el consejo genérico sea erróneo. |
| **Soporte multisitio / agencia** | Comparar una cartera contra su propia línea base en lugar de cada sitio por separado. |

---

## Dónde encaja esto

Contexto honesto, no un ataque competitivo. Varios de estos repositorios son buenos, y algunos son más amplios que este. Estrellas a fecha de 2026-10-19.

| Repo | ★ | Lo que hace bien |
|---|---|---|
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 55k | Amplitud en marketing; sus propias limitaciones autodocumentadas son la práctica que aquí se toma prestada |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | 35k | El instalador `npx skills` por el que se distribuye este repositorio. Infraestructura, no SEO |
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | 19k | Superficie de SEO para Claude Code, muy completa |
| [zubair-trabzada/geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) | 11k | Lo más parecido a un conjunto de skills GEO dedicado |
| [TheCraigHewitt/seomachine](https://github.com/TheCraigHewitt/seomachine) | 7,5k | Cobertura amplia de SEO técnico |
| [Ryze-AI-Adgent/open-seo-mcp-skills](https://github.com/Ryze-AI-Adgent/open-seo-mcp-skills) | 6k | Datos en vivo vía MCP out of the box |
| [nowork-studio/notfair-plugin](https://github.com/nowork-studio/notfair-plugin) | 4k | Auditorías opinadas y decididas |
| [seranking/seo-skills](https://github.com/seranking/seo-skills) | 175 | Skills individuales limpias y bien delimitadas, con ejecuciones reales de ejemplo |
| [inhouseseo/superseo-skills](https://github.com/inhouseseo/superseo-skills) | 360 | Estrictamente sin claves, metodología nombrada, conjunto de reglas anti-slop |

Tres patrones en todo el sector: la mayoría son **solo para Claude Code**, casi todas necesitan una **suscripción de pago** para los datos en vivo, y pocas documentan sus propios límites. Donde ellos son más fuertes —amplitud, datos de SERP en vivo, cobertura de frameworks— la hoja de ruta de arriba es la respuesta.

---

## Cómo contribuir

Lee primero [`AGENTS.md`](AGENTS.md); lo cargan Codex, OpenCode, Cline, Gemini CLI, Cursor, OpenClaw y Hermes. Después lee [`docs/METHODOLOGY-BRIEF.md`](docs/METHODOLOGY-BRIEF.md), la fuente de verdad interna sobre anatomía de las skills, invariantes de portabilidad y la lista de cosas que este repositorio nunca debe hacer.

**Para añadir una skill:**

1. `skills/<name>/SKILL.md` más `references/`. Nada anidado más profundo.
2. El frontmatter lleva **solo** `name`, `description`, `license`, `compatibility` y `metadata` (exactamente cuatro claves de texto: `repo`, `version`, `updated`, `keys-required`). `name` debe ser igual al nombre del directorio, en kebab-case minúscula.
3. `description` adelanta qué hace, cuándo usarla y sus palabras clave disparadoras — Codex presupuesta la lista completa de skills en 8.000 caracteres y trunca las descripciones primero.
4. Orden del cuerpo: propósito · cuándo usarla / cuándo no usarla · entradas (la vía sin claves primero) · procedimiento con una comprobación ejecutable y un aprobado falsable por paso · formato de salida · puntuación · limitaciones conocidas · fuentes de datos opcionales · referencias.
5. Los enlaces a skills hermanas son `references/FILE.md`, un solo nivel, siempre — y deben resolverse.
6. Nada de `context: fork`, nada de hooks en el núcleo. Ambos son exclusivos de Claude Code y romperían la portabilidad.
7. **Cero claves de API obligatorias.** Si no puede completarse sin una cuenta de pago, no está lista.

**Puertas de validación — ejecútalas antes de abrir una PR:**

```bash
python tests/validate_skill_inventory.py --strict
python tests/reference_freshness.py --review-after-days 90 --stale-after-days 365
```

Las dos se ejecutan en CI en cada push. La primera comprueba la conformidad con la especificación y que cada enlace interno resuelve; se niega a informar PASS cuando no ha comprobado nada. La segunda usa **dos umbrales deliberadamente**: 90 días marca un *disparador de revisión* —el hallazgo puede haber quedado superado aunque la fuente no haya caducado— y 365 días falla. Un único umbral marcaría como roto cada artículo de investigación primario con más de tres meses, que es ruido, y el ruido es la razón por la que se acaban ignorando las puertas.

**La regla de citación.** Cada umbral numérico debe remontarse a una fuente fechada con un nivel de evidencia declarado. **Abre la fuente y confirma que dice lo que afirmas.** Leer el texto primario es el mínimo. Si no puedes verificarlo, no lo cites — una afirmación que no se puede verificar se elimina, no se suaviza.

---

## Licencia

Apache-2.0. Úsala, hazle un fork, incorpórala a tu propia herramienta de auditoría.

## Créditos y fuentes

Construido por [Pautthead](https://github.com/Pautthead). Tabla completa de verificación con fechas, tamaños de muestra y veredictos en [`docs/SOURCE-VERIFICATION.md`](docs/SOURCE-VERIFICATION.md).

**Medido**

- [Ahrefs — Analizamos 137K sitios](https://ahrefs.com/blog/llmstxt-study/) — Louise Linehan, 2026-06-15, n=137.210 dominios
- [Ahrefs — Qué es la ganancia de información en SEO](https://ahrefs.com/blog/information-gain/) — Louise Linehan, 2026-08-20
- [arXiv 2605.25517](https://arxiv.org/abs/2605.25517) — *What Gets Cited: Competitive GEO in AI Answer Engines*, 2026-05-25, 252.000 ensayos en 6 LLMs
- [arXiv 2609.15369](https://arxiv.org/abs/2609.15369) — *SlopShape*, Jochen Madler (Sitefire), 2026-09. 97,0 macro-F1 sobre empresas en holdout a partir de 176 rasgos estructurales; el macro-F1 no es un porcentaje de exactitud
- [Zenodo 10.5281/zenodo.23018429](https://doi.org/10.5281/zenodo.23018429) — Arsentev, 2026-09-28, estudio de logs de origen. Límites declarados por el autor: un origen, tres nombres de host agrupados, logging solo en origen detrás de una CDN, identidad autodeclarada
- [Google — Patente US11354342B2](https://patents.google.com/patent/US11354342B2/en) — «Contextual estimation of link information gain», Google LLC. La formulación «no hay posición cuatro» es interpretación de Ahrefs, no el texto de la patente
- [Zenodo 10.5281/zenodo.23128812](https://doi.org/10.5281/zenodo.23128812) — Hall, comportamiento de rastreadores con el anuncio `Sitemap:` de robots.txt. El autor declara un interés legítimo: es dueño del plugin que midió

**Investigación de proveedor (*vendor research*)**

- [Cyrus Shepard / Zyppy](https://signal.zyppy.com/p/ai-citation-ranking-factors) — 2026-05-07, 54 experimentos. Puntuaciones de correlación asignadas a mano, no mediciones
- [SE Ranking](https://seranking.com/blog/llms-txt/) · [CueScout](https://cuescout.com/blog/does-llms-txt-work) (ambos 2026-10-15) · [Otterly.AI](https://otterly.ai/blog/the-llms-txt-experiment/) (2026-02-05)
- [On-Page.ai — estudio de Ganancia de Información](https://api.on-page.ai/research/information-gain-study) — Eric Lancheres, 2026-06-12, 150 páginas. Su propia métrica, y la venden
- Kevin Indig, [The Consensus Gap](https://www.growth-memo.com/p/the-consensus-gap), 2026-05-11 — el 91% de las citas apareció en un único motor (a nivel de URL, entre ChatGPT / Perplexity / AI Overviews). Los datos son de Omnia, el producto propio de Indig, y él declara que la muestra se inclina hacia su base de clientes
- Muck Rack (25M+ enlaces citados) — la cifra del 84% de medios ganados incluye Wikipedia y PubMed Central; solo periodismo es ~27%, y el tamaño de muestra se indica de forma inconsistente en sus propias páginas. Solo orientativo

**Editorial**

- [Search Engine Land](https://searchengineland.com/does-llms-txt-matter-467740) — 2026-01-20. Ojo: su propia aritmética no cuadra (2 al alza + 8 planas + 1 a la baja = 11 para una muestra declarada de 10)
- [a14y.dev](https://a14y.dev/research/llms-txt-linking/) — Claude 2.1.141, Docker aislado, n=5 por brazo, un solo sitio
- Jeremy Moser vía [Digiday](https://digiday.com/media/geo-hype-busted-experts-call-it-more-seo-than-new-discipline/), 2026-03-10 · Lily Ray, [*The AI Slop Loop*](https://lilyraynyc.substack.com/p/the-ai-slop-loop), 2026-04-14 · John Mueller vía [SERoundtable](https://www.seroundtable.com/google-adds-markdown-files-to-help-docs-41342.html), 2026-05-19

**Documentación de proveedor (*vendor docs*)**

- [Google Search Central — AI features and your website](https://developers.google.com/search/docs/appearance/ai-features)
- [OpenAI — documentación de rastreadores](https://platform.openai.com/docs/bots) · [Perplexity — bots](https://docs.perplexity.ai/guides/bots)

**Informes comunitarios** (anecdóticos, un modo de fallo, no evidencia): [r/AiAutomations, 2026-09-07](https://www.reddit.com/r/AiAutomations/comments/1w9h1sv/an_seo_agent_kept_working_for_two_weeks_after_its/) · [r/SEO_Xpert, 2026-07-10](https://www.reddit.com/r/SEO_Xpert/comments/1ush4r6/my_experience_with_using_ai_claude_codecodex_for/) · [r/SideProject, 2026-09-24](https://www.reddit.com/r/SideProject/comments/1wp4s2r/do_unique_stuff_a_real_mcp_data_server/) · [r/SEO, 2026-01-26](https://www.reddit.com/r/SEO/comments/1qngfmm/is_programmatic_seo_still_a_good_move_in_2026/) · [r/AskMarketing, 2026-09-29](https://www.reddit.com/r/AskMarketing/comments/1wt41hp/guys_have_you_used_any_ai_seo_tools_for_aeogeo/).

**Distribución:** la CLI `skills` de Vercel Labs, verificada contra la [especificación de Agent Skills](https://agentskills.io/specification) en lugar de contra posts de blog — varias guías de instalación de 2026 publican rutas que no existen.

---

*Si una afirmación de este repositorio no puede remontarse a una fuente fechada, eso es un bug. Por favor, abre una incidencia.*