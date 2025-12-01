; ================================================
; TESTE ASSEMBLY 5 - Sistema Completo
; Programa completo de limpeza autônoma
; ================================================

SECTION .data
    BATTERY_MIN: 30
    DIRT_THRESHOLD: 3
    MAX_CYCLES: 3

SECTION .text
    START:
        ; Inicialização
        LOAD REG_A, 1000
        OUT REG_A               ; Marcador de início
        
        SENSOR REG_A, bateria
        OUT REG_A
        
        ; Loop principal de limpeza
        LOAD REG_A, 0
        STORE cycle_count, REG_A
        
    main_loop:
        ; Verificar se completou ciclos
        LOAD REG_A, cycle_count
        LOAD REG_B, MAX_CYCLES
        CMP REG_A, REG_B
        JGE end_program
        
        ; Verificar bateria
        SENSOR REG_A, bateria
        LOAD REG_B, BATTERY_MIN
        CMP REG_A, REG_B
        JL need_charge
        
        ; Bateria OK - continuar limpeza
        JMP do_cleaning
        
    need_charge:
        ; Bateria baixa - recarregar
        LOAD REG_A, 9000
        OUT REG_A               ; Marcador de recarga
        
        ROBOT_HOME
        ROBOT_CHARGE
        
        SENSOR REG_A, bateria
        OUT REG_A
        
    do_cleaning:
        ; Mover para próxima posição
        LOAD REG_A, cycle_count
        LOAD REG_B, cycle_count
        ROBOT_MOVE REG_A, REG_B
        
        ; Verificar sujeira
        SENSOR REG_A, sujeira
        LOAD REG_B, DIRT_THRESHOLD
        CMP REG_A, REG_B
        JL skip_cleaning
        
        ; Limpar área
        LOAD REG_A, 10
        ROBOT_CLEAN REG_A
        
        SENSOR REG_A, bateria
        OUT REG_A
        
    skip_cleaning:
        ; Incrementar contador de ciclos
        LOAD REG_A, cycle_count
        INC REG_A
        STORE cycle_count, REG_A
        
        JMP main_loop
        
    end_program:
        ; Finalização - retornar à base
        LOAD REG_A, 2000
        OUT REG_A               ; Marcador de fim
        
        ROBOT_HOME
        ROBOT_CHARGE
        
        ; Status final
        SENSOR REG_A, posX
        OUT REG_A
        
        SENSOR REG_A, posY
        OUT REG_A
        
        SENSOR REG_A, bateria
        OUT REG_A
        
        SENSOR REG_A, estaNoBase
        OUT REG_A
        
        LOAD REG_A, 0
        OUT REG_A               ; Marcador de término
        
        HALT

SECTION .bss
    cycle_count: RESB 4
