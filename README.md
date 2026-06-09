# ZeroMirror

Questo repository contiene il sito web, gli strumenti software e la documentazione per un progetto scientifico di maturità dedicato allo studio di un fascio di onde sonore parallelo che attraversa metamateriali acustici.

## Contenuti principali
- `app.py`: server FastAPI principale del sito.
- `routes/main.py`: gestione delle pagine web e dei template Jinja2.
- `static/html/`: pagine del sito di presentazione del progetto.
- `audio_comparator/`: package Python per l'acquisizione e il confronto di due canali microfonici.
- `Scientific_Paper_ZeroMirror.md`: paper scientifico in formato Markdown basato sul progetto.

## Strumenti e tool
- `audio_comparator`: strumento Python per acquisire e confrontare segnali da due microfoni, con analisi in dominio temporale e frequenziale.
- `ZeroMirror Creator` (descrizione nel sito): software per generare profili di specchi acustici basati su un modello di Fresnel e file STL per la stampa 3D.
- risorse di prototipazione: progettazione di elementi acustici stampabili in 3D per l'esperimento.

## Installazione e avvio
1. Crea e attiva un ambiente virtuale Python:
   - Windows PowerShell:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

3. Avvia il server di sviluppo:
   ```bash
   uvicorn app:app --reload
   ```
   oppure
   ```bash
   fastapi dev
   ```

4. Apri il browser su `http://127.0.0.1:8000/` per visualizzare il sito.

## Pagina del sito
Il sito include le sezioni principali:
- Home
- Strumenti
- Il progetto
- Risultati
- Team
- Download

## Obiettivo del progetto
L'obiettivo è documentare un workflow completo che va dalla modellazione del fascio sonoro parallelo alla realizzazione sperimentale, con l'analisi dei metamateriali acustici e il supporto di tool software dedicati.

## Note aggiuntive
- La documentazione del sito è pensata per supportare la presentazione del progetto, con una visione didattica e tecnica.
- Il file `Scientific_Paper_ZeroMirror.md` contiene un paper scientifico completo, con spazi dedicati ai risultati sperimentali da inserire successivamente.
- Il repository è un buon punto di partenza per separare in seguito i tool Python in progetti indipendenti.
