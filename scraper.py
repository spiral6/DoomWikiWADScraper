from playwright.sync_api import sync_playwright
import json

with open('result.json', 'r', encoding="utf-8") as file:
    PWADS = json.load(file)

playwright = sync_playwright().start()
browser = playwright.chromium.launch(headless=False)
page = browser.new_page()
# page.goto("https://doomwiki.org/wiki/Category:PWADs_by_name")
page.goto("https://doomwiki.org/w/index.php?title=Category:PWADs_by_name&pagefrom=Trydent#mw-pages")
page.set_default_timeout(5000)
page.pause()
next_page_locator = page.get_by_role("link", name="next page").first

while(next_page_locator):
    PWADS_locator = page.locator(".mw-category").get_by_role("listitem")
    for i in range(0, PWADS_locator.count()):
    # for i in range(0, PWADS_locator.count()):
        PWAD_obj = {"name": "", "image": ""}
        PWAD = PWADS_locator.nth(i)
        # print(PWAD.text_content())
        PWAD_obj["name"] = PWAD.text_content()
        # print(PWAD.get_by_role("link").get_attribute('href'))
        # page.pause()
        page.goto("https://doomwiki.org" + str(PWAD.get_by_role("link").get_attribute('href')))
        # page.pause()
        logo_locator = page.locator(".wikitable:not(.dw-navbox)").get_by_role("row").nth(1)
        try:
            # logo_locator.wait_for(timeout=5000)
            logo_asset_link = logo_locator.get_by_role("link").get_attribute('href')
            if (logo_asset_link != "/wiki/Vertex"):
                logo_locator.click()
                # page.pause()
            image_locator = page.locator(".fullImageLink").get_by_role("link").nth(0)
            # print("https://doomwiki.org" + str(image_locator.get_attribute('href')))
            PWAD_obj["image"] = "https://doomwiki.org" + str(image_locator.get_attribute('href'))
            # page.pause()
            page.go_back()
            page.go_back()
        except: 
            # print("Image not found for " + page.title())
            PWAD_obj["image"] = "N/A"
            page.go_back()
        print(PWAD_obj)
        PWADS.append(PWAD_obj)
        print(" ")
        PWADS_locator = page.locator(".mw-category").get_by_role("listitem")
    try:
        next_page_locator = page.get_by_role("link", name="next page").first
        next_page_locator.wait_for(timeout=5000)
        with open('result.json', 'w', encoding="utf-8") as file:
            json.dump(PWADS, file, ensure_ascii=False)
        page.goto("https://doomwiki.org" + next_page_locator.get_attribute('href') )
    except:
        with open('result.json', 'w', encoding="utf-8") as file:
            json.dump(PWADS, file, ensure_ascii=False)
        break

print("All done.")


# print(page.locator(".mw-category").get_by_role("listitem").count())
browser.close() 