import asyncio
import locale
import time
from argparse import Namespace

from dotenv import load_dotenv

from app import App
from entities.entities import ProductData
from log import flagged_logger, logger
from presentation import Presentation
from scraper import run_scraper_task, scrape


# FIX: Move to other place
async def load_test(app_args: Namespace, references: list[str]):
    # iterates to scrape data and log
    for test_idx in range(app_args.load_test):
        print(f"Loop {test_idx+1}/{app_args.load_test}")
        task_result = await scrape(references, app_args.headless)
        if task_result:
            for [ref_data, not_found] in task_result:
                has_data = "not found" if not_found else "ok"
                msg = f"load_test-{test_idx+1}: {ref_data['ref']}-{has_data}"
                logger.info(
                    f"load_test-{test_idx+1}: {ref_data['ref']}-{ref_data['title']}"
                )
                flagged_logger.info(msg)
                print(f"\t{msg}")


async def main():
    # Variables
    start_time = time.time()
    load_dotenv()
    locale.setlocale(locale.LC_TIME, "")

    print("-------------****-------------- ")

    app = App()
    app.prompt()
    saving_path = app.get_saving_path()
    refs_to_quote: list[ProductData] = []

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
        await load_test(app.args, references)

    else:
        found_refs, not_found_refs = await run_scraper_task(app, references)
        refs_to_quote.extend(found_refs)

    if not app.args.load_test:
        if len(not_found_refs) > 0:
            retry = app.prompt_not_found(not_found_refs)
            while retry:
                found_refs, not_found_refs = await run_scraper_task(app, not_found_refs)
                refs_to_quote.extend(found_refs)
                if len(not_found_refs) == 0:
                    break

                retry = app.prompt_not_found(not_found_refs)

        presentation.create_pptx(refs_to_quote)
        presentation.save(saving_path)
        app.increment_consecutive()

    total_time = "{:.2f}".format((time.time() - start_time) / 60)
    print(f"\n-------- Proceso Finalizado en {total_time} minutos --------")


asyncio.run(main())
