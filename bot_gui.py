import json
import requests
import websocket
import time
import pyautogui
import pytesseract
from pytesseract import Output
import cv2
import numpy as np
import threading
import customtkinter as ctk
import tkinter as tk 
import base64
import keyboard 

# ==============================================================================
# CONFIGURACIÓN DEL SISTEMA
# ==============================================================================
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

SISTEMA_VERSION = "v5.0.6 ELITE"

GLASS_COLOR = ("#1A1C2A", "#1A1C2A") 
TEAL_GLOW = ("#15E4C2", "#15E4C2")
PURPLE_GLOW = ("#BB56F8", "#BB56F8")
ACTIVE_COLOR = ("#333646", "#333646") 
TEXT_MAIN = ("#FFFFFF", "#FFFFFF")
TEXT_SUB = ("#AAAAAA", "#AAAAAA")
CORNER_RADIUS = 15

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue") 

# ==============================================================================
# DICCIONARIO MULTILENGUAJE (INTERFAZ Y LOGS)
# ==============================================================================
TEXTOS = {
    "es": {
        "sys_name": "⚡ CENTINELA ELITE",
        "credits": "Desarrollado por Chang • Discord ID: changmvp",
        "btn_tut": "📖 MANUAL TÉCNICO & F.A.Q.",
        "panel1": "1. ¿DÓNDE VAMOS A JUGAR?",
        "inst": "Seleccionar Instancia (RM):",
        "btn_ref": "🔄 Actualizar",
        "main_name": "Nombre Personaje Main (DPS):",
        "follow_key": "Tecla Follow (ej. Z):",
        "panel2": "2. CALIBRACIÓN OBJETIVOS",
        "btn_ocr": "Paso A: Verificar Lectura OCR",
        "btn_ocr_done": "Paso A: ✔️ OCR Operativo",
        "btn_hp": "Paso B: Anclar HP (Main)",
        "btn_hp_done": "Paso B: ✔️ HP Main",
        "btn_clear": "Paso C: Anclar Botón 'X'",
        "btn_clear_done": "Paso C: ✔️ Botón 'X'",
        "btn_hp_rm": "Paso D: Anclar HP (RM)",
        "btn_hp_rm_done": "Paso D: ✔️ HP RM",
        "btn_mp_rm": "Paso E: Anclar MP (RM)",
        "btn_mp_rm_done": "Paso E: ✔️ MP RM",
        "note": "*Nota: Tienes 5 seg para situar el mouse tras presionar cualquier botón.",
        "panel3": "3. TIEMPOS DE BUFFEO",
        "int_lbl": "Intervalo Automático: {} Minutos",
        "cast_lbl": "Tiempo de Casteo (Animación): {} Segs",
        "btn_force_buff": "⚡ Iniciar Buff Forzado",
        "btn_auto_on": "🟢 Auto-Buff: ACTIVO",
        "btn_auto_off": "🔴 Auto-Buff: PAUSADO",
        "panel4": "CONTROL DE EJECUCIÓN MAESTRO",
        "btn_start": "▶ INICIAR",
        "btn_stop": "⏸ DETENER",
        "btn_restart": "🔄 REINICIAR",
        "log_sys": "REGISTRO DE SISTEMA",
        "log_init": "[SISTEMA] CENTINELA ELITE iniciado. Motor de depuración CDP en escucha.",
        "tt_force": "Ejecuta la secuencia de buffs inmediatamente.",
        "tt_auto": "Pausa o reanuda el temporizador de auto-buffs. La curación seguirá activa.",
        "tt_start": "Inicia la vigilancia concurrente de HP, MP y ciclo de buffs.",
        "tt_stop": "Finaliza los hilos de ejecución en segundo plano.",
        "tt_restart": "Limpia las variables de entorno y reinicia la calibración.",
        "l_search_tabs": "Buscando endpoints de depuración de Chrome...",
        "l_found_tabs": "Éxito: {} endpoints localizados.",
        "l_no_tabs": "Error: No se detectaron websockets válidos.",
        "l_err_conn": "ERROR: No se pudo establecer conexión HTTP con el puerto 9222.",
        "l_err_tab": "ERROR: Instancia seleccionada no es válida.",
        "l_err_cdp": "ERROR: Fallo en el Handshake CDP: {}",
        "l_conn_webgl": "Estableciendo túnel WebSocket con el motor de renderizado...",
        "l_scan_party": "Iniciando procesamiento de imagen OpenCV y Tesseract para: '{}'...",
        "l_err_party": "ERROR OCR: Cadena '{}' no encontrada en la matriz de píxeles.",
        "l_succ_party": "ÉXITO OCR: Cadena localizada en coordenadas relativas X:{} Y:{}",
        "l_warn_hp": "CALIBRACIÓN: 5 segundos para registrar el array RGB del HP (Main).",
        "l_succ_hp": "CALIBRACIÓN: Vector RGB fijado exitosamente (Canal Rojo: {})",
        "l_warn_clear": "CALIBRACIÓN: 5 segundos para mapear las coordenadas del nodo 'X'.",
        "l_succ_clear": "CALIBRACIÓN: Coordenadas de interfaz fijadas en X:{} Y:{}",
        "l_warn_hp_rm": "CALIBRACIÓN: 5 segundos para registrar el array RGB del HP (RM).",
        "l_succ_hp_rm": "CALIBRACIÓN: Vector RGB fijado exitosamente (Canal Rojo RM: {})",
        "l_warn_mp_rm": "CALIBRACIÓN: 5 segundos para registrar el array RGB del MP (RM).",
        "l_succ_mp_rm": "CALIBRACIÓN: Vector RGB fijado exitosamente (Canal Azul RM: {})",
        "l_cap_coord": "Interceptando puntero en {}...",
        "l_sys_ready": "SISTEMA PARAMETRIZADO. LISTO PARA EJECUCIÓN.",
        "l_proto_on": "INICIALIZANDO HILOS DE CONTROL ELITE.",
        "l_hp_alert": "Trigger: Caída de HP Main. Inyectando payload (Heal).",
        "l_hp_rm_alert": "Trigger: Caída de HP RM. Inyectando payload (Poción HP).",
        "l_mp_rm_alert": "Trigger: Caída de MP RM. Inyectando payload (Poción MP).",
        "l_man_seq": ">>> INTERRUPCIÓN EXTERNA: EJECUCIÓN FORZADA DE BUFFS <<<",
        "l_buff_start": "Ejecutando coreografía macro (Delay: {}s)...",
        "l_buff_f1": "-> Enviando evento MouseClick (Deselección)...",
        "l_buff_self": "-> Enviando evento KeyEvent F1 (Self-Buff)...",
        "l_buff_sel": "-> Análisis de frame actual para localizar DPS...",
        "l_buff_main": "-> Vector de destino localizado. Inyectando Buffs...",
        "l_buff_follow": "-> Restableciendo tracking (Auto-Follow)...",
        "l_buff_f2": "-> Restaurando estado de vigilancia (F2)...",
        "l_buff_done": "Ciclo de red finalizado. Retornando a modo pasivo.",
        "l_err_exec": "EXCEPCIÓN NO CONTROLADA EN EL HILO PRINCIPAL: {}",
        "l_man_stop": "SISTEMA SUSPENDIDO POR EL USUARIO.",
        "l_reboot": "Vaciando memoria de calibración..."
    },
    "en": {
        "sys_name": "⚡ SENTINEL ELITE",
        "credits": "Developed by Chang • Discord ID: changmvp",
        "btn_tut": "📖 TECHNICAL MANUAL & F.A.Q.",
        "panel1": "1. WORKSPACE INSTANCE",
        "inst": "Target Debugger (RM):",
        "btn_ref": "🔄 Fetch",
        "main_name": "Target String (Main DPS):",
        "follow_key": "Follow Keycode (e.g. Z):",
        "panel2": "2. CALIBRATION VECTORS",
        "btn_ocr": "Step A: Init OCR Test",
        "btn_ocr_done": "Step A: ✔️ OCR Sync",
        "btn_hp": "Step B: Map Main HP",
        "btn_hp_done": "Step B: ✔️ Main HP",
        "btn_clear": "Step C: Map 'X' DOM",
        "btn_clear_done": "Step C: ✔️ DOM 'X'",
        "btn_hp_rm": "Step D: Map RM HP",
        "btn_hp_rm_done": "Step D: ✔️ RM HP",
        "btn_mp_rm": "Step E: Map RM MP",
        "btn_mp_rm_done": "Step E: ✔️ RM MP",
        "note": "*Note: 5s delay after clicking to set X,Y pointer coordinates.",
        "panel3": "3. EXECUTION TIMERS",
        "int_lbl": "Macro Interval: {} Minutes",
        "cast_lbl": "Skill Animation Delay: {} Secs",
        "btn_force_buff": "⚡ Trigger Override",
        "btn_auto_on": "🟢 Auto-Macro: ACTIVE",
        "btn_auto_off": "🔴 Auto-Macro: HALTED",
        "panel4": "MASTER THREAD CONTROL",
        "btn_start": "▶ START",
        "btn_stop": "⏸ STOP",
        "btn_restart": "🔄 PURGE",
        "log_sys": "RUNTIME LOG",
        "log_init": "[SYSTEM] SENTINEL ELITE Boot. CDP WebSocket listener ready.",
        "tt_force": "Overrides loop and triggers buff macro.",
        "tt_auto": "Toggles buff thread. Healing loop remains active.",
        "tt_start": "Deploys background daemon threads.",
        "tt_stop": "Kills background daemons.",
        "tt_restart": "Flushes calibration environment variables.",
        "l_search_tabs": "Querying Chrome debugging endpoints...",
        "l_found_tabs": "Success: {} endpoints retrieved.",
        "l_no_tabs": "Error: No valid JSON endpoints found.",
        "l_err_conn": "HTTP ERROR: Cannot reach localhost:9222.",
        "l_err_tab": "ERROR: Invalid WebSocket target.",
        "l_err_cdp": "CDP Handshake failed: {}",
        "l_conn_webgl": "Establishing WebSocket tunnel...",
        "l_scan_party": "Running OpenCV/Tesseract matrix for: '{}'...",
        "l_err_party": "OCR ERROR: String '{}' not found in pixel matrix.",
        "l_succ_party": "OCR SUCCESS: String mapped at rel X:{} Y:{}",
        "l_warn_hp": "CALIBRATING: 5s to sample RGB vector for Main HP.",
        "l_succ_hp": "CALIBRATION: RGB vector saved (Red: {})",
        "l_warn_clear": "CALIBRATING: 5s to map 'X' DOM node coordinates.",
        "l_succ_clear": "CALIBRATION: UI mapped at X:{} Y:{}",
        "l_warn_hp_rm": "CALIBRATING: 5s to sample RGB vector for RM HP.",
        "l_succ_hp_rm": "CALIBRATION: RGB vector saved (Red RM: {})",
        "l_warn_mp_rm": "CALIBRATING: 5s to sample RGB vector for RM MP.",
        "l_succ_mp_rm": "CALIBRATION: RGB vector saved (Blue RM: {})",
        "l_cap_coord": "Intercepting pointer in {}...",
        "l_sys_ready": "SYSTEM ENVIRONMENT SET. READY.",
        "l_proto_on": "DEPLOYING DAEMON THREADS.",
        "l_hp_alert": "Trigger: Main HP threshold broken. Pushing Heal.",
        "l_hp_rm_alert": "Trigger: RM HP threshold broken. Pushing Potion.",
        "l_mp_rm_alert": "Trigger: RM MP threshold broken. Pushing Potion.",
        "l_man_seq": ">>> EXTERNAL OVERRIDE: FORCING MACRO <<<",
        "l_buff_start": "Executing choreography (Delay: {}s)...",
        "l_buff_f1": "-> Pushing MouseClick event (Deselect)...",
        "l_buff_self": "-> Pushing KeyEvent F1 (Self-Buff)...",
        "l_buff_sel": "-> Frame analysis for dynamic DPS target...",
        "l_buff_main": "-> Target located. Injecting Buff payload...",
        "l_buff_follow": "-> Pushing KeyEvent (Auto-Follow)...",
        "l_buff_f2": "-> Restoring idle state (F2)...",
        "l_buff_done": "Macro cycle finished. Yielding thread.",
        "l_err_exec": "UNHANDLED THREAD EXCEPTION: {}",
        "l_man_stop": "DAEMONS KILLED BY USER.",
        "l_reboot": "Flushing memory..."
    },
    "de": {
        "sys_name": "⚡ WÄCHTER ELITE",
        "credits": "Entwickelt von Chang • Discord ID: changmvp",
        "btn_tut": "📖 TECHNISCHES HANDBUCH & F.A.Q.",
        "panel1": "1. ARBEITSBEREICH",
        "inst": "Ziel-Debugger (RM):",
        "btn_ref": "🔄 Abrufen",
        "main_name": "Zielzeichenfolge (Main DPS):",
        "follow_key": "Folge-Keycode (z.B. Z):",
        "panel2": "2. KALIBRIERUNGSVEKTOREN",
        "btn_ocr": "Schritt A: OCR-Test starten",
        "btn_ocr_done": "Schritt A: ✔️ OCR Synchronisiert",
        "btn_hp": "Schritt B: HP (Main) abbilden",
        "btn_hp_done": "Schritt B: ✔️ HP Main",
        "btn_clear": "Schritt C: 'X' DOM abbilden",
        "btn_clear_done": "Schritt C: ✔️ DOM 'X'",
        "btn_hp_rm": "Schritt D: HP (RM) abbilden",
        "btn_hp_rm_done": "Schritt D: ✔️ HP RM",
        "btn_mp_rm": "Schritt E: MP (RM) abbilden",
        "btn_mp_rm_done": "Schritt E: ✔️ MP RM",
        "note": "*Hinweis: 5s Verzögerung zum Setzen der X,Y-Koordinaten.",
        "panel3": "3. AUSFÜHRUNGSTIMER",
        "int_lbl": "Makro-Intervall: {} Minuten",
        "cast_lbl": "Skill-Animation Delay: {} Sek",
        "btn_force_buff": "⚡ Überschreiben auslösen",
        "btn_auto_on": "🟢 Auto-Makro: AKTIV",
        "btn_auto_off": "🔴 Auto-Makro: GESTOPPT",
        "panel4": "MASTER-THREAD-STEUERUNG",
        "btn_start": "▶ START",
        "btn_stop": "⏸ STOP",
        "btn_restart": "🔄 BEREINIGEN",
        "log_sys": "LAUFZEITPROTOKOLL",
        "log_init": "[SYSTEM] WÄCHTER ELITE Boot. CDP WebSocket bereit.",
        "tt_force": "Überschreibt Schleife und löst Makro aus.",
        "tt_auto": "Schaltet Buff-Thread um. Heilung bleibt aktiv.",
        "tt_start": "Startet Hintergrund-Daemons.",
        "tt_stop": "Beendet Hintergrund-Daemons.",
        "tt_restart": "Löscht Kalibrierungsumgebungsvariablen.",
        "l_search_tabs": "Frage Chrome Debugging-Endpunkte ab...",
        "l_found_tabs": "Erfolg: {} Endpunkte gefunden.",
        "l_no_tabs": "Fehler: Keine gültigen JSON-Endpunkte gefunden.",
        "l_err_conn": "HTTP-FEHLER: localhost:9222 nicht erreichbar.",
        "l_err_tab": "FEHLER: Ungültiges WebSocket-Ziel.",
        "l_err_cdp": "CDP-Handshake fehlgeschlagen: {}",
        "l_conn_webgl": "Baue WebSocket-Tunnel auf...",
        "l_scan_party": "Führe OpenCV/Tesseract-Matrix aus für: '{}'...",
        "l_err_party": "OCR FEHLER: Zeichenfolge '{}' nicht gefunden.",
        "l_succ_party": "OCR ERFOLG: Vektor abgebildet bei rel X:{} Y:{}",
        "l_warn_hp": "KALIBRIERUNG: 5s zum Abtasten des RGB-Vektors (Main HP).",
        "l_succ_hp": "KALIBRIERUNG: RGB-Vektor gespeichert (Rot: {})",
        "l_warn_clear": "KALIBRIERUNG: 5s zum Abbilden der 'X' DOM-Koordinaten.",
        "l_succ_clear": "KALIBRIERUNG: UI abgebildet bei X:{} Y:{}",
        "l_warn_hp_rm": "KALIBRIERUNG: 5s zum Abtasten des RGB-Vektors (RM HP).",
        "l_succ_hp_rm": "KALIBRIERUNG: RGB-Vektor gespeichert (Rot RM: {})",
        "l_warn_mp_rm": "KALIBRIERUNG: 5s zum Abtasten des RGB-Vektors (RM MP).",
        "l_succ_mp_rm": "KALIBRIERUNG: RGB-Vektor gespeichert (Blau RM: {})",
        "l_cap_coord": "Fange Zeiger ab in {}...",
        "l_sys_ready": "SYSTEMUMGEBUNG EINGESTELLT. BEREIT.",
        "l_proto_on": "STARTE DAEMON-THREADS.",
        "l_hp_alert": "Trigger: Main HP-Schwelle unterschritten. Sende Heilung.",
        "l_hp_rm_alert": "Trigger: RM HP-Schwelle unterschritten. Sende Trank.",
        "l_mp_rm_alert": "Trigger: RM MP-Schwelle unterschritten. Sende Trank.",
        "l_man_seq": ">>> EXTERNES ÜBERSCHREIBEN: ERZWINGE MAKRO <<<",
        "l_buff_start": "Führe Choreografie aus (Delay: {}s)...",
        "l_buff_f1": "-> Sende MouseClick (Deselektieren)...",
        "l_buff_self": "-> Sende KeyEvent F1 (Self-Buff)...",
        "l_buff_sel": "-> Frame-Analyse für dynamisches Ziel...",
        "l_buff_main": "-> Ziel lokalisiert. Injiziere Buff-Payload...",
        "l_buff_follow": "-> Sende KeyEvent (Auto-Follow)...",
        "l_buff_f2": "-> Stelle Ruhezustand wieder her (F2)...",
        "l_buff_done": "Makro-Zyklus beendet. Gebe Thread frei.",
        "l_err_exec": "UNBEHANDELTE THREAD-AUSNAHME: {}",
        "l_man_stop": "DAEMONS DURCH BENUTZER BEENDET.",
        "l_reboot": "Speicher wird geleert..."
    }
}

# ==============================================================================
# DICCIONARIO DEL MANUAL TÉCNICO, FAQ Y DISCLAIMER (MARKDOWN)
# ==============================================================================
TUTORIAL_TEXTS = {
    "es": """**========================================================================================**
**🛠️ MANUAL TÉCNICO Y ESPECIFICACIONES: CENTINELA ELITE (v5.0) 🛠️**
**========================================================================================**

Bienvenido a la documentación técnica oficial. Este bot no es un simple programa de macros de teclado; es un sistema de automatización basado en Interfaz de Paso de Mensajes (CDP) y Visión Artificial (Computer Vision). Sigue estrictamente esta guía para garantizar una ejecución sin errores.

**1. ARQUITECTURA DEL SISTEMA Y REQUISITOS**
- **Navegador Obligatorio:** Google Chrome.
- **Motor OCR (Optical Character Recognition):** El bot utiliza `Tesseract-OCR` junto con la librería de procesamiento de imágenes `OpenCV` para convertir el flujo de renderizado del juego en matrices de texto leíbles. 
- **⚠️ INSTALACIÓN ESTRICTA:** Descarga el instalador de Tesseract e instálalo **OBLIGATORIAMENTE** en la ruta absoluta: `C:\\Program Files\\Tesseract-OCR\\tesseract.exe`. Una desviación de esta ruta provocará excepciones en el hilo principal y el bot no podrá escanear.

**2. CONFIGURACIÓN DEL ENTORNO DE DEPURACIÓN (DEBUGGING PORT)**
*Explicación Técnica:* Los navegadores congelan los subprocesos de las pestañas inactivas para optimizar memoria. Para evitar que el motor de renderizado de Chromium se detenga cuando minimizas el juego, debemos ejecutar Chrome habilitando un puerto local de depuración y deshabilitando el "background throttling".

- Ve a tu Escritorio, clic derecho -> **"Nuevo"** -> **"Acceso directo"**.
- En el campo "Destino", pega EXACTAMENTE este argumento de ejecución:
  **"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\ChromeBotFlyff" --remote-allow-origins=* --disable-backgrounding-occluded-windows --disable-renderer-backgrounding --disable-background-timer-throttling**
- Cierra todas las instancias previas de Chrome en tu Administrador de Tareas y abre el juego únicamente desde este acceso directo. Inicia sesión solo con tu **Ringmaster (RM)** aquí.

**3. PARAMETRIZACIÓN DEL CLIENTE (IN-GAME)**
- **Renderizado (Obligatorio):** Presiona **F11** (Pantalla Completa). Las coordenadas X,Y de la interfaz gráfica cambian si el juego está en modo ventana, rompiendo los vectores de calibración.
- **Escala de UI:** En Opciones -> Interfaz, **Aumenta el tamaño de la interfaz al MÁXIMO.** Esto incrementa la densidad de píxeles de las fuentes, reduciendo el margen de error del algoritmo OpenCV/Tesseract al 0%.
- **Mapas de Teclado (Hotbars):**
  * **Barra F1 (Buffs):** Slots del 1 al 0 reservados para Buffs.
  * **Barra F2 (Supervivencia):** Slot 1 = Heal, Slot 2 = HP Potion, Slot 3 = MP Potion.
  * **Tecla Follow:** Verifica tu código de tecla para "Seguir" (Por defecto: **Z**).

**4. CONFIGURACIÓN DE VECTORES (CALIBRACIÓN DEL BOT)**
Inicia el bot, haz clic en **"🔄 Actualizar"** y selecciona el endpoint de la pestaña del RM. Define el nombre de la variable objetivo (Tu Main DPS).

- **🕹️ PASO A (Validación del Array OCR):** Ubica el frame de la Party en la parte INFERIOR IZQUIERDA y activa las barras laterales de la party. Haz clic en "Paso A". El sistema capturará un screenshot interno vía Base64, lo convertirá a escala de grises, aplicará binarización inversa y buscará la cadena de texto de tu Main.
- **❤️ PASO B (Mapeo de Píxel HP Main):** Haz clic sobre tu Main in-game (barra estática superior central). Haz clic en "Paso B" y en los siguientes 5s sitúa el puntero sobre la sección roja. El bot leerá cíclicamente el Canal Rojo (R) de ese píxel específico.
- **❌ PASO C (Mapeo Coordenada 'X'):** Con la barra estática aún arriba, haz clic en "Paso C" y pon el puntero en el botón 'X' (Deseleccionar). Esto envía un evento `Input.dispatchMouseEvent` directo al DOM, deseleccionando al objetivo sin manipular el teclado físico.
- **🛡️ PASO D y E (Mapeo HP/MP Ringmaster):** Repite el proceso para registrar los vectores RGB de TU PROPIA barra de Vida (Canal Rojo) y tu barra de Maná (Canal Azul) situadas arriba a la izquierda.

**--- ⚙️ TROUBLESHOOTING (F.A.Q.) ---**

**P: ¿El bot puede ejecutarse en segundo plano?**
R: Sí. Como utiliza WebSockets (Protocolo CDP), inyecta los comandos directo al motor del navegador. 
**¡LEY ABSOLUTA!:** La pestaña del RM **debe permanecer en F11**. Para gestionar otras ventanas, usa **Alt + Tab**. Si retiras el F11 o minimizas el RM haciendo clic en la barra de tareas, el motor gráfico detiene el pintado de frames y la lectura de los Canales RGB devolverá excepciones, pausando el hilo.

**P: ¿Por qué el bot falla en la lectura (Paso A) o se cura a sí mismo?**
R: (1) La escala de la UI no está al máximo. (2) Hay discrepancia entre la cadena de texto en el bot y el juego (Sensible a mayúsculas/minúsculas). (3) Calibraste el Paso B sobre el HUD de la Party (que es dinámico) en lugar de la barra central de selección (que es estática).

**========================================================================================**
**⚠️ DISCLAIMER DE SEGURIDAD Y AVISO LEGAL ⚠️**
**========================================================================================**

**Código Abierto y Privacidad:**
CENTINELA ELITE es un software 100% de uso libre, de código abierto (Open Source) y gratuito. **NO ES UN VIRUS**, no posee rutinas de Keylogging, ni módulos de red para extracción de datos hacia servidores remotos. Toda la comunicación ocurre exclusivamente a través del puerto de depuración local (`http://localhost:9222`). Para garantizar la integridad de tu equipo, descarga este software **ÚNICAMENTE desde el repositorio oficial de GitHub de Chang**. No aceptes ejecutables (.exe) de terceros.

**Mecanismo de Inyección y Anti-Cheat:**
Este software **NO lee ni escribe en la memoria RAM asignada al cliente del juego**. No inyecta archivos DLL ni utiliza apis de manipulación de memoria de Windows (como `WriteProcessMemory`). Funciona mediante análisis de captura de pantalla y despacho de eventos de hardware virtual vía Chrome. Debido a esto, a nivel técnico, es prácticamente "indetectable" para las firmas de los programas Anti-Cheat convencionales (GameGuard, XignCode, etc).

**Riesgo de Suspensión (Heurística):**
El uso de macros, bots y herramientas de automatización de terceros es una **violación directa a los Términos de Servicio (ToS) de Flyff Universe**. Aunque el software no altere el cliente, los administradores (GMs) poseen herramientas de detección heurística (análisis de comportamiento). Si dejas el bot ejecutándose 24/7 sin supervisión, envías comandos en intervalos exactos, o eres grabado y reportado por otro usuario, tu cuenta será suspendida permanentemente. 

**Exención de Responsabilidad:**
Estás compilando y utilizando esta herramienta bajo **TU PROPIO Y EXCLUSIVO RIESGO**. El desarrollador original (Chang) no asume ningún tipo de responsabilidad legal, moral, ni técnica sobre posibles baneos, pérdidas de cuentas, cierres o daños derivados del uso de este script. Asimismo, se declara abiertamente que este proyecto tiene propósitos puramente educativos y experimentales en el ámbito de la ingeniería de software y automatización; y no guarda ninguna afiliación, patrocinio, asociación ni conexión comercial o de ninguna índole con **Flyff Universe, Gala Lab Corp**, o cualquiera de sus filiales, socios y desarrolladores oficiales.
""",

    "en": """**========================================================================================**
**🛠️ TECHNICAL MANUAL & SPECIFICATIONS: SENTINEL ELITE (v5.0) 🛠️**
**========================================================================================**

Welcome to the official technical documentation. This is not a simple macro recorder; it is an automation system based on Message Passing Interface (CDP) and Computer Vision. Strictly follow this guide to ensure error-free execution.

**1. SYSTEM ARCHITECTURE & REQUIREMENTS**
- **Mandatory Browser:** Google Chrome.
- **OCR Engine:** The bot uses `Tesseract-OCR` bundled with `OpenCV` to convert the game's render stream into readable text arrays.
- **⚠️ STRICT INSTALLATION:** You **MUST** install Tesseract exactly at this absolute path: `C:\\Program Files\\Tesseract-OCR\\tesseract.exe`. Any deviation will throw main-thread exceptions and blind the bot.

**2. DEBUGGING ENVIRONMENT SETUP (CDP PORT)**
*Technical Explanation:* Browsers freeze background tab threads to optimize memory. To prevent Chromium's rendering engine from halting when tabbed out, we must execute Chrome with a local debugging port and background throttling disabled.

- Desktop -> Right-click -> **"New"** -> **"Shortcut"**.
- In the "Target" field, paste EXACTLY this execution argument:
  **"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\ChromeBotFlyff" --remote-allow-origins=* --disable-backgrounding-occluded-windows --disable-renderer-backgrounding --disable-background-timer-throttling**
- Kill all previous Chrome instances in Task Manager. Open the game solely from this shortcut and log in with your **Ringmaster (RM)** only.

**3. CLIENT PARAMETERIZATION (IN-GAME)**
- **Rendering (Mandatory):** Press **F11** (Full Screen). GUI coordinate vectors shift in windowed mode, breaking calibration arrays.
- **UI Scaling:** In Options -> Interface, **Increase UI size to MAXIMUM.** This increases font pixel density, reducing OpenCV/Tesseract algorithmic errors to 0%.
- **Hotbar Mapping:**
  * **F1 Bar (Buffs):** Slots 1 to 0 reserved for Buffs.
  * **F2 Bar (Survival):** Slot 1 = Heal, Slot 2 = HP Potion, Slot 3 = MP Potion.
  * **Follow Key:** Verify your "Follow" keycode (Default: **Z**).

**4. VECTOR CONFIGURATION (CALIBRATION)**
Start the bot, click **"🔄 Fetch"** and select the RM tab endpoint. Define the target variable string (Main DPS name).

- **🕹️ STEP A (OCR Array Validation):** Move Party frame to **BOTTOM LEFT** and enable side party bars. Click "Step A". The system fetches an internal Base64 screenshot, applies grayscale/inverse binarization, and matches your target string.
- **❤️ STEP B (Main HP Pixel Mapping):** Click your Main in-game (static top-center bar). Click "Step B", and within 5s place the pointer on the red section. The bot will cyclically read the Red Channel (R) array of that pixel.
- **❌ STEP C ('X' Coordinate Mapping):** With the static bar still up, click "Step C" and place the pointer on the 'X' button. This triggers a direct DOM `Input.dispatchMouseEvent`, safely clearing the target without hardware key hooks.
- **🛡️ STEP D & E (RM HP/MP Mapping):** Repeat the process to log RGB vectors for YOUR OWN Health (Red Channel) and Mana (Blue Channel) bars located top-left.

**--- ⚙️ TROUBLESHOOTING (F.A.Q.) ---**

**Q: Can the bot run in the background?**
A: Yes. Via WebSockets (CDP Protocol), payloads are injected directly into the browser engine. 
**ABSOLUTE LAW!:** The RM tab **must remain in F11**. To manage other windows, use **Alt + Tab**. If you drop F11 or minimize the RM by clicking the taskbar, the graphic engine stops frame painting; RGB channel polling will return exceptions and halt the thread.

**Q: Why does Step A (OCR) fail or the RM heals itself by mistake?**
A: (1) UI scale is not maximized. (2) String discrepancy (Bot vs Game, case-sensitive). (3) You mapped Step B over the dynamic Party HUD instead of the static center-top target frame.

**========================================================================================**
**⚠️ SECURITY DISCLAIMER & LEGAL NOTICE ⚠️**
**========================================================================================**

**Open Source & Privacy:**
SENTINEL ELITE is 100% free, Open Source software. **IT IS NOT A VIRUS**, it features zero keylogging routines and no network modules for remote data extraction. All communication happens purely via the local debugging port (`http://localhost:9222`). For your machine's integrity, **ALWAYS download from Chang's official GitHub repo**. Do not accept third-party executables.

**Injection Mechanism & Anti-Cheat:**
This software **DOES NOT read or write to RAM allocated to the game client**. It injects no DLLs nor uses Windows memory manipulation APIs (like `WriteProcessMemory`). It functions via screen analysis and virtual hardware dispatch via Chrome. Therefore, on a technical level, it is practically "undetectable" by standard Anti-Cheat signatures (GameGuard, XignCode, etc).

**Suspension Risk (Heuristics):**
The use of macros, bots, and third-party automation tools is a **direct violation of the Flyff Universe Terms of Service (ToS)**. Even if the software leaves the client uncompromised, Game Masters possess heuristic detection tools (behavioral analysis). If you leave the bot 24/7 unsupervised, loop exact time intervals, or get recorded and reported by players, your account will be permanently banned.

**Liability Waiver:**
You are compiling and utilizing this tool at **YOUR SOLE AND EXCLUSIVE RISK**. The original developer (Chang) assumes no legal, moral, or technical liability for bans, account loss, or damages derived from the use of this script. Furthermore, it is explicitly declared that this project is strictly for educational/experimental software engineering purposes and holds absolutely no affiliation, sponsorship, partnership, or commercial connection with **Flyff Universe, Gala Lab Corp**, or any of their subsidiaries and official developers.
""",

    "de": """**========================================================================================**
**🛠️ TECHNISCHES HANDBUCH & SPEZIFIKATIONEN: SENTINEL ELITE (v5.0) 🛠️**
**========================================================================================**

Willkommen zur offiziellen technischen Dokumentation. Dies ist kein einfacher Makrorekorder; es ist ein Automatisierungssystem basierend auf CDP und Computer Vision. Befolgen Sie diese Anleitung strikt für eine fehlerfreie Ausführung.

**1. SYSTEMARCHITEKTUR & ANFORDERUNGEN**
- **Obligatorischer Browser:** Google Chrome.
- **OCR-Engine:** Der Bot nutzt `Tesseract-OCR` und `OpenCV`, um den Render-Stream des Spiels zu lesen.
- **⚠️ STRIKTE INSTALLATION:** Sie **MÜSSEN** Tesseract exakt unter `C:\\Program Files\\Tesseract-OCR\\tesseract.exe` installieren. Jede Abweichung führt zu Thread-Ausnahmen.

**2. DEBUGGING-UMGEBUNG (CDP PORT)**
*Erklärung:* Browser frieren Hintergrund-Tabs ein. Diese Verknüpfung zwingt Chromium, das Rendering aktiv zu halten.

- Desktop -> Rechtsklick -> **"Neu"** -> **"Verknüpfung"**.
- Fügen Sie als Ziel EXAKT dies ein:
  **"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\\ChromeBotFlyff" --remote-allow-origins=* --disable-backgrounding-occluded-windows --disable-renderer-backgrounding --disable-background-timer-throttling**
- Starten Sie das Spiel nur hierüber. Loggen Sie NUR den **Ringmaster (RM)** hier ein.

**3. CLIENT-PARAMETRISIERUNG (IN-GAME)**
- **Rendering:** **F11** (Vollbild) ist zwingend. Fenstermodus verschiebt GUI-Koordinaten.
- **UI-Skalierung:** Optionen -> Interface -> **UI-Größe auf MAXIMAL.** Reduziert OCR-Fehler auf 0%.
- **Hotbar Mapping:**
  * **F1-Leiste:** Slots 1 bis 0 für Buffs.
  * **F2-Leiste:** Slot 1 = Heal, Slot 2 = HP-Trank, Slot 3 = MP-Trank.
  * **Follow Key:** "Folgen"-Taste prüfen (Standard: **Z**).

**4. VEKTORKONFIGURATION (KALIBRIERUNG)**
Bot starten, **"🔄 Abrufen"** klicken, RM-Tab wählen. Ziel-String (Main-Name) definieren.

- **🕹️ SCHRITT A (OCR-Test):** Party-Frame nach **UNTEN LINKS** schieben, seitliche Balken an. "Schritt A" klicken. Bot führt internen Base64-Screenshot und Binarisierung durch.
- **❤️ SCHRITT B (HP Main):** Main im Spiel anklicken (fester Balken oben Mitte). "Schritt B" klicken und Maus innerhalb 5s auf den roten Bereich setzen. Der Bot pollt zyklisch den roten Kanal (R).
- **❌ SCHRITT C ('X' Koordinaten):** "Schritt C" klicken und Maus auf das 'X' setzen. Dies sendet ein direktes `Input.dispatchMouseEvent` an das DOM.
- **🛡️ SCHRITT D & E (HP/MP RM):** Vorgang für die EIGENE Lebens- (Rot) und Manaleiste (Blau) oben links wiederholen.

**--- ⚙️ FEHLERBEHEBUNG (F.A.Q.) ---**

**F: Läuft der Bot im Hintergrund?**
A: Ja, über WebSockets. 
**ABSOLUTE REGEL!:** RM-Tab **muss im F11 bleiben**. Fensterwechsel **NUR mit Alt + Tab**. Wenn Sie F11 beenden oder minimieren, stoppt die Grafik-Engine das Frame-Painting; die RGB-Abfrage wirft Ausnahmen und der Thread stoppt.

**F: Warum scheitert Schritt A oder der RM heilt sich selbst?**
A: (1) UI ist nicht maximal skaliert. (2) String-Diskrepanz (Groß-/Kleinschreibung). (3) Sie haben Schritt B am dynamischen Party-HUD statt am festen Ziel-Frame kalibriert.

**========================================================================================**
**⚠️ SICHERHEITS- & HAFTUNGSAUSSCHLUSS ⚠️**
**========================================================================================**

**Open Source & Datenschutz:**
Dies ist eine 100% kostenlose Open-Source-Software. **ES IST KEIN VIRUS**, enthält keine Keylogger und keine Netzwerkmodule für den Datenabfluss. Kommunikation läuft nur über `http://localhost:9222`. Laden Sie die Software **IMMER vom offiziellen GitHub (Chang)** herunter.

**Injektion & Anti-Cheat:**
Die Software **liest und schreibt NICHT in den Arbeitsspeicher (RAM) des Spiels**. Sie nutzt keine Windows-Speicher-APIs (wie `WriteProcessMemory`). Da sie über Bildschirm-Analyse und Chrome-Ereignisse funktioniert, ist sie für klassische Anti-Cheat-Signaturen (GameGuard, XignCode) praktisch "unauffindbar".

**Sperrrisiko (Heuristik):**
Die Nutzung von Bots ist ein **direkter Verstoß gegen die Flyff Universe Nutzungsbedingungen (ToS)**. Obwohl der Client nicht manipuliert wird, haben GMs heuristische Erkennungswerkzeuge. 24/7 Farming, exakte Zeitintervalle oder Spieler-Meldungen führen zum Permabann.

**Haftungsausschluss:**
Nutzung **AUF EIGENE GEFAHR**. Der Entwickler (Chang) übernimmt keine rechtliche oder technische Haftung für Sperrungen oder Kontoverlust. Dieses Projekt dient ausschließlich Bildungszwecken und steht in keinerlei Verbindung oder kommerzieller Partnerschaft mit **Flyff Universe, Gala Lab Corp** oder deren Entwicklern.
"""
}

# ==============================================================================
# CLASE TOOLTIP PARA LAS AYUDAS EMERGENTES
# ==============================================================================
class ToolTip:
    def __init__(self, widget, get_text_func):
        self.widget = widget
        self.get_text_func = get_text_func 
        self.tw = None
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)

    def enter(self, event=None):
        if self.tw: return
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tw = tk.Toplevel(self.widget)
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(self.tw, text=self.get_text_func(), background="#1A1C2A", foreground="#15E4C2", font=("Segoe UI", 10), relief="solid", borderwidth=1, highlightbackground="#15E4C2", highlightthickness=1, padx=8, pady=4)
        label.pack()

    def leave(self, event=None):
        if self.tw:
            self.tw.destroy()
            self.tw = None

# ==============================================================================
# CLASES DE COMPONENTES VISUALES
# ==============================================================================
class GlassFrame(ctk.CTkFrame):
    def __init__(self, master, border_color=TEAL_GLOW, **kwargs):
        super().__init__(master, corner_radius=CORNER_RADIUS, fg_color=GLASS_COLOR, border_width=1, border_color=border_color, **kwargs)

class NeonButton(ctk.CTkButton):
    def __init__(self, master, glow_color=TEAL_GLOW, **kwargs):
        t_color = kwargs.pop("text_color", TEXT_MAIN)
        super().__init__(master, corner_radius=CORNER_RADIUS, fg_color="transparent", border_width=1, border_color=glow_color, hover_color=ACTIVE_COLOR, text_color=t_color, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), **kwargs)

class NeonSlider(ctk.CTkSlider):
    def __init__(self, master, track_color=PURPLE_GLOW, progress_color=TEAL_GLOW, **kwargs):
        super().__init__(master, corner_radius=CORNER_RADIUS, fg_color=GLASS_COLOR, progress_color=progress_color, button_color=track_color, button_hover_color=TEXT_MAIN, **kwargs)

# ==============================================================================
# CLASE PRINCIPAL: DASHBOARD DEL BOT
# ==============================================================================
class BotFlyffDashboard(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.lang = "es" 
        self.title(f"{self.t('sys_name')} {SISTEMA_VERSION} | Panel de Control")
        self.geometry("720x980") 
        self.resizable(False, False)

        self.bot_corriendo = False
        self.auto_buff_activo = True  
        self.trigger_forzar_buff = False 
        
        self.ws = None
        # Variables Main
        self.x_hp = 0
        self.y_hp = 0
        self.x_clear = 0 
        self.y_clear = 0 
        self.rojo_sano = 0
        
        # Variables Ringmaster (HP y MP)
        self.x_hp_rm = 0
        self.y_hp_rm = 0
        self.rojo_sano_rm = 0
        self.x_mp_rm = 0
        self.y_mp_rm = 0
        self.azul_sano_rm = 0
        
        # Estados
        self.target_calibrado = False
        self.hp_calibrado = False
        self.clear_calibrado = False 
        self.hp_rm_calibrado = False
        self.mp_rm_calibrado = False
        
        self.construir_interfaz()

    def t(self, key, *args):
        texto = TEXTOS.get(self.lang, TEXTOS["es"]).get(key, key)
        if args:
            return texto.format(*args)
        return texto

    def cambiar_idioma(self, seleccion):
        mapa = {"Español": "es", "English": "en", "Deutsch": "de"}
        self.lang = mapa.get(seleccion, "es")
        self.actualizar_textos_ui()

    def abrir_tutorial(self):
        if hasattr(self, "tut_window") and self.tut_window is not None and self.tut_window.winfo_exists():
            self.tut_window.focus()
            return
            
        self.tut_window = ctk.CTkToplevel(self)
        self.tut_window.title(self.t("btn_tut"))
        # Se aumentó el tamaño a 900x850 para que toda la documentación técnica quepa perfectamente
        self.tut_window.geometry("900x850") 
        self.tut_window.resizable(False, False)
        self.tut_window.transient(self) 
        
        lbl_title = ctk.CTkLabel(self.tut_window, text=self.t("btn_tut"), font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color=TEAL_GLOW)
        lbl_title.pack(pady=(20, 10))
        
        txt_tut = ctk.CTkTextbox(self.tut_window, font=ctk.CTkFont(family="Segoe UI", size=13), fg_color=GLASS_COLOR, text_color=TEXT_MAIN, border_width=1, border_color=PURPLE_GLOW, corner_radius=10, wrap="word")
        txt_tut.pack(padx=25, pady=(0, 25), fill="both", expand=True)
        
        txt_tut._textbox.tag_configure("bold", font=("Segoe UI", 13, "bold"), foreground=TEAL_GLOW[1])
        
        texto_tutorial = TUTORIAL_TEXTS.get(self.lang, TUTORIAL_TEXTS["es"])
        partes = texto_tutorial.split("**")
        
        for i, parte in enumerate(partes):
            if i % 2 == 1: 
                txt_tut.insert("end", parte, "bold")
            else:
                txt_tut.insert("end", parte)
                
        txt_tut.configure(state="disabled") 

    def forzar_buff_ui(self):
        if self.bot_corriendo:
            self.trigger_forzar_buff = True
            self.log(self.t("l_man_seq"))
        else:
            self.log("ERROR: Intercepción fallida. Hilo principal inactivo.")

    def toggle_autobuff(self):
        self.auto_buff_activo = not self.auto_buff_activo
        if self.auto_buff_activo:
            self.btn_toggle_buff.configure(text=self.t("btn_auto_on"), border_color="green", text_color="green")
        else:
            self.btn_toggle_buff.configure(text=self.t("btn_auto_off"), border_color="red", text_color="red")

    def construir_interfaz(self):
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(4, weight=1) 

        # --- CABECERA ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, columnspan=2, pady=(15, 5), sticky="ew")
        self.header_frame.grid_columnconfigure(0, weight=1)

        header_title = ctk.CTkFrame(self.header_frame, fg_color="transparent", border_width=0)
        header_title.grid(row=0, column=0, sticky="w")

        self.lbl_titulo = ctk.CTkLabel(header_title, text=self.t("sys_name"), font=ctk.CTkFont(family="Segoe UI", size=28, weight="bold"), text_color=TEAL_GLOW)
        self.lbl_titulo.grid(row=0, column=0, padx=15, sticky="w")
        
        self.lbl_creditos = ctk.CTkLabel(header_title, text=self.t("credits"), font=ctk.CTkFont(family="Segoe UI", size=12, slant="italic"), text_color=TEXT_SUB)
        self.lbl_creditos.grid(row=1, column=0, padx=15, pady=(0, 5), sticky="w")
        
        self.btn_tutorial = NeonButton(self.header_frame, text=self.t("btn_tut"), width=110, height=28, glow_color="#3498DB", text_color="#3498DB", command=self.abrir_tutorial)
        self.btn_tutorial.grid(row=0, column=1, padx=(0, 10), sticky="e")

        self.combo_lang = ctk.CTkOptionMenu(self.header_frame, values=["Español", "English", "Deutsch"], command=self.cambiar_idioma, width=110, height=28, fg_color=GLASS_COLOR, button_color=PURPLE_GLOW, button_hover_color=TEXT_MAIN, font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"))
        self.combo_lang.grid(row=0, column=2, padx=15, sticky="e")

        header_line = ctk.CTkFrame(self.header_frame, fg_color=PURPLE_GLOW, height=2, corner_radius=0)
        header_line.grid(row=1, column=0, columnspan=3, pady=(5, 0), sticky="ew")

        # --- SECCIÓN 1: INSTANCIA ---
        self.card_game_frame = GlassFrame(self, border_color=TEAL_GLOW)
        self.card_game_frame.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")
        self.card_game_frame.grid_columnconfigure((0, 1), weight=1)

        card_game_title_frame = ctk.CTkFrame(self.card_game_frame, fg_color="transparent")
        card_game_title_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 5), sticky="ew")
        card_game_title_frame.grid_columnconfigure(0, weight=1)
        self.lbl_panel1_title = ctk.CTkLabel(card_game_title_frame, text=self.t("panel1"), font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color=TEXT_MAIN)
        self.lbl_panel1_title.grid(row=0, column=0, sticky="w")
        ctk.CTkFrame(card_game_title_frame, fg_color=TEAL_GLOW, height=2, corner_radius=0).grid(row=1, column=0, pady=(3, 0), sticky="ew")

        self.lbl_inst = ctk.CTkLabel(self.card_game_frame, text=self.t("inst"), font=ctk.CTkFont(family="Segoe UI", size=12), text_color=TEXT_SUB)
        self.lbl_inst.grid(row=1, column=0, padx=15, pady=(5, 0), sticky="w")
        
        self.combo_pestana = ctk.CTkOptionMenu(self.card_game_frame, values=["Pestaña 0", "Pestaña 1"], corner_radius=CORNER_RADIUS, font=ctk.CTkFont(family="Segoe UI", size=12, weight="bold"), fg_color=GLASS_COLOR, button_color=TEAL_GLOW, button_hover_color=TEXT_MAIN, dropdown_fg_color=GLASS_COLOR, dropdown_text_color=TEXT_MAIN, dropdown_hover_color=ACTIVE_COLOR)
        self.combo_pestana.grid(row=2, column=0, padx=15, pady=(2, 8), sticky="ew")
        
        self.btn_refrescar = NeonButton(self.card_game_frame, text=self.t("btn_ref"), width=80, glow_color=TEAL_GLOW, command=self.actualizar_lista_pestanas)
        self.btn_refrescar.grid(row=2, column=1, padx=(0, 15), pady=(2, 8), sticky="ew")

        self.lbl_main_name = ctk.CTkLabel(self.card_game_frame, text=self.t("main_name"), font=ctk.CTkFont(family="Segoe UI", size=12), text_color=TEXT_SUB)
        self.lbl_main_name.grid(row=3, column=0, padx=15, pady=(5, 0), sticky="w")
        self.entrada_nombre = ctk.CTkEntry(self.card_game_frame, corner_radius=CORNER_RADIUS, font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), fg_color=GLASS_COLOR, border_width=1, border_color=TEAL_GLOW, text_color=TEXT_MAIN)
        self.entrada_nombre.insert(0, "TuPersonaje")
        self.entrada_nombre.grid(row=4, column=0, columnspan=2, padx=15, pady=(2, 8), sticky="ew")

        self.lbl_follow_key = ctk.CTkLabel(self.card_game_frame, text=self.t("follow_key"), font=ctk.CTkFont(family="Segoe UI", size=12), text_color=TEXT_SUB)
        self.lbl_follow_key.grid(row=5, column=0, padx=15, pady=(5, 0), sticky="w")
        self.entrada_follow = ctk.CTkEntry(self.card_game_frame, width=60, justify="center", font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), corner_radius=CORNER_RADIUS, fg_color=GLASS_COLOR, border_width=1, border_color=TEAL_GLOW, text_color=TEXT_MAIN)
        self.entrada_follow.insert(0, "Z")
        self.entrada_follow.grid(row=6, column=0, padx=15, pady=(2, 10), sticky="w")


        # --- SECCIÓN 2: CALIBRACIÓN EN 2 COLUMNAS (5 PASOS) ---
        self.card_calib_frame = GlassFrame(self, border_color=PURPLE_GLOW)
        self.card_calib_frame.grid(row=2, column=0, padx=15, pady=5, sticky="nsew")
        self.card_calib_frame.grid_columnconfigure((0,1), weight=1)

        card_calib_title_frame = ctk.CTkFrame(self.card_calib_frame, fg_color="transparent")
        card_calib_title_frame.grid(row=0, column=0, columnspan=2, padx=15, pady=(10, 5), sticky="ew")
        card_calib_title_frame.grid_columnconfigure(0, weight=1)
        self.lbl_panel2_title = ctk.CTkLabel(card_calib_title_frame, text=self.t("panel2"), font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color=TEXT_MAIN)
        self.lbl_panel2_title.grid(row=0, column=0, sticky="w")
        ctk.CTkFrame(card_calib_title_frame, fg_color=PURPLE_GLOW, height=2, corner_radius=0).grid(row=1, column=0, pady=(3, 0), sticky="ew")

        # Fila 1: Paso A abarca las dos columnas
        self.btn_calibrar_target = NeonButton(self.card_calib_frame, text=self.t("btn_ocr"), glow_color=TEAL_GLOW, command=self.hilo_calibrar_target)
        self.btn_calibrar_target.grid(row=1, column=0, columnspan=2, pady=(10, 5), padx=15, sticky="ew")

        # Fila 2: Paso B (HP Main) y Paso C (X Clear)
        self.btn_calibrar_hp = NeonButton(self.card_calib_frame, text=self.t("btn_hp"), glow_color=PURPLE_GLOW, state="disabled", command=self.hilo_calibrar_hp)
        self.btn_calibrar_hp.grid(row=2, column=0, pady=5, padx=(15, 5), sticky="ew")

        self.btn_calibrar_clear = NeonButton(self.card_calib_frame, text=self.t("btn_clear"), glow_color="#E74C3C", text_color="#E74C3C", state="disabled", command=self.hilo_calibrar_clear)
        self.btn_calibrar_clear.grid(row=2, column=1, pady=5, padx=(5, 15), sticky="ew")

        # Fila 3: Paso D (HP RM) y Paso E (MP RM)
        self.btn_calibrar_hp_rm = NeonButton(self.card_calib_frame, text=self.t("btn_hp_rm"), glow_color="#F1C40F", text_color="#F1C40F", state="disabled", command=self.hilo_calibrar_hp_rm)
        self.btn_calibrar_hp_rm.grid(row=3, column=0, pady=(5, 10), padx=(15, 5), sticky="ew")

        self.btn_calibrar_mp_rm = NeonButton(self.card_calib_frame, text=self.t("btn_mp_rm"), glow_color="#3498DB", text_color="#3498DB", state="disabled", command=self.hilo_calibrar_mp_rm)
        self.btn_calibrar_mp_rm.grid(row=3, column=1, pady=(5, 10), padx=(5, 15), sticky="ew")

        # Nota
        self.card_note_frame = GlassFrame(self.card_calib_frame, border_color="#333333")
        self.card_note_frame.grid(row=4, column=0, columnspan=2, padx=15, pady=(5, 10), sticky="ew")
        self.lbl_note = ctk.CTkLabel(self.card_note_frame, text=self.t("note"), font=ctk.CTkFont(family="Segoe UI", size=11, slant="italic"), text_color=TEXT_SUB, wraplength=280)
        self.lbl_note.pack(pady=5, padx=10)


        # --- COLUMNA 2: SLIDERS Y CONTROLES DE BUFF ---
        self.card_buffs_frame = GlassFrame(self, border_color=PURPLE_GLOW)
        self.card_buffs_frame.grid(row=1, column=1, rowspan=2, padx=15, pady=10, sticky="nsew")
        self.card_buffs_frame.grid_columnconfigure(0, weight=1)

        card_buffs_title_frame = ctk.CTkFrame(self.card_buffs_frame, fg_color="transparent")
        card_buffs_title_frame.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")
        card_buffs_title_frame.grid_columnconfigure(0, weight=1)
        self.lbl_panel3_title = ctk.CTkLabel(card_buffs_title_frame, text=self.t("panel3"), font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color=TEXT_MAIN)
        self.lbl_panel3_title.grid(row=0, column=0, sticky="w")
        ctk.CTkFrame(card_buffs_title_frame, fg_color=PURPLE_GLOW, height=2, corner_radius=0).grid(row=1, column=0, pady=(3, 0), sticky="ew")

        self.lbl_val_intervalo = ctk.CTkLabel(self.card_buffs_frame, text=self.t("int_lbl", 9), font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color=TEXT_MAIN)
        self.lbl_val_intervalo.grid(row=1, column=0, pady=(15, 0), padx=15, sticky="w")
        
        self.slider_intervalo = NeonSlider(self.card_buffs_frame, from_=1, to=30, number_of_steps=29, command=self.update_lbl_intervalo)
        self.slider_intervalo.set(9) 
        self.slider_intervalo.grid(row=2, column=0, pady=(5, 10), padx=15, sticky="ew")

        self.lbl_val_casteo = ctk.CTkLabel(self.card_buffs_frame, text=self.t("cast_lbl", 3.5), font=ctk.CTkFont(family="Segoe UI", size=13, weight="bold"), text_color=TEXT_MAIN)
        self.lbl_val_casteo.grid(row=3, column=0, pady=(5, 0), padx=15, sticky="w")
        
        self.slider_casteo = NeonSlider(self.card_buffs_frame, from_=1.0, to=6.0, number_of_steps=50, command=self.update_lbl_casteo)
        self.slider_casteo.set(3.5) 
        self.slider_casteo.grid(row=4, column=0, pady=(5, 20), padx=15, sticky="ew")

        self.btn_forzar_buff = NeonButton(self.card_buffs_frame, text=self.t("btn_force_buff"), glow_color="#F1C40F", text_color="#F1C40F", command=self.forzar_buff_ui)
        self.btn_forzar_buff.grid(row=5, column=0, pady=(0, 10), padx=15, sticky="ew")
        ToolTip(self.btn_forzar_buff, lambda: self.t("tt_force"))

        self.btn_toggle_buff = NeonButton(self.card_buffs_frame, text=self.t("btn_auto_on"), glow_color="green", text_color="green", command=self.toggle_autobuff)
        self.btn_toggle_buff.grid(row=6, column=0, pady=(0, 20), padx=15, sticky="ew")
        ToolTip(self.btn_toggle_buff, lambda: self.t("tt_auto"))


        # --- SECCIÓN 4: CONTROL MAESTRO ---
        self.card_control_frame = GlassFrame(self, border_color=TEAL_GLOW)
        self.card_control_frame.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="nsew")
        self.card_control_frame.grid_columnconfigure((0, 1, 2), weight=1)

        card_control_title_frame = ctk.CTkFrame(self.card_control_frame, fg_color="transparent")
        card_control_title_frame.grid(row=0, column=0, columnspan=3, padx=15, pady=(10, 5), sticky="ew")
        card_control_title_frame.grid_columnconfigure(0, weight=1)
        self.lbl_panel4_title = ctk.CTkLabel(card_control_title_frame, text=self.t("panel4"), font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color=TEXT_MAIN)
        self.lbl_panel4_title.grid(row=0, column=0, sticky="w")
        ctk.CTkFrame(card_control_title_frame, fg_color=TEAL_GLOW, height=2, corner_radius=0).grid(row=1, column=0, pady=(3, 0), sticky="ew")

        self.btn_iniciar = NeonButton(self.card_control_frame, text=self.t("btn_start"), glow_color="#1E8449", command=self.arrancar_bot, state="disabled")
        self.btn_iniciar.grid(row=1, column=0, padx=15, pady=(10, 15), sticky="ew")
        ToolTip(self.btn_iniciar, lambda: self.t("tt_start"))

        self.btn_detener = NeonButton(self.card_control_frame, text=self.t("btn_stop"), glow_color="#CB4335", command=self.detener_bot, state="disabled")
        self.btn_detener.grid(row=1, column=1, padx=15, pady=(10, 15), sticky="ew")
        ToolTip(self.btn_detener, lambda: self.t("tt_stop"))

        self.btn_reiniciar = NeonButton(self.card_control_frame, text=self.t("btn_restart"), glow_color="#5B2C6F", command=self.reiniciar_configuracion)
        self.btn_reiniciar.grid(row=1, column=2, padx=15, pady=(10, 15), sticky="ew")
        ToolTip(self.btn_reiniciar, lambda: self.t("tt_restart"))


        # --- TERMINAL DE REGISTROS ---
        self.consola_frame = GlassFrame(self, border_color="#333333")
        self.consola_frame.grid(row=4, column=0, columnspan=2, padx=15, pady=(5, 10), sticky="nsew") 
        self.consola_frame.grid_columnconfigure(0, weight=1)
        self.consola_frame.grid_rowconfigure(1, weight=1)
        
        consola_header_frame = ctk.CTkFrame(self.consola_frame, fg_color="transparent")
        consola_header_frame.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="ew")
        consola_header_frame.grid_columnconfigure(0, weight=1)
        self.lbl_log_title = ctk.CTkLabel(consola_header_frame, text=self.t("log_sys"), font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"), text_color=TEXT_MAIN)
        self.lbl_log_title.grid(row=0, column=0, sticky="w")
        ctk.CTkFrame(consola_header_frame, fg_color="#333333", height=2, corner_radius=0).grid(row=1, column=0, pady=(3, 0), sticky="ew")

        self.consola = ctk.CTkTextbox(self.consola_frame, height=130, font=ctk.CTkFont(family="Consolas", size=11), fg_color=GLASS_COLOR, text_color="#00FF00", corner_radius=0, border_width=1, border_color="#333333")
        self.consola.grid(row=1, column=0, padx=1, pady=(0, 1), sticky="nsew") 
        self.log(self.t("log_init"))


    # --- RUTINA DE CAMBIO DE TEXTOS EN TIEMPO REAL ---
    def actualizar_textos_ui(self):
        self.title(f"{self.t('sys_name')} {SISTEMA_VERSION} | Panel de Control")
        self.lbl_titulo.configure(text=self.t("sys_name"))
        self.lbl_creditos.configure(text=self.t("credits"))
        self.btn_tutorial.configure(text=self.t("btn_tut"))
        self.lbl_panel1_title.configure(text=self.t("panel1"))
        self.lbl_inst.configure(text=self.t("inst"))
        self.btn_refrescar.configure(text=self.t("btn_ref"))
        self.lbl_main_name.configure(text=self.t("main_name"))
        self.lbl_follow_key.configure(text=self.t("follow_key"))
        self.lbl_panel2_title.configure(text=self.t("panel2"))
        
        self.btn_calibrar_target.configure(text=self.t("btn_ocr_done") if self.target_calibrado else self.t("btn_ocr"))
        self.btn_calibrar_hp.configure(text=self.t("btn_hp_done") if self.hp_calibrado else self.t("btn_hp"))
        self.btn_calibrar_clear.configure(text=self.t("btn_clear_done") if self.clear_calibrado else self.t("btn_clear"))
        self.btn_calibrar_hp_rm.configure(text=self.t("btn_hp_rm_done") if self.hp_rm_calibrado else self.t("btn_hp_rm"))
        self.btn_calibrar_mp_rm.configure(text=self.t("btn_mp_rm_done") if self.mp_rm_calibrado else self.t("btn_mp_rm"))
            
        self.lbl_note.configure(text=self.t("note"))
        self.lbl_panel3_title.configure(text=self.t("panel3"))
        self.update_lbl_intervalo(self.slider_intervalo.get())
        self.update_lbl_casteo(self.slider_casteo.get())
        self.btn_forzar_buff.configure(text=self.t("btn_force_buff"))
        self.btn_toggle_buff.configure(text=self.t("btn_auto_on") if self.auto_buff_activo else self.t("btn_auto_off"))
            
        self.lbl_panel4_title.configure(text=self.t("panel4"))
        self.btn_iniciar.configure(text=self.t("btn_start"))
        self.btn_detener.configure(text=self.t("btn_stop"))
        self.btn_reiniciar.configure(text=self.t("btn_restart"))
        self.lbl_log_title.configure(text=self.t("log_sys"))
        
        if hasattr(self, "tut_window") and self.tut_window is not None and self.tut_window.winfo_exists():
            self.tut_window.title(self.t("btn_tut"))
            for widget in self.tut_window.winfo_children():
                if isinstance(widget, ctk.CTkLabel):
                    widget.configure(text=self.t("btn_tut"))
                elif isinstance(widget, ctk.CTkTextbox):
                    widget.configure(state="normal")
                    widget.delete("1.0", "end")
                    texto_tutorial = TUTORIAL_TEXTS.get(self.lang, TUTORIAL_TEXTS["es"])
                    partes = texto_tutorial.split("**")
                    for i, parte in enumerate(partes):
                        if i % 2 == 1:
                            widget.insert("end", parte, "bold")
                        else:
                            widget.insert("end", parte)
                    widget.configure(state="disabled")

    def update_lbl_intervalo(self, val):
        self.lbl_val_intervalo.configure(text=self.t("int_lbl", int(val)))

    def update_lbl_casteo(self, val):
        self.lbl_val_casteo.configure(text=self.t("cast_lbl", round(val, 1)))

    def log(self, texto):
        tiempo = time.strftime("%H:%M:%S")
        self.consola.insert("end", f"[{tiempo}] {texto}\n")
        self.consola.see("end")

    def actualizar_lista_pestanas(self):
        self.log(self.t("l_search_tabs"))
        try:
            response = requests.get("http://localhost:9222/json", timeout=2)
            tabs = response.json()
            nombres_pestanas = []
            for idx, t in enumerate(tabs):
                if t['type'] == 'page':
                    titulo_corto = t['title'][:40] + "..." if len(t['title']) > 40 else t['title']
                    nombres_pestanas.append(f"ID {idx} - {titulo_corto}")
            
            if nombres_pestanas:
                self.combo_pestana.configure(values=nombres_pestanas)
                self.combo_pestana.set(nombres_pestanas[0])
                self.log(self.t("l_found_tabs", len(nombres_pestanas)))
            else:
                self.combo_pestana.configure(values=[self.t("l_no_tabs")])
                self.log(self.t("l_no_tabs"))
                
        except Exception as e:
            self.log(self.t("l_err_conn"))
            self.combo_pestana.configure(values=["Error"])

    def conectar_chrome(self):
        try:
            seleccion = self.combo_pestana.get()
            if not seleccion.startswith("ID "):
                self.log(self.t("l_err_tab"))
                return False
                
            indice = int(seleccion.split(" ")[1])
            
            response = requests.get("http://localhost:9222/json")
            tabs = response.json()
            paginas_web = [t for t in tabs if t['type'] == 'page']
            
            tab = paginas_web[indice]
            self.ws = websocket.create_connection(tab['webSocketDebuggerUrl'])
            self.ws.max_size = 10000000
            return True
        except Exception as e:
            self.log(self.t("l_err_cdp", e))
            return False

    def obtener_color_interno(self, x_coord, y_coord, canal=2):
        self.ws.send(json.dumps({"id": 99, "method": "Page.captureScreenshot", "params": {"format": "jpeg", "quality": 50}}))
        while True:
            try:
                respuesta = json.loads(self.ws.recv())
                if respuesta.get("id") == 99:
                    img_data = base64.b64decode(respuesta["result"]["data"])
                    np_arr = np.frombuffer(img_data, np.uint8)
                    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR) 
                    b, g, r = img[int(y_coord), int(x_coord)]
                    if canal == 2: return int(r)
                    elif canal == 1: return int(g)
                    elif canal == 0: return int(b)
            except:
                continue

    def enviar_click(self, x, y):
        mouse_down = {"id": 3, "method": "Input.dispatchMouseEvent", "params": {"type": "mousePressed", "x": int(x), "y": int(y), "button": "left", "clickCount": 1}}
        mouse_up = {"id": 4, "method": "Input.dispatchMouseEvent", "params": {"type": "mouseReleased", "x": int(x), "y": int(y), "button": "left", "clickCount": 1}}
        self.ws.send(json.dumps(mouse_down))
        time.sleep(0.1)
        self.ws.send(json.dumps(mouse_up))

    def enviar_tecla(self, char, vk):
        tecla_str = str(char).upper() if str(char).lower() in ['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'] else str(char).lower()
        keydown = {"id": 1, "method": "Input.dispatchKeyEvent", "params": {"type": "rawKeyDown", "windowsVirtualKeyCode": vk, "key": tecla_str, "nativeVirtualKeyCode": vk}}
        keyup = {"id": 2, "method": "Input.dispatchKeyEvent", "params": {"type": "keyUp", "windowsVirtualKeyCode": vk, "key": tecla_str, "nativeVirtualKeyCode": vk}}
        self.ws.send(json.dumps(keydown))
        time.sleep(0.05)
        self.ws.send(json.dumps(keyup))

    # --- LÓGICA GHOST: BUSCAR AL MAIN EN TIEMPO REAL ---
    def buscar_main_ghost(self):
        nombre_main = self.entrada_nombre.get().strip().lower()
        self.ws.send(json.dumps({"id": 200, "method": "Page.captureScreenshot", "params": {"format": "png"}}))
        while True:
            resp = json.loads(self.ws.recv())
            if resp.get("id") == 200:
                base64_img = resp["result"]["data"]
                break

        img_data = base64.b64decode(base64_img)
        np_arr = np.frombuffer(img_data, np.uint8)
        img_color = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        
        alto, ancho, _ = img_color.shape
        zona_party = img_color[0:alto, 0:450] 
        
        gris = cv2.cvtColor(zona_party, cv2.COLOR_BGR2GRAY)
        gris = cv2.resize(gris, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        _, gris_bin = cv2.threshold(gris, 120, 255, cv2.THRESH_BINARY_INV)

        datos_ocr = pytesseract.image_to_data(gris_bin, output_type=Output.DICT)

        for i in range(len(datos_ocr['text'])):
            texto_encontrado = datos_ocr['text'][i].lower()
            if nombre_main in texto_encontrado:
                new_x = int(datos_ocr['left'][i] / 2) + 20
                new_y = int(datos_ocr['top'][i] / 2) + 10
                return new_x, new_y
        return None, None

    # --- PROCESOS DE CALIBRACIÓN Y EJECUCIÓN ---
    def chequear_listo_para_iniciar(self):
        if self.target_calibrado and self.hp_calibrado and self.clear_calibrado and self.hp_rm_calibrado and self.mp_rm_calibrado:
            self.btn_iniciar.configure(state="normal")
            self.log(self.t("l_sys_ready"))

    def proceso_calibrar_target(self):
        self.btn_calibrar_target.configure(state="disabled")
        self.log(self.t("l_conn_webgl"))
        if not self.conectar_chrome():
            self.btn_calibrar_target.configure(state="normal")
            return

        nombre_main = self.entrada_nombre.get().strip().lower()
        self.log(self.t("l_scan_party", nombre_main))
        
        gx, gy = self.buscar_main_ghost()
        if gx:
            self.log(self.t("l_succ_party", gx, gy))
            self.target_calibrado = True
            self.btn_calibrar_target.configure(fg_color="green", border_color="green", text=self.t("btn_ocr_done")) 
            
            self.btn_calibrar_hp.configure(state="normal")
            self.btn_calibrar_clear.configure(state="normal")
            self.btn_calibrar_hp_rm.configure(state="normal")
            self.btn_calibrar_mp_rm.configure(state="normal")
        else:
            self.log(self.t("l_err_party", nombre_main))
            self.btn_calibrar_target.configure(state="normal")

    def hilo_calibrar_target(self): threading.Thread(target=self.proceso_calibrar_target, daemon=True).start()

    def proceso_calibrar_hp(self):
        self.btn_calibrar_hp.configure(state="disabled")
        self.log(self.t("l_warn_hp"))
        for i in range(5, 0, -1):
            self.log(self.t("l_cap_coord", i))
            time.sleep(1)
        self.x_hp, self.y_hp = pyautogui.position()
        self.rojo_sano = self.obtener_color_interno(self.x_hp, self.y_hp, canal=2)
        self.log(self.t("l_succ_hp", self.rojo_sano))
        self.hp_calibrado = True
        self.btn_calibrar_hp.configure(fg_color="green", border_color="green", text=self.t("btn_hp_done")) 
        self.chequear_listo_para_iniciar()

    def hilo_calibrar_hp(self): threading.Thread(target=self.proceso_calibrar_hp, daemon=True).start()

    def proceso_calibrar_clear(self):
        self.btn_calibrar_clear.configure(state="disabled")
        self.log(self.t("l_warn_clear"))
        for i in range(5, 0, -1):
            self.log(self.t("l_cap_coord", i))
            time.sleep(1)
        self.x_clear, self.y_clear = pyautogui.position()
        self.clear_calibrado = True
        self.log(self.t("l_succ_clear", self.x_clear, self.y_clear))
        self.btn_calibrar_clear.configure(fg_color="green", border_color="green", text=self.t("btn_clear_done")) 
        self.chequear_listo_para_iniciar()

    def hilo_calibrar_clear(self): threading.Thread(target=self.proceso_calibrar_clear, daemon=True).start()

    def proceso_calibrar_hp_rm(self):
        self.btn_calibrar_hp_rm.configure(state="disabled")
        self.log(self.t("l_warn_hp_rm"))
        for i in range(5, 0, -1):
            self.log(self.t("l_cap_coord", i))
            time.sleep(1)
        self.x_hp_rm, self.y_hp_rm = pyautogui.position()
        self.rojo_sano_rm = self.obtener_color_interno(self.x_hp_rm, self.y_hp_rm, canal=2)
        self.log(self.t("l_succ_hp_rm", self.rojo_sano_rm))
        self.hp_rm_calibrado = True
        self.btn_calibrar_hp_rm.configure(fg_color="green", border_color="green", text=self.t("btn_hp_rm_done")) 
        self.chequear_listo_para_iniciar()

    def hilo_calibrar_hp_rm(self): threading.Thread(target=self.proceso_calibrar_hp_rm, daemon=True).start()

    def proceso_calibrar_mp_rm(self):
        self.btn_calibrar_mp_rm.configure(state="disabled")
        self.log(self.t("l_warn_mp_rm"))
        for i in range(5, 0, -1):
            self.log(self.t("l_cap_coord", i))
            time.sleep(1)
        self.x_mp_rm, self.y_mp_rm = pyautogui.position()
        self.azul_sano_rm = self.obtener_color_interno(self.x_mp_rm, self.y_mp_rm, canal=0) 
        self.log(self.t("l_succ_mp_rm", self.azul_sano_rm))
        self.mp_rm_calibrado = True
        self.btn_calibrar_mp_rm.configure(fg_color="green", border_color="green", text=self.t("btn_mp_rm_done")) 
        self.chequear_listo_para_iniciar()

    def hilo_calibrar_mp_rm(self): threading.Thread(target=self.proceso_calibrar_mp_rm, daemon=True).start()


    # --- BUCLE MAESTRO DEL BOT ---
    def bucle_bot(self):
        self.log(self.t("l_proto_on"))
        
        vk_follow = ord(self.entrada_follow.get()[0].upper())
        tecla_follow = self.entrada_follow.get()[0].lower()
        
        ultimo_buff = time.time() 

        teclas_buffs = [
            ('1', 49), ('2', 50), ('3', 51), ('4', 52), ('5', 53),
            ('6', 54), ('7', 55), ('8', 56), ('9', 57), ('0', 48)
        ]

        while self.bot_corriendo:
            try:
                intervalo_buffs = int(self.slider_intervalo.get()) * 60 
                tiempo_casteo = float(self.slider_casteo.get())

                # 1. GESTIÓN AUTÓNOMA DEL RINGMASTER (HP Propio)
                rojo_rm_actual = self.obtener_color_interno(self.x_hp_rm, self.y_hp_rm, canal=2)
                if rojo_rm_actual < (self.rojo_sano_rm - 40):
                    self.log(self.t("l_hp_rm_alert"))
                    self.enviar_tecla('2', 50) 
                    time.sleep(0.5)

                # 2. GESTIÓN AUTÓNOMA DEL RINGMASTER (MP Propio)
                azul_rm_actual = self.obtener_color_interno(self.x_mp_rm, self.y_mp_rm, canal=0)
                if azul_rm_actual < (self.azul_sano_rm - 40):
                    self.log(self.t("l_mp_rm_alert"))
                    self.enviar_tecla('3', 51) 
                    time.sleep(0.5)

                # 3. CURACIÓN DEL MAIN (Prioridad Máxima del Grupo)
                rojo_actual = self.obtener_color_interno(self.x_hp, self.y_hp, canal=2)
                if rojo_actual < (self.rojo_sano - 40):
                    self.log(self.t("l_hp_alert"))
                    self.enviar_tecla('1', 49) 
                    time.sleep(2.5)
                    continue

                # 4. VERIFICAR TRIGGERS DE BUFFS
                tiempo_actual = time.time()
                forzar_buff = False

                if keyboard.is_pressed('ctrl+backspace') or self.trigger_forzar_buff:
                    self.log(self.t("l_man_seq"))
                    forzar_buff = True
                    self.trigger_forzar_buff = False 
                    time.sleep(0.5) 

                # 5. COREOGRAFÍA ELITE DE BUFFS
                if forzar_buff or (self.auto_buff_activo and (tiempo_actual - ultimo_buff) >= intervalo_buffs):
                    self.log(self.t("l_buff_start", round(tiempo_casteo, 1)))

                    # A) Deseleccionar (Target RM) haciendo clic en la X
                    self.log(self.t("l_buff_f1")) 
                    self.enviar_click(self.x_clear, self.y_clear)
                    time.sleep(0.5)

                    # B) Auto-Buff RM
                    self.enviar_tecla('F1', 112)
                    time.sleep(0.8) 

                    for char, vk in teclas_buffs:
                        if not self.bot_corriendo: break 
                        self.enviar_tecla(char, vk)
                        time.sleep(tiempo_casteo) 

                    # C) Búsqueda Dinámica del Main
                    self.log(self.t("l_buff_sel"))
                    gx, gy = self.buscar_main_ghost()
                    
                    if gx:
                        # Selección y Buffeo al Main
                        self.enviar_click(gx, gy)
                        time.sleep(0.8)

                        self.log(self.t("l_buff_main"))
                        for char, vk in teclas_buffs:
                            if not self.bot_corriendo: break
                            self.enviar_tecla(char, vk)
                            time.sleep(tiempo_casteo) 
                            
                        # D) Activar Auto-Follow
                        self.log(self.t("l_buff_follow"))
                        self.enviar_tecla(tecla_follow, vk_follow)
                        time.sleep(0.5)
                    else:
                        self.log("⚠️ OCR ERROR: No se encontró al Main en la Party. Saltando buffs del Main.")

                    # E) Retorno a Curación
                    self.log(self.t("l_buff_f2"))
                    self.enviar_tecla('F2', 113)
                    time.sleep(0.5)

                    ultimo_buff = time.time()
                    self.log(self.t("l_buff_done"))

                time.sleep(0.1)
            except Exception as e:
                self.log(self.t("l_err_exec", e))
                self.bot_corriendo = False

    def arrancar_bot(self):
        self.bot_corriendo = True
        self.btn_iniciar.configure(state="disabled")
        self.btn_detener.configure(state="normal")
        threading.Thread(target=self.bucle_bot, daemon=True).start()

    def detener_bot(self):
        self.bot_corriendo = False
        self.log(self.t("l_man_stop"))
        self.btn_iniciar.configure(state="normal")
        self.btn_detener.configure(state="disabled")

    def reiniciar_configuracion(self):
        self.log(self.t("l_reboot"))
        self.bot_corriendo = False
        self.target_calibrado = False
        self.hp_calibrado = False
        self.clear_calibrado = False
        self.hp_rm_calibrado = False
        self.mp_rm_calibrado = False
        
        self.x_hp = self.y_hp = self.rojo_sano = 0
        self.x_clear = self.y_clear = 0
        self.x_hp_rm = self.y_hp_rm = self.rojo_sano_rm = 0
        self.x_mp_rm = self.y_mp_rm = self.azul_sano_rm = 0

        if self.ws:
            self.ws.close()
            self.ws = None
        
        self.btn_calibrar_target.configure(fg_color="transparent", border_color=TEAL_GLOW, text=self.t("btn_ocr"), state="normal")
        self.btn_calibrar_hp.configure(fg_color="transparent", border_color=PURPLE_GLOW, text=self.t("btn_hp"), state="disabled")
        self.btn_calibrar_clear.configure(fg_color="transparent", border_color="#E74C3C", text=self.t("btn_clear"), text_color="#E74C3C", state="disabled")
        self.btn_calibrar_hp_rm.configure(fg_color="transparent", border_color="#F1C40F", text=self.t("btn_hp_rm"), text_color="#F1C40F", state="disabled")
        self.btn_calibrar_mp_rm.configure(fg_color="transparent", border_color="#3498DB", text=self.t("btn_mp_rm"), text_color="#3498DB", state="disabled")
        
        self.btn_iniciar.configure(state="disabled")
        self.btn_detener.configure(state="disabled")

if __name__ == "__main__":
    app = BotFlyffDashboard()
    app.mainloop()