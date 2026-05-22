# 📊 EmpreendeData

<div align="center">
  <h3>Dashboard Inteligente para Empreendedores Revendedores</h3>
  <p>Uma aplicação web desenvolvida como Atividade de Extensão Universitária para democratizar a análise de dados para pequenos comerciantes locais.</p>
</div>

---

## 🎯 Sobre o Projeto

O **EmpreendeData** é uma ferramenta simples, porém poderosa, construída para ajudar empreendedores que lidam com planilhas de vendas (como revendedores de cosméticos, perfumaria e chocolates) a entenderem seus dados financeiramente. A plataforma transforma dados brutos em *insights* visuais automaticamente.

### Informações Acadêmicas 🎓
- **Instituição:** Estácio (UNESA)
- **Curso:** Análise e Desenvolvimento de Sistemas (ADS)
- **Disciplina:** Sistemas de Informação e Sociedade
- **Atividade:** Extensão Universitária
- **Desenvolvedor:** James Soares Costa

## 💡 Funcionalidades

- **Upload Simplificado:** Suporte para arquivos `.csv` e `.xlsx`.
- **Análise Automática:** Detecção inteligente de colunas (numéricas, categóricas e temporais).
- **Dashboard Visual:**
  - Cards de KPIs interativos.
  - Gráfico de Barras com layout premium.
  - Gráfico de Distribuição (Rosca/Donut).
  - Mapa de Hierarquia (Treemap).
  - Gráficos extras: Dispersão, Histograma ou Temporal (dependendo dos dados inseridos).
- **Relatório PDF:** Geração automática e exportação de um relatório consolidado contendo os KPIs, imagens dos gráficos e amostra dos dados.
- **Tabela Interativa:** Visualize seus dados completos com filtros dinâmicos e opções de exportação.

## 🛠️ Tecnologias Utilizadas

Este projeto foi construído com Python e as seguintes bibliotecas:
- **[Streamlit](https://streamlit.io/):** Criação da interface web e estrutura do aplicativo.
- **[Pandas](https://pandas.pydata.org/):** Leitura, manipulação e cálculo de estatísticas dos dados.
- **[Plotly](https://plotly.com/python/):** Renderização de gráficos bonitos e interativos.
- **[FPDF2](https://pyfpdf.github.io/fpdf2/):** Geração dinâmica do relatório em PDF.
- **[Kaleido](https://pypi.org/project/kaleido/):** Exportação dos gráficos interativos como imagens para inclusão no PDF.

## 🚀 Como Executar Localmente

### Pré-requisitos
- Python 3.9 ou superior instalado em sua máquina.

### Passos para Instalação

1. **Clone este repositório:**
   ```bash
   git clone https://github.com/SEU_USUARIO/empreendedata.git
   cd empreendedata
   ```

2. **Crie um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   
   # No Windows:
   venv\Scripts\activate
   
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute a aplicação:**
   ```bash
   streamlit run app.py
   ```

5. O aplicativo será aberto automaticamente no seu navegador padrão no endereço `http://localhost:8501`.

## 📁 Estrutura do Projeto

```text
📦 EmpreendeData
 ┣ 📂 .streamlit
 ┃ ┗ 📜 config.toml                 # Configurações de tema visual (Dark Mode Premium)
 ┣ 📜 app.py                        # Arquivo principal contendo a lógica e UI do Streamlit
 ┣ 📜 dados_exemplo_revendedores.csv # Base de dados fictícia para demonstração
 ┣ 📜 requirements.txt              # Lista de dependências do Python
 ┗ 📜 README.md                     # Documentação do projeto
```

## 🤝 Contribuição

Sinta-se à vontade para realizar um *fork* deste projeto, abrir *issues* ou enviar *pull requests*. Toda contribuição para melhorar a acessibilidade da ferramenta para os empreendedores locais é bem-vinda!

---
<div align="center">
  Desenvolvido com ❤️ por James Soares Costa.
</div>
