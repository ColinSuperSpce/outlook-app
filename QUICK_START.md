# Outlook Auto Attach - Quick Start Guide

## För Användare - Snabb Start

### Steg 1: Installera Chrome Extension

1. Öppna Chrome och gå till `chrome://extensions/`
2. Aktivera **Developer mode** (växla längst upp till höger)
3. Klicka **Load unpacked**
4. Välj mappen **"Chrome Extension"** från paketet
5. Extensionen ska nu synas i din extensions-lista ✅

### Steg 2: Starta Server-appen

#### Mac:
1. Öppna mappen **"Server/Mac"**
2. Dubbelklicka på **"Outlook Auto Attach Server.app"**
   - Första gången: Högerklicka → "Öppna" → Klicka "Öppna" igen
3. ✅ Server startar automatiskt! Du kan minimera eller stänga fönstret
4. Server kör i bakgrunden

#### Windows:
1. Öppna mappen **"Server/Windows"**
2. Dubbelklicka på **"Outlook Auto Attach Server.exe"**
3. ✅ Server startar automatiskt! Du kan minimera eller stänga fönstret
4. Server kör i bakgrunden

### Steg 3: Använd det!

1. Ladda ner en fil som innehåller **"Orderbekräftelse"**, **"Inköp"**, eller **"1000322"** i filnamnet
2. Extensionen upptäcker filen och visar en notifikation
3. Klicka på extension-ikonen i Chrome
4. Klicka **"Open Outlook"**
5. Outlook öppnas med filen bifogad! 🎉

## Valfritt: Starta automatiskt vid inloggning

### Mac:
1. Dra `Outlook Auto Attach Server.app` till mappen **Applications**
2. Systeminställningar → Användare & grupper → Login Items
3. Klicka **+** och välj "Outlook Auto Attach Server"

### Windows:
1. Högerklicka på `Outlook Auto Attach Server.exe` → "Skapa genväg"
2. Tryck `Win + R`, skriv `shell:startup`, tryck Enter
3. Kopiera genvägen till Startup-mappen

## Felsökning

**Servern startar inte?**
- Kontrollera att port 8765 inte används av något annat program
- Försök starta om appen

**Extension fungerar inte?**
- Kontrollera att servern körs (öppna http://localhost:8765/status i webbläsaren)
- Kolla att filen innehåller "Orderbekräftelse", "Inköp", eller "1000322" i namnet

**Outlook öppnas inte?**
- Kontrollera att Microsoft Outlook är installerat
- Försök starta om både servern och Chrome

---

**För support, kontakta IT-avdelningen.**

