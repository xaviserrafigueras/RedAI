"""
Metadata and EXIF Extraction
"""

import os
import shutil
import subprocess
from datetime import datetime

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

from redai.core.display import display
from redai.core.utils import suggest_ai_analysis
from redai.database.repository import save_scan


def metadata_scan(filepath: str, project: str = "General", auto: bool = False):
    """Extracción profunda de metadatos (PDF/Docs/Img)."""
    if not os.path.exists(filepath):
        display.error(f"File not found: {filepath}")
        return
        
    display.step(f"Analyzing Metadata: {filepath}")
    
    # Basic stat info
    stat_info = os.stat(filepath)
    creation_time = datetime.fromtimestamp(stat_info.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
    mod_time = datetime.fromtimestamp(stat_info.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
    
    meta_results = [
        f"Creation: {creation_time}",
        f"Modified: {mod_time}",
        f"Size: {stat_info.st_size} bytes"
    ]
    
    # ExifTool if available
    if shutil.which("exiftool"):
        try:
            proc = subprocess.run(["exiftool", filepath], capture_output=True, text=True)
            if proc.returncode == 0:
                meta_results.append("\n" + proc.stdout)
            else:
                meta_results.append("\nExifTool Failed.")
        except:
            pass
    else:
        meta_results.append("\n(ExifTool not installed. Install for PDF/DOC/Video metadata support)")
    
    out = "\n".join(meta_results)
    display.panel(out, "Metadata Report", style="green")
    suggest_ai_analysis(out, "Metadata Analysis")
    save_scan(filepath, "metadata", out, project)


def exif_scan(image_path: str, project: str = "General", auto: bool = False):
    """Extrae metadatos EXIF y GPS de imágenes."""
    display.header(f"EXIF Scanner: {image_path}")
    
    if not os.path.exists(image_path):
        display.error(f"Image not found: {image_path}")
        return
    
    try:
        img = Image.open(image_path)
        exif_data = img._getexif()
        
        if not exif_data:
            display.warning("No EXIF data found in image.")
            return
        
        results = []
        gps_info = {}
        
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            
            if tag == "GPSInfo":
                for gps_tag_id, gps_value in value.items():
                    gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    gps_info[gps_tag] = gps_value
            else:
                results.append(f"{tag}: {value}")
        
        # Parse GPS coordinates
        if gps_info:
            def convert_to_degrees(value):
                d, m, s = value
                return float(d) + float(m) / 60 + float(s) / 3600
            
            try:
                lat = convert_to_degrees(gps_info.get('GPSLatitude', (0, 0, 0)))
                lon = convert_to_degrees(gps_info.get('GPSLongitude', (0, 0, 0)))
                
                if gps_info.get('GPSLatitudeRef') == 'S':
                    lat = -lat
                if gps_info.get('GPSLongitudeRef') == 'W':
                    lon = -lon
                
                results.append(f"\n🌍 GPS Coordinates: {lat}, {lon}")
                results.append(f"📍 Google Maps: https://www.google.com/maps?q={lat},{lon}")
            except:
                pass
        
        output = "\n".join(results)
        display.panel(output, "EXIF Data", style="cyan")
        suggest_ai_analysis(output, "EXIF Analysis")
        save_scan(image_path, "exif", output, project)
        
    except Exception as e:
        display.error(f"EXIF Error: {e}")
