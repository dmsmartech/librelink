[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/dmsmartech/librelink)
[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

[🇬🇧 English](README.md) | 🇮🇹 Italiano

---

# LibreLink Up — Integrazione per Home Assistant

Questa integrazione permette di visualizzare in Home Assistant i dati glicemici del sensore FreeStyle Libre, letti tramite l'app LibreLink Up di Abbott.

---

## Come funziona

Il sensore FreeStyle Libre trasmette i dati all'app **LibreApp** (o **FreeStyle LibreLink**) sul telefono del paziente. Tramite la funzione di condivisione, questi dati vengono inviati in cloud e resi disponibili a un secondo account tramite l'app **LibreLink Up**.

L'integrazione per Home Assistant si collega a questo secondo account LibreLink Up per leggere i dati.

---

## Prerequisiti

- Un sensore FreeStyle Libre attivo
- L'app **LibreApp** (o FreeStyle LibreLink) installata sul telefono del paziente, con un account Abbott registrato
- Un **secondo account Abbott** da usare con LibreLink Up (può essere un tuo account secondario)
- L'app **LibreLink Up** installata sul telefono del paziente
- Home Assistant con HACS installato

---

## Passo 1 — Invitare il secondo account da LibreApp

Sul telefono del paziente, nell'app **LibreApp**:

1. Apri l'app e tocca l'icona del menu in alto a sinistra
2. Seleziona **App connesse**
3. Tocca **Connetti** (se non hai ancora invitato nessuno) oppure **Gestisci** (se hai già invitato qualcuno)
4. Tocca il pulsante **Aggiungi collegamento**
5. Compila il modulo con i dati richiesti
6. Invia l'invito

---

## Passo 2 — Accettare l'invito su LibreLink Up

Sul telefono dove hai installato **LibreLink Up**:

1. Apri l'app LibreLink Up
2. Accedi con il secondo account Abbott (quello a cui hai inviato l'invito)
3. Accetta l'invito ricevuto
4. **Accetta i Termini di Servizio di Abbott** — questo passaggio è obbligatorio: senza di esso l'integrazione non funzionerà
5. Verifica che i dati glicemici del paziente siano visibili nell'app

> **Importante:** ogni volta che Abbott aggiorna i Termini di Servizio, dovrai riaprire l'app LibreLink Up e accettarli di nuovo prima che l'integrazione torni a funzionare. In alcuni casi sarà necessario disconnettersi dall'account LibreLink Up e ri-autenticarsi per visualizzare i nuovi Termini di Servizio.

---

## Passo 3 — Installare l'integrazione in Home Assistant

### Tramite HACS

1. Apri HACS in Home Assistant
2. Vai su **Integrazioni** → clicca sui tre puntini in alto a destra → **Repository personalizzati**
3. Inserisci l'URL del repository: `https://github.com/dmsmartech/librelink`
4. Seleziona la categoria **Integrazione**
5. Clicca **Aggiungi**
6. Cerca **LibreLink** in HACS e installala
7. Riavvia Home Assistant

---

## Passo 4 — Configurare l'integrazione

1. In Home Assistant vai su **Impostazioni** → **Dispositivi e servizi**
2. Clicca **Aggiungi integrazione** e cerca **LibreLink**
3. Inserisci:
   - **Email** e **Password** del secondo account Abbott (quello di LibreLink Up)
   - **Regione** — seleziona quella corretta per il tuo paese (es. Europe)
   - **Unità di misura** — `mg/dL` oppure `mmol/L`
4. Clicca **Invia**

Se le credenziali sono corrette e i Termini di Servizio sono stati accettati nell'app, l'integrazione si connette e i sensori vengono creati automaticamente.

---

## Sensori disponibili

Per ogni paziente collegato all'account LibreLink Up vengono creati:

| Sensore | Descrizione |
|---|---|
| Misurazione glicemia | Valore attuale in mg/dL o mmol/L |
| Tendenza glicemia | Testo + icona (Stabile, In aumento, In diminuzione, ecc.) |
| Sensore attivo (giorni) | Giorni trascorsi dall'attivazione del sensore |
| Minuti dall'ultimo aggiornamento | Minuti passati dall'ultima lettura |
| È alto | Sì / No |
| È basso | Sì / No |

---

## Esempio con custom:mini-graph-card

![image](https://github.com/gillesvs/librelink/assets/51242147/bfed1b2b-dbf7-4666-a202-885ff3db67b8)

Il file yaml per ottenere questo grafico:
https://github.com/gillesvs/librelink/blob/main/custom_components/librelink/mini-graph-glucose.yml

---

## Re-autenticazione

Se i Termini di Servizio vengono aggiornati e l'integrazione smette di funzionare:

1. Apri l'app LibreLink Up e accetta i nuovi Termini di Servizio
2. In Home Assistant vai su **Impostazioni** → **Dispositivi e servizi**
3. Troverai una notifica sull'integrazione LibreLink — clicca **Re-autenticare**
4. Reinserisci le credenziali

Non è necessario rimuovere e reinstallare l'integrazione.

---

## Problemi comuni

| Problema | Soluzione |
|---|---|
| Errore di autenticazione | Verifica email e password del secondo account Abbott |
| Termini di Servizio non accettati | Apri LibreLink Up e accetta i T&S, poi ri-autentica |
| Nessun dato visibile | Verifica che l'invito sia stato accettato e i dati siano visibili in LibreLink Up |
| Regione sbagliata | Rimuovi e reinstalla l'integrazione selezionando la regione corretta |

---

## Crediti

Basato sul lavoro originale di [gillesvs/librelink](https://github.com/gillesvs/librelink).
