<div align="center">

# [cite_start]🛠️ TECHNICAL MANUAL & SPECIFICATIONS: SENTINEL ELITE (v5.0) [cite: 1]

</div>

---

## 📖 Introduction
[cite_start]Welcome to the official technical documentation for Sentinel Elite[cite: 1]. [cite_start]This is not a simple macro recorder; it is an advanced automation system based on Message Passing Interface (CDP) and Computer Vision[cite: 2]. [cite_start]Strictly follow this guide to ensure error-free execution and runtime stability[cite: 3].

---

## 🏗️ 1. SYSTEM ARCHITECTURE & REQUIREMENTS
* [cite_start]**Mandatory Browser:** Google Chrome[cite: 3].
* [cite_start]**OCR Engine:** The bot uses `Tesseract-OCR` bundled with `OpenCV` to convert the game's render stream into readable text arrays[cite: 4].
* [cite_start]**⚠️ STRICT INSTALLATION PATH:** You MUST install Tesseract exactly at this absolute path: `C:\Program Files\Tesseract-OCR\tesseract.exe`[cite: 5]. [cite_start]Any deviation will throw main-thread exceptions and permanently blind the bot[cite: 6].

---

## ⚙️ 2. DEBUGGING ENVIRONMENT SETUP (CDP PORT)
[cite_start]*Technical Explanation:* Browsers freeze background tab threads to optimize memory[cite: 7]. [cite_start]To prevent Chromium's rendering engine from halting when tabbed out, we must execute Chrome with a local debugging port and background throttling disabled[cite: 8].

**Step-by-Step Execution:**
1.  [cite_start]Navigate to your Desktop -> Right-click -> "New" -> "Shortcut"[cite: 9].
2.  [cite_start]In the "Target" field, paste EXACTLY this execution argument[cite: 9]:
    `"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\ChromeBotFlyff" --remote-allow-origins=* --disable-backgrounding-occluded-windows --disable-renderer-backgrounding --disable-background-timer-throttling`
3.  Kill all previous Chrome instances in Task Manager[cite: 9].
4.  Open the game solely from this shortcut and log in with your Ringmaster (RM) only[cite: 10].

---

## 🖥️ 3. CLIENT PARAMETERIZATION (IN-GAME)
* [cite_start]**Rendering (Mandatory):** Press F11 (Full Screen)[cite: 11]. [cite_start]GUI coordinate vectors shift in windowed mode, breaking calibration arrays[cite: 11].
* [cite_start]**UI Scaling:** In Options -> Interface, Increase UI size to MAXIMUM[cite: 12]. [cite_start]This increases font pixel density, reducing `OpenCV`/`Tesseract` algorithmic errors to 0%[cite: 13].
* **Hotbar Mapping Protocol:**
    * [cite_start]**F1 Bar (Buffs):** Slots 1 to 0 are exclusively reserved for Buffs[cite: 14].
    * [cite_start]**F2 Bar (Survival):** Slot 1 = Heal, Slot 2 = HP Potion, Slot 3 = MP Potion[cite: 15].
    * [cite_start]**Follow Key:** Verify your "Follow" keycode (Default: Z)[cite: 16].

---

## 🎯 4. VECTOR CONFIGURATION (CALIBRATION)
[cite_start]Start the bot, click "🔄 Fetch" and select the RM tab endpoint[cite: 16]. [cite_start]You must accurately define the target variable string (Main DPS name)[cite: 17].

* [cite_start]**🕹️ STEP A (OCR Array Validation):** Move the Party frame to the BOTTOM LEFT and enable side party bars[cite: 17, 18]. [cite_start]Click "Step A"[cite: 18]. [cite_start]The system fetches an internal Base64 screenshot, applies grayscale/inverse binarization, and matches your target string[cite: 18].
* [cite_start]**❤️ STEP B (Main HP Pixel Mapping):** Click your Main in-game (static top-center bar)[cite: 19]. [cite_start]Click "Step B", and within 5s place the pointer on the red section[cite: 20]. [cite_start]The bot will cyclically read the Red Channel (R) array of that pixel[cite: 21].
* [cite_start]**❌ STEP C ('X' Coordinate Mapping):** With the static bar still up, click "Step C" and place the pointer on the 'X' button[cite: 22]. [cite_start]This triggers a direct DOM `Input.dispatchMouseEvent`, safely clearing the target without hardware key hooks[cite: 23].
* [cite_start]**🛡️ STEP D & E (RM HP/MP Mapping):** Repeat the process to log RGB vectors for YOUR OWN Health (Red Channel) and Mana (Blue Channel) bars located top-left[cite: 24].

---

## [cite_start]🩺 5. TROUBLESHOOTING (F.A.Q.) [cite: 25]

**Q: Can the bot run in the background?**
> [cite_start]**A:** Yes[cite: 25]. [cite_start]Via WebSockets (CDP Protocol), payloads are injected directly into the browser engine[cite: 26].
> [cite_start]**⚠️ ABSOLUTE LAW!:** The RM tab must remain in F11[cite: 27]. [cite_start]To manage other windows, use `Alt + Tab`[cite: 27]. If you drop F11 or minimize the RM by clicking the taskbar, the graphic engine stops frame painting; [cite_start]RGB channel polling will return exceptions and halt the thread[cite: 28, 29].

[cite_start]**Q: Why does Step A (OCR) fail or the RM heals itself by mistake? [cite: 30]**
> **A:** This usually happens due to one of three reasons: 
> (1) [cite_start]UI scale is not maximized[cite: 31]. 
> (2) [cite_start]String discrepancy (Bot vs Game, case-sensitive)[cite: 31]. 
> (3) [cite_start]You mapped Step B over the dynamic Party HUD instead of the static center-top target frame[cite: 32].

---

## [cite_start]⚖️ 6. SECURITY DISCLAIMER & LEGAL NOTICE [cite: 33]

### 🔓 Open Source & Privacy
[cite_start]SENTINEL ELITE is 100% free, Open Source software[cite: 34]. [cite_start]**IT IS NOT A VIRUS**, it features zero keylogging routines and no network modules for remote data extraction[cite: 34]. [cite_start]All communication happens purely via the local debugging port (`http://localhost:9222`)[cite: 35]. [cite_start]For your machine's integrity, ALWAYS download from Chang's official GitHub repo; do not accept third-party executables[cite: 36].

### 💉 Injection Mechanism & Anti-Cheat
[cite_start]This software DOES NOT read or write to RAM allocated to the game client[cite: 37]. [cite_start]It injects no DLLs nor uses Windows memory manipulation APIs (like `WriteProcessMemory`)[cite: 38]. [cite_start]It functions via screen analysis and virtual hardware dispatch via Chrome[cite: 39]. [cite_start]Therefore, on a technical level, it is practically "undetectable" by standard Anti-Cheat signatures (GameGuard, XignCode, etc)[cite: 40].

### 🚨 Suspension Risk (Heuristics)
[cite_start]The use of macros, bots, and third-party automation tools is a direct violation of the Flyff Universe Terms of Service (ToS)[cite: 41]. [cite_start]Even if the software leaves the client uncompromised, Game Masters possess heuristic detection tools (behavioral analysis)[cite: 42]. [cite_start]If you leave the bot 24/7 unsupervised, loop exact time intervals, or get recorded and reported by players, your account will be permanently banned[cite: 43].

### 📜 Liability Waiver
[cite_start]You are compiling and utilizing this tool at **YOUR SOLE AND EXCLUSIVE RISK**[cite: 44]. [cite_start]The original developer (Chang) assumes no legal, moral, or technical liability for bans, account loss, or damages derived from the use of this script[cite: 45]. [cite_start]Furthermore, it is explicitly declared that this project is strictly for educational/experimental software engineering purposes and holds absolutely no affiliation, sponsorship, partnership, or commercial connection with Flyff Universe, Gala Lab Corp, or any of their subsidiaries and official developers[cite: 46].
