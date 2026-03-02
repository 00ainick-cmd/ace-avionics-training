import asyncio
from playwright.async_api import async_playwright
import sys

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        
        page.on("console", lambda msg: print(f"Console {msg.type}: {msg.text}"))
        page.on("pageerror", lambda exc: print(f"Page Error: {exc}"))
        
        print("Navigating to drill...")
        await page.goto('http://localhost:8080/shared/drill.html')
        await page.wait_for_timeout(2000)
        print("Taking screenshot...")
        await page.screenshot(path='c:/Users/nickb/Downloads/ace-avionics-training-main/ace-avionics-training-main/tmp_drill.png')
        await browser.close()
        print("Done.")

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    asyncio.run(main())
