# Monitoramento de Preços de Alimentos Essenciais

## Acesso ao Histórico de Preços

Você pode visualizar o histórico de preços e as tendências de forma interativa acessando:
[Alimentos para Todos](https://alimentos-para-todos.onrender.com/)

---

## Objetivo Principal

Desenvolver um sistema que colete e analise preços de itens básicos (como arroz, feijão, leite, etc.) em supermercados locais, identificando variações e sugerindo os locais com os preços mais acessíveis. Essa iniciativa visa ajudar famílias a economizar e promover a transparência dos preços no mercado.

---

## Alinhamento com os ODS

- **ODS 2: Fome Zero e Agricultura Sustentável**
- **ODS 12: Consumo e Produção Responsáveis**

---

## Descrição do Projeto

Este projeto integra três componentes essenciais:

1. **Coleta de Dados (Web Scraping):**
   - **Ferramentas:** Python com BeautifulSoup/Scrapy e Selenium.
   - **Funcionalidade:** Acessa páginas de busca em supermercados (ex.: Carrefour) para extrair dados de produtos essenciais. São coletados o nome, o preço, a categoria e a fonte dos dados, os quais são registrados com a data de coleta.

2. **Armazenamento de Dados:**
   - **Tecnologia:** Utilização de arquivos CSV para armazenar o histórico dos dados coletados.
   - **Detalhes:** Os dados são gravados com os campos `date`, `category`, `name`, `price` e `source`, permitindo a criação de um histórico que pode ser analisado ao longo do tempo.

3. **Visualização e Análise:**
   - **Ferramentas:** Flask para backend e Chart.js para a criação de dashboards interativos.
   - **Funcionalidade:** A aplicação web processa o histórico de dados para calcular a média diária dos preços por categoria e apresenta essas informações em gráficos interativos, facilitando a compreensão das tendências de preços.

---

## Funcionalidades

- **Scraping Automatizado:** Extração periódica dos preços de produtos essenciais de supermercados locais.
- **Armazenamento Histórico:** Registro contínuo dos dados em um arquivo CSV para análise longitudinal.
- **Dashboards Interativos:** Visualização das tendências de preços ao longo do tempo, permitindo identificar variações e pontos de economia.
- **Transparência de Preços:** Fornece informações essenciais para que famílias possam tomar decisões mais informadas e economizar nas compras.

---

## Tecnologias Utilizadas

- **Python:** Linguagem principal para desenvolvimento do scraper e processamento dos dados.
- **Selenium & BeautifulSoup:** Para a extração dos dados a partir de páginas web.
- **CSV:** Para armazenamento do histórico dos dados.
- **Flask:** Framework web utilizado para criar a interface interativa.
- **Chart.js:** Biblioteca JavaScript para a criação dos gráficos interativos.

---

## Instruções de Uso

1. **Execução do Scraper:**
   - Configure e execute o script Python responsável pelo web scraping. Certifique-se de ter o Selenium e BeautifulSoup instalados.
   - Os dados coletados serão automaticamente adicionados ao arquivo `historical_food_products.csv`.

2. **Visualização dos Dados:**
   - Inicie a aplicação Flask para carregar e processar o histórico de preços.
   - Acesse a aplicação via navegador para visualizar os gráficos interativos com as tendências diárias dos preços.

3. **Análise dos Dados:**
   - Utilize os gráficos e dashboards para identificar variações de preços e descobrir quais supermercados oferecem os melhores preços para os itens essenciais.

---

## Impacto Esperado

Este sistema contribui para:
- **Economia Familiar:** Oferece informações para que as famílias possam economizar em suas compras diárias.
- **Transparência de Mercado:** Incentiva práticas de consumo e produção mais responsáveis, promovendo a justiça e a acessibilidade nos preços.
- **Sustentabilidade:** Alinha-se com os Objetivos de Desenvolvimento Sustentável (ODS), combatendo a fome e promovendo a sustentabilidade na produção e consumo.

---

## Considerações Finais

Este projeto é uma iniciativa inovadora para melhorar o acesso a informações essenciais, possibilitando decisões de compra mais informadas e contribuindo para a sustentabilidade econômica e social. As melhorias contínuas no tratamento dos dados e na interface de visualização permitirão uma experiência cada vez mais robusta e útil para os usuários.
