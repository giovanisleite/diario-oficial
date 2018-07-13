from database import PARSABLE_TERRITORIES
from database.models import BiddingExemption
from gazette import locations


class SectionParsing:
    def __init__(self, session):
        self.session = session

    def condition(self):
        return "is_parsed = FALSE"

    def update(self, gazettes):
        for gazette in gazettes:
            territory = PARSABLE_TERRITORIES.get(gazette.territory_id)
            if territory:
                parsing_cls = getattr(locations, territory)
                parser = parsing_cls(gazette.source_text)
                self.update_bidding_exemptions(gazette, parser)
                gazette.is_parsed = True

    def update_bidding_exemptions(self, gazette, parser):
        parsed_exemptions = parser.bidding_exemptions()
        if parsed_exemptions:
            for record in gazette.bidding_exemptions:
                self.session.delete(record)
            for attributes in parsed_exemptions:
                record = BiddingExemption(**attributes)
                record.date = gazette.date
                gazette.bidding_exemptions.append(record)
