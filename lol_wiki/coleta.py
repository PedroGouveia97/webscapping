# %%
import requests as r
import pandas as pd
from bs4 import BeautifulSoup
from datetime import date
# %%
cookies = {
    'Geo': '{%22region%22:%22SP%22%2C%22city%22:%22barueri%22%2C%22country_name%22:%22brazil%22%2C%22country%22:%22BR%22%2C%22continent%22:%22SA%22}',
    'wikia_beacon_id': 'BXaPRGmVDL',
    '_b2': 'YgW_R7e9EL.1712916761798',
    'sessionId': '43ad116a-2b26-46d9-bbfa-574f4d6c9c89',
    'wikia_session_id': 'PQelQYwdpo',
    '_pubcid': '56154216-73fd-4932-8378-81b0d527d14c',
    '_pubcid_cst': 'NizBLMYsmw%3D%3D',
    'Geo': 'OK',
    'euconsent-v2': 'CPt3fQAPt3fQACNAFAENDLCgAAAAAAAAACiQAAAOCgDAB-AIsAZ8A6QDBAHBAAAA.YAAAAAAAAAAA',
    'tracking-opt-in-status': 'rejected',
    'addtl_consent': '1~',
    'disable_no_video_exp': '1',
    'pvNumber': '6',
    'pvNumberGlobal': '9',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'accept-language': 'pt-BR,pt;q=0.9',
    'cache-control': 'max-age=0',
    'referer': 'https://leagueoflegends.fandom.com/pt-br/wiki/Campe%C3%A3o',
    'sec-ch-ua': '"Brave";v="123", "Not:A-Brand";v="8", "Chromium";v="123"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'sec-gpc': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
}

# %%
def get_content(url):    
    resp = r.get(url, headers=headers, cookies=cookies)
    return resp
# %%
url = 'https://leagueoflegends.fandom.com/pt-br/wiki/Lista_de_campe%C3%B5es'
resp = get_content(url)
soup = BeautifulSoup(resp.text)

# %%
champ_list = soup.find('tbody').find_all('tr')

columns = champ_list[0].text.split('\n')
columns = [x.strip() for x in columns if x != '']
# %%
df_champ = pd.DataFrame(columns=columns)

for prop_brz in champ_list[1:]:
    prop_brz = prop_brz.text.split('\n')
    prop = [x.strip() for x in prop_brz if x != '']

    campeao = prop[0]
    classes = prop[1]
    dt_lanc = prop[2]
    dt_muda = prop[3]
    cust_ea = prop[4]
    cust_rp = prop[5]

    new_row = {
	    'Campeão'           : campeao,
        'Classes'           : classes,
        'Data de Lançamento': dt_lanc,
        'Última Mudança'    : dt_muda,
        'Essência Azul'     : cust_ea,
        'RP'                : cust_rp,
    }
    new_df = pd.DataFrame(new_row, index=[0])
    #df_champ = df_champ.append(new_row, ignore_index = True) #about to be deprecated
    df_champ = pd.concat([df_champ, new_df], ignore_index=True)


# %%
hoje = date.today()
# %%
df_champ.to_csv(f'dados/lol_champion_list__{hoje}')

# %%
