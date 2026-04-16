# 🛠️ TECHNICAL MANUAL & SPECIFICATIONS: CENTINELA ELITE BOT (v5.0)
### Key Features:
* **Ghost OCR Scan:** Real-time dynamic localization of the Main DPS.
* **Self-Management:** The RM monitors its own HP/MP and automatically triggers potions.
* **Safe Deselection:** Utilizes the 'X' DOM node to clear targets without visual bugs.
* **Memory Stealth:** No RAM injection (0% risk of detection by standard anti-cheat signatures).

## 🚀 DOWNLOAD / DESCARGA
Go to the [Releases](https://github.com/LambdaHG/Flyff-Universe-Centinela-Elite-Bot/releases/) section to download the compiled **.exe** file.
---

# 📖 Introduction
---

Welcome to the official technical documentation for Sentinel Elite. This is not a simple macro recorder; it is an advanced automation system based on Message Passing Interface (CDP) and Computer Vision. Strictly follow this guide to ensure error-free execution and runtime stability.

---

# 🏗️ 1. SYSTEM ARCHITECTURE & REQUIREMENTS
---
Mandatory Browser: Google Chrome.
OCR Engine: The bot uses Tesseract-OCR bundled with OpenCV to convert the game's render stream into readable text arrays.

# ⚠️ STRICT INSTALLATION PATH: You MUST install Tesseract exactly at this absolute path: C:\Program Files\Tesseract-OCR\tesseract.exe. Any deviation will throw main-thread exceptions and permanently blind the bot.

---

# ⚙️ 2. DEBUGGING ENVIRONMENT SETUP (CDP PORT)
---
Technical Explanation: Browsers freeze background tab threads to optimize memory. To prevent Chromium's rendering engine from halting when tabbed out, we must execute Chrome with a local debugging port and background throttling disabled.

Step-by-Step Execution:

Navigate to your Desktop -> Right-click -> "New" -> "Shortcut".

In the "Target" field, paste EXACTLY this execution argument:
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeBotFlyff" --remote-allow-origins=* --disable-backgrounding-occluded-windows --disable-renderer-backgrounding --disable-background-timer-throttling

Kill all previous Chrome instances in Task Manager.

Open the game solely from this shortcut and log in with your Ringmaster (RM) only.

---

# 🖥️ 3. CLIENT PARAMETERIZATION (IN-GAME)
---
Rendering (Mandatory): Press F11 (Full Screen). GUI coordinate vectors shift in windowed mode, breaking calibration arrays.

UI Scaling: In Options -> Interface, Increase UI size to MAXIMUM. This increases font pixel density, reducing OpenCV/Tesseract algorithmic errors to 0%.

Hotbar Mapping Protocol:

F1 Bar (Buffs): Slots 1 to 0 are exclusively reserved for Buffs.

F2 Bar (Survival): Slot 1 = Heal, Slot 2 = HP Potion, Slot 3 = MP Potion.

Follow Key: Verify your "Follow" keycode (Default: Z).

---

# 🎯 4. VECTOR CONFIGURATION (CALIBRATION)
---
Start the bot, click "🔄 Fetch" and select the RM tab endpoint. You must accurately define the target variable string (Main DPS name).

🕹️ STEP A (OCR Array Validation): Move the Party frame to the BOTTOM LEFT and enable side party bars. Click "Step A". The system fetches an internal Base64 screenshot, applies grayscale/inverse binarization, and matches your target string.

❤️ STEP B (Main HP Pixel Mapping): Click your Main in-game (static top-center bar). Click "Step B", and within 5s place the pointer on the red section. The bot will cyclically read the Red Channel (R) array of that pixel.

❌ STEP C ('X' Coordinate Mapping): With the static bar still up, click "Step C" and place the pointer on the 'X' button. This triggers a direct DOM Input.dispatchMouseEvent, safely clearing the target without hardware key hooks.

🛡️ STEP D & E (RM HP/MP Mapping): Repeat the process to log RGB vectors for YOUR OWN Health (Red Channel) and Mana (Blue Channel) bars located top-left.

---

# 🩺 5. TROUBLESHOOTING (F.A.Q.)
---
Q: Can the bot run in the background?

A: Yes. Via WebSockets (CDP Protocol), payloads are injected directly into the browser engine.
⚠️ ABSOLUTE LAW!: The RM tab must remain in F11. To manage other windows, use Alt + Tab. If you drop F11 or minimize the RM by clicking the taskbar, the graphic engine stops frame painting; RGB channel polling will return exceptions and halt the thread.

Q: Why does Step A (OCR) fail or the RM heals itself by mistake?

A: This usually happens due to one of three reasons:
(1) UI scale is not maximized.
(2) String discrepancy (Bot vs Game, case-sensitive).
(3) You mapped Step B over the dynamic Party HUD instead of the static center-top target frame.

---

# ⚖️ 6. SECURITY DISCLAIMER & LEGAL NOTICE
---
🔓 Open Source & Privacy
SENTINEL ELITE is 100% free, Open Source software. IT IS NOT A VIRUS, it features zero keylogging routines and no network modules for remote data extraction. All communication happens purely via the local debugging port (http://localhost:9222). For your machine's integrity, ALWAYS download from Chang's official GitHub repo; do not accept third-party executables.

---

# 💉 Injection Mechanism & Anti-Cheat
This software DOES NOT read or write to RAM allocated to the game client. It injects no DLLs nor uses Windows memory manipulation APIs (like WriteProcessMemory). It functions via screen analysis and virtual hardware dispatch via Chrome. Therefore, on a technical level, it is practically "undetectable" by standard Anti-Cheat signatures (GameGuard, XignCode, etc).

---

# 🚨 Suspension Risk (Heuristics)
The use of macros, bots, and third-party automation tools is a direct violation of the Flyff Universe Terms of Service (ToS). Even if the software leaves the client uncompromised, Game Masters possess heuristic detection tools (behavioral analysis). If you leave the bot 24/7 unsupervised, loop exact time intervals, or get recorded and reported by players, your account will be permanently banned.

---

# 📜 Liability Waiver
You are compiling and utilizing this tool at YOUR SOLE AND EXCLUSIVE RISK. The original developer (Chang) assumes no legal, moral, or technical liability for bans, account loss, or damages derived from the use of this script. Furthermore, it is explicitly declared that this project is strictly for educational/experimental software engineering purposes and holds absolutely no affiliation, sponsorship, partnership, or commercial connection with Flyff Universe, Gala Lab Corp, or any of their subsidiaries and official developers.
---
