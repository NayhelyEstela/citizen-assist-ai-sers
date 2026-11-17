# Testes com usuários simulados — Citizen Assist AI

Registro e análise de testes realizados com usuários para verificar se as orientações do assistente são **compreensíveis** e **úteis**, com foco especial na **opção 4 (Transporte e energia)**.

| Item | Valor                                                                                                                                        |
|---|----------------------------------------------------------------------------------------------------------------------------------------------|
| Data | 17/11/2026                                                                                                                                   |
| Participantes | 5 pessoas fora da equipe (A a E)                                                                                                           |
| Atendimentos | 15 ao total                                                                                                                                  |
| Dados pessoais | Nenhum dado real. Perfis anônimos, sem nome, escola, empresa ou endereço                                                                     |

---

## 1. Perfis

| Usuário | Situação |
|---------|---|
| A      | 16 anos, estudante, quer ser Jovem Aprendiz |
| B      | 19 anos, vai começar o primeiro emprego |
| C      | 22 anos, empregado, vai de carro e pensa em mudar |
| D      | 20 anos, mora longe do trabalho e se interessa por carro elétrico |
| E      | 21 anos, demitido e procurando vaga |

## 2. Os 15 atendimentos

**Legenda:** Confiança = nível mostrado pelo assistente. Ajudou = resposta do próprio perfil à pergunta "essa orientação respondeu sua dúvida?". Os atendimentos da opção 4 estão em **negrito**.

| # | Perfil | Funcionalidade | O que foi feito | Resultado no sistema                                                                                                                   | Ajudou |
|---|---|---|---|----------------------------------------------------------------------------------------------------------------------------------------|---|
| 1 | A | Pergunta livre | "posso ser jovem aprendiz com 15 anos" | Jovem Aprendiz, confiança ALTA                                                                                                         | Sim |
| **2** | A | **Opção 4: cenário estimado** | Não sabe o trajeto, escolhe cenário médio. Transporte público, tarifa estudantil, metrô | 12 km por viagem, 44 viagens: 4,4 kWh, R$ 118,80, 0,3 kg de CO2 por mês                                                                | Sim |
| 3 | B | Pergunta livre (não encontrou) | "o que preciso pra ser contratado" | Não encontrou orientação                                                                                                               | Não |
| 4 | B | Dado pessoal + reformulação | Digita um CPF e o assistente recusa e não registra. Depois escreve "quais documentos para o primeiro emprego" | Primeiro emprego, confiança ALTA, na 2ª tentativa                                                                                      | Sim |
| 5 | B | Navegação por categorias | Documentos e identidade, depois Carteira de Trabalho Digital | Orientação exibida com documentos, local e fonte                                                                                       | Sim |
| 6 | C | Pergunta livre (resposta errada) | "quanto gasto indo de ônibus" | Mostrou a orientação do **carro**, confiança MÉDIA                                                                                     | Não |
| **7** | C | **Opção 4: trajeto informado, transporte próprio** | Ida e volta de 30 km, 5 dias por semana, gasolina | 472,2 kWh, R$ 362,66, 86,2 kg de CO2 por mês. Mostrou a comparação com elétrico e solar                                                | Sim |
| **8** | C | **Opção 4: outro tipo de transporte** | Mesmo trajeto, transporte público, tarifa comum, ônibus a diesel | 92,2 kWh, R$ 233,20, 25,0 kg de CO2. Metrô ficou 2% mais caro e as opções foram classificadas como "praticamente iguais" em custo      | Sim |
| 9 | D | Pergunta livre | "qual a forma mais sustentável de ir trabalhar" | Forma mais sustentável, confiança ALTA. O texto indica a opção 4                                                                       | Sim |
| **10** | D | **Opção 4: elétrico + solar com dimensionamento** | Só ida de 25 km, 4 dias por semana, elétrico + painéis, aceita o dimensionamento | 134,4 kWh, R$$ 16,77, 0,0 kg de CO2. Dimensionamento: 1,39 kWp calculado, 2 kWp mínimo, investimento de R$ 7.240 e retorno em 3,6 anos | Sim |
| **11** | D | **Opção 4: comparação com transporte público** | Mesmo trajeto, tarifa comum, ônibus elétrico | 29,0 kWh, R$ 186,56, 2,0 kg de CO2                                                                                                     | Sim |
| 12 | E | Pergunta livre (resposta parcial) | "posso sacar o fgts se pedir demissão" | Saque do FGTS na demissão sem justa causa, confiança MÉDIA                                                                             | Não |
| 13 | E | Pergunta livre | "fui mandado embora e agora" | Seguro-desemprego, confiança MÉDIA                                                                                                     | Sim |
| 14 | E | Pergunta fora do escopo | "o que é vale transporte" | Não encontrou orientação e sugeriu outras palavras ou categorias                                                                       | Não |
| **15** | E | **Opção 4: validação de entradas** | Digita 200 km (recusado), "doze" (recusado), depois "12,5" (aceito). Público, tarifa comum, metrô | 12,5 km por viagem: 4,6 kWh, R$ 237,60, 0,3 kg de CO2                                                                                  | Sim |

**Funcionalidades ilustradas:** pergunta livre (confiança ALTA, MÉDIA e "não encontrei"), reformulação de pergunta, bloqueio de dado pessoal, navegação por categorias, opção 4 com cenário estimado e com trajeto informado, transporte público e próprio, tarifa comum e estudantil, comparação e recomendação, solar com dimensionamento, validação de entradas, nota de facilidade, indicadores e exportação do CSV.

### Indicadores calculados pelo sistema ao final

| Indicador | Resultado |
|---|---|
| Atendimentos registrados | 15 |
| Resposta encontrada | 86,7% (13 de 15) |
| Taxa de acerto ("ajudou") | 73,3% (11 de 15) |
| Tentativas por atendimento | 1,1 |
| Facilidade de uso (nota de 1 a 5, uma por pessoa) | 4,0 (notas 4, 3, 4, 5 e 4) |
| Dúvidas sem solução | 4 (atendimentos 3, 6, 12 e 14) |

## 3. Análise

### 3.1 Opção 4: Transporte e energia

Foi a parte com melhor desempenho: **6 atendimentos (40%), todos marcados como úteis**.

**O que funcionou**
- O fluxo é guiado por menus numerados, e o `0` volta ao menu principal em qualquer pergunta.
- O assistente pede só distância e dias, nunca endereço. Isso foi bem recebido (comentário de E).
- As validações funcionaram: 200 km foi recusado, texto foi recusado, vírgula decimal foi aceita.
- A comparação mostra diferenças em porcentagem e uma recomendação, o que ajudou C a ver que ônibus e metrô custam quase o mesmo, mas o metrô gasta muito menos energia.
- Os resultados parecem coerentes com a realidade: o carro a gasolina custou cerca de 55% a mais que o ônibus no trajeto de C, mas com 5 vezes mais energia e mais de 3 vezes mais CO2.

**O que dificultou**
- **Tela muito longa:** só o resultado do carro a gasolina de C ocupa cerca de 85 linhas, com lista de fontes e siglas como kWh e "[DERIVADO]". A informação principal (custo, energia, CO2) fica no começo e as fontes ocupam o resto.
- **"CO2: 0,0 kg" no elétrico com solar** pode ser lido como "não polui nada". A ressalva de que fabricação não entra aparece só mais abaixo.
- **O dimensionamento solar supõe casa com telhado.** O texto avisa que a economia vem sobretudo do consumo da casa, mas um jovem de 20 anos como D pode não ter casa própria. O "retorno em 3,6 anos" pode criar expectativa que não se aplica a ele, devido a dimensionamento simples.


### 3.2 Perguntas livres e navegação

- Dos 9 atendimentos de pergunta livre e navegação (1, 3, 4, 5, 6, 9, 12, 13 e 14), 5 foram atendidos, 2 falharam (3 e 6), 1 foi parcial (12) e 1 foi uma recusa correta (14).
- **Falha de vocabulário (3):** "pra ser contratado" não bate com as palavras-chave, que usam "para". B conseguiu na segunda tentativa, mas só depois de reescrever a pergunta.
- **Resposta errada (6):** a orientação do carro ganha 3 pontos só por "quanto", "gasto" e "indo" aparecerem no título. Com 3 pontos o assistente já mostra "confiança MÉDIA".
- **Resposta parcial (12):** a orientação 13 trata da demissão sem justa causa e não diz o que acontece quando a pessoa pede demissão.
- **Fora do escopo (14):** o assistente não inventou resposta, que era o comportamento correto.
- A navegação por categorias (5) funcionou sem problemas e é uma boa saída quando a pergunta livre falha.


## 4. Comentários dos usuários

- **A:** "Gostei de ver o valor do mês com a meia-tarifa. Entendi que o metrô gasta bem menos energia"
- **B:** "Quando não achou, pensei que o sistema não sabia a respeito. Só deu certo quando troquei 'pra' por 'para' sem saber." Nota 3: foi o único que sentiu dificuldade.
- **C:** "A comparação entre carro e ônibus foi o que eu queria. Mas a tela é enorme, tive que rolar bastante para achar o valor do mês."
- **D:** "Achei o painel solar interessante, mas moro de aluguel. O retorno de 3,6 anos não vale pra mim." Nota 5.
- **E:** "Perguntei do FGTS se eu pedisse demissão e veio a resposta de demissão sem justa causa. Fiquei sem saber. Do transporte gostei, muito interessante"

## 5. Ajustes aplicados

| #  | Problema (atendimento)                                                                              | Ajuste                                                                                                                     |
|----|-----------------------------------------------------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| A1 | Ônibus levava à orientação do carro (6)                                                             | Incluir em `palavras_chave` da orientação 17: `indo de onibus`, `de onibus`, `carro ou onibus`, `de metro`                 |
| A2 | "pra ser contratado" não encontrava (3)                                                             | Incluir em `palavras_chave` da orientação 14: `ser contratado`, `pra ser contratado`, `para ser contratado`                |
| A3 | Resposta do FGTS não cobre pedido de demissão (12)                                                  | Acrescentar uma frase na orientação 13 dizendo se o saque é permitido nesse caso. Conferir antes na fonte oficial e atualizar `verificado_em` |
| A4 | Resultado da opção 4 em duas camadas: resposta e comparação primeiro e detalhes e fontes sob pedido | Resolve a tela longa e deixa uma saída mais organizada.                                                                    |

## 6. Futuras evoluções

| # | Evolução | Por quê |
|---|---|---|
| E1 | **Ampliar a base de conhecimento com novas orientações e fontes oficiais** | Os testes e comentários identificaram dúvidas que a base atual ainda não consegue responder. A inclusão de novas orientações, acompanhadas de fontes confiáveis, permitirá fornecer respostas mais completas e precisas aos usuários. |
| E2 | **Ampliar a opção 4 para outras cidades, tarifas, integrações e modelos de veículos** | Atualmente, os cálculos utilizam dados de São Paulo capital e um conjunto limitado de veículos. A ampliação permitirá atender a diferentes realidades de transporte e tornar as comparações mais representativas para usuários de outras localidades. |
| E3 | **Aprimorar a integração com IA para interpretar dúvidas e oferecer orientações mais completas** | Melhorar a capacidade da IA de compreender perguntas em linguagem natural, identificar dúvidas relacionadas a energia e sustentabilidade e direcionar o usuário à funcionalidade ou orientação mais adequada. Isso permitirá lidar com perguntas variadas, inclusive aquelas que não correspondem exatamente às opções inicialmente previstas no sistema. |

## 7. Limitações e a complexidade de cobrir todas as dúvidas

**O assistente cobre hoje 18 orientações.** Cada uma foi escrita com resposta, documentos, local, fonte oficial e data de conferência. Isso garante qualidade, mas traz limites que crescem com o tamanho da base:

- **O público faz perguntas de formas imprevisíveis.** A busca depende de palavras-chave escritas. Cada jeito novo de perguntar ("pra", "de graça", "me mandaram embora") exige incluir uma variação. Nunca se chega ao fim da lista, e é isso que os atendimentos 3 e 6 mostraram.
- **Quanto maior a base, mais conflitos.** Com mais orientações, mais palavras se repetem entre elas, como "gasto" e "FGTS", e fica mais fácil a pergunta cair no tema errado. Cada adição exige testar de novo todas as perguntas anteriores.
- **O conteúdo envelhece.** Regras do FGTS, tarifas de ônibus e metrô, preço da gasolina e custo de painéis solares mudam. Cada orientação e cada número da opção 4 precisa ser conferido de tempos em tempos. Uma resposta desatualizada sobre trabalho ou dinheiro pode prejudicar quem confia nela.
- **Nem todo caso cabe numa resposta pronta.** Situações particulares (contrato irregular, empresa que não deposita FGTS) exigem atendimento humano ou canal oficial. O assistente deve continuar dizendo que não é um canal oficial.
- **A opção 4 é uma estimativa.** Usa dados de São Paulo capital, um modelo de carro de entrada e premissas do grupo. Serve para dar uma noção de ordem de grandeza, não para decidir uma compra.