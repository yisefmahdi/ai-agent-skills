"""
Monteur Baba Cut - Openverse Audio & Foley Sound Engine (v6.6)
Searches and downloads real studio-recorded Foley sound effects and background audio
from Openverse (Creative Commons, CC0, FreeSound, Wikimedia, Jamendo).
Features:
  - Smart persistent caching in `sfx_cache/` (zero redundant downloads).
  - Commercial license filtering (100% copyright-safe).
  - Uniform conversion to 44.1kHz Stereo WAV via FFmpeg.
  - Automatic graceful fallback to Procedural Waveform Synthesis when offline.
"""

import os
import json
import ssl
import re
import urllib.request
import urllib.parse
import subprocess

# Default SSL context for resilient requests
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MonteurBabaCut/6.6 (Creative Commons Production Engine)"
}

API_BASE = "https://api.openverse.org/v1/audio/"

FOLEY_PRESETS = {
    "excavator_digging": "excavator digging diesel dirt",
    "gas_leak_hiss": "gas leak steam air pressure hiss",
    "liquid_trickle": "liquid water dripping puddle splash",
    "metal_vault": "heavy metal container hollow clank",
    "ui_click": "mouse click switch button",
    "fast_whoosh": "fast whoosh air cinematic transition",
    "deep_impact": "cinematic sub bass impact drop",
    "ambient_tech_bgm": "ambient technology light corporate background"
}


class OpenverseAudioClient:
    """عميل البحث والتنزيل التلقائي للمؤثرات الصوتية الحقيقية من Openverse."""
    
    def __init__(self, cache_dir="sfx_cache"):
        self.cache_dir = os.path.abspath(cache_dir)
        os.makedirs(self.cache_dir, exist_ok=True)

    def search_audio(self, query, license_type="commercial,modification", max_duration_sec=45, page_size=6):
        """البحث في Openverse عن مؤثرات صوتية مرخصة تجارياً."""
        params = {
            "q": query,
            "license_type": license_type,
            "page_size": page_size
        }
        query_string = urllib.parse.urlencode(params)
        url = f"{API_BASE}?{query_string}"
        
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=8) as response:
                if response.status == 200:
                    data = json.loads(response.read().decode("utf-8"))
                    results = data.get("results", [])
                    # Filter candidates that have valid preview/stream URLs
                    valid = []
                    for item in results:
                        audio_url = item.get("url")
                        dur_ms = item.get("duration") or 0
                        dur_sec = dur_ms / 1000.0 if dur_ms > 0 else 0
                        if audio_url and (max_duration_sec is None or dur_sec <= max_duration_sec):
                            valid.append({
                                "id": item.get("id"),
                                "title": item.get("title"),
                                "url": audio_url,
                                "duration_sec": dur_sec,
                                "license": item.get("license"),
                                "provider": item.get("provider")
                            })
                    return valid
        except Exception as e:
            print(f"[Openverse] Search notice for '{query}': {e}")
            return []
        return []

    def download_and_convert(self, audio_url, output_wav_path):
        """تنزيل الملف الصوتي وتحويله إلى صيغة WAV 44.1kHz متوافقة مع الفيديو."""
        temp_ext = os.path.splitext(audio_url.split("?")[0])[-1] or ".mp3"
        temp_file = output_wav_path + ".temp" + temp_ext
        
        req = urllib.request.Request(audio_url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, context=SSL_CTX, timeout=15) as resp:
                with open(temp_file, "wb") as f:
                    f.write(resp.read())
            
            # Convert to standard 44.1kHz stereo WAV
            cmd = f'ffmpeg -y -i "{temp_file}" -ar 44100 -ac 2 "{output_wav_path}"'
            subprocess.run(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return True
        except Exception as e:
            print(f"[Openverse] Download/Conversion error: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            return False

    def get_foley_sfx(self, semantic_tag, fallback_generator=None):
        """
        جلب المؤثر الصوتي المطلوب؛ إما من الكاش المحلي، أو بتنزيله من Openverse،
        أو عبر المولد الإجرائي في حالة عدم الاتصال.
        """
        clean_tag = re.sub(r"[^a-zA-Z0-9_]+", "_", semantic_tag.strip().lower())
        cached_path = os.path.join(self.cache_dir, f"sfx_{clean_tag}.wav")
        
        # 1. Check Local Cache
        if os.path.exists(cached_path) and os.path.getsize(cached_path) > 1024:
            return cached_path
            
        # 2. Search Openverse
        search_query = FOLEY_PRESETS.get(semantic_tag, semantic_tag.replace("_", " "))
        print(f"[Openverse Foley] Querying real audio for: '{search_query}'...")
        candidates = self.search_audio(search_query)
        
        if candidates:
            # Pick best match (prefer CC0 or shortest fitting sound)
            best = candidates[0]
            for c in candidates:
                if c.get("license") in ["cc0", "pdm"]:
                    best = c
                    break
                    
            print(f"[Openverse Foley] Downloading '{best['title']}' ({best['provider']}, {best['license']})...")
            ok = self.download_and_convert(best["url"], cached_path)
            if ok and os.path.exists(cached_path):
                return cached_path
                
        # 3. Offline / Fallback Generator
        if fallback_generator:
            print(f"[Openverse Foley] Using local fallback synthesizer for '{semantic_tag}'")
            return fallback_generator(cached_path)
            
        return None


# Global singleton client instance
_default_client = None

def get_openverse_client(cache_dir="sfx_cache"):
    global _default_client
    if _default_client is None:
        _default_client = OpenverseAudioClient(cache_dir=cache_dir)
    return _default_client


def resolve_scene_foley_sfx(tag, output_dir="sfx_cache", fallback_func=None):
    """دالة المساعدة السريعة لاستدعاء أي مؤثر صوتي حقيقي."""
    client = get_openverse_client(cache_dir=output_dir)
    return client.get_foley_sfx(tag, fallback_generator=fallback_func)


if __name__ == "__main__":
    client = OpenverseAudioClient(cache_dir="scratch/sfx_cache_test")
    print("Testing Openverse Foley Engine...")
    path = client.get_foley_sfx("fast_whoosh")
    print("Resolved Whoosh Path:", path)
    if path and os.path.exists(path):
        print("File size:", os.path.getsize(path), "bytes")
