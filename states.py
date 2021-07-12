"""US States dictionary"""

from bs4 import BeautifulSoup
from urllib.request import urlopen
import json


def has_href_and_title(tag):
    return tag.has_attr('href') and tag.has_attr('title')


def states_dictionary():
    '''Returns a dictionary of state codes indexed by state name
    source "https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations"'''

    '''
    First table in page contains rows like this:
    <tr>
    <td><span class="flagicon"><img alt="" ...... <a href="/wiki/Alabama" title="Alabama">Alabama</a></td>
    <td><a href="/wiki/U.S._state" title="U.S. state">State</a></td>
    <td style="text-align:center;"><link rel="mw-deduplicated-inline-style" href="mw-data:TemplateStyles:r886049734"/><span class="monospaced">US-AL</span></td>
    <td style="text-align:center;">AL</td>
    <td style="text-align:center;">01</td>
    <td style="text-align:center;">AL</td>
    <td style="text-align:center;">AL</td>
    <td>Ala.</td>
    <td>Ala.</td>
    <td>
    </td></tr>
    '''

    states = {}
    html = urlopen("https://en.wikipedia.org/wiki/List_of_U.S._state_abbreviations")
    soup = BeautifulSoup(html, 'html.parser')

    # Each row in 1st table contains the state name and state code
    # There are some references don't want but they can't be resolved in this step
    table_soup = soup.find('table')

    for r in table_soup.find_all('tr'):
        name_tag = r.find(has_href_and_title)
        # Some tags are empty so they have no text property!
        if name_tag:
            if name_tag.text.strip():
                name = name_tag.text

        code = None
        code_tag = r.find('span', class_='monospaced')
        if code_tag:
            if code_tag.text.strip():
                code = code_tag.text

        states[name] = code

    # Now remove any entries with empty values
    states = {k: v for k, v in states.items() if v}

    return(states)


if __name__ == '__main__':
    states = states_dictionary()

    with open('states.json', 'w', encoding='utf8') as f:
        json.dump(states, f, ensure_ascii=False)
