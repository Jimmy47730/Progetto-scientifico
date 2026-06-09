# Studio di un fascio sonoro parallelo attraverso metamateriali acustici

**Autori:** Matteo Forni, Rocco Napoli, Giorgio Bolognini, Matthieu Louis

---

## Abstract

Questo paper descrive lo sviluppo di un sistema per la generazione e l'analisi di un fascio di onde sonore parallelo destinato allo studio di metamateriali acustici. La generazione del fascio è composta da un modello matematico basato su un profilo simile alla lente di Fresnel. Per l'analisi del fascio è invece formata da un sistema di acquisizione a doppio microfono e strumenti software di analisi audio supportano la validazione sperimentale del comportamento del fascio. I risultati non sono ancora presenti, ma il paper è già strutturato per inserirli in futuro.

---

## 1. Introduzione

Questo progetto nasce da un nostro interesse condiviso per tecnologia, fisica e acustica. Dopo varie sessioni di brainstorming, abbiamo deciso di studiare in particolare il funzionamento dei metamateriali e la loro influenza sulle onde sonore.
Ci siamo poi accorti però che, da un punto di vista sperimentale, utilizzare onde sferiche avrebbe compromesso i nostri dati, in quanto parte della perdita di intensità del suono sarebbe dovuta dall'aumento della distanza dalla fonte. Per risolvere questo problema, ci serviva un fascio di onde piane. Queste sono facilmente ottenibili tramite un'antenna parabolica, dove l'emettitore delle onde sonore è situato al fuoco della parabola.
Di nuovo, abbiamo realizzato che un'antenna parabolica sarebbe stata troppo grande per il nostro prototipo, e abbiamo cercato una soluzione. Alla fine, abbiamo deciso di frammentare la superficie della parabola, creando uno specchio a parabole concentriche con stesso fuoco. Questa idea è basata sulla famosa lente di Fresnel. 

## 2. Obiettivi

Gli obiettivi del lavoro sono:

- definire un modello matematico per la generazione di un fascio sonoro parallelo mediante uno specchio di Fresnel;
- realizzare un prototipo fisico compatto e stampabile in 3D;
- progettare e implementare un sistema di acquisizione sperimentale a doppio microfono per valutare uniformità e direzionalità del fascio;
- predisporre strumenti software che supportino l'analisi comparativa dei segnali audio acquisiti.

## 3. Contesto teorico

Le superfici paraboliche riflettono onde incidenti parallele verso un punto focale; invertendo il processo, è possibile progettare una superficie in grado di convertire un'emissione puntiforme in un fascio parallelo. Lo specchio di Fresnel è una versione segmentata di una parabola, in cui ciascuna zona è riallineata per mantenere la stessa condizione di fuoco, riducendo lo spessore complessivo rispetto a una parabola continua.

I metamateriali acustici sono materiali strutturati con proprietà effective che non si trovano facilmente in natura. Nel campo acustico, le strutture periodiche e le cavità risonanti possono modificare l'impedenza, la velocità di fase e il coefficiente di riflessione delle onde sonore. Lo studio di un fascio parallelo fornisce un opportuno banco di prova per misurare l'interazione tra onde direzionate e strutture acustiche complesse.

## 4. Metodologia

### 4.1 Modellazione matematica

Il modello matematico parte da una funzione parametrica che descrive un profilo parabolico sul piano cartesiano. La sezione della parabola è trasformata in una successione di segmenti di Fresnel mediante traslazioni longitudinali, mantenendo costante la distanza focale per ogni sezione.

Si assume che la superficie riflettente sia altamente rigida e che l'incidenza del suono sia vicino all'asse principale, in modo da applicare l'approssimazione geometrica della riflessione. Il profilo finale è descritto da una funzione discreta delle altezze delle zone di Fresnel, ciascuna calcolata per rispettare la condizione di fase.

### 4.2 Prototipazione 3D

Il profilo matematico è stato convertito in un modello fisico generabile tramite stampa 3D. Il prototipo è costituito da un insieme di sezioni concentriche che riproducono il profilo di Fresnel ridotto.

La scelta dei materiali punta su plastiche rigide adatte a mantenere la forma durante l'uso sperimentale. Il progetto è stato sviluppato per essere compatto e facilmente stampabile, con geometrie adatte all'uso in un laboratorio scolastico.

### 4.3 Sistema di misura

Per verificare le proprietà del fascio parallelo è stato impiegato un sistema a doppio microfono. Il pacchetto software `Audio Comparator` fornisce le funzionalità fondamentali per l'acquisizione contemporanea dei due canali, il calcolo dei valori RMS e la trasformata di Fourier delle tracce.

Il sistema sperimentale consente di confrontare il segnale acquisito vicino alla linea d'asse del fascio con un segnale di riferimento, evidenziando variazioni di ampiezza e frequenza. Questa comparazione è essenziale per giudicare l'uniformità e la direzionalità del fascio generato.

### 4.4 Strumenti software

Oltre al confronto audio, il progetto prevede lo sviluppo di un tool denominato `ZeroMirror Creator`, destinato a generare profili geometrici e file STL a partire dai parametri del fascio e dalle specifiche dimensionali.

## 5. Risultati

Questa sezione è predisposta per l'inserimento futuro dei risultati sperimentali completi.

### 5.1 Misure di uniformità del fascio

- Tabella 1: Parametri sperimentali del fascio parallelo e valori rilevati.
- Figura 1: Distribuzione dell'ampiezza lungo l'asse centrale.

### 5.2 Comparazione tra canali microfonici

- Tabella 2: Confronto RMS e frequenza dominante tra i due microfoni.
- Figura 2: Spettro FFT dei segnali registrati.

### 5.3 Interazione con metamateriali acustici

- Tabella 3: Variazione del coefficiente di trasmissione e riflessione in presenza di metamateriali.
- Figura 3: Diagramma dell'attenuazione e del cambio di fase.

> I dati specifici saranno inseriti qui quando saranno disponibili i risultati delle misure e dei test sperimentali.

## 6. Discussione

In base al modello matematico e alla soluzione prototipale descritta, ci attendiamo i seguenti comportamenti ipotetici:

- il fascio generato dallo specchio di Fresnel dovrebbe mostrare una distribuzione di intensità longitudinalmente uniforme, con minori variazioni rispetto a una sorgente non collimata;
- la comparazione tra i due microfoni dovrebbe evidenziare una preservazione della frequenza dominante, mentre le differenze di ampiezza possono riflettere la qualità del collimamento e le perdite introdotte dalla struttura;
- l'interazione con metamateriali acustici dovrebbe essere caratterizzata da una variazione misurabile nell'attenuazione e nella fase, confermando le proprietà effective del materiale.

Se i risultati sperimentali dovessero mostrare una buona compatibilità con il modello, ciò sosterrà l'ipotesi che un profilo di Fresnel acustico sia un metodo efficace per generare un fascio parallelo in un dispositivo compatto. In presenza di discrepanze, le cause probabili includono imperfezioni nella stampa 3D, disallineamento del sistema microfonico o effetti diffrattivi non trascurabili.

### 6.1 Interpretazione ipotetica dei dati

- Uniformità del fascio: valori di RMS costanti lungo la direzione del fascio suggellerebbero un comportamento vicino al modello ideale.
- Direzionalità: un angolo di divergenza contenuto supporterebbe l'efficacia del design.
- Effetto dei metamateriali: le misure di attenuazione differenziale e i picchi di risonanza potrebbero indicare l'azione filtrante delle strutture acustiche studiate.

### 6.2 Implicazioni e limiti

Il metodo proposto potrebbe essere applicato a esperimenti didattici e a prototipi di dispositivi acustici direzionali. Un limite importante è che il modello assume condizioni ideali di riflessione e non considera completamente le perdite viscose/termiche e la dispersione tipica dei materiali plastici.

## 7. Conclusioni

Questo lavoro descrive un approccio integrato alla generazione di un fascio sonoro parallelo basato su un profilo di Fresnel e su una catena sperimentale a doppio microfono. La combinazione di modellazione matematica, prototipazione 3D e strumenti software mira a creare un ambiente riproducibile per lo studio dei metamateriali acustici.

Il paper lascia spazio all'inserimento futuro dei risultati sperimentali, mentre la discussione offre una visione critica e ipotetica delle prestazioni attese. Il progetto può essere ampliato con misure più precise, l'ottimizzazione del profilo e l'integrazione di nuove tipologie di metamateriali.


---

## Appendice A: Strumenti software sviluppati

- `audio_comparator`: pacchetto Python per l'acquisizione e l'analisi comparativa di due canali microfonici.
- `ZeroMirror Creator`: tool per la generazione di geometrie acustiche basate su profili di Fresnel e file STL per la stampa 3D.
- `Sito ZeroMirror`: la repository del sito ZeroMirror (attualmente privo di dominio) si può trovare al seguente link: https://github.com/Jimmy47730/Progetto-scientifico
