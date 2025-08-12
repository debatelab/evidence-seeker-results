# Grundidee der EvidenceSeeker DemoApp

Die EvidenceSeeker Demoapp illustriert, wie man mit Hilfe der [*EvidenceSeeker Boilerplate*](https://debatelab.github.io/evidence-seeker) KI Fact-Checking Tools aufsetzen kann, die prüfen, in welchem Grad eine beliebige Aussage über eine gegebene Wissensbasis gestützt oder widerlegt wird.

## Einsatz von generativer KI

Die **EvidenceSeeker Pipeline** verwendet generative Sprachmodelle und geht bei der Prüfung einer Aussage in folgenden Schritten vor: 

1. **Voranalyse:** Die Pipeline findet in einem ersten Schritt
unterschiedliche Interpretationen der Eingabe und unterscheidet 
dabei *deskriptive, zuschreibende und normative Aussagen*. 
2. **Extraktion:** Für die gefundenen deskriptiven und zuschreibenden Interpretationen wird dann in einer *Wissensbasis* nach relevanten Textstellen gesucht und analysiert, inwiefern 
die Textstellen die gefundene Interpretation bestätigen oder widerlegen.
3. **Evidenzanalyse:** Diese Einzelanalysen werden für jede Interpretation in Form eines
*Bestätigungslevels* von insgesamt 7 aggregiert:
    + 'im hohen Maße bestätigt', 
    + 'bestätigt',
    + 'im geringen Maße bestätigt',
    + 'weder bestätigt noch widerlegt',
    + 'im niedrigen Maße widerlegt',
    + 'widerlegt', und 
    + 'im hohen Maße widerlegt'. 

Nähere Informationen
zur Pipeline findest Du [hier](https://debatelab.github.io/evidence-seeker/workflow.html).


**Verwendete Modelle und Wissensbasis:** 

+ In dieser Demo App verwenden wir:
    + [Kimi-K2-Instruct](https://huggingface.co/moonshotai/Kimi-K2-Instruct) als generatives Sprachmodell für die Voranalyse,
    + [paraphrase-multilingual-mpnet-base-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2) als Embedding Modell für die Extraktion und
    + [Llama-3.3-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct) als generatives Sprachmodell für die Evidenzanalyse.
+ Als Wissensbasis dienen
alle Ausgaben von *"Aus Politik und Zeitgeschichte" (APuZ)* aus dem Jahr 2024
([Link](https://www.bpb.de/shop/zeitschriften/apuz/?field_filter_thema=all&field_date_content=2024&d=1)). *APuZ* wird von der Bundeszentrale für politische Bildung herausgegeben.


## Hintergrund des EvidenceSeeker Projekts

Die EvidenceSeeker-Pipeline wurde im Rahmen des [KIdeKu-Projekts](https://compphil2mmae.github.io/research/kideku/) 
am Karlsruher Institut für Technologie entwickelt. 
KIdeKu wird gefördert vom [BMBFSFJ](https://www.bmbfsfj.bund.de/).

Nähere Informationen zur *EvidenceSeeker Boilerplate* findest Du
[hier](https://debatelab.github.io/evidence-seeker).


*[deskriptiv]: Deskriptive Aussagen sind beschreibende wertfreie Aussagen, die typischerweise Sachverhalte zum Ausdruck bringen sollen.
*[deskriptive]: Deskriptive Aussagen sind beschreibende wertfreie Aussagen, die typischerweise Sachverhalte zum Ausdruck bringen sollen.
*[normativ]: Normative Aussagen sind Aussagen, die Werturteile, Empfehlungen oder Vorschriften enthalten. Unsere EvidenceSeeker-Pipeline erkennt normative Aussagen, aber prüft sie nicht weiter.
*[normative]: Normative Aussagen sind Aussagen, die Werturteile, Empfehlungen oder Vorschriften enthalten. Unsere EvidenceSeeker-Pipeline erkennt normative Aussagen, aber prüft sie nicht weiter.
*[zuschreibend]: Zuschreibende Aussagen sind Aussagen darüber, was eine Person oder Gruppe von Personen bspw. denkt, fühlt oder sagt. Zugeschrieben werden hier also Einstellungen und Handlungen bzgl. bestimmter Aussagen (wie bspw. Überzeugungen).
*[zuschreibende]: Zuschreibende Aussagen sind Aussagen darüber, was eine Person oder Gruppe von Personen bspw. denkt, fühlt oder sagt. Zugeschrieben werden hier also Einstellungen und Handlungen bzgl. bestimmter Aussagen (wie bspw. Überzeugungen).
*[Bestätigungslevel]: Der EvidenceSeeker weist jeder gefundenen Interpretation ein von 7 Bestätigungsleveln durch die Wissensbasis zu: 'im hohen Maße bestätigt', 'bestätigt', 'im geringen Maße bestätigt', 'weder bestätigt noch widerlegt', 'im niedrigen Maße widerlegt', 'widerlegt' und 'im hohen Maße widerlegt'. 