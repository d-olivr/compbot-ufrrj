<div align="center">

# 🎓 CompBot UFRRJ — Academic Chatbot
### *Academic advisor chatbot for the Computer Science program at UFRRJ*

**Undergraduate Research Project · UFRRJ**

[![Python](https://img.shields.io/badge/Python-3.13.5-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![pyTelegramBotAPI](https://img.shields.io/badge/pyTelegramBotAPI-4.33-2CA5E0?style=flat-square&logo=telegram&logoColor=white)](https://github.com/eternnoir/pyTelegramBotAPI)
[![Status](https://img.shields.io/badge/Status-In_Development-brightgreen?style=flat-square)]()

<img width="250" alt="capybara" 
    src="https://github.com/user-attachments/assets/9f85f5a5-5bd1-4cce-9402-a787133cd2bb">
    

</div>

## 📌 About
<div align="center">
  <p>
    <b>CompBot UFRRJ</b> is a chatbot designed to support students of the Computer Science program at the Universidade Federal Rural do Rio de Janeiro (UFRRJ). It helps students make informed decisions about course enrollment, understand prerequisite chains, plan their     semester, and stay on track toward graduation.
  </p>
</div>

---

## 🌐 Features

- **Prerequisite Mapping** — explains prerequisite chains so students know exactly what unlocks what
- **Conversational Interface** — natural language interaction, no need to navigate complex academic portals
- **Portuguese Language Support** — fully optimized for Brazilian students :)

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python |
| Frontend | Telegram |
| Data | UFRRJ official curriculum & course catalogue |

---

## Navigation Flow

``` mermaid

---
config:
  layout: elk
  theme: redux-dark
---
flowchart TB
 subgraph LEGENDA["Legenda"]
        L_BTN["Botão"]
        L_TXT["Texto exibido na tela"]
        L_NEU["Elemento neutro"]
  end
    WELCOME["Bem-vindo ao CompBot!\nEscolha uma opção:"] --> BTN_AJUDA["Quero ajuda"] & BTN_GITHUB["Ver no Github"]
    BTN_GITHUB --> GITHUB_LINK["Abre repositório 🔗"]
    BTN_AJUDA --> EM_QUE["Em que posso te ajudar?"]
    EM_QUE --> BTN_REQ["Requisitos para\npuxar matéria"] & BTN_DISC["Entendendo melhor\numa disciplina"] & BTN_CAL["Calendário\nAcadêmico"] & BTN_ANA["Análise via histórico"]
    BTN_REQ --> INFO_REQ["Exibe informações\nsobre pré-requisitos"]
    BTN_DISC --> NAV_PER["Navegue pelos períodos para acessar as matérias:"]
    NAV_PER --> PER1["1º Período"] & PER2["2º Período"] & PER_N["... (nº)"] & n3["↩ Voltar"]
    PER1 --> SEL_MAT["Selecione a matéria\ndo 1º período:"]
    SEL_MAT --> MAT_PE["Programação Estruturada"] & MAT_OUT["Outra matéria"] & MAT_N["..."] & n4["↩ Voltar"]
    MAT_PE --> INFO_PE["Descrição da matéria exibida aqui"]
    INFO_PE --> BTN_PLAY["Playlist indicada"] & n5["↩ Voltar"]
    INFO_CAL["Exibe calendário\ndo semestre"] --> PDF_CAL["Envia .pdf do calendário"]
    BTN_CAL --> INFO_CAL
    BTN_ANA --> INFO_ANA["Por favor, envie o seu arquivo PDF do histórico acadêmico."]
    INFO_ANA --> RECEBIDO["O .pdf é recebido"]
    RECEBIDO --> ANALISE["Análise"]

     L_BTN:::botao
     L_TXT:::texto
     L_NEU:::neutro
     WELCOME:::texto
     BTN_AJUDA:::botao
     BTN_GITHUB:::botao
     GITHUB_LINK:::neutro
     EM_QUE:::texto
     BTN_REQ:::botao
     BTN_DISC:::botao
     BTN_CAL:::botao
     BTN_ANA:::botao
     INFO_REQ:::texto
     NAV_PER:::texto
     PER1:::botao
     PER2:::botao
     PER_N:::neutro
     n3:::neutro
     n3:::neutro
     SEL_MAT:::texto
     MAT_PE:::botao
     MAT_OUT:::botao
     MAT_N:::neutro
     n4:::neutro
     n4:::neutro
     INFO_PE:::texto
     BTN_PLAY:::botao
     n5:::neutro
     n5:::neutro
     INFO_CAL:::texto
     PDF_CAL:::neutro
     INFO_ANA:::texto
     RECEBIDO:::neutro
     ANALISE:::texto
    classDef botao fill:#FDFBF0,stroke:#C8C49A,color:#3D3A1E
    classDef texto fill:#0F6E56,stroke:#085041,color:#E1F5EE
    classDef neutro fill:#5F5E5A,stroke:#444441,color:#F1EFE8
    style LEGENDA fill:transparent

```

---

<!--- ## 🚀 Getting Started

### Prerequisites

> TBD

### Installation

```bash
# Clone the repository
git clone https://github.com/d-olivr/compbot-ufrrj.git
cd compbot-ufrrj

# Install dependencies
pip install -r requirements.txt
# or
npm install
```

### Configuration

```bash
# Copy the example environment file
cp .env.example .env

# Add your API key and settings
ANTHROPIC_API_KEY=your_key_here
```

### Running

```bash
python main.py
# or
npm start
```

--->

## 📂 Project Structure

```
compbot-ufrrj/
├── data/               # pdf files 
├── src/
│   ├── bot.py          # core bot logic    
│   ├── .env.example    # environment variable (API TOKEN)                 
│   └── .gitignore          
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! If you are a UFRRJ student or just want to help improve the chatbot, feel free to open an issue or submit a pull request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

## 👥 Collaborators

Built as part of an undergraduate research program (*Iniciação Científica*) at **UFRRJ - Universidade Federal Rural do Rio de Janeiro**.

<div align="center">
  <a href="https://github.com/d-olivr/compbot-ufrrj/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=d-olivr/compbot-ufrrj" />
  </a>
</div>


---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.


