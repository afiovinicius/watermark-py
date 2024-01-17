# Watermark PDF

Este é um projeto simples para adicionar marca d'água a arquivos PDF.

## Estrutura do Projeto

- `pdf/`: Coloque seus arquivos PDFs nesta pasta.
- `imgs/`: Adicione suas imagens de marca d'água (.png, .jpg, .jpeg) aqui.
- `novo-pdf/`: Os arquivos de saída com a marca d'água serão salvos aqui.
- `requirements.txt`: Lista de dependências do projeto.
- `main.py` : Script em python
- `.menv` : Máquina virtual

## Clonando o Projeto

Você pode clonar o projeto usando o seguinte comando no seu terminal:

```bash
git clone https://github.com/afiovinicius/watermark-py.git
```

## Configurando a Máquina Virtual com Virtualenv

Certifique-se de ter o Python 3 e o virtualenv instalados em sua máquina. Você pode criar uma máquina virtual com os seguintes comandos:


cd watermark-py
python3 -m venv venv

Ative a máquina virtual:

No Linux/Mac:

source venv/bin/activate

No Windows:

venv\Scripts\activate

## Instalando Dependências

Certifique-se de que a máquina virtual esteja ativada. Em seguida, instale as dependências do projeto com o seguinte comando:


pip install -r requirements.txt

## Rodando o Projeto

Após configurar a máquina virtual e instalar as dependências, você pode rodar o projeto usando:


python watermark.py

Os arquivos de saída serão gerados na pasta novo-pdf/.

