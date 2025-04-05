import asyncio
import locale
import time

from dotenv import load_dotenv

from entities.presentation import Presentation
from app import App
from scrape import scrape


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

    data = await scrape(references)
    for d in data:
        print(d)
        print("\n")

    presentation = Presentation(len(references))
    presentation.set_slides(contact)
    presentation.add_header(representative, consecutive)
    presentation.add_client_name(client)
    presentation.add_commercial_policy_slide()
    #
    # # quotation.save()
    # quotation.create_new_consecutive()
    #
    total_time = "{:.2f}".format((time.time() - start_time) / 60)
    print(f"\n-------- Proceso Finalizado en {total_time} minutos --------")


asyncio.run(main())
