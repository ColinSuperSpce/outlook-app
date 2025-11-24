# Hur man använder Outlook Auto Attach Server-appen

## För Användare

### Första gången du startar appen:

1. **Dubbelklicka på `Outlook Auto Attach Server.app`**
   - Mac kan varna om att appen inte är signerad
   - Gå till **Systeminställningar → Säkerhet** och klicka **"Öppna ändå"**
   - Eller högerklicka och välj **"Öppna"** och klicka **"Öppna"** igen

2. **Appen öppnas** med ett fönster som visar:
   - Server Status (Status: Stopped/Running)
   - Port nummer (8765)
   - Start Server / Stop Server knappar
   - Activity Log

3. **Klicka "Start Server"**
   - Status ändras till grön "Status: Running"
   - Appen är nu redo att ta emot filer från Chrome extension

4. **Du kan minimera fönstret**
   - Servern fortsätter köra i bakgrunden
   - Du kan alltid öppna appen igen för att se status eller stoppa servern

### För att stoppa servern:
- Öppna appen igen (om minimerad)
- Klicka **"Stop Server"**
- Eller stäng fönstret (servern stoppas automatiskt)

## Var lägger man appen?

### Alternativ 1: I Applications-mappen (Rekommenderat)
1. Dra `Outlook Auto Attach Server.app` till `/Applications`
2. Du kan skapa en genväg i Dock (dra från Applications till Dock)
3. Nu kan du starta den från Dock eller Launchpad

### Alternativ 2: På Skrivbordet
- Behåll den där den är
- Dubbelklicka när du vill starta servern

### Alternativ 3: I en egen mapp
- Skapa en mapp, t.ex. `/Users/DittAnvändarnamn/Applications`
- Lägg appen där för bättre organisation

## Auto-Start vid Inloggning

Om du vill att servern startar automatiskt när du loggar in:

1. **Flytta appen till Applications** (om inte redan gjort)
2. **Systeminställningar → Användare & grupper → Login Items**
3. Klicka **"+"** knappen
4. Välj `Outlook Auto Attach Server.app` från Applications
5. ✅ Nu startar servern automatiskt när du loggar in

**Alternativ metod:**
- Högerklicka på appen i Applications
- Välj **"Options → Open at Login"**

## Tips

- **Första gången**: Starta appen manuellt och klicka "Start Server" för att testa
- **Activity Log**: Visar när filer tas emot och behandlas
- **Status-indikator**: Grön = Kör, Röd = Stoppad
- **Port**: Appen använder port 8765 (om den är upptagen får du ett felmeddelande)

## Felsökning

**Appen öppnas inte:**
- Mac blockerar ofta unsigned apps första gången
- Gå till Systeminställningar → Säkerhet och klicka "Öppna ändå"

**Servern startar inte:**
- Kontrollera om port 8765 redan används av en annan process
- Försök starta om appen

**Chrome extension fungerar inte:**
- Kontrollera att servern är igång (Status: Running)
- Kontrollera Activity Log för felmeddelanden

