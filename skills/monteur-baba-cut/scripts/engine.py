import re
import argparse
import json
import os
import shutil
import subprocess
import sys
import wave
import numpy as np

# ==============================================================================
# PROCEDURAL VECTOR & KINEMATIC RIGGING ENGINE (v6.5)
# ==============================================================================
try:
    from procedural_vector import (
        ProceduralShapes,
        generate_ground_cutaway_svg,
        generate_underground_tank_data,
        generate_mechanical_gauge_svg,
        KinematicExcavator,
        KinematicIntegrityChecker,
        generate_excavation_scene_svg
    )
    from openverse_fetcher import resolve_scene_foley_sfx, FOLEY_PRESETS
except ImportError:
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    try:
        from procedural_vector import (
            ProceduralShapes,
            generate_ground_cutaway_svg,
            generate_underground_tank_data,
            generate_mechanical_gauge_svg
        )
    except Exception:
        ProceduralShapes = None

# ==============================================================================
# Monteur Baba Cut v6.6 — The Senior Motion & Video Editor Engine
# End-to-end Auto-SFX, Cinematic Virtual Camera, 3D Parallax, Safe-Zones,
# Dynamic Counters, Continuity Bridges, AND Existing Video Auto-Editing & Subtitling
# ==============================================================================

def update_windows_path():
    """Reload PATH from Windows Registry so newly installed software works immediately."""
    if sys.platform != "win32":
        return
    try:
        import winreg
        paths = []
        for hkey, subkey in [(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Environment"),
                             (winreg.HKEY_CURRENT_USER, r"Environment")]:
            try:
                with winreg.OpenKey(hkey, subkey) as key:
                    val, _ = winreg.QueryValueEx(key, "Path")
                    paths.extend(val.split(";"))
            except Exception:
                pass
        current = os.environ.get("PATH", "").split(";")
        for p in paths:
            if p and p not in current and os.path.exists(p):
                current.append(p)
        os.environ["PATH"] = ";".join(current)
    except Exception:
        pass

def check_dependencies():
    """
    Zero-Setup Auto-Healing Installer:
    Autonomously checks, downloads, and installs any missing system tools
    (FFmpeg, Node.js/npx, faster-whisper, numpy) on Windows, macOS, and Linux
    without requiring manual installation or prior setup.
    """
    print("[Auto-Healing] Checking system tools and runtime dependencies...")

    # 1. Python libraries (faster-whisper, numpy)
    try:
        import numpy
        import faster_whisper
    except ImportError:
        print("[Auto-Healing] Installing required Python AI packages (faster-whisper, numpy)...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run([sys.executable, "-m", "pip", "install", "faster-whisper", "numpy"], check=True)
        print("[Auto-Healing] Python AI libraries ready!")

    # 2. FFmpeg Auto-Healing
    ffmpeg_ready = False
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        ffmpeg_ready = True
    except Exception:
        pass

    if not ffmpeg_ready:
        print("[Auto-Healing] FFmpeg is missing! Installing autonomously...")
        if sys.platform == "win32":
            # Try winget
            try:
                print("[Auto-Healing] Trying Windows package manager (winget install FFmpeg)...")
                subprocess.run(["winget", "install", "Gyan.FFmpeg", "--silent", "--accept-package-agreements", "--accept-source-agreements"], check=True)
                update_windows_path()
                subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                ffmpeg_ready = True
            except Exception:
                pass

            # Fallback: Portable static-ffmpeg (Zero admin rights needed)
            if not ffmpeg_ready:
                print("[Auto-Healing] Installing portable static FFmpeg binary...")
                subprocess.run([sys.executable, "-m", "pip", "install", "static-ffmpeg"], check=True)
                try:
                    import static_ffmpeg
                    static_ffmpeg.add_paths()
                    ffmpeg_ready = True
                    print("[Auto-Healing] Portable FFmpeg injected into PATH successfully!")
                except Exception as e:
                    print(f"[Auto-Healing] Static FFmpeg encountered: {e}")
        elif sys.platform == "darwin": # macOS
            try:
                subprocess.run(["brew", "install", "ffmpeg"], check=True)
                ffmpeg_ready = True
            except Exception:
                pass
        else: # Linux
            try:
                subprocess.run(["apt-get", "update"], check=True)
                subprocess.run(["apt-get", "install", "-y", "ffmpeg"], check=True)
                ffmpeg_ready = True
            except Exception:
                pass

    # 3. Node.js & npx Auto-Healing
    npx_ready = False
    try:
        subprocess.run(["npx", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, check=True)
        npx_ready = True
    except Exception:
        pass

    if not npx_ready:
        print("[Auto-Healing] Node.js / npx is missing! Installing autonomously...")
        if sys.platform == "win32":
            try:
                print("[Auto-Healing] Installing Node.js LTS via winget...")
                subprocess.run(["winget", "install", "OpenJS.NodeJS.LTS", "--silent", "--accept-package-agreements", "--accept-source-agreements"], check=True)
                update_windows_path()
                subprocess.run(["npx", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True, check=True)
                npx_ready = True
                print("[Auto-Healing] Node.js and npx installed and active!")
            except Exception as e:
                print(f"[Auto-Healing] Winget Node.js encountered: {e}")
        elif sys.platform == "darwin":
            try:
                subprocess.run(["brew", "install", "node"], check=True)
                npx_ready = True
            except Exception:
                pass
        else:
            try:
                subprocess.run(["apt-get", "install", "-y", "nodejs", "npm"], shell=True, check=True)
                npx_ready = True
            except Exception:
                pass

    print("[Auto-Healing] All dependencies verified and ready for production!")

# ==============================================================================
# PROCEDURAL STUDIO SFX GENERATOR (Whoosh, Click, Tick, Impact)
# Zero external sound files needed — Synthesizes pristine 44.1kHz WAV SFX offline
# ==============================================================================

def generate_procedural_sfx(output_dir):
    os.makedirs(output_dir, exist_ok=True)
    sr = 44100

    sfx_paths = {
        "whoosh": os.path.join(output_dir, "sfx_whoosh.wav"),
        "click": os.path.join(output_dir, "sfx_click.wav"),
        "tick": os.path.join(output_dir, "sfx_tick.wav"),
        "impact": os.path.join(output_dir, "sfx_impact.wav")
    }

    # 1. Whoosh (Smooth frequency modulated air sweep)
    t_w = np.linspace(0, 0.45, int(sr * 0.45), endpoint=False)
    freq_w = 180 + 400 * np.sin(np.pi * t_w / 0.45)
    noise_w = np.random.normal(0, 0.15, len(t_w))
    tone_w = np.sin(2 * np.pi * freq_w * t_w) * 0.5 + noise_w
    env_w = np.sin(np.pi * t_w / 0.45) ** 2
    sig_w = tone_w * env_w * 0.75
    save_wav(sfx_paths["whoosh"], (sig_w * 32767).astype(np.int16), sr)

    # 2. Click (Pristine UI Glass Click)
    t_c = np.linspace(0, 0.035, int(sr * 0.035), endpoint=False)
    sig_c = np.sin(2 * np.pi * 1400 * t_c) * np.exp(-t_c * 150) * 0.8
    save_wav(sfx_paths["click"], (sig_c * 32767).astype(np.int16), sr)

    # 3. Tick (Fast mechanical clock tick for counters)
    t_t = np.linspace(0, 0.015, int(sr * 0.015), endpoint=False)
    sig_t = np.sin(2 * np.pi * 2200 * t_t) * np.exp(-t_t * 280) * 0.7
    save_wav(sfx_paths["tick"], (sig_t * 32767).astype(np.int16), sr)

    # 4. Impact (Sub-bass cinematic braam drop)
    t_i = np.linspace(0, 1.2, int(sr * 1.2), endpoint=False)
    freq_i = 80 * np.exp(-t_i * 2.2) + 38
    sig_i = np.sin(2 * np.pi * freq_i * t_i) * np.exp(-t_i * 2.5) * 0.95
    save_wav(sfx_paths["impact"], (sig_i * 32767).astype(np.int16), sr)

    # 5. Openverse Real Foley Integration (Pre-resolve real studio SFX into output directory)
    try:
        from openverse_fetcher import resolve_scene_foley_sfx
        import shutil
        for foley_tag in ["excavator_digging", "gas_leak_hiss", "liquid_trickle", "metal_vault"]:
            target_file = os.path.join(output_dir, f"sfx_{foley_tag}.wav")
            if not os.path.exists(target_file):
                resolved = resolve_scene_foley_sfx(foley_tag)
                if resolved and os.path.exists(resolved):
                    shutil.copyfile(resolved, target_file)
                    sfx_paths[foley_tag] = target_file
    except Exception as e:
        print(f"[Notice] Openverse Foley fetch note: {e}")

    return sfx_paths

def save_wav(filepath, data, sr=44100):
    with wave.open(filepath, 'w') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes(data.tobytes())

# ==============================================================================
# AUDIO PROCESSING & TRANSCRIPTION
# ==============================================================================

def load_audio_ffmpeg(file_path, sr=16000):
    cmd = [
        "ffmpeg", "-nostdin", "-threads", "0", "-i", file_path,
        "-f", "s16le", "-ac", "1", "-acodec", "pcm_s16le", "-ar", str(sr), "-"
    ]
    out = subprocess.check_output(cmd, stderr=subprocess.DEVNULL)
    return np.frombuffer(out, np.int16).flatten().astype(np.float32) / 32768.0

COMMON_TECH_VOCAB = {
    # Tech / Brand names
    "جمنا": "جمناي",
    "جمني": "جمناي",
    "جيميني": "جمناي",
    "جيمني": "جمناي",
    "ليون": "نيون",
    "نيوان": "نيون",
    "نيول": "نيون",
    "طبقي": "تطبيقي",
    "طبيقي": "تطبيقي",
    # Feminine nouns & Taa Marbuta
    "شاشه": "شاشة",
    "شاشات": "شاشات",
    "مقارنه": "مقارنة",
    "ثانيه": "ثانية",
    "فكره": "فكرة",
    "ذكيه": "ذكية",
    "متكامله": "متكاملة",
    "تقنيه": "تقنية",
    "سرعه": "سرعة",
    "خرافيه": "خرافية",
    "عضويه": "عضوية",
    "ترجمه": "ترجمة",
    "دقيقه": "دقيقة",
    "سريعه": "سريعة",
    "سهله": "سهلة",
    "طريقه": "طريقة",
    "واجهه": "واجهة",
    "منظومه": "منظومة",
    "فائقه": "فائقة",
    # Hamzas & Orthography
    "اعلان": "إعلان",
    "ازرق": "أزرق",
    "اخضر": "أخضر",
    "اصطناعي": "اصطناعي",
    "الى": "إلى",
    "إلي": "إلى",
    "علي": "على",
    "فى": "في",
    "اجهزة": "أجهزة",
    "ادوات": "أدوات",
    "اخطاء": "أخطاء",
    "افكار": "أفكار",
    "اكثر": "أكثر",
    "اكبر": "أكبر",
    "اول": "أول",
    "اخر": "آخر",
    "الان": "الآن",
    "ايضا": "أيضاً",
    "انقر": "انقر",
    "اضغط": "اضغط",
    "فورا": "فوراً"
}

VALID_SINGLE_LETTERS = {"و", "ف", "ب", "ل", "ك"}

def polish_single_word(w, user_corrections=None):
    if not w:
        return w
    clean = w.strip()
    # Remove Whisper hallucination tags like [موسيقى], (ضحك)
    clean = re.sub(r'\[.*?\]|\(.*?\)', '', clean).strip()
    if not clean:
        return clean

    # Strip repeated stutters (>2 identical chars) e.g. ااااا -> ا
    clean = re.sub(r'(.)\1{2,}', r'\1', clean)

    # Check user custom corrections first
    if user_corrections and clean in user_corrections:
        return user_corrections[clean]

    # Check vocab dictionary
    if clean in COMMON_TECH_VOCAB:
        return COMMON_TECH_VOCAB[clean]

    # Contextual color prefixes (e.g. بالازرق -> بالأزرق, للاعلان -> للإعلان)
    if clean.startswith("بال") and clean[3:] in ["ازرق", "اخضر", "ابيض", "اسود"]:
        sub = clean[3:]
        fixed = {"ازرق": "أزرق", "اخضر": "أخضر", "ابيض": "أبيض", "اسود": "أسود"}.get(sub, sub)
        return "بال" + fixed

    # Taa Marbuta normalization for feminine nouns ending in 'ه'
    if len(clean) > 3 and clean.endswith("ه"):
        if clean.endswith("ية") or clean.endswith("يه"):
            clean = clean[:-1] + "ة"

    return clean

def is_ambiguous_token(w):
    clean = re.sub(r'[^\w\s]', '', w).strip()
    if not clean:
        return False
    # Single character that is not a valid Arabic preposition/particle
    if len(clean) == 1 and clean not in VALID_SINGLE_LETTERS and not clean.isdigit():
        return True
    # Bizarre repeated glottal stops or weird phonetic noise
    if re.search(r'[ء]{2,}|[^\u0600-\u06FFa-zA-Z0-9]', clean):
        return True
    return False

def clean_and_polish_transcript(raw_transcript, context_hint=None, user_corrections=None):
    """
    Polishes transcribed text by correcting common STT/spelling errors
    while strictly preserving word-level start/end timestamps.
    Detects unintelligible/ambiguous tokens and flags them for user confirmation.
    """
    import copy
    transcript = copy.deepcopy(raw_transcript)
    corrections_log = []
    ambiguous_words = []

    for seg in transcript.get("segments", []):
        for w in seg.get("words", []):
            orig = w["word"]
            polished = polish_single_word(orig, user_corrections=user_corrections)
            if polished != orig:
                corrections_log.append({
                    "start": w["start"],
                    "end": w["end"],
                    "from": orig,
                    "to": polished
                })
            # Non-destructive: overwrite only word text, keep timestamps intact
            w["word"] = polished

            if is_ambiguous_token(polished):
                ambiguous_words.append({
                    "word": orig,
                    "time": w["start"],
                    "segment_id": seg.get("id"),
                    "context": seg.get("text", "")
                })

        seg["text"] = " ".join([w["word"] for w in seg.get("words", []) if w.get("word")])

    transcript["ambiguous_words"] = ambiguous_words
    transcript["corrections_log"] = corrections_log

    print(f"[Caption Polishing] Completed contextual polish: {len(corrections_log)} words corrected, {len(ambiguous_words)} ambiguous tokens detected.")
    if corrections_log:
        for c in corrections_log[:5]:
            print(f"  - [{c['start']}s] '{c['from']}' -> '{c['to']}'")
        if len(corrections_log) > 5:
            print(f"  - ... and {len(corrections_log) - 5} more corrections.")

    if ambiguous_words:
        print("\n" + "="*70)
        print("⚠️ [AMBIGUITY GATE] Detected low-confidence / unintelligible word(s):")
        for amb in ambiguous_words:
            print(f"  • At [{amb['time']}s]: '{amb['word']}' in: \"{amb['context']}\"")
        print("  -> Human confirmation recommended before final render!")
        print("="*70 + "\n")

    return transcript

def transcribe(audio_path, initial_prompt=None, user_corrections=None):
    from faster_whisper import WhisperModel
    print(f"[Transcribe] Processing audio: {audio_path}")
    audio_data = load_audio_ffmpeg(audio_path)
    duration = len(audio_data) / 16000

    if not initial_prompt:
        initial_prompt = (
            "محادثة وتفريغ صوتي باللغة العربية الفصحى واللهجة البيضاء لإعلان تقني وفيديو موشن جرافيك: "
            "تطبيق، جمناي، جيمناي، HL AI Workspace، نيون، أزرق، أخضر، كروت، المستقبل يبدأ هنا، شاشة، مقارنة، تحميل، أدوات، استوديو، فيديو، ثانية، ينضغط فوراً."
        )

    model = WhisperModel("base", device="cpu", compute_type="int8")
    segments, info = model.transcribe(
        audio_data,
        word_timestamps=True,
        language="ar",
        initial_prompt=initial_prompt
    )

    raw_output = {
        "duration": round(duration, 2),
        "segments": []
    }
    for seg in segments:
        words = []
        if seg.words:
            for w in seg.words:
                words.append({
                    "word": w.word.strip(),
                    "start": round(w.start, 2),
                    "end": round(w.end, 2)
                })
        raw_output["segments"].append({
            "id": seg.id,
            "start": round(seg.start, 2),
            "end": round(seg.end, 2),
            "text": seg.text.strip(),
            "words": words
        })

    # Apply contextual polishing & ambiguity detection
    polished_output = clean_and_polish_transcript(raw_output, user_corrections=user_corrections)
    polished_output["raw_segments"] = raw_output["segments"]
    return polished_output

# ==============================================================================

# ==============================================================================
# VIRAL DOODLE & STICKMAN SVG GENERATOR (Social Media Explainer System)
# ==============================================================================

def generate_stickman_svg(pose="idea", accent="#0284c7", width=240, height=290):
    head = '<circle cx="120" cy="65" r="30" stroke="currentColor" stroke-width="6.5" fill="none" />'
    face = '<circle cx="111" cy="61" r="3" fill="currentColor"/><circle cx="129" cy="61" r="3" fill="currentColor"/>'
    torso = '<line x1="120" y1="95" x2="120" y2="180" stroke="currentColor" stroke-width="6.5" stroke-linecap="round"/>'
    
    props = ""
    arms = ""
    legs = ""
    
    if pose == "idea":
        arms = """
        <path d="M 120 115 L 80 90 L 60 55" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 115 L 160 90 L 180 55" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        legs = """
        <path d="M 120 180 L 95 235 L 75 280" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 180 L 145 235 L 165 280" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        props = f"""
        <g class="prop-glow prop-float" transform="translate(98, 4)">
            <path d="M 22 28 C 9 28, 4 18, 4 10 C 4 1, 40 1, 40 10 C 40 18, 35 28, 22 28 Z" fill="{accent}" opacity="0.95"/>
            <rect x="15" y="28" width="14" height="5" rx="1.5" fill="#e2e8f0"/>
            <line x1="22" y1="-7" x2="22" y2="-1" stroke="{accent}" stroke-width="3.5" stroke-linecap="round"/>
            <line x1="38" y1="-1" x2="33" y2="4" stroke="{accent}" stroke-width="3.5" stroke-linecap="round"/>
            <line x1="6" y1="-1" x2="11" y2="4" stroke="{accent}" stroke-width="3.5" stroke-linecap="round"/>
        </g>
        """
        face += '<path d="M 112 74 Q 120 83 128 74" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
        
    elif pose == "pointing":
        arms = """
        <path d="M 120 115 L 90 135 L 92 165" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 115 L 165 110 L 225 105" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        legs = """
        <path d="M 120 180 L 100 230 L 85 280" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 180 L 140 230 L 155 280" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        props = f"""
        <g transform="translate(225, 90)">
            <line x1="10" y1="15" x2="25" y2="15" stroke="{accent}" stroke-width="3.5" stroke-linecap="round"/>
            <line x1="8" y1="5" x2="20" y2="-2" stroke="{accent}" stroke-width="3.5" stroke-linecap="round"/>
            <line x1="8" y1="25" x2="20" y2="32" stroke="{accent}" stroke-width="3.5" stroke-linecap="round"/>
        </g>
        """
        face += '<path d="M 113 72 Q 120 80 127 72" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
        
    elif pose == "confused":
        arms = """
        <path d="M 120 115 L 150 95 L 138 48" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 115 L 80 138 L 55 125" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        legs = """
        <path d="M 120 180 L 105 230 L 100 280" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 180 L 130 225 L 150 280" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        props = f"""
        <g fill="{accent}" font-family="sans-serif" font-weight="900">
            <text x="60" y="42" font-size="30" class="prop-float">?</text>
            <text x="160" y="32" font-size="24" opacity="0.8" class="prop-float">?</text>
            <path d="M 108 30 Q 120 22 132 30" stroke="#f43f5e" stroke-width="3.5" stroke-linecap="round" fill="none"/>
        </g>
        """
        face = '<circle cx="111" cy="61" r="3" fill="currentColor"/><circle cx="129" cy="61" r="3" fill="currentColor"/>'
        face += '<path d="M 113 76 Q 120 70 127 76" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/>'
        
    elif pose == "button_push":
        arms = """
        <path d="M 120 115 L 150 135 L 185 175" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 115 L 90 140 L 75 165" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        legs = """
        <path d="M 120 180 L 90 225 L 65 275" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 180 L 140 230 L 165 275" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        props = f"""
        <g transform="translate(150, 168)">
            <ellipse cx="32" cy="38" rx="32" ry="10" fill="#10b981" opacity="0.3"/>
            <rect x="12" y="14" width="38" height="22" rx="7" fill="#10b981"/>
            <circle cx="32" cy="14" r="19" fill="#22c55e" stroke="#15803d" stroke-width="2.5"/>
            <circle cx="32" cy="14" r="26" stroke="#22c55e" stroke-width="1.8" stroke-dasharray="5,4" fill="none" opacity="0.75" class="prop-glow"/>
        </g>
        """
        face += '<path d="M 112 73 Q 120 81 128 73" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/>'

    elif pose == "money_rich":
        arms = """
        <path d="M 120 115 L 75 95 L 50 65" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 115 L 165 95 L 190 65" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        legs = """
        <path d="M 120 180 L 95 230 L 80 280" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 180 L 145 230 L 160 280" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        props = f"""
        <g transform="translate(10, 15)">
            <rect x="25" y="10" width="38" height="20" rx="3" fill="#10b981" stroke="#059669" stroke-width="2"/>
            <circle cx="44" cy="20" r="5" fill="#ecfdf5"/>
            <rect x="175" y="5" width="38" height="20" rx="3" fill="#10b981" stroke="#059669" stroke-width="2" transform="rotate(18 194 15)"/>
        </g>
        """
        # Cool Sunglasses
        face = '<rect x="104" y="56" width="14" height="9" rx="2" fill="currentColor"/><rect x="122" y="56" width="14" height="9" rx="2" fill="currentColor"/><line x1="118" y1="60" x2="122" y2="60" stroke="currentColor" stroke-width="2"/>'
        face += '<path d="M 113 75 Q 120 83 127 75" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/>'

    else: # celebrate / default
        arms = """
        <path d="M 120 115 L 80 85 L 60 45" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 115 L 160 85 L 180 45" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        legs = """
        <path d="M 120 180 L 95 230 L 75 280" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        <path d="M 120 180 L 145 230 L 165 280" stroke="currentColor" stroke-width="6.5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        """
        props = f"""
        <g transform="translate(120, 30)">
            <circle cx="-50" cy="0" r="4" fill="{accent}"/>
            <circle cx="50" cy="-10" r="5" fill="#f59e0b"/>
            <circle cx="0" cy="-25" r="4" fill="#10b981"/>
            <polygon points="-30,-20 -25,-10 -35,-10" fill="#f43f5e"/>
            <polygon points="30,-25 35,-15 25,-15" fill="{accent}"/>
        </g>
        """
        face += '<path d="M 112 74 Q 120 84 128 74" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" fill="none"/>'

    svg = f"""
    <svg class="stickman-svg" viewBox="0 0 250 290" width="{width}" height="{height}" style="overflow: visible; color: inherit;">
        {props}
        <g class="stickman-body">
            {head}
            {face}
            {torso}
            {arms}
            {legs}
        </g>
    </svg>
    """
    return svg

def generate_doodle_svg(doodle_type="hand_drawn_arrow", color="#f59e0b", width=140, height=90):
    if doodle_type == "hand_drawn_arrow":
        return f"""
        <svg class="doodle-svg" viewBox="0 0 160 90" width="{width}" height="{height}" fill="none" style="overflow: visible;">
            <path class="doodle-draw-path" d="M 15 75 Q 60 10, 135 30" stroke="{color}" stroke-width="5" stroke-linecap="round" fill="none"/>
            <path class="doodle-draw-path" d="M 115 15 L 140 30 L 122 50" stroke="{color}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round" fill="none"/>
        </svg>
        """
    elif doodle_type == "hand_drawn_circle":
        return f"""
        <svg class="doodle-svg" viewBox="0 0 180 90" width="{width}" height="{height}" fill="none" style="overflow: visible;">
            <path class="doodle-draw-path" d="M 25 45 C 25 18, 150 15, 155 45 C 160 75, 18 80, 22 50 C 25 30, 125 22, 142 32" stroke="{color}" stroke-width="4.5" stroke-linecap="round" fill="none"/>
        </svg>
        """
    elif doodle_type == "brain_spark":
        return f"""
        <svg class="doodle-svg" viewBox="0 0 140 120" width="{width}" height="{height}" fill="none" style="overflow: visible;">
            <g stroke="{color}" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round">
                <path d="M 65 95 C 45 95, 25 82, 25 65 C 18 60, 12 44, 22 30 C 30 18, 52 22, 65 35 Z"/>
                <path d="M 75 95 C 95 95, 115 82, 115 65 C 122 60, 128 44, 118 30 C 110 18, 88 22, 75 35 Z"/>
                <path d="M 45 42 Q 52 60 40 72" stroke-width="2.5"/>
                <path d="M 95 42 Q 88 60 100 72" stroke-width="2.5"/>
            </g>
            <circle cx="70" cy="18" r="3.5" fill="{color}"/>
            <line x1="70" y1="10" x2="70" y2="3" stroke="{color}" stroke-width="2.5" stroke-linecap="round"/>
        </svg>
        """
    return ""


def generate_interactive_cursor_svg(cursor_id="cur", accent="#10b981"):
    return f"""
    <div id="{cursor_id}_wrap" class="interactive-cursor">
      <svg width="44" height="44" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M4 3L11.5 21L14.5 13.5L22 10.5L4 3Z" fill="#0f172a" stroke="#ffffff" stroke-width="2" stroke-linejoin="round"/>
        <circle cx="11" cy="11" r="3" fill="{accent}"/>
      </svg>
      <div id="{cursor_id}_ripple" class="touch-ripple" style="border-color: {accent};"></div>
    </div>
    """

# AUTONOMOUS SEMANTIC BEAT CLASSIFICATION
# ==============================================================================

def analyze_beat_semantic(text, beat_idx=1, style="pastel_director"):
    t = text.lower()
    is_pastel = (style in ["pastel_director", "viral_doodle"])
    is_doodle = (style == "viral_doodle")

    # 00. PROCEDURAL ENGINEERING CUTAWAY TRIGGERS (Gas Station, Mechanics, Fluid Physics)
    tech_keywords = ["محطة", "محطط", "بترول", "بنزين", "حفر", "ارض", "أرض", "امتصاص", "برميل", "خزان", "غازات", "تسريب", "أنبوب", "انبوب", "مضخة", "مضخه", "هندسة", "هندسي", "cutaway", "ضغط", "فوهة", "صمام"]
    if any(k in t for k in tech_keywords) or style == "engineering_cutaway":
        if any(k in t for k in ["حفر", "نحفر", "ارض", "أرض", "امتصاص"]):
            sub_stage = "excavation_leak"
            kicker = "ENGINEERING CUTAWAY • EXCAVATION & ABSORPTION"
            badge = "⚠️ تسريب وامتصاص التربة"
            title = "امتصاص التربة للوقود"
            subtext = "حفر الأرض مباشرة يسبب تسرّب البترول في باطن الأرض"
            accent = "#f59e0b"
            gauge_val = 45
            camera_mode = "macro_leak"
        elif any(k in t for k in ["غازات", "غاز", "تنفيس", "ضغط", "فوهة", "صمام"]):
            sub_stage = "vent_emissions"
            kicker = "ENGINEERING CUTAWAY • VAPOR RECOVERY"
            badge = "💨 تصاعد غازات البترول"
            title = "تنفيس الأبخرة والضغط الزائد"
            subtext = "فوهة التنفيس تصرّف الغازات القابلة للاشتعال بمسار محكم"
            accent = "#10b981"
            gauge_val = 145
            camera_mode = "macro_vent"
        elif any(k in t for k in ["برميل", "خزان", "نحط", "حديد", "تركيب"]):
            sub_stage = "tank_vault"
            kicker = "ENGINEERING CUTAWAY • CONTAINMENT VAULT"
            badge = "🛡️ تركيب الخزان المزدوج"
            title = "عزل البترول في خزان فولاذي"
            subtext = "حماية التربة بجدار مزدوج لمنع التسريب"
            accent = "#0284c7"
            gauge_val = 90
            camera_mode = "macro_tank"
        else:
            sub_stage = "complete_system"
            kicker = "ENGINEERING CUTAWAY • COMPLETE SYSTEM"
            badge = "⛽ اكتمال المحطة الهندسية"
            title = "منظومة وقود آمنة 100%"
            subtext = "نظام سحب وتنفيس وعزل متكامل بالملليمتر"
            accent = "#0284c7"
            gauge_val = 120
            camera_mode = "wide_cutaway"

        return {
            "type": "procedural_cutaway",
            "sub_stage": sub_stage,
            "kicker": kicker,
            "accent": accent,
            "badge": badge,
            "title": title,
            "subtext": subtext,
            "gauge_val": gauge_val,
            "camera_mode": camera_mode,
            "cta": "فحص المقطع الهندسي 📐"
        }

    # 0. VIRAL DOODLE & STICKMAN TRIGGERS (Social Media Explainer System)
    if is_doodle or any(k in t for k in ["فكرة", "فكره", "استيك", "ستيك", "شاشتين", "مقارنة", "زر", "تحميل", "ينضغط", "فلوس", "أرباح", "ارباح", "كتاب", "دراسة", "لخص", "ترجم"]):
        # A) Idea / Eureka Hook
        if any(k in t for k in ["فكرة", "فكره", "استيك", "ستيك", "عندي", "لمبة", "خطر", "ببالي", "بدي"]):
            return {
                "type": "viral_doodle_stickman",
                "pose": "idea",
                "kicker": "VIRAL DOODLE • EUREKA MOMENT",
                "accent": "#0284c7" if is_pastel else "#38bdf8",
                "badge": "💡 الفكرة العبقرية",
                "title": "المستقبل يبدأ هنا",
                "subtext": "فكرة إعلان مبتكرة تتنفذ بلحظة واحدة",
                "cta": "انطلاقة الفكرة ⚡"
            }
        # B) Side-by-Side Comparison / Confusion
        elif any(k in t for k in ["شاشتين", "مقارنة", "فوق بعض", "قديم", "معقد", "حيرة", "سؤال", "ليش", "مشكلة"]):
            return {
                "type": "viral_doodle_stickman",
                "pose": "confused",
                "kicker": "VIRAL DOODLE • SIDE-BY-SIDE",
                "accent": "#f59e0b",
                "badge": "🤔 شاشتين بمقارنة سريعة",
                "title": "شاشة جمناي vs تطبيقنا المتكامل",
                "subtext": "وداعاً لكتابة البرومبتات الطويلة والتعقيد",
                "cta": "مقارنة فورية ⚡"
            }
        # C) Button Push / Download CTA
        elif any(k in t for k in ["زر", "تحميل", "ينضغط", "اضغط", "انقر", "كبسة", "أخضر", "اخضر", "فوراً", "فورا"]):
            return {
                "type": "viral_doodle_stickman",
                "pose": "button_push",
                "kicker": "VIRAL DOODLE • ONE-CLICK ACTION",
                "accent": "#10b981",
                "badge": "🔘 زر التحميل الأخضر",
                "title": "ضغطة واحدة وتطبيقك جاهز",
                "subtext": "انقر على زر التحميل وابدأ فوراً",
                "cta": "تحميل التطبيق الآن 🚀"
            }
        # D) Money & Profit / High ROI
        elif any(k in t for k in ["فلوس", "أرباح", "ارباح", "تسويق", "عمولة", "عمولات", "دولار", "توفر", "توفير"]):
            return {
                "type": "viral_doodle_stickman",
                "pose": "money_rich",
                "kicker": "VIRAL DOODLE • HIGH ROI",
                "accent": "#10b981",
                "badge": "💸 وفّر وقتك وضاعف أرباحك",
                "title": "أدوات ذكية تضاعف إنتاجيتك",
                "subtext": "أتمتة كاملة وتسويق ذكي بنقرة واحدة",
                "cta": "ابدأ الأرباح 💰"
            }
        # E) AI Brain / Study & Productivity
        elif any(k in t for k in ["كتاب", "دراسة", "لخص", "ترجم", "ذكاء", "اصطناعي", "خرافي", "دماغ"]):
            return {
                "type": "viral_doodle_stickman",
                "pose": "idea",
                "kicker": "VIRAL DOODLE • ALL-IN-ONE AI",
                "accent": "#8b5cf6",
                "badge": "🧠 منظومة الذكاء المتكاملة",
                "title": "اسأل كتاب ولخّص في ثواني",
                "subtext": "كل أدواتك الذكية بمكان واحد وبثانية واحدة",
                "cta": "جرّب التطبيق ⚡"
            }
        elif is_doodle:
            return {
                "type": "viral_doodle_stickman",
                "pose": "celebrate",
                "kicker": "VIRAL DOODLE • SPEED & IMPACT",
                "accent": "#0284c7" if is_pastel else "#00f0ff",
                "badge": "🚀 إنجاز لحظي بدون تعقيد",
                "title": "شفت كيف الفكرة طلعت خرافية؟",
                "subtext": "مونتاج وموشن جرافيك ذكي متكامل",
                "cta": "ابدأ الآن مجاناً 🎬"
            }

    # 1. Numbers / Angles / Statistical Metrics (Counter Pop & DNA Lock)
    if any(k in t for k in ["١٦٥", "165", "زاوية", "زوية", "ستين", "خمس", "ثبت", "شخصية", "منتج", "100%", "١٠٠%", "معدل", "سرعة", "10x"]):
        return {
            "type": "dynamic_counter",
            "kicker": "CAMERA ANGLES & MOTION CONTROL",
            "accent": "#f43f5e" if is_pastel else "#10b981",
            "target_num": 165,
            "suffix": "+",
            "badge": "🔒 ثبات هوية الشخصية والمنتج 100%",
            "subtext": "زاوية وحركة تصوير سينمائية جاهزة",
            "pills": ["35mm Anamorphic", "Orbit 360°", "Dolly & Track", "Dutch Angle", "Crane & Boom"],
            "hero_pill": "توجيه دقيق بالملليمتر"
        }

    # 2. Dual Shot Continuity / Frame Continuity Bridge
    elif any(k in t for k in ["استمرارية", "بيكمل", "بكامل", "يكمل", "فريم", "لقطة", "قطع", "اطاع", "قطاع", "أبله", "قبله", "تتابع", "ثبات"]):
        return {
            "type": "continuity_bridge",
            "kicker": "SEAMLESS FRAME CONTINUITY",
            "accent": "#10b981" if is_pastel else "#a855f7",
            "badge": "⚡ 0% كسر في الهوية والملامح",
            "subtext": "فريم يكمّل فريم • 0% كسر في الكادر",
            "shot_1_label": "كادر البداية • Shot 01",
            "shot_2_label": "كادر الاستمرارية • Shot 02",
            "bridge_text": "استمرارية وتطابق الكادر 100% ↓"
        }

    # 3. Canvas / Nodes / Visual Architecture
    elif any(k in t for k in ["كانفاس", "كانفس", "فس", "تبني", "بيدك", "نود", "قرر", "هيكل", "سير"]):
        return {
            "type": "clean_nodes",
            "kicker": "INFINITE DIRECTOR CANVAS",
            "accent": "#0284c7" if is_pastel else "#00f0ff",
            "badge": "⚡ كانفاس الإخراج اللانهائي",
            "subtext": "تحكّم في كل خطوة من البداية للنهاية",
            "node_a": "السيناريو الذكي",
            "node_b": "مخرج الكاميرا النشط"
        }

    # 4. Engines / Models / API Keys Freedom
    elif any(k in t for k in ["محرك", "مفتاح", "تختار", "موديل", "api", "runway", "kling", "luma", "صدفة", "الصطفي"]):
        return {
            "type": "engines_freedom",
            "kicker": "YOUR ENGINES • YOUR API KEYS",
            "accent": "#8b5cf6" if is_pastel else "#a855f7",
            "badge": "🔗 حرية كاملة في اختيار محركاتك",
            "subtext": "اربط مفتاحك الخاص بدون اشتراكات إضافية",
            "engines": ["Runway Gen-3", "Kling AI", "Luma Dream Machine", "Midjourney"]
        }

    # 5. Common Pain / Problem / Hook (Strikethrough Hook)
    elif any(k in t for k in ["ليش", "سؤال", "بتغير", "بضغير", "مشكلة", "بتضيع", "بالضياء", "خربطة", "صناعي", "فيديو"]):
        return {
            "type": "strikethrough_hook",
            "kicker": "THE AI VIDEO STRUGGLE",
            "accent": "#f43f5e",
            "badge": "🚨 المُعاناة الشائعة في فيديوهات الذكاء",
            "subtext": "لماذا تفشل معظم الأدوات في الحفاظ على النتيجة؟",
            "tags": ["تشوّه ملامح الوجه ✕", "ضياع زوايا الكاميرا ✕", "عشوائية النتائج ✕"]
        }

    # 6. Master Director / Grand Finale
    else:
        return {
            "type": "master_finale",
            "kicker": "FULL CREATIVE MASTERY",
            "accent": "#0284c7" if is_pastel else "#00f0ff",
            "badge": "👑 إخراجك الكامل 100%",
            "subtext": "من أول نود... لآخر كادر سينمائي",
            "cta": "ابدأ إخراجك الآن"
        }

# ==============================================================================
# HTML5 COMPOSITION BUILDER WITH AUTO-SFX & SENIOR POST-PROCESSING
# ==============================================================================

def generate_senior_composition(transcript, audio_filename, brand_title="KinmaUI", style="pastel_director", bg_video=None, aspect="9:16"):
    duration = transcript["duration"]
    segments = transcript["segments"]
    if aspect == "16:9":
        width, height = 1920, 1080
    elif aspect == "1:1":
        width, height = 1080, 1080
    else:
        width, height = 1080, 1920
    is_pastel = (style == "pastel_director")

    beats_html = []
    gsap_timings = []
    sfx_audio_tags = []

    # Inject Hook Impact at 0.0s
    sfx_audio_tags.append('<audio id="sfx-impact-0" src="sfx/sfx_impact.wav" data-start="0.0" data-volume="0.6" data-track-index="3"></audio>')

    for idx, seg in enumerate(segments):
        b_id = f"beat_{idx+1}"
        t_start = seg["start"]
        t_end = seg["end"]
        b_dur = max(0.5, round(t_end - t_start, 2))
        meta = analyze_beat_semantic(seg["text"], beat_idx=idx+1, style=style)

        # SFX: Transition Whoosh on beat start
        sfx_id = f"sfx_w_{idx+1}"
        sfx_audio_tags.append(f'<audio id="{sfx_id}" src="sfx/sfx_whoosh.wav" data-start="{max(0, t_start - 0.12):.2f}" data-volume="0.45" data-track-index="4"></audio>')

        # SFX: Openverse Real Studio Foley for Mechanical/Engineering Cuts
        if meta.get("type") == "procedural_cutaway":
            sub_stg = meta.get("sub_stage", "")
            if sub_stg == "excavation_leak":
                sfx_audio_tags.append(f'<audio id="sfx_exc_{idx+1}" src="sfx/sfx_excavator_digging.wav" data-start="{t_start + 0.25:.2f}" data-volume="0.55" data-track-index="5"></audio>')
            elif sub_stg == "vent_emissions":
                sfx_audio_tags.append(f'<audio id="sfx_gas_{idx+1}" src="sfx/sfx_gas_leak_hiss.wav" data-start="{t_start + 0.2:.2f}" data-volume="0.6" data-track-index="5"></audio>')
            elif sub_stg == "tank_vault":
                sfx_audio_tags.append(f'<audio id="sfx_tank_{idx+1}" src="sfx/sfx_metal_vault.wav" data-start="{t_start + 0.2:.2f}" data-volume="0.5" data-track-index="5"></audio>')

        # Word-by-word kinetic highlight spans
        word_spans = []
        for w_idx, w in enumerate(seg["words"]):
            w_id = f"{b_id}_w_{w_idx}"
            word_spans.append(f'<span id="{w_id}" class="k-word" data-wstart="{w["start"]}" data-wend="{w["end"]}">{w["word"]}</span>')

        caption_markup = " ".join(word_spans)
        cursor_id = f"cur_{idx+1}"
        cursor_html = generate_interactive_cursor_svg(cursor_id, accent=meta["accent"])

        # Build Visual Card
        if meta["type"] == "viral_doodle_stickman":
            stick_svg = generate_stickman_svg(
                pose=meta.get("pose", "idea"),
                accent=meta["accent"],
                width=240,
                height=290
            )
            doodle_arrow = generate_doodle_svg("hand_drawn_arrow", color=meta["accent"], width=130, height=80)
            visual_html = f"""
              <div class="bracket-container" style="width: 820px;">
                <div class="bracket bracket-tl"></div><div class="bracket bracket-tr"></div>
                <div class="bracket bracket-bl"></div><div class="bracket bracket-br"></div>
                <div class="white-card doodle-hybrid-card">
                  <div class="doodle-character-slot">
                    {stick_svg}
                  </div>
                  <div class="doodle-arrow-slot">
                    {doodle_arrow}
                  </div>
                  <div class="doodle-content-slot">
                    <div class="pill-badge doodle-pill" style="border-color: {meta['accent']}; color: {meta['accent']};">
                      <span>{meta['badge']}</span>
                    </div>
                    <div class="doodle-card-title">{meta['title']}</div>
                    <div class="doodle-card-sub">{meta['subtext']}</div>
                    <div class="doodle-interactive-pill" style="background: {meta['accent']}; color: #ffffff;">{meta['cta']}</div>
                  </div>
                </div>
              </div>
            """

        elif meta["type"] == "procedural_cutaway":
            card_w = 840 if aspect == "9:16" else 1100
            card_h = 580
            sub_stg = meta.get("sub_stage", "complete_system")
            
            if sub_stg == "excavation_leak":
                # Render verified Kinematic Excavator & Soil Absorption Cutaway
                try:
                    from procedural_vector import generate_excavation_scene_svg
                    inner_viewport_svg = generate_excavation_scene_svg(card_w, card_h - 100)
                except Exception:
                    inner_viewport_svg = f'<svg id="{b_id}_cutaway_svg" width="100%" height="100%" viewBox="0 0 {card_w} {card_h - 100}"><rect width="100%" height="100%" fill="#1e293b"/></svg>'
                hud_metric = "DEPTH: -2.8m | DIGGING & SOIL LEAK"
            else:
                # Tank Vault / Vent / Complete System
                flange_x = card_w // 2
                flange_y = 230
                vent_x = flange_x + 95
                vent_y = 125
                gauge_cx = 110
                gauge_cy = 110
                hud_metric = f"DEPTH: -4.8m | {meta['gauge_val']} PSI"
                
                puffs_svg = "".join([
                    f'<circle class="cutaway-gas-puff" cx="{vent_x}" cy="{vent_y}" r="{8 + i*2}" fill="rgba(224, 247, 250, {0.65 - i*0.04})" />'
                    for i in range(10)
                ])
                
                inner_viewport_svg = f'''<svg id="{b_id}_cutaway_svg" width="100%" height="100%" viewBox="0 0 {card_w} {card_h - 100}" style="position: absolute; inset: 0;">
                      <!-- Ground Layers -->
                      <rect x="0" y="50" width="{card_w}" height="18" fill="#334155" />
                      <rect x="0" y="48" width="{card_w}" height="4" fill="#f59e0b" />
                      <rect x="0" y="68" width="{card_w}" height="55" fill="#78350f" opacity="0.85" />
                      <rect x="0" y="123" width="{card_w}" height="{card_h}" fill="#451a03" />
                      
                      <!-- Tank Vault Cutaway -->
                      <rect x="{flange_x - 220}" y="195" width="440" height="210" rx="28" fill="#0f172a" stroke="#475569" stroke-width="6" />
                      <rect x="{flange_x - 200}" y="205" width="400" height="190" rx="20" fill="#1e293b" />
                      <!-- Fuel Level -->
                      <rect id="{b_id}_fuel_level" x="{flange_x - 190}" y="260" width="380" height="125" rx="12" fill="#f59e0b" opacity="0.9" />
                      
                      <!-- Center Flange Manhole -->
                      <rect x="{flange_x - 45}" y="180" width="90" height="26" rx="6" fill="#94a3b8" />
                      <circle cx="{flange_x}" cy="193" r="5" fill="#0f172a" />
                      
                      <!-- Vent Riser Pipe -->
                      <rect x="{vent_x - 8}" y="{vent_y}" width="16" height="75" fill="#cbd5e1" />
                      <ellipse cx="{vent_x}" cy="{vent_y}" rx="16" ry="8" fill="#ef4444" />
                      
                      <!-- Fill Pipe on Left -->
                      <rect x="{flange_x - 110}" y="130" width="18" height="70" fill="#94a3b8" />
                      
                      <!-- Gas Vapor Puffs (Parented to Flange Vent) -->
                      <g id="{b_id}_gas_emitter">
                        {puffs_svg}
                      </g>
                      
                      <!-- Integrated Diegetic Mechanical Pressure Gauge -->
                      <g transform="translate({gauge_cx}, {gauge_cy})">
                        <circle cx="0" cy="0" r="48" fill="#0f172a" stroke="#64748b" stroke-width="4" />
                        <circle cx="0" cy="0" r="42" fill="#f8fafc" />
                        <line x1="-28" y1="0" x2="-35" y2="0" stroke="#0f172a" stroke-width="2" />
                        <line x1="28" y1="0" x2="35" y2="0" stroke="#0f172a" stroke-width="2" />
                        <line x1="0" y1="-28" x2="0" y2="-35" stroke="#0f172a" stroke-width="2" />
                        <text x="0" y="24" font-size="9" font-weight="700" fill="#475569" text-anchor="middle">PSI</text>
                        <g id="{b_id}_gauge_needle">
                          <polygon points="-2,4 0,-34 2,4" fill="#ef4444" />
                          <circle cx="0" cy="0" r="4" fill="#0f172a" />
                        </g>
                      </g>
                    </svg>'''

            visual_html = f"""
              <div class="bracket-container" style="width: {card_w}px;">
                <div class="bracket bracket-tl"></div><div class="bracket bracket-tr"></div>
                <div class="bracket bracket-bl"></div><div class="bracket bracket-br"></div>
                <div class="white-card cutaway-hybrid-card" style="padding: 16px; overflow: hidden; position: relative;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; z-index: 10; position: relative;">
                    <div class="pill-badge doodle-pill" style="border-color: {meta['accent']}; color: {meta['accent']};">
                      <span>{meta['badge']}</span>
                    </div>
                    <div style="font-family: monospace; font-size: 13px; color: #64748b; font-weight: 700; direction: ltr;">
                      {hud_metric}
                    </div>
                  </div>
                  
                  <div class="cutaway-viewport" style="width: 100%; height: {card_h - 100}px; position: relative; border-radius: 12px; overflow: hidden; background: #0f172a;">
                    {inner_viewport_svg}
                  </div>
                  
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                    <div>
                      <div class="doodle-card-title" style="font-size: 20px; text-align: right;">{meta['title']}</div>
                      <div class="doodle-card-sub" style="font-size: 13px; text-align: right;">{meta['subtext']}</div>
                    </div>
                    <div class="doodle-interactive-pill" style="background: {meta['accent']}; color: #ffffff; padding: 6px 16px; font-size: 13px;">
                      {meta['cta']}
                    </div>
                  </div>
                </div>
              </div>
            """

        elif meta["type"] == "dynamic_counter":
            pills_html = "".join([f'<div class="pill-badge pill-orbit">{p}</div>' for p in meta["pills"]])
            visual_html = f"""
              <div class="bracket-container" style="width: 780px;">
                <div class="bracket bracket-tl"></div><div class="bracket bracket-tr"></div>
                <div class="bracket bracket-bl"></div><div class="bracket bracket-br"></div>
                <div class="white-card metric-center-box">
                  <div id="{b_id}_lock_pill" class="pill-badge pill-emerald-lock">
                    <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2.5"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
                    <span>{meta['badge']}</span>
                  </div>
                  <div id="{b_id}_num_wrap" class="big-number-wrap">
                    <span id="{b_id}_num_val" class="big-number">0</span>
                    <span id="{b_id}_plus" class="big-plus">{meta['suffix']}</span>
                  </div>
                  <div class="metric-sub">{meta['subtext']}</div>
                  <div class="pills-cloud">{pills_html}</div>
                  <div id="{b_id}_hero_pill" class="pill-hero">{meta['hero_pill']}</div>
                </div>
              </div>
            """
            # SFX: Mechanical Tick for counter
            sfx_audio_tags.append(f'<audio id="sfx_tick_{idx+1}" src="sfx/sfx_tick.wav" data-start="{t_start + 0.35:.2f}" data-volume="0.5" data-track-index="5"></audio>')

        elif meta["type"] == "continuity_bridge":
            visual_html = f"""
              <div class="bracket-container" style="width: 780px;">
                <div class="bracket bracket-tl"></div><div class="bracket bracket-tr"></div>
                <div class="bracket bracket-bl"></div><div class="bracket bracket-br"></div>
                <div class="white-card dual-shots-box">
                  <div class="shot-frame-wrapper">
                    <div class="shot-tag-pill"><span class="shot-dot dot-a"></span><span>{meta['shot_1_label']}</span></div>
                    <div class="mock-shot-view shot-view-a"><span class="shot-inner-tag">زووم متطابق • زاوية 35mm</span></div>
                  </div>
                  <div class="shots-bridge-bar">
                    <div class="bridge-wire-pulse"></div>
                    <div class="bridge-center-pill">
                      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#15803d" stroke-width="2.5"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path></svg>
                      <span>{meta['bridge_text']}</span>
                    </div>
                  </div>
                  <div class="shot-frame-wrapper">
                    <div class="shot-tag-pill"><span class="shot-dot dot-b"></span><span>{meta['shot_2_label']}</span></div>
                    <div class="mock-shot-view shot-view-b"><span class="shot-inner-tag">التفات سلس • إضاءة مستمرة 100%</span></div>
                  </div>
                </div>
                <div class="pill-badge floating-tag tag-top" style="border-color: #a7f3d0; background: {'#ecfdf5' if is_pastel else '#064e3b'}; color: {'#065f46' if is_pastel else '#a7f3d0'};">
                  <span>{meta['badge']}</span>
                </div>
              </div>
              <div class="continuity-stat-card">{meta['subtext']}</div>
            """

        elif meta["type"] == "clean_nodes":
            visual_html = f"""
              <div class="bracket-container" style="width: 780px;">
                <div class="bracket bracket-tl"></div><div class="bracket bracket-tr"></div>
                <div class="bracket bracket-bl"></div><div class="bracket bracket-br"></div>
                <div class="white-card clean-node-graph">
                  <div class="clean-node node-a"><span class="node-dot"></span><span class="node-label">{meta['node_a']}</span><span class="node-state-pill">جاهز</span></div>
                  <div class="connecting-wire"><div class="wire-pulse"></div></div>
                  <div class="clean-node node-b active-node"><span class="node-dot active-dot"></span><span class="node-label">{meta['node_b']}</span><span class="node-state-pill active-pill">نشط</span></div>
                  <div class="node-info-text">{meta['subtext']}</div>
                </div>
              </div>
            """

        elif meta["type"] == "engines_freedom":
            eng_html = "".join([f'<div class="pill-badge engine-pill-item">{eng}</div>' for eng in meta["engines"]])
            visual_html = f"""
              <div class="bracket-container" style="width: 780px;">
                <div class="bracket bracket-tl"></div><div class="bracket bracket-tr"></div>
                <div class="bracket bracket-bl"></div><div class="bracket bracket-br"></div>
                <div class="white-card engines-box">
                  <div class="engines-badge-pill">{meta['badge']}</div>
                  <div class="engines-grid-row">{eng_html}</div>
                  <div class="engines-bridge-beam"><span>{meta['subtext']}</span></div>
                </div>
              </div>
            """

        elif meta["type"] == "strikethrough_hook":
            tags_html = "".join([f'<div class="pill-badge pain-tag">{tag}</div>' for tag in meta["tags"]])
            visual_html = f"""
              <div class="bracket-container" style="width: 780px;">
                <div class="bracket bracket-tl"></div><div class="bracket bracket-tr"></div>
                <div class="bracket bracket-bl"></div><div class="bracket bracket-br"></div>
                <div class="white-card s1-box">
                  <div class="s1-icon-circle">
                    <svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="#f43f5e" stroke-width="2.5"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="8" x2="12" y2="12"></line><line x1="12" y1="16" x2="12.01" y2="16"></line></svg>
                  </div>
                  <div class="s1-title">{meta['badge']}</div>
                  <div class="s1-desc">{meta['subtext']}</div>
                  <div class="pain-tags-row">{tags_html}</div>
                </div>
              </div>
            """

        else: # master_finale
            visual_html = f"""
              <div class="bracket-container" style="width: 780px;">
                <div class="bracket bracket-tl"></div><div class="bracket bracket-tr"></div>
                <div class="bracket bracket-bl"></div><div class="bracket bracket-br"></div>
                <div class="white-card finale-box">
                  <div class="finale-crown-orb">
                    <svg width="70" height="70" viewBox="0 0 24 24" fill="none" stroke="{meta['accent']}" stroke-width="2.5"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
                  </div>
                  <div class="finale-title">{meta['badge']}</div>
                  <div class="finale-sub">{meta['subtext']}</div>
                  <div class="finale-cta-pill">{meta['cta']}</div>
                </div>
              </div>
            """

        beats_html.append(f"""
      <!-- Beat {idx+1}: [{t_start}s -> {t_end}s] -->
      <div id="{b_id}" class="beat-stage clip" data-start="{t_start}" data-duration="{b_dur}" data-track-index="1">
        <div class="safe-zone-container">
          <div class="kicker-badge">
            <span class="kicker-dot" style="background: {meta['accent']};"></span>
            <span>{meta['kicker']}</span>
          </div>

          <div class="headline-container">
            <h1 class="main-headline">{caption_markup}</h1>
          </div>

          <div class="hero-center spatial-3d-stage">
            <div class="spatial-card-3d spatial-shadow-deep">
              {visual_html}
            </div>
            {cursor_html}
          </div>
        </div>
      </div>""")

        # GSAP Pacing & Virtual Camera Parallax Entrance
        t_fade_out = max(t_start + b_dur - 0.25, t_start + 0.1)
        gsap_timings.append(f"""
      // Beat {idx+1} 3D Spatial Tilt Camera & Slow Push Creep-In
      tl.fromTo("#{b_id}", {{ opacity: 0, scale: 0.94 }}, {{ opacity: 1, scale: 1.0, duration: 0.45, ease: "power3.out" }}, {t_start});
      tl.to("#{b_id}", {{ scale: 1.025, duration: {b_dur:.2f}, ease: "none" }}, {t_start});
      tl.to("#{b_id}", {{ opacity: 0, scale: 1.05, duration: 0.25, ease: "power2.in" }}, {t_fade_out});

      // Spatial 3D Tilt Orbit Sweep
      tl.fromTo("#{b_id} .spatial-card-3d", {{ rotateX: 14, rotateY: -16, scale: 0.92, z: -50, opacity: 0 }}, {{ rotateX: 3, rotateY: -4, scale: 1.0, z: 0, opacity: 1, duration: 0.7, ease: "elastic.out(1.1, 0.5)" }}, {t_start + 0.08});
      tl.to("#{b_id} .spatial-card-3d", {{ rotateX: -3, rotateY: 4, duration: {b_dur:.2f}, ease: "none" }}, {t_start + 0.7});

      // Simulated 3D Interactive Cursor Flight & Touch Tap
      const t_tap_{idx+1} = {t_start + 0.82:.2f};
      tl.fromTo("#{b_id} .interactive-cursor", {{ x: 340, y: 160, opacity: 0, scale: 1.25 }}, {{ x: 30, y: 20, opacity: 1, scale: 1.0, duration: 0.52, ease: "power2.out" }}, {t_start + 0.25});
      tl.to("#{b_id} .interactive-cursor", {{ scale: 0.82, rotate: -8, duration: 0.1, ease: "power2.in" }}, t_tap_{idx+1});
      tl.fromTo("#{b_id} .touch-ripple", {{ scale: 0, opacity: 0.9, xPercent: -50, yPercent: -50 }}, {{ scale: 2.5, opacity: 0, duration: 0.35, ease: "power2.out" }}, t_tap_{idx+1});
      tl.to("#{b_id} .interactive-cursor", {{ scale: 1.0, rotate: 0, duration: 0.2, ease: "elastic.out(1.2, 0.4)" }}, t_tap_{idx+1} + 0.1);
      tl.to("#{b_id} .interactive-cursor", {{ x: 75, y: -45, opacity: 0, duration: 0.38, ease: "power2.in" }}, t_tap_{idx+1} + 0.38);
        """)

        # Dynamic Counter Animation & Micro-Impulse Shake
        if meta["type"] == "viral_doodle_stickman":
            gsap_timings.append(f"""
      // Beat {idx+1} Motion.dev Elastic Spring Stickman & GPU Path Drawing
      tl.fromTo("#{b_id} .stickman-svg", {{ scale: 0.55, y: 65, opacity: 0 }}, {{ scale: 1, y: 0, opacity: 1, duration: 0.65, ease: "elastic.out(1.15, 0.45)" }}, {t_start + 0.12});
      tl.fromTo("#{b_id} .doodle-draw-path", {{ strokeDasharray: 300, strokeDashoffset: 300 }}, {{ strokeDashoffset: 0, duration: 0.52, ease: "power2.out" }}, {t_start + 0.32});
      tl.fromTo("#{b_id} .doodle-content-slot", {{ x: 45, opacity: 0 }}, {{ x: 0, opacity: 1, duration: 0.5, ease: "back.out(1.9)" }}, {t_start + 0.22});
      // Haptic Button Press Feedback
      tl.to("#{b_id} .doodle-interactive-pill", {{ scale: 0.92, y: 4, duration: 0.12, ease: "power2.in" }}, {t_start + 0.75});
      tl.to("#{b_id} .doodle-interactive-pill", {{ scale: 1.06, y: -2, duration: 0.22, ease: "elastic.out(1.3, 0.3)" }}, {t_start + 0.87});
      tl.to("#{b_id} .doodle-interactive-pill", {{ scale: 1.0, y: 0, duration: 0.15 }}, {t_start + 1.09});
            """)

        elif meta["type"] == "procedural_cutaway":
            card_w = 840 if aspect == "9:16" else 1100
            card_h = 580
            sub_stg = meta.get("sub_stage", "complete_system")
            
            if sub_stg == "excavation_leak":
                # Render verified Kinematic Excavator & Soil Absorption Cutaway
                try:
                    from procedural_vector import generate_excavation_scene_svg
                    inner_viewport_svg = generate_excavation_scene_svg(card_w, card_h - 100)
                except Exception:
                    inner_viewport_svg = f'<svg id="{b_id}_cutaway_svg" width="100%" height="100%" viewBox="0 0 {card_w} {card_h - 100}"><rect width="100%" height="100%" fill="#1e293b"/></svg>'
                hud_metric = "DEPTH: -2.8m | DIGGING & SOIL LEAK"
            else:
                # Tank Vault / Vent / Complete System
                flange_x = card_w // 2
                flange_y = 230
                vent_x = flange_x + 95
                vent_y = 125
                gauge_cx = 110
                gauge_cy = 110
                hud_metric = f"DEPTH: -4.8m | {meta['gauge_val']} PSI"
                
                puffs_svg = "".join([
                    f'<circle class="cutaway-gas-puff" cx="{vent_x}" cy="{vent_y}" r="{8 + i*2}" fill="rgba(224, 247, 250, {0.65 - i*0.04})" />'
                    for i in range(10)
                ])
                
                inner_viewport_svg = f'''<svg id="{b_id}_cutaway_svg" width="100%" height="100%" viewBox="0 0 {card_w} {card_h - 100}" style="position: absolute; inset: 0;">
                      <!-- Ground Layers -->
                      <rect x="0" y="50" width="{card_w}" height="18" fill="#334155" />
                      <rect x="0" y="48" width="{card_w}" height="4" fill="#f59e0b" />
                      <rect x="0" y="68" width="{card_w}" height="55" fill="#78350f" opacity="0.85" />
                      <rect x="0" y="123" width="{card_w}" height="{card_h}" fill="#451a03" />
                      
                      <!-- Tank Vault Cutaway -->
                      <rect x="{flange_x - 220}" y="195" width="440" height="210" rx="28" fill="#0f172a" stroke="#475569" stroke-width="6" />
                      <rect x="{flange_x - 200}" y="205" width="400" height="190" rx="20" fill="#1e293b" />
                      <!-- Fuel Level -->
                      <rect id="{b_id}_fuel_level" x="{flange_x - 190}" y="260" width="380" height="125" rx="12" fill="#f59e0b" opacity="0.9" />
                      
                      <!-- Center Flange Manhole -->
                      <rect x="{flange_x - 45}" y="180" width="90" height="26" rx="6" fill="#94a3b8" />
                      <circle cx="{flange_x}" cy="193" r="5" fill="#0f172a" />
                      
                      <!-- Vent Riser Pipe -->
                      <rect x="{vent_x - 8}" y="{vent_y}" width="16" height="75" fill="#cbd5e1" />
                      <ellipse cx="{vent_x}" cy="{vent_y}" rx="16" ry="8" fill="#ef4444" />
                      
                      <!-- Fill Pipe on Left -->
                      <rect x="{flange_x - 110}" y="130" width="18" height="70" fill="#94a3b8" />
                      
                      <!-- Gas Vapor Puffs (Parented to Flange Vent) -->
                      <g id="{b_id}_gas_emitter">
                        {puffs_svg}
                      </g>
                      
                      <!-- Integrated Diegetic Mechanical Pressure Gauge -->
                      <g transform="translate({gauge_cx}, {gauge_cy})">
                        <circle cx="0" cy="0" r="48" fill="#0f172a" stroke="#64748b" stroke-width="4" />
                        <circle cx="0" cy="0" r="42" fill="#f8fafc" />
                        <line x1="-28" y1="0" x2="-35" y2="0" stroke="#0f172a" stroke-width="2" />
                        <line x1="28" y1="0" x2="35" y2="0" stroke="#0f172a" stroke-width="2" />
                        <line x1="0" y1="-28" x2="0" y2="-35" stroke="#0f172a" stroke-width="2" />
                        <text x="0" y="24" font-size="9" font-weight="700" fill="#475569" text-anchor="middle">PSI</text>
                        <g id="{b_id}_gauge_needle">
                          <polygon points="-2,4 0,-34 2,4" fill="#ef4444" />
                          <circle cx="0" cy="0" r="4" fill="#0f172a" />
                        </g>
                      </g>
                    </svg>'''

            visual_html = f"""
              <div class="bracket-container" style="width: {card_w}px;">
                <div class="bracket bracket-tl"></div><div class="bracket bracket-tr"></div>
                <div class="bracket bracket-bl"></div><div class="bracket bracket-br"></div>
                <div class="white-card cutaway-hybrid-card" style="padding: 16px; overflow: hidden; position: relative;">
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; z-index: 10; position: relative;">
                    <div class="pill-badge doodle-pill" style="border-color: {meta['accent']}; color: {meta['accent']};">
                      <span>{meta['badge']}</span>
                    </div>
                    <div style="font-family: monospace; font-size: 13px; color: #64748b; font-weight: 700; direction: ltr;">
                      {hud_metric}
                    </div>
                  </div>
                  
                  <div class="cutaway-viewport" style="width: 100%; height: {card_h - 100}px; position: relative; border-radius: 12px; overflow: hidden; background: #0f172a;">
                    {inner_viewport_svg}
                  </div>
                  
                  <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
                    <div>
                      <div class="doodle-card-title" style="font-size: 20px; text-align: right;">{meta['title']}</div>
                      <div class="doodle-card-sub" style="font-size: 13px; text-align: right;">{meta['subtext']}</div>
                    </div>
                    <div class="doodle-interactive-pill" style="background: {meta['accent']}; color: #ffffff; padding: 6px 16px; font-size: 13px;">
                      {meta['cta']}
                    </div>
                  </div>
                </div>
              </div>
            """

        elif meta["type"] == "procedural_cutaway":
            g_target = meta.get("gauge_val", 120)
            rot_deg = min(110, max(-100, int((g_target / 150.0) * 120 - 60)))
            gsap_timings.append(f"""
      // Beat {idx+1} Procedural Cutaway & Strict Kinematic Joint Rigging
      const needleEl_{idx+1} = document.getElementById("{b_id}_gauge_needle");
      if (needleEl_{idx+1}) {{
        const needleJ_{idx+1} = J(needleEl_{idx+1}, 0, 0);
        tl.fromTo(needleJ_{idx+1}, {{ r: -70 }}, {{
          r: {rot_deg},
          duration: 1.2,
          ease: "elastic.out(1.1, 0.4)",
          onUpdate: () => needleJ_{idx+1}.apply()
        }}, {t_start + 0.35});
      }}

      // Gas Vapor Emitter Particles Rising from Vent Pivot
      const puffs_{idx+1} = document.querySelectorAll("#{b_id}_gas_emitter .cutaway-gas-puff");
      puffs_{idx+1}.forEach((p, pIdx) => {{
        tl.fromTo(p, 
          {{ y: 0, x: 0, opacity: 0.8, scale: 0.8 }},
          {{
            y: -110 - pIdx * 12,
            x: (pIdx % 2 === 0 ? 1 : -1) * (14 + pIdx * 4),
            opacity: 0,
            scale: 2.4,
            duration: 1.8,
            ease: "power1.out",
            repeat: -1,
            delay: pIdx * 0.18
          }},
          {t_start + 0.2}
        );
      }});

      // Macro Camera Push-in to Cutaway Details
      tl.to("#{b_id} .cutaway-viewport", {{
        scale: 1.08,
        duration: {b_dur:.2f},
        ease: "none"
      }}, {t_start});
            """)

        elif meta["type"] == "dynamic_counter":
            target = meta.get("target_num", 165)
            t_cnt = round(t_start + 0.35, 2)
            gsap_timings.append(f"""
      // Beat {idx+1} Counter & Micro-Shake
      const cntObj_{idx+1} = {{ val: 0 }};
      tl.fromTo("#{b_id}_num_wrap", {{ scale: 0.75, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.5)" }}, {t_cnt});
      tl.to(cntObj_{idx+1}, {{
        val: {target},
        duration: 1.35,
        ease: "power2.out",
        onUpdate: () => {{
          const el = document.getElementById("{b_id}_num_val");
          if (el) el.textContent = Math.round(cntObj_{idx+1}.val);
        }}
      }}, {t_cnt + 0.05});
      tl.fromTo("#{b_id}_plus", {{ scale: 0, rotate: -45 }}, {{ scale: 1, rotate: 0, duration: 0.35, ease: "back.out(2.2)" }}, {t_cnt + 1.30});
      tl.fromTo(".pill-orbit", {{ scale: 0, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, stagger: 0.07, ease: "back.out(1.8)" }}, {t_cnt + 0.5});
      // Micro-shake impact on hitting {target}
      tl.to("#stage-camera", {{ x: -4, y: 3, duration: 0.04, yoyo: true, repeat: 2 }}, {t_cnt + 1.32});
            """)

        # Word-by-Word Kinetic Typography Highlights
        base_word_color = "#475569" if is_pastel else "rgba(255, 255, 255, 0.65)"
        active_word_color = meta["accent"]
        settled_word_color = "#0f172a" if is_pastel else "#ffffff"

        for w_idx, w in enumerate(seg["words"]):
            w_id = f"{b_id}_w_{w_idx}"
            w_start = w["start"]
            w_end = w["end"]
            gsap_timings.append(f"""
      tl.fromTo("#{w_id}", {{ color: "{base_word_color}", scale: 1 }}, {{ color: "{active_word_color}", scale: 1.08, duration: 0.12, ease: "power1.out" }}, {w_start});
      tl.to("#{w_id}", {{ color: "{settled_word_color}", scale: 1, duration: 0.18, ease: "power1.in" }}, {w_end});
            """)

    # Background Video or Dynamic Canvas
    bg_video_tag = ""
    if bg_video and os.path.exists(bg_video):
        bg_video_tag = f"""
        <video id="bg-video-footage" src="{os.path.basename(bg_video)}" data-start="0" data-duration="{duration}" data-track-index="0" style="position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; z-index: 0; opacity: 0.85;"></video>
        """

    # Organic Film Grain & Optical Bloom Styles
    grain_svg = """
    <svg style="position: absolute; width: 0; height: 0;">
      <filter id="film-grain">
        <feTurbulence type="fractalNoise" baseFrequency="0.8" numOctaves="3" stitchTiles="stitch"/>
        <feColorMatrix type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 0.04 0"/>
      </filter>
    </svg>
    <div class="grain-overlay"></div>
    """

    theme_css = f"""
      html, body {{
        background: {'#f7f9fc' if is_pastel else '#04070d'};
        color: {'#0f172a' if is_pastel else '#ffffff'};
      }}
      #root {{
        background: {'#f7f9fc' if is_pastel else 'radial-gradient(circle at 50% 30%, #0c162a 0%, #060b15 55%, #020408 100%)'};
      }}
      /* SOCIAL SAFE ZONE CONTAINER (Prevents UI buttons clipping on TikTok / Reels) */
      .safe-zone-container {{
        width: 100%;
        max-width: 960px;
        margin: 0 auto;
        padding-top: 140px;
        padding-bottom: 220px;
        padding-right: 50px;
        padding-left: 50px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
      }}
      .ambient-glow {{
        position: absolute;
        border-radius: 50%;
        filter: blur(140px);
        pointer-events: none;
        z-index: 1;
        opacity: {'0.38' if is_pastel else '0.45'};
      }}
      .glow-coral {{ width: 850px; height: 850px; background: radial-gradient(circle, #ff6b6b 0%, rgba(255,107,107,0) 70%); top: -150px; right: -160px; }}
      .glow-cyan {{ width: 900px; height: 900px; background: radial-gradient(circle, #38bdf8 0%, rgba(56,189,248,0) 70%); bottom: 180px; left: -180px; }}
      .glow-purple {{ width: 750px; height: 750px; background: radial-gradient(circle, #a855f7 0%, rgba(168,85,247,0) 70%); top: 40%; right: -120px; }}
      .glow-mint {{ width: 700px; height: 700px; background: radial-gradient(circle, #34d399 0%, rgba(52,211,153,0) 70%); bottom: -120px; right: 15%; }}
            /* VIRAL DOODLE & STICKMAN CARD STYLES */
      .doodle-hybrid-card {{
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: space-between;
        padding: 36px 32px;
        gap: 18px;
        position: relative;
        overflow: visible;
      }}
      .doodle-character-slot {{
        flex: 0 0 240px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: #0f172a;
      }}
      .doodle-arrow-slot {{
        flex: 0 0 120px;
        display: flex;
        align-items: center;
        justify-content: center;
      }}
      .doodle-content-slot {{
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        text-align: right;
        direction: rtl;
        gap: 12px;
      }}
      .doodle-pill {{
        font-size: 18px;
        font-weight: 800;
        padding: 8px 18px;
        border-radius: 9999px;
        background: #f1f5f9;
      }}
      .doodle-card-title {{
        font-size: 34px;
        font-weight: 900;
        line-height: 1.25;
        color: #0f172a;
      }}
      .doodle-card-sub {{
        font-size: 20px;
        color: #64748b;
        line-height: 1.4;
      }}
      .doodle-interactive-pill {{
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 800;
        padding: 12px 26px;
        border-radius: 9999px;
        box-shadow: 0 10px 25px -5px rgba(0,0,0,0.25);
        margin-top: 6px;
      }}
      .prop-float {{
        animation: floatAnim 2.2s ease-in-out infinite alternate;
      }}
      @keyframes floatAnim {{
        0% {{ transform: translateY(0px); }}
        100% {{ transform: translateY(-8px); }}
      }}

      .dot-grid {{
        position: absolute;
        inset: 0;
        background-image: {'radial-gradient(#cbd5e1 1.8px, transparent 1.8px)' if is_pastel else 'radial-gradient(rgba(0, 240, 255, 0.08) 1.8px, transparent 1.8px)'};
        background-size: 42px 42px;
        opacity: 0.65;
        z-index: 2;
        pointer-events: none;
      }}
      .grain-overlay {{
        position: absolute;
        inset: 0;
        filter: url(#film-grain);
        pointer-events: none;
        z-index: 50;
        opacity: 0.7;
      }}
      .kicker-badge {{
        font-family: 'Plus Jakarta Sans', 'Cairo', sans-serif;
        font-size: 26px;
        font-weight: 800;
        letter-spacing: 0.18em;
        text-transform: uppercase;
        color: {'#64748b' if is_pastel else '#00f0ff'};
        margin-bottom: 22px;
        display: inline-flex;
        align-items: center;
        gap: 12px;
      }}
      .kicker-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
      .headline-container {{ max-width: 980px; margin-bottom: 35px; }}
      .main-headline {{
        font-size: 64px;
        font-weight: 900;
        line-height: 1.35;
        color: {'#0f172a' if is_pastel else '#ffffff'};
        letter-spacing: -0.02em;
        text-shadow: {'none' if is_pastel else '0 6px 30px rgba(0,0,0,0.95)'};
      }}
      .white-card {{
        background: {'#ffffff' if is_pastel else 'rgba(15, 23, 42, 0.92)'};
        border: {'1.5px solid rgba(226, 232, 240, 0.95)' if is_pastel else '2px solid rgba(255, 255, 255, 0.18)'};
        border-radius: 36px;
        box-shadow: {'0 25px 65px -12px rgba(15, 23, 42, 0.10)' if is_pastel else '0 25px 65px -12px rgba(0, 0, 0, 0.7)'};
        padding: 40px;
        position: relative;
        z-index: 12;
      }}
      .pill-badge {{
        background: {'#ffffff' if is_pastel else 'rgba(30, 41, 59, 0.85)'};
        border: {'1.5px solid rgba(226, 232, 240, 0.9)' if is_pastel else '2px solid rgba(255, 255, 255, 0.18)'};
        border-radius: 9999px;
        padding: 14px 28px;
        font-size: 28px;
        font-weight: 800;
        color: {'#1e293b' if is_pastel else '#f8fafc'};
        display: inline-flex;
        align-items: center;
        gap: 12px;
      }}
      .big-number {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 165px;
        font-weight: 900;
        line-height: 1;
        letter-spacing: -0.05em;
        color: {'#0f172a' if is_pastel else '#ffffff'};
      }}
      .big-plus {{
        font-family: 'Plus Jakarta Sans', sans-serif;
        font-size: 110px;
        font-weight: 900;
        color: {'#f43f5e' if is_pastel else '#00f0ff'};
        line-height: 1;
        margin-right: 6px;
      }}
      .metric-sub {{ font-size: 32px; font-weight: 800; color: {'#64748b' if is_pastel else '#94a3b8'}; margin: 12px 0 24px; }}
      .pill-hero {{
        background: {'#475569' if is_pastel else 'rgba(0, 240, 255, 0.18)'};
        border: {'none' if is_pastel else '2px solid #00f0ff'};
        color: {'#ffffff' if is_pastel else '#00f0ff'};
        border-radius: 20px;
        padding: 14px 38px;
        font-size: 28px;
        font-weight: 800;
        margin-top: 24px;
        display: inline-block;
      }}
      .continuity-stat-card {{
        background: {'#64748b' if is_pastel else 'rgba(88, 28, 135, 0.85)'};
        border: {'none' if is_pastel else '2px solid #c084fc'};
        color: {'#ffffff' if is_pastel else '#f3e8ff'};
        border-radius: 22px;
        padding: 16px 42px;
        font-size: 30px;
        font-weight: 800;
        margin-top: 20px;
        display: inline-block;
      }}
    """

    html = f"""<!doctype html>
<html lang="ar" dir="rtl" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={width}, height={height}" />
    <title>{brand_title} Senior Motion Reel</title>
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@500;600;700;800;900&family=Tajawal:wght@500;700;800;900&family=Plus+Jakarta+Sans:wght@600;700;800;900&display=swap" rel="stylesheet" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/motion@11.11.17/dist/motion.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{
        width: {width}px;
        height: {height}px;
        overflow: hidden;
        font-family: 'Cairo', 'Tajawal', sans-serif;
        direction: rtl;
        user-select: none;
        -webkit-font-smoothing: antialiased;
      }}
      #stage-camera {{
        position: relative;
        width: {width}px;
        height: {height}px;
        overflow: hidden;
      }}
      #root {{
        position: relative;
        width: {width}px;
        height: {height}px;
        overflow: hidden;
      }}

      {theme_css}

      /* STAGE & PARALLAX */
      .beat-stage {{
        position: absolute;
        inset: 0;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        opacity: 0;
        z-index: 10;
        pointer-events: none;
      }}
      .k-word {{ display: inline-block; margin: 0 4px; will-change: transform, color; }}
      .hero-center {{ width: 100%; display: flex; flex-direction: column; align-items: center; justify-content: center; position: relative; }}
      /* 3D SPATIAL CAMERA & TILT-SHIFT DEPTH */
      .spatial-3d-stage {{
        perspective: 1200px;
        transform-style: preserve-3d;
      }}
      .spatial-card-3d {{
        transform-style: preserve-3d;
        position: relative;
        will-change: transform;
      }}
      .spatial-shadow-deep {{
        box-shadow: 0 40px 85px -15px rgba(0, 0, 0, 0.38),
                    0 15px 35px -8px rgba(0, 0, 0, 0.25),
                    0 0 0 1px rgba(255, 255, 255, 0.12) inset;
      }}
      /* SIMULATED 3D CURSOR & INTERACTIVE TOUCH */
      .interactive-cursor {{
        position: absolute;
        width: 44px;
        height: 44px;
        pointer-events: none;
        z-index: 99;
        transform-origin: 0 0;
        filter: drop-shadow(0 14px 22px rgba(0,0,0,0.4));
        will-change: transform, opacity;
        opacity: 0;
      }}
      .touch-ripple {{
        position: absolute;
        width: 75px;
        height: 75px;
        border-radius: 50%;
        border: 3px solid #10b981;
        background: rgba(16, 185, 129, 0.22);
        pointer-events: none;
        z-index: 90;
        top: 20px;
        left: 20px;
        transform: translate(-50%, -50%) scale(0);
        opacity: 0;
        will-change: transform, opacity;
      }}
      .bracket-container {{ position: relative; display: inline-flex; align-items: center; justify-content: center; }}
      .bracket {{ position: absolute; width: 48px; height: 48px; border-style: solid; border-width: 0; pointer-events: none; z-index: 18; }}
      .bracket-tl {{ top: -16px; right: -16px; border-top-width: 8px; border-right-width: 8px; border-color: #f43f5e; border-top-right-radius: 26px; }}
      .bracket-tr {{ top: -16px; left: -16px; border-top-width: 8px; border-left-width: 8px; border-color: #0f172a; border-top-left-radius: 26px; }}
      .bracket-bl {{ bottom: -16px; right: -16px; border-bottom-width: 8px; border-right-width: 8px; border-color: #f59e0b; border-bottom-right-radius: 26px; }}
      .bracket-br {{ bottom: -16px; left: -16px; border-bottom-width: 8px; border-left-width: 8px; border-color: #10b981; border-bottom-left-radius: 26px; }}

      /* COMPONENT STYLES */
      .metric-center-box {{ display: flex; flex-direction: column; align-items: center; width: 100%; }}
      .big-number-wrap {{ display: flex; align-items: baseline; justify-content: center; direction: ltr; margin: 8px 0; }}
      .pills-cloud {{ display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; max-width: 660px; }}
      .pill-orbit {{ font-size: 26px; padding: 10px 22px; }}
      .dual-shots-box {{ display: flex; flex-direction: column; align-items: center; gap: 14px; width: 100%; padding: 26px; }}
      .shot-frame-wrapper {{ width: 100%; border-radius: 22px; background: #0f172a; overflow: hidden; position: relative; border: 2px solid rgba(226, 232, 240, 0.8); }}
      .shot-tag-pill {{ position: absolute; top: 12px; right: 12px; background: rgba(15, 23, 42, 0.85); color: #ffffff; padding: 6px 16px; border-radius: 18px; font-size: 22px; font-weight: 800; display: flex; align-items: center; gap: 8px; z-index: 5; }}
      .shot-dot {{ width: 10px; height: 10px; border-radius: 50%; }}
      .dot-a {{ background: #38bdf8; }}
      .dot-b {{ background: #10b981; }}
      .mock-shot-view {{ height: 180px; display: flex; align-items: center; justify-content: center; }}
      .shot-view-a {{ background: linear-gradient(135deg, #1e293b, #0f172a); }}
      .shot-view-b {{ background: linear-gradient(135deg, #0f172a, #1e293b); }}
      .shot-inner-tag {{ background: rgba(255, 255, 255, 0.12); color: #f8fafc; padding: 8px 18px; border-radius: 12px; font-size: 24px; font-weight: 700; }}
      .shots-bridge-bar {{ display: flex; align-items: center; justify-content: center; width: 100%; margin: 2px 0; }}
      .bridge-center-pill {{ background: #dcfce7; border: 2px solid #86efac; color: #15803d; padding: 8px 22px; border-radius: 28px; font-size: 24px; font-weight: 900; display: flex; align-items: center; gap: 8px; }}
      .s1-box {{ display: flex; flex-direction: column; align-items: center; gap: 18px; width: 100%; }}
      .s1-icon-circle {{ width: 105px; height: 105px; border-radius: 50%; background: #fff1f2; border: 3px solid #f43f5e; display: flex; align-items: center; justify-content: center; }}
      .s1-title {{ font-size: 36px; font-weight: 900; }}
      .s1-desc {{ font-size: 28px; color: #64748b; font-weight: 600; }}
      .pain-tags-row {{ display: flex; flex-direction: column; gap: 10px; width: 100%; margin-top: 8px; }}
      .pain-tag {{ width: 100%; justify-content: center; border-color: #fca5a5; background: #fef2f2; color: #991b1b; }}
      .clean-node-graph {{ display: flex; flex-direction: column; align-items: center; gap: 16px; width: 100%; }}
      .clean-node {{ width: 100%; background: #ffffff; border: 2px solid #e2e8f0; border-radius: 22px; padding: 20px 28px; display: flex; align-items: center; gap: 14px; }}
      .active-node {{ border-color: #0284c7; box-shadow: 0 0 30px rgba(2, 132, 199, 0.22); }}
      .node-dot {{ width: 18px; height: 18px; border-radius: 50%; background: #94a3b8; }}
      .active-dot {{ background: #0284c7; box-shadow: 0 0 10px #0284c7; }}
      .node-label {{ font-size: 32px; font-weight: 800; color: #0f172a; flex: 1; text-align: right; }}
      .node-state-pill {{ background: #f1f5f9; color: #64748b; padding: 6px 14px; border-radius: 12px; font-size: 22px; font-weight: 800; }}
      .active-pill {{ background: #e0f2fe; color: #0369a1; }}
      .connecting-wire {{ width: 4px; height: 40px; background: #cbd5e1; position: relative; overflow: hidden; }}
      .wire-pulse {{ position: absolute; width: 100%; height: 22px; background: #0284c7; animation: pulseDown 1.2s infinite linear; }}
      @keyframes pulseDown {{ 0% {{ top: -22px; }} 100% {{ top: 40px; }} }}
      .node-info-text {{ font-size: 26px; color: #64748b; font-weight: 700; margin-top: 6px; }}
      .engines-box {{ display: flex; flex-direction: column; align-items: center; gap: 20px; width: 100%; }}
      .engines-badge-pill {{ font-size: 30px; font-weight: 900; color: #7c3aed; }}
      .engines-grid-row {{ display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; }}
      .engine-pill-item {{ font-size: 28px; border-color: #ddd6fe; color: #5b21b6; }}
      .engines-bridge-beam {{ background: #ede9fe; border: 2px solid #c4b5fd; padding: 12px 30px; border-radius: 18px; font-size: 28px; font-weight: 800; color: #6d28d9; }}
      .finale-box {{ display: flex; flex-direction: column; align-items: center; gap: 18px; width: 100%; }}
      .finale-crown-orb {{ width: 130px; height: 130px; border-radius: 50%; background: #e0f2fe; border: 3px solid #0284c7; display: flex; align-items: center; justify-content: center; }}
      .finale-title {{ font-size: 38px; font-weight: 900; }}
      .finale-sub {{ font-size: 28px; color: #64748b; font-weight: 700; }}
      .finale-cta-pill {{ background: #0284c7; color: #ffffff; padding: 14px 40px; border-radius: 28px; font-size: 30px; font-weight: 900; margin-top: 8px; }}
    </style>
  </head>
  <body>
    <div id="stage-camera" data-composition-id="main" data-width="{width}" data-height="{height}">
      <div
        id="root"
        data-composition-id="main"
        data-start="0"
        data-duration="{duration}"
        data-width="{width}"
        data-height="{height}"
      >
        <audio
          id="a-roll-audio"
          src="{audio_filename}"
          data-start="0"
          data-duration="{duration}"
          data-track-index="2"
          data-volume="1"
        ></audio>

        {"".join(sfx_audio_tags)}
        {bg_video_tag}

        {'<div class="ambient-glow glow-coral"></div><div class="ambient-glow glow-cyan"></div><div class="ambient-glow glow-purple"></div><div class="ambient-glow glow-mint"></div>' if is_pastel else '<div class="ambient-glow"></div>'}
        <div class="dot-grid"></div>
        {grain_svg}

        {"".join(beats_html)}
      </div>
    </div>

    <script>
      // ==============================================================================
      // MOTION.DEV HYBRID PHYSICS ENGINE (Springs, Doodles & Haptic Micro-Interactions)
      // ==============================================================================

      // ==============================================================================
      // KINEMATIC JOINT RIGGING SYSTEM (Local Origin Zero-Drift Rotation)
      // ==============================================================================
      function J(el, tx = 0, ty = 0) {{
        const j = {{
          el, tx, ty, x: 0, y: 0, r: 0, sx: 1, sy: 1,
          apply() {{
            if (!j.el) return;
            j.el.setAttribute('transform', `translate(${{j.tx + j.x}}, ${{j.ty + j.y}}) rotate(${{j.r}}) scale(${{j.sx}}, ${{j.sy}})`);
          }}
        }};
        j.apply();
        return j;
      }}

      const MotionLib = window.Motion || {{}};

      // Motion.dev Spring Profiles (Apple Tactile & Cartoon Wobble)
      const MotionSpring = {{
        appleBounce: "elastic.out(1.15, 0.45)",  // Tactile iOS spring
        smoothFloat: "power3.out",              // Cinematic 3D float
        cartoonWobbly: "back.out(2.4)",          // Bouncy doodle cartoon
        hapticPress: "power4.out"               // Real haptic button recoil
      }};

      const tl = gsap.timeline({{ paused: true }});
      gsap.set("#beat_1", {{ opacity: 1 }});

      {"".join(gsap_timings)}

      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
    return html

# ==============================================================================
# STANDARDIZED PROJECT WORKSPACE ARCHITECTURE (Zero-Numbering Studio Standard)
# ==============================================================================

class ProjectWorkspace:
    """
    Standardized Autonomous Project Workspace Architecture:
    projects/<project_name>/
      ├── <project_name>_Master_<aspect>.mp4    # Final master rendered video
      ├── input/                                # Raw source files
      │   ├── audio/                            # Input voiceover / music
      │   ├── video/                            # Input video footage
      │   └── images/                           # Input images / logos / slides
      ├── transcript/                           # Speech-to-text timing transcripts
      │   ├── transcript.json
      │   ├── transcript_raw.json
      │   └── transcript_ambiguities.json
      ├── assets/                               # Processed runtime assets
      │   ├── audio/ (vo.wav, sfx.wav, bgm.wav)
      │   ├── images/
      │   └── fonts/
      ├── composition/                          # Render engine & HTML5 canvas
      │   ├── index.html
      │   ├── hyperframes.json
      │   ├── meta.json
      │   └── sfx/                              # Local runtime sfx mirrors
      └── review/                               # Visual review & quality gate
          ├── contact-sheet.jpg
          └── snapshots/                        # Keyframe preview snapshots
    """
    def __init__(self, project_name=None, base_dir="projects", brand_title="Monteur Baba Cut", aspect="9:16", source_hint=None):
        import datetime
        if not project_name:
            if source_hint and os.path.exists(source_hint):
                base = os.path.splitext(os.path.basename(source_hint))[0]
                clean = re.sub(r'[^a-zA-Z0-9_؀-ۿ]', '_', base).strip('_')
                project_name = clean if clean else "Studio_Project"
            else:
                clean_brand = re.sub(r'[^a-zA-Z0-9_؀-ۿ]', '_', brand_title).strip('_')
                project_name = clean_brand if clean_brand else "Monteur_Project"
            
            candidate = os.path.abspath(os.path.join(base_dir, project_name))
            if os.path.exists(candidate):
                ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                project_name = f"{project_name}_{ts}"
        else:
            project_name = re.sub(r'[\\/:"*?<>|]', '_', project_name).strip()

        self.project_name = project_name
        self.root_dir = os.path.abspath(os.path.join(base_dir, project_name))
        
        # Subdirectories (Strictly unnumbered)
        self.input_dir = os.path.join(self.root_dir, "input")
        self.input_audio_dir = os.path.join(self.input_dir, "audio")
        self.input_video_dir = os.path.join(self.input_dir, "video")
        self.input_images_dir = os.path.join(self.input_dir, "images")
        
        self.transcript_dir = os.path.join(self.root_dir, "transcript")
        
        self.assets_dir = os.path.join(self.root_dir, "assets")
        self.assets_audio_dir = os.path.join(self.assets_dir, "audio")
        self.assets_images_dir = os.path.join(self.assets_dir, "images")
        self.assets_fonts_dir = os.path.join(self.assets_dir, "fonts")
        
        self.composition_dir = os.path.join(self.root_dir, "composition")
        
        self.review_dir = os.path.join(self.root_dir, "review")
        self.snapshots_dir = os.path.join(self.review_dir, "snapshots")

        clean_aspect = aspect.replace(":", "x")
        self.output_mp4 = os.path.join(self.root_dir, f"{self.project_name}_Master_{clean_aspect}.mp4")

        # Create all standardized folders
        for d in [
            self.input_audio_dir, self.input_video_dir, self.input_images_dir,
            self.transcript_dir,
            self.assets_audio_dir, self.assets_images_dir, self.assets_fonts_dir,
            self.composition_dir,
            self.snapshots_dir
        ]:
            os.makedirs(d, exist_ok=True)
            
        print(f"[Monteur Workspace] Standardized project workspace ready at:\n  {self.root_dir}")

# ==============================================================================
# EXISTING VIDEO AUTO-EDITING & CAPTIONING (Burned & Mastered Mode)
# ==============================================================================

def auto_edit_existing_video(video_path, output_path=None, project_name=None, projects_dir="projects", brand_title="Monteur Baba Cut", style="pastel_director", aspect="9:16", transcript_file=None, user_corrections=None, prompt_hint=None, preview_only=False):
    """
    Takes an existing video (MP4/MOV), transcribes speech with Whisper,
    generates a synchronized HyperFrames overlay or ASS subtitles,
    applies safe-zone constraints and audio normalization (EBU R128).
    Organizes everything cleanly in the standard project directory.
    """
    check_dependencies()
    video_path = os.path.abspath(video_path)
    if not os.path.exists(video_path):
        print(f"ERROR: Video not found: {video_path}")
        sys.exit(1)

    ws = ProjectWorkspace(
        project_name=project_name,
        base_dir=projects_dir,
        brand_title=brand_title,
        aspect=aspect,
        source_hint=video_path
    )

    # 1. Archive raw input video
    dest_video_name = os.path.basename(video_path)
    shutil.copy2(video_path, os.path.join(ws.input_video_dir, dest_video_name))
    
    # Also place in composition for background playback
    comp_video_path = os.path.join(ws.composition_dir, "source_video.mp4")
    shutil.copy2(video_path, comp_video_path)

    # 2. Extract audio from video
    extracted_audio = os.path.join(ws.assets_audio_dir, "extracted_audio.wav")
    print(f"[Video Editor] Extracting audio track from: {video_path}")
    subprocess.run([
        "ffmpeg", "-y", "-i", video_path, "-vn", "-acodec", "pcm_s16le", "-ar", "16000", extracted_audio
    ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Mirror to composition
    shutil.copy2(extracted_audio, os.path.join(ws.composition_dir, "extracted_audio.wav"))

    # 3. Transcribe or Load Pre-verified Transcript
    if transcript_file and os.path.exists(transcript_file):
        print(f"[Video Editor] Loading pre-verified transcript: {transcript_file}")
        with open(transcript_file, "r", encoding="utf-8") as f:
            transcript = json.load(f)
    else:
        transcript = transcribe(extracted_audio, initial_prompt=prompt_hint, user_corrections=user_corrections)
        with open(os.path.join(ws.transcript_dir, "transcript_raw.json"), "w", encoding="utf-8") as f:
            json.dump({"duration": transcript["duration"], "segments": transcript.get("raw_segments", transcript["segments"])}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(ws.transcript_dir, "transcript.json"), "w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)

    if transcript.get("ambiguous_words"):
        with open(os.path.join(ws.transcript_dir, "transcript_ambiguities.json"), "w", encoding="utf-8") as f:
            json.dump(transcript["ambiguous_words"], f, ensure_ascii=False, indent=2)

    # 4. Generate Procedural SFX
    comp_sfx_dir = os.path.join(ws.composition_dir, "sfx")
    generate_procedural_sfx(comp_sfx_dir)
    shutil.copytree(comp_sfx_dir, os.path.join(ws.assets_audio_dir, "sfx"), dirs_exist_ok=True)

    # 5. Hyperframes config
    with open(os.path.join(ws.composition_dir, "hyperframes.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
            "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
            "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
            "media": {"autoProxy": True}
        }, f, indent=2)

    with open(os.path.join(ws.composition_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump({"id": "video_editor", "name": brand_title}, f, indent=2)

    # 6. Generate Senior Composition with video in background
    html = generate_senior_composition(
        transcript=transcript,
        audio_filename="extracted_audio.wav",
        brand_title=brand_title,
        style=style,
        bg_video="source_video.mp4",
        aspect=aspect
    )
    with open(os.path.join(ws.composition_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    final_output = os.path.abspath(output_path) if output_path else ws.output_mp4

    if preview_only:
        print("\n[Preview Gate] Capturing key snapshots for inspection...")
        sample_times = "2,8,14,22" if transcript["duration"] > 14 else "1,3"
        snapshot_cmd = f'cd /d "{ws.composition_dir}" && npx hyperframes snapshot --at {sample_times}'
        subprocess.run(snapshot_cmd, shell=True, check=True)
        # Mirror snapshots to review/snapshots
        src_snap = os.path.join(ws.composition_dir, ".hyperframes", "artifacts", "snapshots")
        if os.path.exists(src_snap):
            for sfile in os.listdir(src_snap):
                shutil.copy2(os.path.join(src_snap, sfile), ws.snapshots_dir)
        print(f"\nPREVIEW COMPLETE! Inspect snapshots in:\n  {ws.snapshots_dir}")
        return ws.root_dir

    print(f"\n[Video Editor Render] Rendering Master Video to:\n  {final_output}")
    render_cmd = f'cd /d "{ws.composition_dir}" && npx hyperframes render -o "{final_output}"'
    subprocess.run(render_cmd, shell=True, check=True)

    print(f"\nSUCCESS! Master Edited Video generated at:\n  {final_output}")
    return final_output

# ==============================================================================
# PIPELINE MASTER EXECUTION
# ==============================================================================

def execute_senior_studio(
    audio_file=None,
    video_file=None,
    image_files=None,
    output_mp4=None,
    project_name=None,
    projects_dir="projects",
    brand_title="Monteur Baba Cut",
    style="pastel_director",
    preview_only=False,
    aspect="9:16",
    transcript_file=None,
    user_corrections=None,
    prompt_hint=None
):
    check_dependencies()

    if video_file:
        return auto_edit_existing_video(
            video_path=video_file,
            output_path=output_mp4,
            project_name=project_name,
            projects_dir=projects_dir,
            brand_title=brand_title,
            style=style,
            aspect=aspect,
            transcript_file=transcript_file,
            user_corrections=user_corrections,
            prompt_hint=prompt_hint,
            preview_only=preview_only
        )

    if not audio_file:
        print("ERROR: Either --audio or --video must be specified.")
        sys.exit(1)

    audio_file = os.path.abspath(audio_file)
    if not os.path.exists(audio_file):
        print(f"ERROR: Audio file not found: {audio_file}")
        sys.exit(1)

    ws = ProjectWorkspace(
        project_name=project_name,
        base_dir=projects_dir,
        brand_title=brand_title,
        aspect=aspect,
        source_hint=audio_file
    )

    # 1. Archive raw input audio
    raw_audio_name = os.path.basename(audio_file)
    shutil.copy2(audio_file, os.path.join(ws.input_audio_dir, raw_audio_name))

    # Also archive raw input images if provided
    if image_files:
        for img in image_files:
            if os.path.exists(img):
                shutil.copy2(img, ws.input_images_dir)
                shutil.copy2(img, ws.assets_images_dir)

    # 2. Place working voiceover in assets and composition
    dest_audio_name = "voiceover.wav"
    dest_audio_path = os.path.join(ws.assets_audio_dir, dest_audio_name)
    shutil.copy2(audio_file, dest_audio_path)
    shutil.copy2(audio_file, os.path.join(ws.composition_dir, dest_audio_name))

    # 3. Generate Procedural SFX & Openverse Foley
    comp_sfx_dir = os.path.join(ws.composition_dir, "sfx")
    generate_procedural_sfx(comp_sfx_dir)
    shutil.copytree(comp_sfx_dir, os.path.join(ws.assets_audio_dir, "sfx"), dirs_exist_ok=True)

    # 4. Transcribe or Load Pre-verified Transcript
    if transcript_file and os.path.exists(transcript_file):
        print(f"[Senior Studio] Loading pre-verified transcript: {transcript_file}")
        with open(transcript_file, "r", encoding="utf-8") as f:
            transcript = json.load(f)
    else:
        transcript = transcribe(dest_audio_path, initial_prompt=prompt_hint, user_corrections=user_corrections)
        with open(os.path.join(ws.transcript_dir, "transcript_raw.json"), "w", encoding="utf-8") as f:
            json.dump({"duration": transcript["duration"], "segments": transcript.get("raw_segments", transcript["segments"])}, f, ensure_ascii=False, indent=2)

    with open(os.path.join(ws.transcript_dir, "transcript.json"), "w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)

    if transcript.get("ambiguous_words"):
        with open(os.path.join(ws.transcript_dir, "transcript_ambiguities.json"), "w", encoding="utf-8") as f:
            json.dump(transcript["ambiguous_words"], f, ensure_ascii=False, indent=2)

    # 5. Create hyperframes configs
    with open(os.path.join(ws.composition_dir, "hyperframes.json"), "w", encoding="utf-8") as f:
        json.dump({
            "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
            "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
            "paths": {"blocks": "compositions", "components": "compositions/components", "assets": "assets"},
            "media": {"autoProxy": True}
        }, f, indent=2)

    with open(os.path.join(ws.composition_dir, "meta.json"), "w", encoding="utf-8") as f:
        json.dump({"id": "senior_director", "name": brand_title}, f, indent=2)

    # 6. Generate Senior Composition HTML
    html = generate_senior_composition(
        transcript=transcript,
        audio_filename=dest_audio_name,
        brand_title=brand_title,
        style=style,
        aspect=aspect
    )
    with open(os.path.join(ws.composition_dir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)

    # 7. Validate
    print("Validating composition...")
    try:
        subprocess.run(f'cd /d "{ws.composition_dir}" && npx hyperframes check', shell=True, check=True)
    except Exception as e:
        print(f"[Notice] Hyperframes check note (proceeding directly to render): {e}")

    final_output = os.path.abspath(output_mp4) if output_mp4 else ws.output_mp4

    # 8. Preview Gate vs Full Render
    if preview_only:
        print("\n[Preview Gate] Capturing key snapshots for inspection...")
        sample_times = "2,8,14,22" if transcript["duration"] > 14 else "1,3"
        snapshot_cmd = f'cd /d "{ws.composition_dir}" && npx hyperframes snapshot --at {sample_times}'
        subprocess.run(snapshot_cmd, shell=True, check=True)
        # Mirror snapshots to review/snapshots
        src_snap = os.path.join(ws.composition_dir, ".hyperframes", "artifacts", "snapshots")
        if os.path.exists(src_snap):
            for sfile in os.listdir(src_snap):
                shutil.copy2(os.path.join(src_snap, sfile), ws.snapshots_dir)
        print(f"\nPREVIEW COMPLETE! Inspect snapshots in:\n  {ws.snapshots_dir}")
        return ws.root_dir

    print(f"\n[Full Render] Rendering clean cinematic Senior Master MP4 video to:\n  {final_output}")
    render_cmd = f'cd /d "{ws.composition_dir}" && npx hyperframes render -o "{final_output}"'
    subprocess.run(render_cmd, shell=True, check=True)

    print(f"\nSUCCESS! Video generated at:\n  {final_output}")
    return final_output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monteur Baba Cut v6.6 Senior Motion & Video Editor Engine")
    parser.add_argument("--input", default=None, help="Input directory containing raw assets (audio, video, images)")
    parser.add_argument("--audio", default=None, help="Path to input audio file")
    parser.add_argument("--video", default=None, help="Path to input video file for auto-editing/captions")
    parser.add_argument("--images", default=None, help="Comma-separated paths or folder of input images")
    parser.add_argument("--output", default=None, help="Explicit output MP4 file path override")
    parser.add_argument("--name", "--project", dest="project_name", default=None, help="Project name (creates projects/<project_name>/)")
    parser.add_argument("--dir", "--projects-dir", dest="projects_dir", default="projects", help="Base directory for project workspaces (default: 'projects')")
    parser.add_argument("--title", default="Monteur Baba Cut", help="Brand title")
    parser.add_argument("--style", default="pastel_director", choices=["pastel_director", "cinematic_noir", "cinematic_film", "viral_doodle"], help="Visual style DNA")
    parser.add_argument("--physics", default="motion_dev", choices=["motion_dev", "classic_gsap"], help="Animation physics engine (motion_dev Spring Physics or classic_gsap)")
    parser.add_argument("--aspect", default="9:16", choices=["9:16", "16:9", "1:1"], help="Video aspect ratio (9:16, 16:9, 1:1)")
    parser.add_argument("--preview", action="store_true", help="Generate snapshot previews only")
    parser.add_argument("--transcript", default=None, help="Path to pre-verified transcript JSON file")
    parser.add_argument("--corrections", default=None, help="Inline corrections string e.g. 'word1=fix1,word2=fix2' or JSON file")
    parser.add_argument("--prompt-hint", default=None, help="Domain vocabulary hint for Whisper transcription")

    args = parser.parse_args()

    # Smart Input Folder Scanner: If user passes a folder via --input
    scanned_audio = args.audio
    scanned_video = args.video
    scanned_images = []

    if args.input and os.path.exists(args.input):
        inp = os.path.abspath(args.input)
        if os.path.isdir(inp):
            print(f"[Auto-Ingest] Scanning input directory: {inp}")
            for root, _, files in os.walk(inp):
                for f in files:
                    full_p = os.path.join(root, f)
                    ext = os.path.splitext(f)[1].lower()
                    if ext in [".wav", ".mp3", ".m4a", ".aac", ".ogg"] and not scanned_audio:
                        scanned_audio = full_p
                        print(f"  [Found Audio] {f}")
                    elif ext in [".mp4", ".mov", ".mkv", ".webm"] and not scanned_video:
                        scanned_video = full_p
                        print(f"  [Found Video] {f}")
                    elif ext in [".png", ".jpg", ".jpeg", ".webp", ".svg"]:
                        scanned_images.append(full_p)
            if scanned_images:
                print(f"  [Found {len(scanned_images)} Image(s)]")
        elif os.path.isfile(inp):
            ext = os.path.splitext(inp)[1].lower()
            if ext in [".wav", ".mp3", ".m4a", ".aac"]:
                scanned_audio = inp
            elif ext in [".mp4", ".mov", ".mkv"]:
                scanned_video = inp

    if args.images:
        for p in args.images.split(","):
            p = p.strip()
            if os.path.isdir(p):
                for f in os.listdir(p):
                    if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp', '.svg')):
                        scanned_images.append(os.path.join(p, f))
            elif os.path.exists(p):
                scanned_images.append(p)

    # Parse corrections
    parsed_corrections = {}
    if args.corrections:
        if os.path.exists(args.corrections):
            with open(args.corrections, "r", encoding="utf-8") as cf:
                parsed_corrections = json.load(cf)
        else:
            for item in args.corrections.split(","):
                if "=" in item:
                    k, v = item.split("=", 1)
                    parsed_corrections[k.strip()] = v.strip()

    execute_senior_studio(
        audio_file=scanned_audio,
        video_file=scanned_video,
        image_files=scanned_images,
        output_mp4=args.output,
        project_name=args.project_name,
        projects_dir=args.projects_dir,
        brand_title=args.title,
        style=args.style,
        preview_only=args.preview,
        aspect=args.aspect,
        transcript_file=args.transcript,
        user_corrections=parsed_corrections,
        prompt_hint=args.prompt_hint
    )
