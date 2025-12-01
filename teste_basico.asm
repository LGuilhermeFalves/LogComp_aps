; ================================================
; TESTE ASSEMBLY 1 - Operações Básicas
; Testa instruções básicas da RoboVM
; ================================================

; Seção de dados iniciais
SECTION .data

; Seção de código
SECTION .text
    START:
        ; Carregar valores nos registradores
        LOAD REG_A, 10          ; REG_A = 10
        LOAD REG_B, 5           ; REG_B = 5
        
        ; Operações aritméticas básicas
        ADD REG_A, REG_B        ; REG_A = 10 + 5 = 15
        STORE soma, REG_A       ; soma = 15
        
        LOAD REG_A, 10          ; REG_A = 10
        LOAD REG_B, 5           ; REG_B = 5
        SUB REG_A, REG_B        ; REG_A = 10 - 5 = 5
        STORE diferenca, REG_A  ; diferenca = 5
        
        LOAD REG_A, 10          ; REG_A = 10
        LOAD REG_B, 5           ; REG_B = 5
        MUL REG_A, REG_B        ; REG_A = 10 * 5 = 50
        STORE produto, REG_A    ; produto = 50
        
        LOAD REG_A, 10          ; REG_A = 10
        LOAD REG_B, 5           ; REG_B = 5
        DIV REG_A, REG_B        ; REG_A = 10 / 5 = 2
        STORE divisao, REG_A    ; divisao = 2
        
        ; Saída
        LOAD REG_A, soma
        OUT REG_A               ; OUTPUT: 15
        
        LOAD REG_A, diferenca
        OUT REG_A               ; OUTPUT: 5
        
        LOAD REG_A, produto
        OUT REG_A               ; OUTPUT: 50
        
        LOAD REG_A, divisao
        OUT REG_A               ; OUTPUT: 2
        
        HALT

; Seção de variáveis
SECTION .bss
    soma: RESB 4
    diferenca: RESB 4
    produto: RESB 4
    divisao: RESB 4
