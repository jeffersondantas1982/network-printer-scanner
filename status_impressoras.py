import requests
from bs4 import BeautifulSoup
import urllib3
import base64
import re

# Desativa warnings SSL para certificados autoassinados
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Lista de IPs
ips = [f"172.17.27.{i}" for i in range(101, 111)]

# Palavras-chave para busca no HTML
keywords = [
    "toner", "suprimento", "nivel", "ink", "cartucho", "cartridge",
    "level", "remaining", "status", "amount", "quantidade"
]

resultados = []

def classificar_nivel(texto):
    # Remove tudo que não for número ou % para evitar problemas tipo "60%*"
    texto_limpo = re.sub(r'[^\d%]', '', texto)
    match = re.search(r'(\d+)', texto_limpo)
    if match:
        valor = int(match.group(1))
        if valor <= 20:
            return "BAIXO"
        elif 21 <= valor <= 50:
            return "BOM"
        else:
            return "ALTO"
    return "Não identificado"

for ip in ips:
    nivel = None

    # Tenta acesso HTTP, depois HTTPS ignorando certificado
    try:
        url = f"http://{ip}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        html = response.text
    except requests.exceptions.RequestException:
        try:
            url = f"https://{ip}"
            response = requests.get(url, timeout=5, verify=False)
            response.raise_for_status()
            html = response.text
        except Exception as e:
            print(f"{ip} => ERRO: {e}")
            resultados.append([ip, "ERRO"])
            continue

    # Parse HTML
    soup = BeautifulSoup(html, 'html.parser')

    # Método 1: procura texto com % e keywords
    for line in soup.stripped_strings:
        line_lower = line.lower()
        if "%" in line and any(k in line_lower for k in keywords):
            nivel = line.strip()
            break

    # Método 2: procura estrutura Pantum conhecida
    if nivel is None:
        # div com class 'line cartridges'
        div_cartridges = soup.find("div", class_="line cartridges")
        if div_cartridges:
            span_plr = div_cartridges.find("span", class_="plr")
            if span_plr and "%" in span_plr.text:
                nivel = span_plr.text.strip()
            else:
                span_supply = div_cartridges.find("span", id="SupplyGauge0")
                if span_supply and "%" in span_supply.text:
                    nivel = span_supply.text.strip()

    if nivel is None:
        # span com style contendo width em %
        for span in soup.find_all("span"):
            style = span.get("style", "")
            match = re.search(r'width:\s*(\d+%)', style)
            if match:
                nivel = match.group(1)
                break

    if nivel is None:
        # procura em tabelas valores com %
        for table in soup.find_all("table"):
            for tr in table.find_all("tr"):
                cells = tr.find_all(["td", "th"])
                texts = [c.text.lower() for c in cells]
                if any(any(k in text for k in keywords) for text in texts):
                    for c in cells:
                        if "%" in c.text:
                            nivel = c.text.strip()
                            break
                    if nivel:
                        break
            if nivel:
                break

    # Método 3: procura valores base64 no HTML e decodifica
    if nivel is None:
        matches = re.findall(r'value\s*[:=]\s*["\']([A-Za-z0-9+/=]{4,})["\']', html)
        for val in matches:
            try:
                decoded = base64.b64decode(val).decode('utf-8')
                if "%" in decoded:
                    nivel = decoded.strip()
                    break
            except Exception:
                continue

    # Classifica e imprime resultado
    if nivel:
        classificacao = classificar_nivel(nivel)
        print(f"{ip} => {nivel} => {classificacao}")
        resultados.append([ip, classificacao])
    else:
        print(f"{ip} => Não encontrado")
        resultados.append([ip, "Não encontrado"])
