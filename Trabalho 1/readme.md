O código é estruturado em torno da classe StateFarmer, que gerencia os estados do problema de travessia do rio. Esta classe inicializa o estado com as posições do fazendeiro, lobo, ovelha, repolho e cachorro, além de um indicador de ferimento.


![Cachorro brincando com repolho enquanto lobo descansa no fundo.](./assets/dogandcabbage.png)

A classe implementa métodos fundamentais:
- __eq__: Compara dois estados para verificar igualdade, evitando duplicação de estados na busca
- __hash__: Gera um valor hash único para cada estado, permitindo seu uso eficiente em coleções como sets e dicionários
- __str__: Formata o estado como string para facilitar a visualização do resultado
- is_valid(): Valida o estado atual considerando as restrições do problema:
  * A ovelha come o repolho quando estão sozinhos
  * O lobo come a ovelha quando estão sozinhos
  * O cachorro morde o lobo quando estão sozinhos, exceto se o repolho estiver presente (pois o cachorro brincará com ele)(única forma de ter uma solução para o problema)
- is_objective(): Verifica se todos os elementos chegaram ao destino

A função generate_successors mapeia transições válidas entre estados, incluindo o comportamento aleatório da ovelha que pode espontaneamente pular para o barco. Esta aleatoriedade é controlada por uma função randômica que simula a impaciência do animal.

Apesar da imprevisibilidade, o comportamento só ocorre quando gera estados válidos. Curiosamente, mesmo com esta aleatoriedade, a solução ideal mantém nove passos, pois os momentos em que a ovelha pode validamente pular coincidem com situações onde o fazendeiro já poderia transportá-la. A impaciência da ovelha apenas cria caminhos alternativos sem alterar o comprimento da solução, criando uma invariância estrutural.

O único impacto negativo é o aumento no número de sucessores gerados. Este comportamento aleatório pode ser ativado ou desativado pelo parâmetro allow_random na função breath_first_search, que implementa uma busca em largura.

Para rodar o programa:
```bash
python3 main.py
```
