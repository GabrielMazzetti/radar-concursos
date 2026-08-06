# Concurso Radar 🎯

MVP de um sistema automatizado para monitorar concursos públicos brasileiros voltados para a área de **Estatística**.

## Estrutura do Projeto

- `main.py`: Script principal que orquestra a raspagem, filtragem e notificação.
- `config.py`: Configurações de palavras-chave, pontuações e credenciais.
- `database.py`: Gerenciamento do banco de dados SQLite.
- `scrapers/`: Módulos de raspagem para PCI Concursos, Folha Dirigida e DOU.
- `parser/`: Lógica de pontuação baseada em palavras-chave.
- `notifier/`: Sistema de notificações (E-mail e log).
- `keywords.json`: Lista customizável de termos e pesos.

## Como Usar

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure suas credenciais**:
   Edite o arquivo `config.py` ou defina as variáveis de ambiente:
   - `EMAIL_SENDER`
   - `EMAIL_PASSWORD`
   - `EMAIL_RECEIVER`

3. **Execute o script**:
   ```bash
   python main.py
   ```

## Lógica de Pontuação

O sistema utiliza um arquivo `keywords.json` para definir o que é relevante.
- **Estatística**: Termos obrigatórios para considerar o concurso.
- **Bônus**: Tecnologias como Python, R, SQL aumentam a pontuação.
- **Prioridades**: Órgãos (ex: IBGE) e cidades específicas ganham pontos extras.

## Próximos Passos (Fase 2)
- Implementar `pdf_parser.py` para ler editais completos.
- Adicionar integração com API do Telegram.
- Agendar execução diária via Cron ou GitHub Actions.
