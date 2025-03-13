import asyncio
import requests
from io import BytesIO
from PIL import Image
from playwright.async_api import async_playwright
from pptx import Presentation
from pptx.util import Inches


async def scrape_product(browser, product_code):
    """Scrapes product details (name & image URL) for a given product code."""
    context = await browser.new_context()  # Isolated context per product
    page = await context.new_page()

    await page.goto("https://www.catalogospromocionales.com/")
    print(product_code)

    await search_product(page, product_code, delay=0)

    # Click the first product image in the results
    await page.click(".img-producto")

    # Ensure navigation completes
    # await page.wait_for_url("**/p/**", timeout=1000)

    # Wait for product details to be available
    await page.wait_for_selector("#img_01", timeout=5000)

    # Extract product name and image URL
    product_name = await page.locator(".hola").first.text_content()
    product_image_url = await page.locator("#img_01").first.get_attribute("src")

    await context.close()  # Close context to free up memory
    return product_code, product_name, product_image_url


async def download_image(url, save_path):
    """Downloads an image from the given URL and saves it."""
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    image.save(save_path)


async def create_ppt(products):
    """Generates a PowerPoint presentation with a slide for each product."""
    prs = Presentation()

    for product_code, product_name, image_path in products:
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # Blank slide

        # Add product name
        title = slide.shapes.title
        title.text = f"{product_code} - {product_name}"

        # Add product image
        left, top, height = Inches(1), Inches(2), Inches(3)
        slide.shapes.add_picture(image_path, left, top, height=height)

    prs.save("Product_Presentation.pptx")
    print("PowerPoint created: Product_Presentation.pptx")


async def search_product(page, product_code, retries=3, delay=2):
    """Attempts to search for a product, retrying if the selector is not found."""
    for attempt in range(retries):
        print(f"Searching for product {product_code} (Attempt {attempt + 1}/{retries})")

        # Clear input before retrying
        await page.fill("input[id='productos']", "")
        await asyncio.sleep(0.5)  # Short delay before retyping

        # Perform search
        await page.fill("input[id='productos']", product_code)
        await page.press("input[id='productos']", "Enter")

        # Wait for search results
        found = await wait_for_selector_with_retry(
            page, ".img-producto", timeout=1000, retries=3, delay=0
        )
        if found:
            return  # Product found, exit loop

        print(f"Retrying search for {product_code} in {delay} seconds...")
        await asyncio.sleep(delay)  # Wait before retrying

    print(f"Failed to find product {product_code} after {retries} attempts.")


async def wait_for_selector_with_retry(
    page, selector, timeout=5000, retries=3, delay=2
):
    """Retries waiting for a selector multiple times before failing."""
    for attempt in range(retries):
        try:
            await page.wait_for_selector(selector, timeout=timeout)
            return True  # Found selector, exit function
        except Exception as e:
            print(
                f"Retry {attempt + 1}/{retries}: {selector} not found. Retrying in {delay} sec..."
            )
            if attempt < retries - 1:
                await asyncio.sleep(delay)  # Wait before retrying
            else:
                print(f"Failed to find selector: {selector} after {retries} attempts.")
                return False  # Final failure


async def main():

    product_codes = ["VA-1153", "VA-509", "so-65"]  # Add more product codes
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        # Run scrapers concurrently with separate contexts
        tasks = [scrape_product(browser, code) for code in product_codes]
        results = await asyncio.gather(*tasks)

        await browser.close()

    # Download images and prepare data for PowerPoint
    product_data = []
    for code, name, img_url in results:
        image_path = f"{code}.jpg"
        await download_image(img_url, image_path)
        product_data.append((code, name, image_path))

    # Create PowerPoint presentation
    await create_ppt(product_data)


asyncio.run(main())
