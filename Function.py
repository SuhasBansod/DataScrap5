from playwright.sync_api import sync_playwright

def Wait(Browserpage,Timeout=3000):
    Browserpage.wait_for_load_state('networkidle')
    Browserpage.wait_for_load_state('domcontentloaded')
    Browserpage.wait_for_timeout(Timeout)
