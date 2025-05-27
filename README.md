🖨️ Monitor de Nível de Toner
Sistema automático para rastrear suprimentos de toner/tinta em impressoras de rede

Um script em Python que varre impressoras em rede, verifica os níveis de toner/tinta através de suas interfaces web e classifica o status (Baixo/Bom/Alto) para evitar interrupções nas impressões.

✨ Principais Funcionalidades
Varredura de IPs - Verifica múltiplas impressoras em sequência

Suporte a HTTP/HTTPS - Funciona mesmo com certificados inválidos

Detecção inteligente - Encontra níveis usando:

Padrões com porcentagem (##%) + palavras-chave (toner, cartucho, nível)

Estruturas HTML específicas (compatível com HP e Pantum)

Valores codificados em Base64 nas páginas

Classificação automática - Categoriza os níveis como:

🔴 Baixo (≤20%) - Necessita substituição

🟡 Bom (21-50%) - Monitorar

🟢 Alto (>50%) - Sem ações necessárias

🛠️ Tecnologias Utilizadas
python
Python » requests, BeautifulSoup, re, base64, urllib3

🚀 Casos de Uso
Departamentos de TI gerenciando impressoras corporativas

Empresas de suporte técnico monitorando frotas de impressoras

Gráficas prevendo reposição de suprimentos

📌 Comece Rápido
Edite os IPs no script: ips = ["172.17.27.101...110"]

Execute:

bash
python status_impressoras.py
# ou via arquivo BAT:
start.bat
