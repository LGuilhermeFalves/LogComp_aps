; ================================================
; TESTE ASSEMBLY 2 - Controle de Fluxo
; Testa condicionais e loops
; ================================================

SECTION .data

SECTION .text
    START:
        ; Teste de condicional (IF)
        LOAD REG_A, 10
        LOAD REG_B, 5
        CMP REG_A, REG_B        ; Compara REG_A e REG_B
        JG maior_label          ; Jump se REG_A > REG_B
        
        ; Caso falso
        LOAD REG_A, 0
        OUT REG_A
        JMP fim_if
        
    maior_label:
        ; Caso verdadeiro
        LOAD REG_A, 1
        OUT REG_A               ; OUTPUT: 1
        
    fim_if:
        ; Teste de loop (WHILE)
        LOAD REG_A, 0           ; contador = 0
        STORE contador, REG_A
        
    loop_inicio:
        LOAD REG_A, contador
        LOAD REG_B, 5
        CMP REG_A, REG_B
        JGE loop_fim            ; Jump se contador >= 5
        
        ; Corpo do loop
        LOAD REG_A, contador
        OUT REG_A               ; OUTPUT: 0, 1, 2, 3, 4
        
        ; Incrementa contador
        LOAD REG_A, contador
        INC REG_A
        STORE contador, REG_A
        
        JMP loop_inicio
        
    loop_fim:
        HALT

SECTION .bss
    contador: RESB 4
