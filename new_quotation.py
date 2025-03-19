import os

from entities.entities import Contact, Representative

# from suppliers import catalogospromo, cdopromo, mppromos, nwpromo, promoop
from utils import create_supplier_ref_list, text_frame_paragraph

# from demo import main
from x import scrape


class Quotation:
    def __init__(self, references: list[str]) -> None:

        self.strip_reference = [ref.strip() for ref in references]

    async def scrapp_data(self):
        await scrape(self.strip_reference)
        # if len(suppliers_list["cat_promo"]) != 0:
        #     # catalogospromo.crawl(suppliers_dict, self.prs, self.strip_reference)
        #     await main(suppliers_dict["cat_promo"], self.prs, self.strip_reference)
        #
        # if len(suppliers_list["mp_promo"]) != 0:
        #     mppromos.crawl(suppliers_dict, self.prs, self.strip_reference)
        # if len(suppliers_list["promo_op"]) != 0:
        #     promoop.get_data(suppliers_dict, self.prs, self.strip_reference)
        # if len(suppliers_list["nw_promo"]) != 0:
        #     nwpromo.get_nw_promo_data(suppliers_dict, self.prs, self.strip_reference)
        # if len(suppliers_list["cdo_promo"]) != 0:
        #     cdopromo.crawl(suppliers_dict, self.prs, self.strip_reference)
