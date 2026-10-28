# Visão Artificial — API Local de Processamento de IA

> Este repositório faz parte do ecossistema **Visão Artificial**. Ele atua como o **motor de inteligência artificial** localizado na borda (edge). Para ver as outras pontas, consulte os repositórios da [API Central (Nuvem)](https://github.com/Thurzinfs/vision-artificial-cloud) e do [Aplicativo Mobile (Flutter)](https://github.com/Thurzinfs/vision-artificial-mobile).

---

## Sobre, Motivo e Objetivo

### O Problema (O Desafio)
Sistemas de visão computacional em tempo real exigem alto poder de processamento gráfico e computacional para rodar modelos de inteligência artificial (como YOLO). Tentar processar fluxos pesados de imagens diretamente em nuvens genéricas de baixo custo ou em hardwares de captura limitados gera gargalos críticos de latência, inviabilizando uma resposta rápida para o usuário final.

### A Solução e o Objetivo da API Local
O objetivo desta **API Local** é descentralizar o esforço computacional. Rodando próxima ao ambiente de captura, ela consome os frames encaminhados pela API Central (Nuvem), executa a inferência de IA localmente com alta performance (utilizando YOLOv8n otimizado com OpenVINO), traduz e classifica os dados espaciais (posição e proporção), e devolve os resultados de forma ágil para a central redistribuir ao aplicativo mobile.

---

## Resumo do Ecossistema

| Componente | Papel Principal |
|---|---|
| **Hardware** | Captura e envia os frames brutos do ambiente. |
| **API Central (Nuvem)** | Gerencia rotas, conexões WebSocket/MQTT e o tráfego geral. |
| **API Local de IA** | *Este repositório* — Executa a inferência pesada de visão computacional. |
| **App Mobile** | Consome os dados processados e os converte em acessibilidade por voz (TTS). |

---

## Método

O fluxo de comunicação e processamento implementado é:

1. Ao iniciar a aplicação, um cliente WebSocket conecta-se ao endereço definido em `CLOUD_WS_URL` (fornecido pela API Central) e começa a escutar mensagens.
2. Cada mensagem deve conter os 16 bytes do UUID do dispositivo, seguidos pelos bytes de uma imagem que o OpenCV consiga decodificar.
3. O serviço executa a inferência localmente com YOLOv8n. Enquanto um quadro está sendo processado, novos quadros recebidos são ignorados para otimizar os recursos.
4. As detecções são traduzidas para português quando houver tradução disponível. A posição é classificada como `esquerda`, `centro` ou `direita` conforme o centro do objeto no eixo horizontal; `area_ratio` representa a fração do quadro ocupada pela caixa delimitadora.
5. Se houver detecções com confiança superior ao limiar configurado (padrão `0.4`), o serviço envia uma mensagem JSON estruturada de volta à conexão:

```json
{
  "device": "00000000-0000-0000-0000-000000000000",
  "detections": [
    {
      "label": "pessoa",
      "position": "centro",
      "confidence": 0.91,
      "area_ratio": 0.18
    }
  ]
}
```

---

## Tecnologias

- **Python 3.12 ou superior** — linguagem e versão mínima declarada.
- **FastAPI** — aplicação e gerenciamento do ciclo de vida.
- **WebSockets** — conexão assíncrona com o servidor remoto.
- **Ultralytics YOLOv8n** — detecção de objetos.
- **OpenVINO** — execução do modelo local incluído em
  `yolov8n_openvino_model/`.
- **OpenCV e NumPy** — decodificação e preparação das imagens.
- **uv** — gerenciamento de dependências e ambiente do projeto.

---

## Configuração e execução

Instale o [uv](https://docs.astral.sh/uv/) e as dependências do projeto:

```bash
uv sync
```

Defina o endereço do servidor WebSocket antes de iniciar a aplicação:

```bash
export CLOUD_WS_URL="wss://seu-servidor/exemplo"
uv run uvicorn main:app --reload
```

No Windows PowerShell, configure a variável com
`$env:CLOUD_WS_URL="wss://seu-servidor/exemplo"` antes do comando de execução.
Também é possível definir `CLOUD_WS_URL` em um arquivo `.env` local, que é
carregado pelo projeto e não deve conter valores compartilhados publicamente.

O cliente remoto deve enviar mensagens binárias no formato descrito em
[Método](#método). Não há endpoints HTTP de processamento de imagem definidos
no momento.

---

## Arquitetura

O código está organizado em camadas, com contratos no domínio e adaptadores na
infraestrutura:

```text
Servidor remoto
      │ WebSocket (UUID + imagem)
      ▼
WebSocketClientAdapter ──► ReceiveFrameUseCase
                                  │
                                  ▼
                      YoloTranslatorAdapter
                                  │
                                  ▼
                       YoloDetectorAdapter
                       YOLOv8n + OpenVINO
                                  │
                                  ▼
Servidor remoto ◄──── JSON com as detecções
```

- `app/domain/` contém a entidade de detecção e os contratos dos adaptadores.
- `app/application/` contém o caso de uso que coordena o recebimento,
  processamento e envio dos quadros.
- `app/infrastructure/` contém o cliente WebSocket e os adaptadores de
  inferência e tradução.
- `app/api/` fornece as dependências usadas para montar o caso de uso.
- `config/settings.py` carrega configurações do ambiente, incluindo o endereço
  WebSocket, o caminho do modelo e o limiar de confiança.
- `main.py` cria a aplicação FastAPI e inicia o cliente WebSocket no ciclo de
  vida da aplicação.

---

## Roadmap

### Concluído

- [x] Receber quadros de imagem por uma conexão WebSocket com reconexão automática.
- [x] Extrair o UUID do dispositivo e os bytes da imagem recebida.
- [x] Executar detecção local com YOLOv8n no formato OpenVINO.
- [x] Traduzir para português os rótulos COCO mapeados.
- [x] Calcular confiança, posição horizontal e proporção da área de cada detecção.
- [x] Enviar os resultados como JSON ao servidor conectado.

### Próximos passos

- [ ] Validar o formato das mensagens recebidas e documentar o protocolo com o serviço remoto.
- [ ] Adicionar testes para decodificação, detecção e serialização dos resultados.
- [ ] Tornar o limiar de confiança e o caminho do modelo configuráveis por ambiente.
- [ ] Melhorar logs e tratamento observável de falhas de conexão e inferência.
- [ ] Definir métricas de desempenho e limites para o processamento de quadros.

---

## Licença do modelo

Os metadados do modelo incluído indicam licença **AGPL-3.0**. Verifique os
termos aplicáveis ao distribuir ou utilizar o modelo; este aviso não substitui
uma licença para o código do projeto.

---

## Contato

- **Autor** — Arthur França Silva
- **E-mail** — arthurfranca.dev@gmail.com
- **GitHub** — [@Thurzinfs](https://github.com/Thurzinfs)

---

<div align="center">
  Desenvolvido com ❤️ por <a href="https://github.com/Thurzinfs">Arthur França Silva</a>
</div>