# SPDX-FileCopyrightText: 2025 Aindo SpA
#
# SPDX-License-Identifier: MIT

from functools import partial
from typing import Any, Callable, ClassVar, Literal

import pandas as pd
from faker import Faker
from faker.typing import SeedType

from aindo.anonymize.techniques.base import BaseSingleColumnTechnique

# fmt: off
MockingGeneratorMethods = Literal[
    "aba","address","administrative_unit","am_pm","android_platform_token","ascii_company_email","ascii_email",
    "ascii_free_email","ascii_safe_email","bank_country","bban","binary","boolean","bothify","bs","building_number",
    "catch_phrase","century","chrome","city","city_prefix","city_suffix","color","color_name","company",
    "company_email", "company_suffix","coordinate","country","country_calling_code","country_code",
    "credit_card_expire", "credit_card_full","credit_card_number","credit_card_provider",
    "credit_card_security_code","cryptocurrency", "cryptocurrency_code","cryptocurrency_name","csv","currency",
    "currency_code","currency_name","currency_symbol","current_country","current_country_code","date","date_between",
    "date_between_dates","date_object","date_of_birth","date_this_century","date_this_decade","date_this_month",
    "date_this_year","date_time","date_time_ad","date_time_between","date_time_between_dates",
    "date_time_this_century","date_time_this_decade","date_time_this_month","date_time_this_year","day_of_month",
    "day_of_week","dga","domain_name","domain_word","dsv","ean","ean13","ean8","ein","email","emoji","enum",
    "file_extension","file_name","file_path","firefox","first_name","first_name_female","first_name_male",
    "first_name_nonbinary","fixed_width","free_email","free_email_domain","future_date","future_datetime",
    "hex_color","hexify","hostname","http_method","iana_id","iban","image","image_url","internet_explorer",
    "invalid_ssn","ios_platform_token","ipv4","ipv4_network_class","ipv4_private","ipv4_public","ipv6","isbn10",
    "isbn13","iso8601","itin","job","json","json_bytes","language_code","language_name","last_name",
    "last_name_female","last_name_male","last_name_nonbinary","latitude","latlng","lexify","license_plate",
    "linux_platform_token","linux_processor","local_latlng","locale","localized_ean","localized_ean13",
    "localized_ean8","location_on_land","longitude","mac_address","mac_platform_token","mac_processor",
    "md5","military_apo","military_dpo","military_ship","military_state","mime_type","month","month_name",
    "msisdn","name","name_female","name_male","name_nonbinary","nic_handle","nic_handles","null_boolean",
    "numerify","opera","paragraph","paragraphs","password","past_date","past_datetime","phone_number",
    "port_number","postalcode","postalcode_in_state","postalcode_plus4","postcode","postcode_in_state",
    "prefix","prefix_female","prefix_male","prefix_nonbinary","pricetag","profile","providers","psv",
    "pybool","pydecimal","pydict","pyfloat","pyint","pyiterable","pylist","pyset","pystr","pystr_format",
    "pystruct","pytimezone","pytuple","random_choices","random_digit","random_digit_not_null",
    "random_digit_not_null_or_empty","random_digit_or_empty","random_element","random_elements","random_int",
    "random_letter","random_letters","random_lowercase_letter","random_number","random_sample",
    "random_uppercase_letter","randomize_nb_elements","rgb_color","rgb_css_color","ripe_id","safari",
    "safe_color_name","safe_domain_name","safe_email","safe_hex_color","secondary_address","sentence",
    "sentences","sha1","sha256","simple_profile","slug","ssn","state","state_abbr","street_address",
    "street_name","street_suffix","suffix","suffix_female","suffix_male","suffix_nonbinary","swift",
    "swift11","swift8","tar","text","texts","time","time_delta","time_object","time_series","timezone","tld","tsv",
    "unix_device","unix_partition","unix_time","upc_a","upc_e","uri","uri_extension","uri_page","uri_path","url",
    "user_agent","user_name","uuid4","windows_platform_token","word","words","year","zip","zipcode",
    "zipcode_in_state","zipcode_plus4",
]
# fmt: on


class Mocking(BaseSingleColumnTechnique):
    """Implements mocking.

    Mocking generates realistic mock data for various fields such as names, addresses, emails, and more.
    It leverages the `faker` library to produce customizable, locale-aware fake data.

    Attributes:
        data_generator: Faker's generator method ("fake") used to generate data (e.g., name, email).
        seed: A seed to initialize numpy `Generator`.
    """

    preserve_type: ClassVar[bool] = False

    data_generator: "MockingGeneratorMethods"
    seed: SeedType = None

    def __init__(
        self,
        data_generator: "MockingGeneratorMethods",
        seed: SeedType = None,
        faker_kwargs: dict[str, Any] | None = None,
        faker_generator_kwargs: dict[str, Any] | None = None,
    ) -> None:
        """
        Args:
            data_generator: Faker's generator method ("fake") used to generate data (e.g., name, email).
            faker_kwargs: Additional arguments passed to the main Faker object (proxy class).
            faker_generator_kwargs: Additional arguments passed to the Faker's generator method.
        """
        super().__init__()
        fake = Faker(**(faker_kwargs or {}))
        fake_method = getattr(fake, data_generator, None)
        if fake_method is None:
            raise ValueError(f"Faker's generator method '{data_generator}' not found")

        self._fake: Faker = fake
        self.seed = seed
        if seed is not None:
            self._fake.seed_instance(self.seed)

        self._fake_method: Callable[[], Any] = partial(fake_method, **(faker_generator_kwargs or {}))

    def _apply_to_col(self, col: pd.Series) -> pd.Series:
        return pd.Series([self._fake_method() for _ in col])
