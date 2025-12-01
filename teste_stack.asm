; ================================================
; TESTE ASSEMBLY 4 - Stack e Pilha
; Testa operações com pilha
; ================================================

SECTION .data

SECTION .text
    START:
        ; Empilhar valores
        LOAD REG_A, 10
        PUSH REG_A              ; Stack: [10]
        
        LOAD REG_A, 20
        PUSH REG_A              ; Stack: [10, 20]
        
        LOAD REG_A, 30
        PUSH REG_A              ; Stack: [10, 20, 30]
        
        ; Desempilhar e mostrar
        POP REG_A
        OUT REG_A               ; OUTPUT: 30
        
        POP REG_A
        OUT REG_A               ; OUTPUT: 20
        
        POP REG_A
        OUT REG_A               ; OUTPUT: 10
        
        ; Expressão usando pilha: (5 + 3) * 2
        LOAD REG_A, 5
        PUSH REG_A
        
        LOAD REG_A, 3
        PUSH REG_A
        
        POP REG_B               ; REG_B = 3
        POP REG_A               ; REG_A = 5
        ADD REG_A, REG_B        ; REG_A = 8
        
        PUSH REG_A              ; Stack: [8]
        
        LOAD REG_B, 2
        POP REG_A               ; REG_A = 8
        MUL REG_A, REG_B        ; REG_A = 16
        
        OUT REG_A               ; OUTPUT: 16
        
        HALT

SECTION .bss
