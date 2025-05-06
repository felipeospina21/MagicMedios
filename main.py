import asyncio
import locale
import time

from dotenv import load_dotenv

from app import App
from log import flagged_logger
from presentation import Presentation
from scraper import scrape


async def main():
    # Variables
    start_time = time.time()
    load_dotenv()
    locale.setlocale(locale.LC_TIME, "")

    print("-------------****-------------- ")

    app = App()
    app.prompt()

    contact = app.get_footer()
    representative = app.get_contact_info()
    consecutive = app.get_consecutive()
    client = app.get_client()
    references = app.get_references()

    presentation = Presentation(len(references))
    presentation.set_slides(contact)
    presentation.add_header(representative, consecutive)
    presentation.add_client_name(client)
    presentation.add_commercial_policy_slide()

    if app.args.load_test:
        # iterates to scrape data and log
        for test_idx in range(app.args.load_test):
            print(f"Loop {test_idx+1}/{app.args.load_test}")
            scraped_refs = await scrape(references, app.args.headless)
            if scraped_refs:
                for ref_data in scraped_refs:
                    has_data = "ok" if ref_data["title"] else "not found"
                    flagged_logger.info(
                        f"load_test-{test_idx+1}: {ref_data['ref']}-{has_data}"
                    )

    else:
        scraped_refs = await scrape(references, app.args.headless)
        if scraped_refs:
            for idx, ref_data in enumerate(scraped_refs):
                presentation.create_title(
                    ref_data["title"], idx, count=idx + 1, ref=ref_data["ref"]
                )
                if "subtitle" in ref_data:
                    presentation.create_subtitle(ref_data["subtitle"], idx)

                presentation.create_description(ref_data["description"], idx)
                presentation.create_img(ref_data["image"], idx)
                presentation.create_quantity_table(idx)
                presentation.create_inventory_table(ref_data["color_inventory"], idx)

    if not app.args.load_test:
        path = app.get_saving_path()
        presentation.save(path)
        app.create_new_consecutive()

    total_time = "{:.2f}".format((time.time() - start_time) / 60)
    print(f"\n-------- Proceso Finalizado en {total_time} minutos --------")


asyncio.run(main())
