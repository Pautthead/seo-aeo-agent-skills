# Skills de SEO, AEO y GEO para agentes de IA — cuatro skills de agente verificables

Skills de AI SEO respaldadas por evidencia para Claude Code, Codex, Cursor, OpenCode, Gemini CLI, Cline, Hermes y ~75 hosts más. Cada regla de puntuación se remonta a una fuente fechada. **Sin claves de API, sin servidores MCP, sin suscripción.**

[![Licencia: Apache-2.0](https://img.shields.io/badge/licencia-Apache--2.0-blue.svg)](LICENSE)
[![Instalación](https://img.shields.io/badge/instalar-npx%20skills-8a2be2.svg)](https://www.npmjs.com/package/skills)
[![Claves de API](https://img.shields.io/badge/claves%20de%20API-ninguna%20requerida-brightgreen.svg)](skills/)
[![Skills](https://img.shields.io/badge/skills-4-orange.svg)](skills/)

---

## Qué es esto

Cuatro Agent Skills que ejecutan auditorías SEO y AEO deterministas dentro de un agente de código — y te dicen, por escrito, qué no pueden detectar.

| Skill | La pregunta que responde | ¿Necesita claves? |
|---|---|---|
| [`seo-data-contract`](skills/seo-data-contract/SKILL.md) | ¿Estos datos son lo bastante frescos y fiables como para actuar sobre ellos? | No |
| [`aeo-bot-access-audit`](skills/aeo-bot-access-audit/SKILL.md) | ¿Pueden los bots de IA leer realmente este sitio? | No (solo `curl`) |
| [`aeo-citability-audit`](skills/aeo-citability-audit/SKILL.md) | ¿Sobreviviría esta página a ser extraída y citada? | No |
| [`information-gain-analysis`](skills/information-gain-analysis/SKILL.md) | ¿Qué sabe esta página que el SERP no? | No |

## Qué no es esto

- No es una biblioteca de prompts. Cada comprobación tiene una prueba ejecutable y una condición de aprobado falsable.
- No es un producto GEO. Alrededor del **80% del GEO es buen SEO fundamental** — y el posicionamiento de tu sitio es la mayor parte de lo que hace que te citen. Si un servicio de GEO no te lo dice abiertamente, te están vendiendo aceite de serpiente ([Jeremy Moser, vía Digiday, 2026-03-10](https://digiday.com/media/geo-hype-busted-experts-call-it-more-seo-than-new-discipline/)).
- No es una suscripción. Si no puedes ejecutarlo sin credenciales, no está en este repositorio. Una muestra de mando de la vía sin claves:

```bash
curl -sSL -w '\n---HTTP %{http_code} | final: %{url_effective} | type: %{content_type}\n' \
  https://example.com/robots.txt
```
- No es un sitio donde el folklore de 2026 se reimplemente en silencio. Mira [Lo que estas skills se niegan a hacer](#lo-que-estas-skills-se-niegan-a-hacer): esa sección *es* la propuesta de valor.

---

## El problema

Tres modos de fallo, todos estructurales, no de falta de ingenio.

**1. Datos obsoletos en silencio.** La queja estructural más citada del SEO agéntico. De `r/AiAutomations`, 2026-09-07:

> *"At analook dot com, a GSC OAuth token expired and the agent continued using cached Search Console data for two weeks. Rankings were changing while its decisions were still based on the old view. That is an awkward failure to catch with a simple 'did the workflow run?' check. The workflow can run successfully against an input that should no longer be trusted."*

El flujo termina con código 0. El informe parece correcto. Cada cifra es un hecho del pasado redactado en presente. `seo-data-contract` existe para que ese fallo sea imposible de publicar.

**2. Salida confiada e irreproducible.** De `r/SEO_Xpert`, 2026-07-19: un agente propuso **~150 enlaces internos con total confianza; ~20 eran utilizables.** La misma página, abierta en una **sesión nueva —un arranque en frío del agente—**, produjo recomendaciones distintas. El agente no lograba reproducir su propio análisis anterior. Nada en la salida te decía cuántos puntos venían de datos y cuántos de los priors del modelo.

**3. Técnicas que nunca funcionaron.** Este es el grande de 2026. `llms.txt` se ha vendido, documentado y desplegado como palanca de visibilidad en IA durante todo el año. Seis mediciones independientes de 2026 dicen que no hace nada. [La tabla de evidencia está más abajo](#lo-que-estas-skills-se-niegan-a-hacer). También otros favoritos de 2026.

---

## Las cuatro skills

### `seo-data-contract` — frescura y procedencia antes de analizar

Cada cifra SEO que usa un agente es una afirmación sobre el pasado. Esta skill obliga a pegar un sobre fechado y con fuente a esa cifra antes de escribir una sola línea de análisis, y rechaza el análisis cuando la entrada ya no es fiable.

Hace **tres preguntas separadas**, y las tres tienen que pasar:

1. **¿Puede autenticarse ahora mismo?** Una respuesta cacheada no es una comprobación de autenticación.
2. **¿Cuándo tuvo éxito una recuperación por última vez?** No la última actualización del proveedor: la última extracción correcta del propio agente.
3. **¿Cuál es la fecha más reciente representada *dentro* de los datos?** No la hora de la descarga. Una consulta ejecutada hoy a las 14:03 puede devolver filas cuyo último día completo es de hace tres semanas.

Después, una clasificación determinista — `fresh · aging · stale · expired · unknown · observed` — calculada como una resta contra la latencia esperada de la fuente. `stale` o `expired` significan que el agente no analiza: emite un bloque de frescura y ofrece tres vías: refrescar ahora, continuar sobre entrada obsoleta etiquetada explícitamente, o hacer la parte que no necesita datos obsoletos.

Funciona totalmente offline. Trata de forma explícita el camino real más habitual: *el usuario acaba de teclear una cifra en el chat*.

### `aeo-bot-access-audit` — ¿pueden los bots leerte de verdad?

Shepard puntúa la **accesibilidad de URL con 9,5/10 — la más alta de 23 factores de citación en IA medidos** ([Zyppy, 2026-05-07](https://signal.zyppy.com/p/ai-citation-ranking-factors)). Todo lo demás en este repositorio depende de si el bot de recuperación recibió los bytes.

Siete pasos, todos con `curl`:

- Leer `robots.txt` como una especificación, no como una impresión.
- Clasificar cada token `User-agent:` por finalidad — **entrenamiento vs recuperación vs petición de usuario**. Bloquear `GPTBot` no bloquea la búsqueda de ChatGPT (`OAI-SearchBot` sí). Permitir `GPTBot` no aporta nada a las citas. La mayoría de sitios se equivoca aquí.
- Ejecutar las cuatro trampas documentadas de `robots.txt`, incluidas rutas críticas de render bloqueadas bajo `/assets/`, `/wp-content/`, `/css/`, `/js/`: parecen un bloqueo y se comportan como un éxito parcial.
- **Verificar en el borde, bot por bot, con la cadena de UA exacta.** Este es el paso que todo el mundo se salta. Cloudflare, Akamai, Fastly y AWS WAF aplican *antes* de que tu origen llegue a parsear un robots. Un `robots.txt` impecable detrás de una regla de challenge significa un sitio que ningún bot de IA puede leer; y un robots limpio no prueba nada por sí solo.
- Confirmar el descubrimiento vía sitemap.
- Leer el control de vista previa (`nosnippet`), que es una decisión distinta con economía opuesta: bloquear `OAI-SearchBot` te saca de ese motor; `nosnippet` solo limita la cita.

**La política de entrenamiento vs recuperación puntúa cero a propósito.** No hay consenso profesional, al menos una tabla de crawlers de 2026 copiada por todo el mundo simplemente está equivocada al respecto, y la decisión es tuya, no un hallazgo.

### `aeo-citability-audit` — puntuado para un segundo modo de consumo

Posicionar no es el único trabajo de una página. El otro es ser *extraída, citada y atribuida* dentro de una respuesta sintetizada. 20 comprobaciones deterministas, 5 puntos cada una, en tres bloques:

| Bloque | Checks | Puntos | Qué mide |
|---|---|---|---|
| Extraibilidad | X-01…X-08 | 40 | Posición de la respuesta, renderizado en servidor vs inyectado por JS, jerarquía de encabezados, marcado semántico, bloques autocontenidos, presencia de listas/tablas, `<html lang>` |
| Mérito de citación | W-01…W-07 | 35 | Densidad de hechos con fuente, cobertura de los hechos que comparten las páginas citadas, citas atribuidas, referencias externas, tablas comparativas, definiciones citables, precio visible + fecha visible |
| Entidad e integridad | E-01…E-05 | 25 | Consistencia de nombres, clúster temático, superficie de confianza, control de vista previa, frescura legible por máquina |

**Multilingüe, y honesto al respecto.** El conteo de palabras es basado en caracteres por idioma (tabla de `chars/token` para 11 familias de idiomas), las comprobaciones de posición son basadas en caracteres y no en palabras, y las etapas léxicas de X-05, W-03 y W-06 incluyen lexicons para **en, nl, es, pt, it, fr, de**. En cualquier otro idioma esos tres checks devuelven **N/A**, nunca una puntuación fallida. El marcador de citabilidad líder del mercado es solo inglés por expresiones regulares —un bug documentado en su propio issue tracker— y el informe siempre lista los checks N/A por ID. Un informe que dice 95/100 con dos N/A silenciosos es peor que uno que dice 90/95.

La línea de cabecera que la auditoría imprime cuando puntúa por encima de 70 sin ningún N/A: *«no hay nada mal en la página»*. No «serás citado». El factor n.º 2 de Shepard es **posición en búsqueda, 9,4/10**, y esta auditoría no puede medirlo sin claves.

### `information-gain-analysis` — por qué te citan o te recortan

La patente de Google **US11354342B2** describe a un asistente que responde con la fuente 1 para los hechos A+B, y después con la fuente 2 únicamente para el hecho C, borrando el solapamiento. La consecuencia que señala Ahrefs es la frase sobre la que está construido este repositorio:

> *"In a ranked list, even if you're the fourth site saying the same thing, you're still on the SERP… But in a synthesized answer there **is** no position four. Either you provide the information that hasn't been said yet, or your content gets cut."*

La skill construye un registro de hechos a partir de las páginas que hoy posicionan, lo resta de tu página y devuelve una **lista de trabajo** priorizada con los hechos que nadie más tiene, cada uno con una vía concreta para obtenerlo. Un hecho que no puedes producir es un deseo, no un hallazgo.

Dos reglas gobiernan la puntuación, y son la razón de que esta skill sea fiable:

1. **La posición no aporta ni un punto.** El estudio de On-Page.ai sobre 150 páginas en top 3 apenas separó las posiciones 1–3, mientras que las páginas con ≥15 puntos de datos únicos promediaban 62 frente a 40 de las que tenían 0–1. Puntuar la posición aquí convertiría una señal buena y ya conocida en una etiqueta llamada «information gain».
2. **El conteo es determinista; el juicio de significado no.** «¿Este número informa o es relleno?» es un juicio sobre el significado. La skill lo reporta como juicio, nunca como medición, e incluye un bloque de advertencia obligatorio que debe reproducirse sin editar.

---

## Instalación

Funciona con el CLI `skills` (Vercel Labs) en ~75 hosts de agentes.

```bash
# Auto-detect installed agents
npx skills add Pautthead/seo-aeo-agent-skills

# Explicit host list (recommended: Claude Code needs to be named explicitly,
# otherwise the installer may write only to .agents/skills/, which Claude Code
# does not read)
npx skills add Pautthead/seo-aeo-agent-skills -a claude-code -a opencode -a codex -a hermes-agent
```

Marketplace de plugins para Claude Code:

```
/plugin marketplace add Pautthead/seo-aeo-agent-skills
/plugin install seo-aeo@seo-aeo-agent-skills
```

O copia `skills/<nombre>/` a mano en el directorio de tu host:

| Host | Ruta de proyecto | Ruta global |
|---|---|---|
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| OpenCode | `.agents/skills/` | `~/.config/opencode/skills/` |
| Codex | `.agents/skills/` | `~/.agents/skills/` |
| Cursor | `.agents/skills/` | `~/.cursor/skills/` |
| Hermes Agent | `.hermes/skills/` | `~/.hermes/skills/` |
| OpenClaw | `skills/` | `~/.openclaw/skills/` |
| Gemini CLI | `.agents/skills/` | `~/.gemini/skills/` |
| Cline | `.agents/skills/` | `~/.agents/skills/` |

`.agents/skills/` es la ubicación de proyecto portátil de facto. OpenCode además lee `.opencode/skills/`, `.claude/skills/` y `.agents/skills/`, subiendo desde el directorio actual hasta la raíz del worktree.

Tras instalar, pregunta al agente por nombre o por descripción — el frontmatter `description` lleva las palabras clave de activación para que pueda autoseleccionarse. `AGENTS.md` es el punto de entrada que la mayoría de hosts carga automáticamente.

---

## Lo que estas skills se niegan a hacer

Esta es la sección que debes revisar si estás aquí para evaluarnos.

### `llms.txt` no es una palanca de tráfico ni de citas

Seis mediciones independientes de 2026. Todas negativas o nulas.

| Estudio | Fecha | N | Resultado |
|---|---|---|---|
| [Ahrefs](https://ahrefs.com/blog/llmstxt-study/) | 2026-06-15 | 137.210 dominios | El 28% tiene uno; **el 97% no recibió ninguna petición**; **cero peticiones de bots de IA para archivos que no existen: nunca van a buscarlos** |
| [SE Ranking](https://seranking.com/blog/llms-txt/) | 2026-10-15 | ~300.000 dominios | 10,13% de adopción; su modelo mejoró **más** al quitar la variable — *«LLMs.txt might currently introduce more noise than value»* |
| [Otterly.AI](https://otterly.ai/blog/llms-txt/) | 2026-02-05 | 62.100 visitas de bots de IA / 90d | 0,1% de visitas a `/llms.txt`; sin correlación positiva con la actividad de rastreo por IA |
| [Search Engine Land](https://searchengineland.com/llms-txt/) | 2026-01-20 | 10 sitios, antes/después | 8 sin cambios; los sitios que publican **contenido funcional nuevo** ganaron, los que solo documentaban contenido existente no ganaron nada |
| CueScout | 2026-10-15 | 537 sitios SaaS, 80 respuestas de AI Mode | 24,3% citados *con* él frente a 21,8% *sin* él (p=0,53, no significativo); **ninguno de los 708 enlaces citados apuntaba a un archivo llms.txt** |
| Log del servidor de origen | 15 días | 345.808 peticiones | **Cero** peticiones a `/llms.txt` de ninguno de los 22 tokens de crawler; robots.txt recibió 2.135, sitemap.xml 282 |

Google, de forma oficial — Danny Sullivan, [Search Central Live Toronto, 2026-04](https://developers.google.com/search/blog): *«There is no benefit to creating a llms.txt file for SEO.»* Shepard lo puntúa con **2,0/10 — el más bajo de 23 factores**.

**El único matiz que merece desplegarse, presentado como descubrimiento y no como adopción:** los crawlers *sí* descargan un llms.txt que se anuncia en `robots.txt` vía `Sitemap:` ([Nathan Hall, Zenodo, 2026-09-17](https://doi.org/10.5281/zenodo.22814843)) — 1.549 descargas en 165 días-sitio, frente a cero peticiones para diez archivos hermanos sin referenciar a lo largo de 60 meses-archivo. La advertencia del propio autor es la lectura correcta: *«Tell a crawler where a file is and it fetches the file. That is discovery, not adoption.»* Una descarga no es una cita.

**Lo que hacemos en su lugar:** espejos en markdown. Con un índice llms.txt más espejos `.md` presentes, el coste de ingestión del agente bajó a ~123K tokens / ~10 llamadas a herramientas frente a ~240K tokens / ~20 sin ellos ([investigación de a14y, 2026](https://a14y.dev/research/llms-txt-linking/)). La calidad de la respuesta quedó igual. *«The cost is ingestion, not generation.»* Y fíjate en lo que *no* funcionó ahí: se probaron cinco formatos de enlace y **los cinco obtuvo 0/5 de adopción**. Lo único que movió la aguja fue una línea en el prompt. Presupuesta cero contra `llms.txt`; si lo despliegas, hazlo en una hora y anúncialo.

### FAQPage schema no es una táctica GEO

Shepard puntúa los datos estructurados con 5,6/10 y señala que *«LLMs don't typically ingest schema as part of their training»* y que hay *«limited evidence they can at least see schema when searching»*. Google dejó de mostrar resultados enriquecidos de FAQ para la mayoría de sitios hace tiempo (`r/AskMarketing`, 2026-09-29). Varias skills de 2026 siguen recomendando automáticamente añadir FAQPage. El schema merece la pena por rich results y por claridad de entidad, no por GEO.

### Nada de publicación automatizada en Reddit ni en ningún foro

Reddit empezó a etiquetar cuentas legítimas de bots (2026-03) y reportó detectar **25.000 posts spameados al día** (2026-07) explícitamente para impedir que *«brands from planting posts meant to get them recommended by ChatGPT and Gemini»*, y **baneó 4 subreddits** usados en un experimento GEO que automatizaba votos y comentarios. **Mide Reddit. Nunca publiques en él.**

### Ninguna promesa de visibilidad en IA en menos de 60 días

Los cambios on-page se mueven en semanas. Los cambios en citas tardan 4–12 semanas; el test de campo que encontramos sitúa la primera subida de citas en **60–120 días** (ProCloser, 2026-05-27, n=5; el propio autor señala que la muestra es estadísticamente insuficiente). Todos los informes de este repositorio llevan ese horizonte en la salida. Si alguien te promete 60 días, te está vendiendo un calendario, no un método.

### Ninguna afirmación de que el GEO es una disciplina aparte

**El 80 por ciento del GEO es buen SEO fundamental.** Si un servicio de GEO no te dice abiertamente que el éxito en visibilidad de IA es un 80% buen SEO fundamental, te están vendiendo aceite de serpiente. — Jeremy Moser (uSERP), vía Digiday, 2026-03-10

Lily Ray documenta el corolario: una marca con autoridad consolidada aparece en ChatGPT y concluye que su campaña GEO funciona, cuando la explicación más plausible es que su visibilidad SEO existente la metió en los índices que alimentan esos productos. También encontró un caso de estudio de un proveedor donde el tráfico orgánico **cayó un 66%** mientras la «visibilidad en IA» subía.

### Y lo que importa más que todo lo anterior

**No produzcas un hallazgo que la técnica no puede detectar.** Si un check es N/A — idioma no soportado, campo ausente, fuente inaccesible — repórtalo como *no puntuado*. Nunca como aprobado, nunca como fallido. Un aprobado falso es lo que destruye la confianza en una auditoría. Si no has podido descargar una página, dilo. `web_fetch` y `curl` eliminan las etiquetas `<script>`, así que informar «no se encontraron datos estructurados» sobre una página descargada es un hallazgo falso, no un resultado limpio.

---

## Datos de pago opcionales — DataForSEO

**Nada en este repositorio requiere nada de esto.** Las cuatro skills se completan sin credenciales. Esta sección existe porque una carencia — datos de posición en SERP para los dos factores mejor puntuados — no tiene equivalente gratuito, y porque los precios aquí tienen una trampa que conviene conocer.

DataForSEO es un proveedor de pago que usamos y del que podemos obtener una comisión de afiliado. Aparece aquí porque es el conjunto de datos SERP/keywords más barato que encontramos, no porque sea necesario.

| Endpoint | Precio | Notas |
|---|---|---|
| `dataforseo_labs/google/*/live` | **$0,012/tarea + $0,00012/item** | Por defecto. Solo live, sin cola. Máx. 700 keywords/tarea, 1.000 items/respuesta, 2.000 llamadas/min, 30 concurrentes |
| `historical_rank_overview/live` | $0,12/tarea + $0,0012/item | Habilita posición en búsqueda (9,4) y fan-out rank (9,3) en la auditoría de citabilidad |
| `historical_serps/live` | $0,00012/SERP | |
| `search_intent/live` | $0,012/tarea + $0,00012/keyword | |
| SERP API (tarifa publicada) | **$2,00 / 1k live** · $1,20 / 1k priority · $0,60 / 1k standard | Mira la trampa de abajo |

> **Trampa de precios.** La tarifa de titular de **$0,60/1k** es la cola *standard*, que tarda unos **5 minutos**. Para un agente interactivo no es un producto equivalente, así que **$2,00/1k live es la comparación honesta**. En todas partes citamos $2,00.

**La base de datos se refresca cada 30–90 días.** Nunca presentes la salida de Labs como tiempo real. Su `newest_data_date` no está en el payload; usa la ventana de refresco declarada por el proveedor y etiquétala como `provider_refresh_window`.

**Servidor MCP oficial — el servidor es gratis, pagas las tarifas de API:**

- Remoto: `https://mcp.dataforseo.com/v3/mcp` con `Authorization: Basic base64(login:password)`
- Local: `npx -y dataforseo-mcp-server` con `DATAFORSEO_USERNAME` / `DATAFORSEO_PASSWORD`
- Código: `github.com/dataforseo/mcp-server-typescript`

**Aviso de autenticación:** solo HTTP Basic, y las credenciales vienen del login de **API** en `app.dataforseo.com/api-access`. Usar el login del panel es el fallo de autenticación más habitual.

**Para empezar:** $1 de crédito de prueba, mínimo $50 de recarga. Prueba DataForSEO: https://try.dataforseo.com/jijqq4kuyyde (enlace de afiliado)

---

## Cómo funciona la puntuación

Cuatro reglas, aplicadas a todas las skills:

1. **Análisis determinista, reescritura por LLM.** Los marcadores, listas de comprobación y parsers son reglas reproducibles que el agente aplica, no juicios improvisados. El riesgo de alucinación pertenece a la capa que produce prosa, no a la que produce números.
2. **Cada umbral numérico se remonta a una fuente fechada.** O cita `METHODOLOGY-BRIEF §1`, o se etiqueta explícitamente como decisión de criterio. La tabla `chars/token` de la skill de citabilidad está etiquetada como decisión de criterio. El 9,5 de Shepard para accesibilidad de URL es una medición. Ambas cosas dicen cuál son.
3. **Las afirmaciones de proveedor se etiquetan como afirmaciones de proveedor.** `Fuente: Ahrefs, 2026-06-15, n=137.210 dominios — medido` frente a `Fuente: afirmación de proveedor, sin verificar`. Un número de marketing nunca se disfraza de hecho.
4. **Documenta tus propios límites, y en serio.** Cada skill incluye una sección `Known limitations` que se copia literalmente en el informe. `information-gain-analysis` dice sin rodeos que Google no ha confirmado ningún requisito de information gain, e incluye el disenso de la comunidad junto al mecanismo.

La regla de honestidad se aplica en la práctica: **durante la validación se encontró y se eliminó una cita fabricada.** Una estadística atribuida a un informe de comunidad concreto en una fecha concreta, sin nada detrás. Queda registrada en `docs/METHODOLOGY-BRIEF.md` §1.9c para que el siguiente colaborador no la reintroduzca. Por el mismo motivo se retiraron dos citas no verificables.

---

## Hoja de ruta

Son huecos reales, no un backlog inventado. Provienen de una revisión del mercado actual y están documentados en `docs/METHODOLOGY-BRIEF.md` §5. **Ninguno está en la v1.**

| Previsto | Por qué es un hueco real |
|---|---|
| **Validador de schema JSON-LD** contra rich results | Muchas skills generan datos estructurados. Casi ninguna los valida. |
| **Mapeador del grafo de enlaces internos** | *«Plenty of skills mention it, none actually map a link graph»*. Directamente relevante para el fallo de 150 sugerencias y 20 utilizables. |
| **Análisis de keyword gap** | La cobertura competitiva hoy exige una exportación de pago. |
| **Coincidencia de intención / tipo de página de SERP** | Factor n.º 6 de Shepard (9,0). La auditoría de citabilidad lo aproxima; nada lo puntúa bien. |
| **Triaje de decay de contenido** | Distingue caída de tráfico, caída de posición y obsolescencia. Requiere GSC. |
| **Tracker de experimentos GEO** | Una variable, 7–21 días, tres motores. El mercado no tiene ninguna herramienta que resista la tentación de cambiar cinco cosas. |
| **SEO drift como GitHub Action, puerta previa al merge** | El fallo de datos obsoletos detectado antes del merge en lugar de después de una revisión trimestral. |
| **SEO específico por framework** para Next.js, Astro, Nuxt | El render y los metadatos difieren lo bastante como para que el consejo genérico sea erróneo. |
| **Multi-sitio / soporte de agencia** | Comparar una cartera contra su propia línea base en lugar de cada sitio por separado. |

---

## Dónde encaja esto

Contexto honesto, no un ataque competitivo. Varios de estos repositorios son buenos, y algunos son mejores que este en amplitud.

| Repo | ★ | Lo que hace bien | Notas |
|---|---|---|---|
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | 35k | El instalador `npx skills` por el que se distribuye este repositorio | Infraestructura, no SEO |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 55k | Amplitud en marketing; el único repo del mercado que documenta sus propias limitaciones —práctica tomada de aquí | Su propio aviso sobre instalar en `.agents/skills/` merece tenerse en cuenta |
| [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo) | 19k | Superficie SEO muy completa para Claude Code | 16 archivos referencian herramientas MCP v3 de DataForSEO que ya no existen (#319); roto en una instalación limpia (#180) |
| [zubair-trabzada/geo-seo-claude](https://github.com/zubair-trabzada/geo-seo-claude) | 11k | Lo más parecido a un conjunto de skills GEO dedicado | Las expresiones regulares de `citability_scorer` son solo en inglés (#80); el paso de `robots` pide herramientas que no pueden devolver los datos (#81) |
| [TheCraigHewitt/seomachine](https://github.com/TheCraigHewitt/seomachine) | 7,5k | Amplia cobertura de SEO técnico | Solo Claude Code |
| [Ryze-AI-Adgent/open-seo-mcp-skills](https://github.com/Ryze-AI-Adgent/open-seo-mcp-skills) | 6k | Datos en vivo vía MCP de serie | MCP-first significa que la vía sin claves no es la línea base |
| [nowork-studio/notfair-plugin](https://github.com/nowork-studio/notfair-plugin) | 4k | Auditorías opinadas y decididas | Ser opinado es una ventaja hasta que se topa con una página donde la opinión es incorrecta |
| [seranking/seo-skills](https://github.com/seranking/seo-skills) | — | Skills individuales limpias y bien delimitadas | Depende del proveedor y de una suscripción de SE Ranking; desactualizado en el momento de escribir esto |
| [inhouseseo/superseo-skills](https://github.com/inhouseseo/superseo-skills) | — | Énfasis en datos estructurados | |

Tres patrones en el sector: casi todos son **solo para Claude Code**, casi todos necesitan una **suscripción de pago** para datos en vivo, y ninguno documenta sus propios límites como lo hace este. Donde ellos son más fuertes —amplitud, datos SERP en vivo, cobertura de frameworks— la hoja de ruta de arriba es la respuesta.

---

## Cómo contribuir

Lee [`AGENTS.md`](AGENTS.md) primero; lo cargan Codex, OpenCode, Cline, Gemini CLI, Cursor, OpenClaw y Hermes. Después lee [`docs/METHODOLOGY-BRIEF.md`](docs/METHODOLOGY-BRIEF.md), que es la fuente de verdad interna sobre anatomía de las skills, invariantes de portabilidad y la lista de cosas que este repositorio nunca debe hacer.

**Añadir una skill:**

1. `skills/<nombre>/SKILL.md` más `references/`. Nada anidado más profundo.
2. El frontmatter lleva **solo** `name`, `description`, `license`, `compatibility` y `metadata` (exactamente cuatro claves string: `repo`, `version`, `updated`, `keys-required`). `name` debe ser igual al nombre del directorio, en kebab-case minúsculas.
3. `description` adelanta qué hace, cuándo usarla y sus palabras clave de activación — Codex presupuesta la lista completa de skills en 8.000 caracteres y trunca las descripciones antes que nada.
4. Orden del cuerpo: propósito · cuándo usarla / cuándo no · inputs (primero la vía sin claves) · procedimiento con una comprobación ejecutable y un aprobado falsable por paso · formato de salida · puntuación · limitaciones conocidas · fuentes de datos opcionales · referencias.
5. Los enlaces a archivos hermanos son `references/ARCHIVO.md`, un solo nivel, siempre — y tienen que resolver.
6. Nada de `context: fork`, nada de hooks en el núcleo. Ambos son exclusivos de Claude Code y romperían la portabilidad.
7. **Cero claves de API obligatorias.** Si no puede completarse sin una cuenta de pago, no está lista.

**Puertas de validación — ejecuta esto antes de abrir una PR:**

```bash
python tests/validate_skill_inventory.py
python tests/reference_freshness.py --max-age-days 90
```

Ambas se ejecutan en CI en cada push. La primera comprueba que cada skill declarada existe, que el inventario coincide y que el frontmatter es conforme. La segunda falla cualquier documento de referencia cuya evidencia haya superado el umbral.

**La regla de citación.** Cada umbral numérico debe remontarse a una fuente fechada con un nivel de evidencia declarado. **Verifica que la fuente diga realmente lo que afirmas antes de citarla**: leer el texto primario es el mínimo, y si no puedes verificarlo, no lo cites. Una afirmación que no se puede verificar de forma independiente se elimina, no se suaviza.

---

## Licencia

Apache-2.0. Úsala, haz un fork, incorpórala a tu propia herramienta interna de auditoría.

## Créditos y fuentes

Creado por [Pautthead](https://github.com/Pautthead). Cada afirmación de estas skills se remonta a una de las siguientes fuentes primarias; la tabla completa de evidencia con fechas y tamaños de muestra está en [`docs/METHODOLOGY-BRIEF.md`](docs/METHODOLOGY-BRIEF.md).

**Medición y fuentes primarias**

- [Cyrus Shepard / Zyppy — The 23 AI Citation Ranking Factors](https://signal.zyppy.com/p/ai-citation-ranking-factors) (2026-05-07, 54 experimentos) — accesibilidad 9,5, posición en búsqueda 9,4, llms.txt 2,0
- [Ahrefs — estudio de llms.txt](https://ahrefs.com/blog/llmstxt-study/) (2026-06-15, n=137.210 dominios)
- [Ahrefs — Information gain](https://ahrefs.com/blog/information-gain/), Louise Linehan (2026-08-20)
- [Google — Patente US11354342B2](https://patents.google.com/patent/US11354342B2/en) — composición de respuestas y poda de hechos
- [arXiv 2605.25517](https://arxiv.org/html/2605.25517) (2026-05-25) — experimento GEO controlado, 252.000 trials, 6 LLMs
- [Nathan Hall, Zenodo, 2026-09-17](https://doi.org/10.5281/zenodo.22814843) — comportamiento de crawlers con anuncio `Sitemap:` en robots.txt
- [a14y.dev — investigación sobre enlaces a llms.txt](https://a14y.dev/research/llms-txt-linking/) (2026) — espejos en markdown y coste de ingestión
- [arsentev.ai — Crawlers and llms.txt](https://arsentev.ai/research/crawlers-and-llms-txt.pdf) — estudio de logs de origen de 15 días
- [Sitefire / arXiv 2609.15369](https://github.com/pulse-energy-eu/slopshape) — detección estructural de contenido generado por IA
- [Search Engine Land](https://searchengineland.com/llms-txt/) (2026-01-20) · [Otterly.AI](https://otterly.ai/blog/llms-txt/) (2026-02-05) · SE Ranking (2026-10-15) · CueScout (2026-10-15)
- Muck Rack (+25M de enlaces citados) · GeoTest (2026-06) · On-Page.ai (150 páginas top-3) · Indig H1 2026 vía [Search Engine Journal](https://www.searchenginejournal.com/) · test de campo de ProCloser (2026-05-27, n=5, subdimensionado)

**Profesionales citados**

Jeremy Moser (uSERP) vía Digiday (2026-03-10) · Lily Ray, [*The AI Slop Loop*](https://lilyraynyc.substack.com/p/the-ai-slop-loop) (2026-04-14) · Louise Linehan (Ahrefs) · Bernard Huang (ex-Clearscope) · Barry Schwartz · Danny Sullivan y Gary Illyes (Search Central Live, 2026) · `r/AiAutomations`, `r/SEO_Xpert`, `r/SideProject`, `r/SEO`, `r/DigitalMarketing`, `r/AskMarketing`, `r/bigseo`

**Distribución:** el CLI `skills` de Vercel Labs, verificado contra la [especificación de Agent Skills](https://agentskills.io/specification) y no contra blogs: varias guías de instalación de 2026 publican rutas que no existen.

---

*Si una afirmación de este repositorio no se remonta a una fuente fechada, es un bug. Por favor, abre un issue.*