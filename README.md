# ⚖️ Balança de Microempuxo  

Este projeto tem como objetivo construir melhorias para a **balança de microempuxo** da UnB para medições precisas de forças muito pequenas, utilizando eletrônica embarcada e processamento digital de sinais.  

---

## Objetivo  
- Melhorar a **precisão de medição** da balança.
- Validar o sistema com experimentos controlados.  

---

## Estrutura do Projeto  

| Seção | Descrição | Link |
|-------|-----------|------|
|  **Documentação** | Explicações teóricas, anotações e relatórios parciais | [docs/](./docs) |
|  **Documentação** | Estudos de códigos | [estudos/](./estudos_de_codigo/) |
|  **Código FPGA (VHDL/Verilog)** | Lógica de controle e processamento em hardware | [fpga/](./fpga) |
|  **Código Python** | Scripts para análise de dados e visualização de resultados | [python/](./python) |
|  **Firmware** | Código para microcontroladores / interface com sensores | [firmware/](./firmware) |
|  **Resultados** | Gráficos, simulações e comparações experimentais | [results/](./results) |

---

##  Tecnologias Utilizadas  
- **FPGA** (Xilinx/Intel) para aquisição de sinais em alta precisão  
- **Python** (NumPy, Matplotlib) para análise de dados  
- **Sensores de força** de alta sensibilidade  
 

---

## Demonstrações  
*(gifs, imagens ou diagramas do sistema em funcionamento)*  

---

## Como Executar  

1. Clone este repositório:  
   ```bash
   git clone https://github.com/luanaa2005/balanca-de-microempuxo.git
   cd balanca-de-microempuxo
