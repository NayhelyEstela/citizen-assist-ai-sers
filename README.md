# Citizen Assist AI — Módulo Energia e Sustentabilidade

> **Global Solution 2026 · Ciência da Computação (1CCPI) · Soluções em Energias Renováveis e Sustentáveis**
>
> Este repositório reúne a implementação integrada do projeto Citizen Assist AI. O sistema possui funcionalidades desenvolvidas no contexto de outra disciplina, que servem como estrutura principal do assistente, incluindo o menu, o histórico de atendimentos, a busca na base de conhecimento e as orientações gerais sobre trabalho e vagas.
>
> A contribuição específica da disciplina **Soluções em Energias Renováveis e Sustentáveis** é o desenvolvimento do módulo **"Transporte e energia" (opção 4 do menu)**, incluindo seus cálculos, dados energéticos, comparações, recomendações e dimensionamento solar, além das orientações 16, 17 e 18 da base de conhecimento.
>
> Portanto, as funcionalidades não foram todas desenvolvidas no âmbito desta disciplina. Este README destaca especialmente as contribuições relacionadas a energia e sustentabilidade.
---

## 1. Integrantes

| Nome                         | RM    |
|------------------------------|-------|
| Kauanne Paula de Oliveira    | 574191|
| Nayhely Estela Calle Castillo | 571416|

**Vídeo técnico (YouTube, não listado):** https://youtu.be/xndIVWnT3-k

---

## 2. Contexto: público, problema e contribuição

**Público.** Jovens (a partir de 15–16 anos) que estão entrando no mercado de trabalho: Jovem Aprendiz, primeiro emprego, primeiros meses de contrato. O Citizen Assist AI orienta esse público sobre documentos, FGTS, seguro-desemprego, conta-salário etc.

**Necessidade energética.** Ao começar a trabalhar, o jovem passa a fazer um deslocamento diário casa–trabalho, e esse deslocamento é o seu **maior consumo de energia cotidiano e uma despesa fixa relevante** do primeiro salário. Em geral ele ainda não sabe quanto vai gastar, nem como a escolha entre ônibus, metrô ou carro (a gasolina, elétrico ou elétrico carregado com energia solar) muda **energia consumida, custo mensal e emissões de CO₂**.

**Como as orientações contribuem.** O assistente deixa o jovem informar só a distância e os dias de trabalho (nunca o endereço) e devolve, para um mesmo trajeto e um mesmo mês, a comparação de alternativas em energia (kWh), custo (R$) e CO₂ (kg), com uma recomendação, as fontes dos dados e as limitações. Assim ele decide com números, e não por palpite.

**Por que transporte?** O enunciado cita consumo de equipamentos, eficiência energética e fontes renováveis como exemplos. Aqui aplicamos os mesmos conceitos (energia, potência, eficiência, fonte renovável, sustentabilidade) a uma necessidade real do nosso público: **energia por passageiro·km, eficiência do veículo, mistura de fontes da rede elétrica e geração solar**.

### 2.1 Relação do projeto com os impactos ambientais e a conscientização

O Citizen Assist AI — Módulo Energia e Sustentabilidade busca conscientizar jovens sobre os impactos ambientais das escolhas de transporte no deslocamento entre casa e trabalho.

Por meio da comparação entre ônibus a diesel, ônibus elétrico, metrô e carros a gasolina ou elétricos, o sistema demonstra as diferenças no consumo de energia, nos custos e nas emissões de CO₂. Também destaca a importância das fontes renováveis, como a matriz elétrica brasileira e a energia solar.

Além de apresentar resultados, o projeto incentiva a reflexão sobre hábitos de deslocamento, eficiência energética e uso responsável dos recursos naturais, contribuindo para a conscientização ambiental.

**Observação:** os cálculos consideram principalmente as emissões durante a operação dos transportes, não incluindo os impactos da fabricação de veículos, baterias e painéis solares.

---

## 3. Onde está a contribuição de Energia

O projeto utiliza uma estrutura de assistente desenvolvida no contexto de outra disciplina. Sobre essa estrutura, foi implementado o módulo de transporte e energia, que representa a contribuição desta disciplina.

| Arquivo | Papel |
|---|---|
| `modulo_energia.py` | Conversa com o usuário (opção 4): trajeto, tipo de transporte, validação de entradas, resultado, comparação, recomendação, fontes sob pedido e dimensionamento solar. |
| `calculos_energia.py` | **Todas as fórmulas**: viagens e km do mês, conversões de unidade, consumo real, custo e CO₂ por opção, custo dos painéis, dimensionamento e retorno solar, critério de recomendação. |
| `data/energia_dados.json` | **Todos os dados**, cada um com valor, unidade, tipo (real/derivado/estimado), fonte, link, data de consulta, período e premissas. |
| `data/base_conhecimento.json` (orientações **16, 17 e 18**, categoria "Transporte e energia") | Integração com a pergunta livre: quem pergunta "quanto gasto de ônibus?" ou "qual a forma mais sustentável?" recebe a orientação e é levado à opção 4. |
| `testes_usuarios.md` | Testes com usuários. Os atendimentos da opção 4 estão **em negrito**. |
| `main.py`, `assistente.py`, `base_conhecimento.py`, `orientacao.py` | Assistente geral (menu, busca, histórico, indicadores). A opção 4 do menu chama `modulo_energia.executar()`. Os demais atendimentos (documentos, FGTS etc.) são de outras disciplinas. |


---

## 4. Como executar

Requisitos: **Python 3.8 ou superior**. Não há dependências externas (só biblioteca padrão).

```bash
git clone <URL-DO-REPOSITORIO>
cd citizen-assist-ai-sers-main
python main.py          # em alguns sistemas: python3 main.py
```

### Como testar as funcionalidades de energia

1. No menu principal, digite **4** (*Transporte e energia*).
2. Escolha o trajeto: **1** (cenários estimados: curto 5 km, médio 12 km, longo 25 km, só ida) ou **2** (informar distância e dias por semana).
3. Escolha **transporte público** (ônibus a diesel, ônibus elétrico, metrô; tarifa comum ou estudantil) ou **transporte próprio** (gasolina, elétrico na rede, elétrico + painéis solares).
4. Leia o resultado, a comparação e a recomendação. Responda `s` para ver as fontes (2ª camada). Escolhendo *elétrico + solar*, é possível pedir o dimensionamento dos painéis.
5. Digite **0** em qualquer pergunta para voltar ao menu.

Casos sugeridos para conferir:

| Entrada | Resultado esperado (mês) |
|---|---|
| 2 → ida e volta → 30 km → 5 dias → próprio → gasolina | 472,2 kWh · R$ 362,66 · 86,2 kg CO₂ |
| 2 → ida e volta → 30 km → 5 dias → público → tarifa comum → ônibus diesel | 92,2 kWh · R$ 233,20 · 25,0 kg CO₂ |
| 1 → cenário médio → público → estudantil → metrô | 4,4 kWh · R$ 118,80 · 0,3 kg CO₂ |
| Digitar 200 km (só ida) ou "doze" | Recusado com mensagem; "12,5" é aceito |
| Pergunta livre: "quanto gasto indo de ônibus" (opção 1 do menu) | Orientação 17, confiança ALTA |

Os atendimentos ficam em `data/historico.json` e podem ser exportados para `data/atendimentos.csv` ao sair do programa. Esses arquivos são gerados na execução e **não** contêm dados pessoais.

---

## 5. Funcionalidades de energia

- Dois modos de trajeto: cenários estimados ou dados informados pelo usuário (com validação: texto, zero, negativos e valores absurdos são recusados; vírgula decimal é aceita).
- Seis alternativas para a mesma necessidade: **ônibus a diesel, ônibus elétrico, metrô, carro a gasolina, carro elétrico (rede) e carro elétrico + painéis solares**.
- Para cada uma: **energia (kWh), custo (R$) e CO₂ (kg) por mês**.
- **Comparação** entre as opções do mesmo tipo, em porcentagem ou "vezes", e **recomendação por critério** (menor custo, menor energia, menor CO₂). Diferenças menores que 5% são tratadas como "praticamente iguais".
- **Dimensionamento solar** (kWp necessário, investimento, geração, economia, retorno).
- **Resposta em duas camadas**: resultado e recomendação primeiro; fontes numeradas sob pedido (ajuste feito após os testes).
- Cada dado estimado aparece marcado como **ESTIMADO** e todo resultado traz aviso de que não é garantia.
- Não coleta dados pessoais: o assistente recusa e não registra mensagens que pareçam conter CPF, telefone, e-mail etc.

---

## 6. Análise de consumo: dados, unidades, período e premissas

**Período de referência comum: 1 mês** (22 dias úteis = 5 dias/semana × 4,4 semanas; 2 viagens por dia, ida e volta). **Local de referência:** São Paulo (capital). **Data de consulta dos dados:** 15 e 16/11/2026.

Cada valor está em `data/energia_dados.json` com seu tipo:

- **real**: encontrado em fonte pública (com origem e data);
- **derivado**: calculado por nós a partir de dados reais (a fórmula está no campo `formula`);
- **Estimado**: valor adotado como premissa para viabilizar os cálculos quando não há um dado único ou diretamente aplicável ao cenário analisado, identificada como ESTIMADA nas respostas.

**Como são fundamentadas as estimativas**:

As informações classificadas como estimadas não foram necessariamente escolhidas sem referência. Algumas são baseadas em estudos, artigos, páginas e sites de apoio que apresentam valores típicos, referências de mercado ou informações que ajudam a estabelecer premissas razoáveis.

Essas referências servem como apoio à escolha dos parâmetros, mas não significam que o valor estimado seja uma medição oficial ou que corresponda exatamente à realidade de todos os usuários.

### 6.1 Dados principais

| Dado | Valor | Tipo | Fonte |
|---|---|---|---|
| Preço da gasolina C (capital SP) | R$ 6,33/L | real | ANP, Síntese Semanal 43/2026 (semana 18–24/10/2026) |
| Densidade e PCI da gasolina C e do diesel | 0,754 kg/L · 9.400 kcal/kg; 0,84 kg/L · 10.100 kcal/kg | real | EPE/BEN via ANP, Fatores de conversão 2026 |
| Energia por litro | gasolina 8,24 kWh/L; diesel 9,87 kWh/L | derivado | densidade × PCI × 4,1868 ÷ 3600 |
| Consumo do carro a gasolina (Kwid, urbano) | 14,4 km/L | real | Inmetro, Tabela PBEV 2026 |
| Consumo do carro elétrico (E-Kwid) | 0,44 MJ/km = 0,1222 kWh/km | real / derivado | Inmetro, Tabela PBEV 2026 |
| **Fator de uso real** (laboratório → trânsito) | 0,8 | **estimado** | Testes e relatos de proprietários (fonte secundária) |
| Tarifa de energia residencial (com tributos) | R$ 1,012/kWh | derivado | Enel SP / ANEEL (REH 3.596/2026) × fator de tributos |
| Bandeira tarifária (nov/2026) | verde: R$ 0,00 adicional | real | ANEEL |
| Renováveis na eletricidade do Brasil | 86,8% (2025) | real | EPE, BEN 2026 |
| Fator de emissão da rede elétrica | 0,0674 kg CO₂/kWh | real | EPE, BEN 2026 |
| Emissão da gasolina C (fóssil) | 1,5042 kg CO₂/L | derivado | GHG Protocol Brasil × mistura ANP (68% gasolina A) |
| Consumo do ônibus a diesel | 0,5665 L/km | derivado | CDTI (ano-base 2023) |
| Consumo do ônibus elétrico | 4,75 MJ/km = 1,319 kWh/km | real / derivado | CDTI (ano-base 2023) |
| Energia do metrô | 0,03 MJ/passageiro·km = 0,00833 kWh/passageiro·km | real / derivado | CDTI (ano-base 2023) |
| **Lotação média do ônibus** | 40 passageiros | **estimado** | Premissa do grupo (passageiros sentados) |
| Tarifas de ônibus / metrô (comum) | R$ 5,30 / R$ 5,40 | real | SPTrans e Governo do Estado de SP (2026) |
| Tarifas estudantis | R$ 2,65 / R$ 2,70 | real | SPTrans (2026) |
| Horas de sol pleno em São Paulo | 4,3 kWh/m²·dia | real | Atlas Brasileiro de Energia Solar (2ª ed.) |
| Desempenho do sistema solar | 0,75 | **estimado** | Premissa (valor típico de projeto) |
| Custo do sistema solar | 2 kWp: R$ 3,62/Wp; 4 kWp: R$ 2,91/Wp | real | Greener, 1º sem. 2026 (via pv magazine) |
| Vida útil do sistema solar | 25 anos | **estimado** | Premissa (garantia típica dos módulos) |
| Fração da tarifa economizada (compensação) | 0,85 | **estimado** | Premissa, com base na Lei 14.300/2022 |
| Consumo médio residencial | 160 kWh/mês | **estimado** | Premissa do grupo (referência: EPE, PDE 2035) |

A lista completa, com link, data de consulta e observações de cada dado, está em `data/energia_dados.json`. O assistente mostra essas fontes na tela quando o usuário pede.

### 6.2 Cálculos (resumo das fórmulas em `calculos_energia.py`)

```
viagens/mês   = dias/semana × 4,4 semanas × 2 viagens
km/mês        = km por viagem (só ida) × viagens/mês

Gasolina:     litros   = km/mês × (1 ÷ 14,4) ÷ 0,8
              energia  = litros × 8,24 kWh/L
              custo    = litros × R$ 6,33
              CO₂      = litros × 1,5042 kg/L (parte fóssil)

Elétrico (rede):  energia = km/mês × (0,1222 ÷ 0,8) kWh/km
                  custo   = energia × R$ 1,012/kWh (+ bandeira)
                  CO₂     = energia × 0,0674 kg/kWh

Ônibus:       energia por passageiro = km/mês × consumo do ônibus ÷ lotação (40)
              custo = tarifa × viagens/mês
Metrô:        energia = km/mês × 0,00833 kWh/passageiro·km
              custo = tarifa × viagens/mês

Painéis:      geração por kWp = 4,3 h × 30 dias × 0,75 = 96,75 kWh/mês
              kWp necessário  = kWh do carro ÷ 96,75
              custo mensal atribuído ao carro = (kWp necessário × preço/Wp) ÷ 300 meses
```

---

## 7. Comparação das alternativas

### 7.1 Resultados por cenário (tarifa comum, 5 dias/semana, 44 viagens no mês)

Calculados pelo próprio código (`modulo_energia.calcular_opcao`).

**Trajeto curto, 5 km só de ida (220 km/mês)**

| Alternativa | Energia (kWh) | Custo (R$) | CO₂ (kg) |
|---|---:|---:|---:|
| Carro a gasolina | 157,4 | 120,89 | 28,7 |
| Carro elétrico (rede) | 33,6 | 34,01 | 2,3 |
| Carro elétrico + solar (*) | 33,6 | 4,19 | 0,0 |
| Ônibus a diesel | 30,7 | 233,20 | 8,3 |
| Ônibus elétrico | 7,3 | 233,20 | 0,5 |
| Metrô | 1,8 | 237,60 | 0,1 |

**Trajeto médio, 12 km só de ida (528 km/mês)**

| Alternativa | Energia (kWh) | Custo (R$) | CO₂ (kg) |
|---|---:|---:|---:|
| Carro a gasolina | 377,8 | 290,12 | 68,9 |
| Carro elétrico (rede) | 80,7 | 81,63 | 5,4 |
| Carro elétrico + solar (*) | 80,7 | 10,06 | 0,0 |
| Ônibus a diesel | 73,8 | 233,20 | 20,0 |
| Ônibus elétrico | 17,4 | 233,20 | 1,2 |
| Metrô | 4,4 | 237,60 | 0,3 |

**Trajeto longo, 25 km só de ida (1.100 km/mês)**

| Alternativa | Energia (kWh) | Custo (R$) | CO₂ (kg) |
|---|---:|---:|---:|
| Carro a gasolina | 787,1 | 604,43 | 143,6 |
| Carro elétrico (rede) | 168,1 | 170,07 | 11,3 |
| Carro elétrico + solar (*) | 168,1 | 20,96 | 0,0 |
| Ônibus a diesel | 153,7 | 233,20 | 41,6 |
| Ônibus elétrico | 36,3 | 233,20 | 2,4 |
| Metrô | 9,2 | 237,60 | 0,6 |

(*) **Leia com cuidado.** O custo do elétrico + solar é **apenas a parcela dos painéis que cabe ao carro, diluída em 25 anos**. Ele **não inclui a compra do veículo**, juros nem a troca do inversor. Por isso **não deve ser lido como "o carro custa R$ 10 por mês"**. Veja a análise de viabilidade abaixo.

### 7.2 Dimensionamento solar (exemplo: 15 km de ida, 5 dias/semana)

| Item | Valor |
|---|---|
| Energia do carro | 100,8 kWh/mês |
| Painéis necessários / considerados | 1,04 kWp / **2,00 kWp** (mínimo pesquisado) |
| Geração mensal | 193,5 kWh |
| Investimento estimado | R$ 7.240,00 (2 kWp × R$ 3,62/Wp) |
| Economia mensal estimada (carro + casa) | R$ 166,45 |
| Tempo de retorno | ≈ 3,6 anos |

A maior parte da economia vem do consumo **da casa** (160 kWh/mês supostos), não do carro. Só vale a quem tem telhado e conta de luz própria ou da família.

---

## 8. Justificativa das recomendações: custos, viabilidade e impactos ambientais

### 8.1 Leitura geral dos resultados

- **Impacto ambiental e energia:** o **metrô e o ônibus elétrico** são os que menos gastam energia e emitem CO₂ por passageiro (ordem de 1 a 10% da energia do carro a gasolina no mesmo trajeto), porque a energia é dividida entre muitos passageiros e a rede elétrica brasileira é 86,8% renovável.
- **Custo:** no transporte público o custo é a tarifa (R$ 233,20 a R$ 237,60 por mês com 44 viagens), **igual para qualquer distância**. Com tarifa estudantil cai para cerca de metade (R$ 118,80 no metrô). O carro a gasolina só fica mais barato que o transporte público em trajetos muito curtos (no cenário de 5 km, custa R$ 120,89). O carro elétrico carregado na rede tem custo de uso menor que a tarifa em todos os cenários, mas **sem contar a compra do veículo** (ver 8.2).
- **Carro a gasolina:** é o de maior custo, energia e CO₂ nos trajetos médios e longos. No trajeto de 30 km ida e volta custa cerca de 55% a mais que o ônibus, com cerca de 5 vezes mais energia e mais de 3 vezes mais CO₂.
- **Fonte renovável (solar):** zera o CO₂ de operação e o custo de eletricidade para carregar, **mas exige investimento inicial e condições próprias**.

### 8.2 Viabilidade de cada alternativa

| Alternativa | Custos considerados | Viabilidade para o jovem | Impacto ambiental (operação) |
|---|---|---|---|
| **Metrô / trem** | Tarifa × viagens | Alta onde há estação perto de casa e do trabalho; depende da cobertura da rede. Sem investimento inicial. | Muito baixo |
| **Ônibus elétrico** | Tarifa × viagens | Depende de a linha usada ter ônibus elétricos (frota ainda parcial). Sem investimento inicial. | Muito baixo |
| **Ônibus a diesel** | Tarifa × viagens | Alta: é a opção mais disponível. | Médio |
| **Carro a gasolina** | Combustível. **Não inclui** compra, seguro, IPVA, manutenção nem estacionamento | Exige ter ou comprar um veículo: custo alto para quem está no primeiro emprego. | Alto |
| **Carro elétrico (rede)** | Eletricidade residencial. **Não inclui** a compra do veículo | Exige ter o veículo e **onde carregar** (tomada em casa ou garagem). Emissão baixa, mas só é "renovável" na proporção da rede. | Baixo |
| **Carro elétrico + solar** | Parcela dos painéis atribuída ao carro. **Não inclui** o veículo, juros nem a troca do inversor | **A menos viável para o público**: exige veículo elétrico, imóvel com telhado adequado (próprio ou da família) e investimento mínimo estimado de R$ 7.240. | Muito baixo na operação (fabricação não entra) |

### 8.3 Recomendação final para o público

1. **Para o jovem que está começando a trabalhar, o transporte público é a recomendação mais coerente com a análise**: menor energia e CO₂ por pessoa, custo previsível, sem investimento inicial e com **meia-tarifa para estudantes**. Entre metrô e ônibus, o custo é praticamente o mesmo (diferença menor que 5%), então o critério de escolha deve ser energia/CO₂ e conveniência de trajeto.
2. **Se o jovem já tem ou precisa de carro**, o assistente mostra quanto o elétrico reduziria energia e CO₂ em relação à gasolina, **lembrando que o custo de compra do veículo não entrou**.
3. **A energia solar** é apresentada como alternativa renovável para **a casa da família ou para o futuro**, e não como solução imediata. O assistente avisa isso na tela.

---

## 9. Limitações e condições das estimativas

**Nada neste projeto é garantia de economia, geração ou custo.** São estimativas para orientação, e a ordem de grandeza é mais confiável que o valor exato.

- **Abrangência:** dados de **São Paulo (capital)**, tarifas de 2026, um modelo de carro de entrada (Renault Kwid / E-Kwid) e um ônibus padrão. Outras cidades e modelos terão resultados diferentes.
- **Premissas estimadas:** fator de uso real (0,8), lotação do ônibus (40), desempenho do sistema solar (0,75), vida útil (25 anos), fração compensada (0,85) e consumo residencial (160 kWh/mês). Mudar qualquer uma muda o resultado.
- **Lotação do ônibus:** a lotação real em horários de pico é maior que 40, o que reduziria a energia por passageiro do ônibus. Em horários vazios, aumentaria.
- **Compra do veículo e custos fixos** (seguro, IPVA, manutenção, estacionamento): **não entram** em nenhuma opção de carro.
- **Solar:** sem sombra, sem bateria, sistema ligado à rede, sem considerar a taxa mínima da distribuidora, sem juros, sem troca do inversor. Resultado válido só para quem tem telhado adequado. Pode estar subestimado acima de 4 kWp (sem preço pesquisado).
- **Emissões de fabricação** (painéis, veículos, baterias) e de produção e distribuição de combustíveis **não entram** (só a operação).
- **Base de energia diferente por opção:** para gasolina e diesel, "energia" é a **energia contida no combustível** (PCI); para elétrico e metrô, é a **eletricidade consumida**. A comparação mostra quanto cada opção consome, e não a energia primária de ponta a ponta.
- **Tratamento do CO₂ dos combustíveis:** na gasolina C contamos só a parte fóssil (o etanol da mistura é biogênico); no diesel todo o combustível é tratado como fóssil (valor conservador, pois o diesel atual tem 15% de biodiesel).
- **Rede elétrica:** a média nacional de 86,8% renovável não garante que a energia usada em cada hora seja renovável.
- **Tarifas e preços mudam** (combustível, tarifas de transporte, bandeira tarifária, custo de painéis). Os dados têm data de consulta e devem ser atualizados periodicamente.
- **Tarifa de ônibus e metrô:** o cálculo considera uma tarifa por viagem, sem integrações. A meia-tarifa depende de requisitos de elegibilidade.
- **Fontes secundárias:** alguns dados vêm de fontes secundárias (reportagens, estudo do CDTI divulgado pela imprensa, pv magazine), indicadas como tal no JSON (`fonte_nivel`). O fator de tributos da conta de luz foi derivado de faturas, sem link público. Eles devem ser substituídos por fontes primárias sempre que possível.
- **Premissas estimadas e referências de apoio:** alguns parâmetros, como fator de uso real dos veículos, lotação média dos ônibus, desempenho e vida útil do sistema solar e consumo residencial, foram definidos pelo grupo com apoio de referências externas, estudos e sites especializados. Essas fontes ajudam a fundamentar a escolha dos valores, mas não transformam as premissas em medições oficiais. Por isso, os parâmetros permanecem classificados como estimados e podem variar conforme as condições reais de utilização.
---

## 10. Referências

**Combustíveis e conversões**
- ANP. *Síntese Semanal de Preços dos Combustíveis*, edição 43/2026: https://www.gov.br/anp/pt-br/assuntos/precos-e-defesa-da-concorrencia/precos/arq-sintese-semanal/2026/sintese-precos-43.pdf
- ANP / EPE (BEN). *Fatores de conversão 2026*: https://www.gov.br/anp/pt-br/centrais-de-conteudo/publicacoes/anuario-estatistico/arquivos-anuario-estatistico-2026/outras-pecas-documentais/fatores-de-conversao-2026.pdf

**Veículos**
- Inmetro. *Tabela PBE Veicular 2026* (rev. 27/fev): https://static.ndmais.com.br/2026/03/Tabela-PBEV-2026_27_FEV-REV05-2-2.pdf
- Teste de consumo real (fator de uso real): https://portaldeprefeitura.com.br/automoveis/renault-kwid-enfrenta-o-transito-pesado-de-recife-e-mantem-lideranca/632545/

**Energia elétrica e meio ambiente**
- Enel SP / ANEEL. Tarifas residenciais (REH 3.596/2026): https://www.enel.com.br/pt-saopaulo/Para_Voce/tarifa-energia-eletrica.html
- ANEEL. Bandeira tarifária de novembro/2026: https://www.gov.br/aneel/pt-br/assuntos/noticias/2026/aneel-anuncia-bandeira-verde-para-vigorar-em-novembro
- EPE. *Balanço Energético Nacional 2026 — Síntese* (matriz elétrica e fator de emissão): https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-975/topico-847/BEN_Síntese_2026_PT.pdf
- EPE. *PDE 2035 — Caderno de Demanda de Eletricidade* (consumo residencial): https://www.epe.gov.br/sites-pt/publicacoes-dados-abertos/publicacoes/PublicacoesArquivos/publicacao-894/PDE%202035_Caderno_Demanda_Eletricidade_rev_mme_20250914.pdf
- Programa Brasileiro GHG Protocol (fatores de emissão), via inventário de emissões: https://procids.ufms.br/files/2024/04/Inventario_de_Emissao_de_Gases_2023.pdf

**Transporte público**
- SPTrans. Tarifas: https://www.sptrans.com.br/tarifas/
- Metrô/CPTM. Tarifas 2026: https://www.metrocptm.com.br/veja-os-valores-da-tarifa-de-trem-metro-e-integracoes-para-2026/
- CDTI, estudo de consumo energético do transporte de passageiros em SP (ano-base 2023), via Diário do Transporte: https://diariodotransporte.com.br/2025/07/12/estudo-revela-consumo-energetico-e-impacto-ambiental-do-transporte-de-passageiros-em-sao-paulo-eletricos-tem-ampla-vantagem/
- Lotação de ônibus: https://clubedoonibus.com.br/quantos-passageiros-cabem-em-um-onibus/

**Energia solar**
- INPE/LABREN. *Atlas Brasileiro de Energia Solar, 2ª ed.*: https://labren.ccst.inpe.br/atlas_2017.html
- pv magazine. Custos de sistemas fotovoltaicos no Brasil, 1º sem. 2026 (Greener): https://www.pv-magazine.com/2026/09/26/pv-system-costs-increase-7-percent-brazil-h1/
- Desempenho de sistemas solares (performance ratio): https://solarz.com.br/medicao-performance-usinas-solares/
- Vida útil de painéis solares: https://quantumengenharia.com.br/qual-a-vida-util-dos-paineis-solares/
- Lei 14.300/2022 (geração distribuída): https://www.planalto.gov.br/ccivil_03/_ato2019-2022/2022/lei/l14300.htm

**Contexto do público**
- Lei 7.418/1985 (vale-transporte): https://www.planalto.gov.br/ccivil_03/leis/l7418.htm

---

## 11. Testes com usuários

O registro completo está em [`testes_usuarios.md`](testes_usuarios.md). Resumo:

- **5 pessoas fora da equipe** (perfis A a E, com idades de 16 a 22 anos e situações diferentes: estudante, primeiro emprego, trabalhador com carro, jovem com trajeto longo e desempregado), **15 atendimentos** em 17/11/2026. **Nenhum dado pessoal** foi coletado: os perfis são anônimos, sem nome, escola, empresa ou endereço.
- **6 atendimentos usaram a opção 4**, e **todos foram considerados úteis**.
- Indicadores do próprio sistema: resposta encontrada em 86,7% dos atendimentos, "ajudou" em 73,3%, facilidade de uso 4,0 (de 1 a 5).

**Ajustes feitos a partir dos testes**

| # | Problema observado | Ajuste |
|---|---|---|
| A1 | "quanto gasto indo de ônibus" levava à orientação do carro | Novas palavras-chave na orientação 17 |
| A2 | "pra ser contratado" não era encontrado | Novas palavras-chave na orientação 14 |
| A3 | Resposta do FGTS não cobria pedido de demissão | Frase acrescentada na orientação 13, conferida na fonte oficial |
| A4 | Tela da opção 4 longa demais | Resultado em duas camadas: resposta e comparação primeiro, fontes sob pedido |

Os comentários dos usuários indicaram dois pontos que **já estão tratados na tela e neste README**: (1) o retorno solar de 3,6 anos não se aplica a quem mora de aluguel (por isso o assistente avisa que o solar vale para a casa da família ou para o futuro); (2) "CO₂: 0,0 kg" no elétrico + solar não significa "não polui" (a fabricação não entra, e a nota está na tela e na seção 9).

**Verificação dos ajustes:** as buscas dos atendimentos 3 ("pra ser contratado"), 6 ("quanto gasto indo de ônibus") e 12 (FGTS ao pedir demissão) passaram a retornar as orientações 14, 17 e 13, respectivamente, com confiança MÉDIA ou ALTA.

---

## 12. Evoluções futuras

- Ampliar a base de conhecimento com novas orientações e fontes oficiais (ex.: vale-transporte).
- Ampliar a opção 4 para outras cidades, tarifas, integrações e modelos de veículos.
- Incluir o custo de compra do veículo e um indicador de viabilidade na recomendação.
- Melhorar a interpretação de perguntas em linguagem natural com IA.

## 13. Aviso

Este assistente **não é um canal oficial**. As orientações são informativas, e os valores de energia são estimativas. Não digite dados pessoais (nome, CPF, telefone, e-mail, endereço).