# Level 3: Hardwarenaher C++-Bot

Implementiere `chooseStudentMove` in `student_bot.h`.

## Anforderungen

- feste Arrays statt dynamischer Container
- Hindernisse und Snake-Körper berücksichtigen
- sichere Rückfallstrategie
- Entscheidung innerhalb von ungefähr 3 Millisekunden
- PlatformIO-Build darf die RAM-Grenze nicht überschreiten

Build:

```sh
platformio run --environment uno
```

Hardwaremessung:

```powershell
& "$env:USERPROFILE\.platformio\penv\Scripts\python.exe" .\scripts\sample_uno.py --port COM3
```
