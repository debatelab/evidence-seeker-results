# Ergebnisse der EvidenceSeeker-DemoApp

Die EvidenceSeeker-Pipeline ist ein RAG-basierter LLM-Workflow für das 
Fact-Checking beliebiger Aussagen relativ zu einer gegebenen Datenbasis. 
Die EvidenceSeeker-Pipeline wurde im Rahmen des [KIdeKu-Projekts](https://compphil2mmae.github.io/research/kideku/) 
am Karlsruher Institut für Technologie entwickelt. 
KIdeKu wird gefördert vom [BMBFSFJ](https://www.bmbfsfj.bund.de/).

Diese Webseite sammelt Ergebnisse der Pipeline, die durch Nutzer*inneninteraktion 
über eine DemoApp erstellt wurden. Die der DemoApp zugrundeliegende Datenbasis 
verwendet die Artikel des Jahrgangs 2024 der Zeitschrift 
"Aus Politik und Zeitgeschichte" ([APuZ](https://www.bpb.de/shop/zeitschriften/apuz/)), 
die von der Bundeszentrale für politische Bildung herausgegeben wird.

[:simple-huggingface: DemoApp jetzt selbst ausprobieren](https://huggingface.co/spaces/DebateLabKIT/evidence-seeker-demo){ .md-button .md-button--primary }
### Beispiele

!!! warning "Inhaltswarnung"

    Die folgenden Beispiele enthalten Nutzer\*inneneingaben, die auf ihre Inhalte von den Ersteller\*innen dieser Seite nicht geprüft wurden 
    und möglicherweise sensible oder für manche Personen beunruhigende Inhalte haben können. 
    Die beinhalteten Aussagen und ihre Bewertung durch die Pipeline geben nicht die Meinung der Ersteller\*innen dieser Seite wieder.

<div class="grid cards" markdown>


-   :fontawesome-solid-quote-right:  _Populismus bedroht Demokratien._
    
    
    ---

    Analysiert als

    - 1 zuschreibende,
    - 3 normative
    - und 3 deskriptive Aussagen
    

    ---
    
    :material-dots-circle:{ .lg .top } <font color="grey" size=size=2em>2025-08-08 19:23:06 UTC</font>
    

    [:octicons-arrow-right-24: Details](results/result_677e1e34-a850-41d4-bf90-4ff5ffc9f010.md)


-   :fontawesome-solid-quote-right:  _Populismus bedroht Demokratien._
    
    
    ---

    Analysiert als

    - 3 zuschreibende,
    - 3 normative
    - und 1 deskriptive Aussagen
    

    ---
    
    :material-dots-circle:{ .lg .top } <font color="grey" size=size=2em>2025-08-08 19:28:47 UTC</font>
    

    [:octicons-arrow-right-24: Details](results/result_56ccd501-c10e-458a-a1ba-7cdb4386bce7.md)


</div>

*[deskriptive]: Deskriptive Aussagen sind beschreibende wertfreie Aussagen, die typischerweise Sachverhalte zum Ausdruck bringen sollen.
*[normative]: Normative Aussagen sind Aussagen, die Werturteile, Empfehlungen oder Vorschriften enthalten. Unsere EvidenceSeeker-Pipeline erkennt normative Aussagen, aber prüft sie nicht weiter.
*[zuschreibende]: Zuschreibende Aussagen sind Aussagen darüber, was eine Person oder Gruppe von Personen bspw. denkt, fühlt oder sagt. Zugeschrieben werden hier also Einstellungen und Handlungen bzgl. bestimmter Aussagen (wie bspw. Überzeugungen).