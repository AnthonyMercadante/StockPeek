from unittest import mock
import pandas as pd
from stockpeek.scraper import scrape_quote

@mock.patch("stockpeek.scraper.webdriver")
def test_scrape_quote(mock_webdriver):
    inst = mock_webdriver.Chrome.return_value
    # mock find_element twice: name, price
    inst.find_element.side_effect = (
        mock.Mock(text="Sample Inc (SMP)"),
        mock.Mock(text="123.45")
    )
    df = scrape_quote("SMP")
    assert isinstance(df, pd.DataFrame)
    assert df.loc[0, "Company"] == "Sample Inc"
    assert df.loc[0, "Price"] == 123.45
