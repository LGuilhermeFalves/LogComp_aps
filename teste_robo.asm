; ================================================
; TESTE ASSEMBLY 3 - Robô e Sensores
; Testa instruções específicas do robô
; ================================================

SECTION .data

SECTION .text
    START:
        ; Verificar estado inicial
        SENSOR REG_A, bateria
        OUT REG_A               ; OUTPUT: bateria inicial
        
        SENSOR REG_A, posX
        OUT REG_A               ; OUTPUT: 0
        
        SENSOR REG_A, posY
        OUT REG_A               ; OUTPUT: 0
        
        ; Movimento do robô
        LOAD REG_A, 5
        LOAD REG_B, 3
        ROBOT_MOVE REG_A, REG_B ; Mover para (5, 3)
        
        SENSOR REG_A, posX
        OUT REG_A               ; OUTPUT: 5
        
        SENSOR REG_A, posY
        OUT REG_A               ; OUTPUT: 3
        
        ; Limpeza
        LOAD REG_A, 10
        ROBOT_CLEAN REG_A       ; Aspirar com intensidade 10
        
        SENSOR REG_A, bateria
        OUT REG_A               ; OUTPUT: bateria após limpeza
        
        ; Verificar sujeira
        SENSOR REG_A, sujeira
        OUT REG_A               ; OUTPUT: nível de sujeira
        
        ; Retornar à base
        ROBOT_HOME              ; Voltar para (0, 0)
        
        SENSOR REG_A, posX
        OUT REG_A               ; OUTPUT: 0
        
        SENSOR REG_A, posY
        OUT REG_A               ; OUTPUT: 0
        
        SENSOR REG_A, estaNoBase
        OUT REG_A               ; OUTPUT: 1
        
        ; Recarregar
        ROBOT_CHARGE
        
        SENSOR REG_A, bateria
        OUT REG_A               ; OUTPUT: 100
        
        HALT

SECTION .bss
