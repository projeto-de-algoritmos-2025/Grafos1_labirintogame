# 🧩 Labirinto Misterioso — Grafos1_GradeUnB

*Projeto da disciplina de Grafos 1 — Aplicação prática com visualização interativa em Pygame*

## 👥 Alunos
| Matrícula | Nome |
|----------|------|
| 222006641 | Davi de Aguiar Vieira |
| 222006801 | Henrique Carvalho Neves |

## 📝 Entregas
| Grafos 1 |
|----------|
| [Apresentação](https://youtu.be/du0I2ZHD-vA) 
---

## 🎯 Sobre o Projeto

*Labirinto Misterioso* é um jogo de exploração e sobrevivência baseado em grafos, desenvolvido com a biblioteca Pygame.  
O jogador deve navegar por um labirinto representado por um *grafo não direcionado, no qual cada **nó é uma sala* e cada *aresta é um caminho possível entre salas*.

Você começa com uma quantidade limitada de energia e deve *descobrir a saída* antes que ela acabe. O labirinto possui *armadilhas, **benefícios escondidos* e *caminhos múltiplos*.

---

## 🧠 Como este projeto se relaciona com Grafos?

Este jogo é, essencialmente, uma *representação visual interativa de um grafo* com as seguintes características:

- Cada *nó* (ex: "N1", "N2"...) representa uma *sala* do labirinto.
- As *arestas* representam os *caminhos possíveis* entre salas.
- O grafo é *não direcionado*: é possível ir e voltar entre as salas.
- É possível aplicar os algoritmos clássicos de busca:
  - 🔶 *BFS (Busca em Largura)*: pressionando a tecla B, o jogo destaca o caminho encontrado da posição atual até a saída.
  - 🟣 *DFS (Busca em Profundidade)*: pressionando a tecla D, o jogo mostra um caminho alternativo baseado em profundidade.
- A estrutura de dados principal usada para representar o grafo é um *dicionário de listas de adjacência*:

  python
  self.grafo = {
      "N1": ["N2", "N3"],
      "N2": ["N1", "N4", "N5"],
      ...
  }
  

- A movimentação manual pelo grafo também permite experimentar *caminhos alternativos* e perceber, na prática, o custo de percorrê-los.

---

## 📸 Visualização

Durante a execução do jogo:

- 🟢 A sala atual é destacada em verde.
- 🔷 Salas visitadas manualmente ficam azuladas.
- 🔶 Caminho BFS: cor laranja.
- 🟣 Caminho DFS: cor roxa.
- 🟡 A saída é destacada com um contorno amarelo.

---

## ⚙️ Instalação

### ✅ Pré-requisitos

- Python 3.x
- Pygame

### 🔧 Instalação do Pygame

bash
pip install pygame


---

## ▶️ Como Jogar

1. Execute o jogo:

bash
python main.py


2. *Use o mouse* para clicar nos nós vizinhos e se mover pelo labirinto.
3. A cada movimento, sua *energia é reduzida em 1*.
4. Algumas salas podem *aumentar ou diminuir* sua energia.
5. Pressione:
   - B → Executar busca em largura (BFS)
   - D → Executar busca em profundidade (DFS)
   - R → Reiniciar o jogo (após perder ou vencer)

6. *Objetivo: Encontrar o nó de saída (N15) **antes que a energia acabe!*

---

## 💡 Conceitos de Grafos Aplicados

- ✅ Representação com lista de adjacência
- ✅ Exploração com BFS (Busca em Largura)
- ✅ Exploração com DFS (Busca em Profundidade)
- ✅ Custo de caminhos (energia como "peso" indireto)
- ✅ Componentes conectados (o grafo forma um labirinto conexo)
- ✅ Visualização de caminhos e nós visitados

---

## 🧪 Aprendizado com o Projeto

Este projeto é uma forma prática e divertida de aplicar os conhecimentos de grafos, tornando conceitos abstratos em elementos visuais e interativos.  
Além disso, incentiva a experimentação com algoritmos clássicos e sua comparação na prática.




