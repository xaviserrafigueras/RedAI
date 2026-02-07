"""
Phone Number OSINT
"""

from redai.core.display import display
from redai.core.utils import suggest_ai_analysis
from redai.database.repository import save_scan

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
    PHONENUMBERS_AVAILABLE = True
except ImportError:
    PHONENUMBERS_AVAILABLE = False


def phone_osint(number: str, project: str = "General", auto: bool = False):
    """Phone Number Intelligence (Carrier, Location, Timezone)."""
    display.step(f"Analyzing Number: {number}...")
    
    if not PHONENUMBERS_AVAILABLE:
        display.error("Phonenumbers library not found. Run: pip install phonenumbers")
        return
    
    try:
        parsed_num = phonenumbers.parse(number)
        
        if not phonenumbers.is_valid_number(parsed_num):
            display.warning("Number is invalid or impossible.")
            return
            
        region = geocoder.description_for_number(parsed_num, "en")
        org = carrier.name_for_number(parsed_num, "en")
        tz = timezone.time_zones_for_number(parsed_num)
        
        info_text = (
            f"🌍 Region: {region}\n"
            f"🏢 Carrier: {org}\n"
            f"🕒 Timezones: {', '.join(tz)}\n"
            f"✅ Valid: Yes\n"
            f"📞 Format: {phonenumbers.format_number(parsed_num, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}"
        )
        
        display.panel(info_text, "Phone Intelligence", style="green")
        suggest_ai_analysis(info_text, "Phone OSINT")
        save_scan(number, "phone_osint", info_text, project)
        
    except Exception as e:
        display.error(f"Phone Analysis Failed: {e}")
