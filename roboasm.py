#!/usr/bin/env python3
"""
RoboVM Assembly Interpreter
Interpreta e executa código assembly para a RoboVM
"""

import sys
import re

class RoboASM:
    def __init__(self):
        # Registradores
        self.registers = {
            'REG_A': 0,
            'REG_B': 0
        }
        
        # Memória (variáveis)
        self.memory = {}
        
        # Pilha
        self.stack = []
        
        # Sensores (read-only)
        self.sensors = {
            'bateria': 100,
            'sujeira': 5,
            'posX': 0,
            'posY': 0,
            'estaNoBase': 1,
            'obstaculo': 0
        }
        
        # Estado do robô
        self.robot = {
            'x': 0,
            'y': 0,
            'battery': 100,
            'at_base': True
        }
        
        # Controle de execução
        self.pc = 0  # Program counter
        self.labels = {}
        self.instructions = []
        self.output = []
        self.running = True
    
    def get_value(self, operand):
        """Obtém valor de operando (registrador, variável ou literal)"""
        operand = operand.strip()
        
        # Literal numérico
        try:
            return int(operand)
        except:
            pass
        
        # Registrador
        if operand in self.registers:
            return self.registers[operand]
        
        # Variável/constante na memória
        if operand in self.memory:
            return self.memory[operand]
        
        # Sensor
        if operand in self.sensors:
            self.update_sensors()
            return self.sensors[operand]
        
        return 0
    
    def set_register(self, reg, value):
        """Define valor de registrador"""
        if reg in self.registers:
            self.registers[reg] = value
    
    def update_sensors(self):
        """Atualiza valores dos sensores"""
        self.sensors['bateria'] = self.robot['battery']
        self.sensors['posX'] = self.robot['x']
        self.sensors['posY'] = self.robot['y']
        self.sensors['estaNoBase'] = 1 if self.robot['at_base'] else 0
        self.sensors['sujeira'] = max(0, 5 - len(self.output) // 5)
    
    def parse_file(self, filename):
        """Parseia arquivo assembly"""
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        current_section = None
        line_num = 0
        
        for line in lines:
            # Remove comentários
            if ';' in line:
                line = line[:line.index(';')]
            
            line = line.strip()
            if not line:
                continue
            
            # Seções
            if line.startswith('SECTION'):
                current_section = line.split()[1]
                continue
            
            # Labels
            if line.endswith(':'):
                label = line[:-1].strip()
                self.labels[label] = len(self.instructions)
                continue
            
            # Diretivas de dados
            if current_section == '.data':
                if ':' in line:
                    parts = line.split(':')
                    name = parts[0].strip()
                    value = parts[1].strip()
                    try:
                        self.memory[name] = int(value)
                    except:
                        pass
                continue
            
            # Instruções
            if current_section == '.text' or 'SECTION' not in line:
                self.instructions.append(line)
    
    def execute(self):
        """Executa programa assembly"""
        print("=" * 60)
        print("RoboVM Assembly - Executando programa")
        print("=" * 60)
        print(f"Estado inicial: posição=({self.robot['x']}, {self.robot['y']}), bateria={self.robot['battery']}%\n")
        
        self.pc = 0
        self.running = True
        
        while self.running and self.pc < len(self.instructions):
            instr = self.instructions[self.pc]
            self.execute_instruction(instr)
            self.pc += 1
        
        print(f"\n{'=' * 60}")
        print(f"Estado final: posição=({self.robot['x']}, {self.robot['y']}), bateria={self.robot['battery']}%")
        print(f"Outputs gerados: {len(self.output)}")
        print("=" * 60)
    
    def execute_instruction(self, instr):
        """Executa uma instrução"""
        parts = instr.split()
        if not parts:
            return
        
        opcode = parts[0].upper()
        
        # LOAD reg, value
        if opcode == 'LOAD':
            reg = parts[1].rstrip(',')
            value = self.get_value(parts[2])
            self.set_register(reg, value)
        
        # STORE var, reg
        elif opcode == 'STORE':
            var = parts[1].rstrip(',')
            reg = parts[2]
            self.memory[var] = self.get_value(reg)
        
        # ADD reg, value
        elif opcode == 'ADD':
            reg = parts[1].rstrip(',')
            value = self.get_value(parts[2])
            self.registers[reg] += value
        
        # SUB reg, value
        elif opcode == 'SUB':
            reg = parts[1].rstrip(',')
            value = self.get_value(parts[2])
            self.registers[reg] -= value
        
        # MUL reg, value
        elif opcode == 'MUL':
            reg = parts[1].rstrip(',')
            value = self.get_value(parts[2])
            self.registers[reg] *= value
        
        # DIV reg, value
        elif opcode == 'DIV':
            reg = parts[1].rstrip(',')
            value = self.get_value(parts[2])
            if value != 0:
                self.registers[reg] //= value
        
        # INC reg
        elif opcode == 'INC':
            reg = parts[1]
            self.registers[reg] += 1
        
        # DEC reg
        elif opcode == 'DEC':
            reg = parts[1]
            self.registers[reg] -= 1
        
        # CMP reg1, reg2
        elif opcode == 'CMP':
            reg1 = parts[1].rstrip(',')
            val1 = self.get_value(reg1)
            val2 = self.get_value(parts[2])
            self.cmp_result = val1 - val2
        
        # JMP label
        elif opcode == 'JMP':
            label = parts[1]
            if label in self.labels:
                self.pc = self.labels[label] - 1
        
        # JG label (Jump if Greater)
        elif opcode == 'JG':
            if hasattr(self, 'cmp_result') and self.cmp_result > 0:
                label = parts[1]
                if label in self.labels:
                    self.pc = self.labels[label] - 1
        
        # JL label (Jump if Less)
        elif opcode == 'JL':
            if hasattr(self, 'cmp_result') and self.cmp_result < 0:
                label = parts[1]
                if label in self.labels:
                    self.pc = self.labels[label] - 1
        
        # JGE label (Jump if Greater or Equal)
        elif opcode == 'JGE':
            if hasattr(self, 'cmp_result') and self.cmp_result >= 0:
                label = parts[1]
                if label in self.labels:
                    self.pc = self.labels[label] - 1
        
        # JLE label (Jump if Less or Equal)
        elif opcode == 'JLE':
            if hasattr(self, 'cmp_result') and self.cmp_result <= 0:
                label = parts[1]
                if label in self.labels:
                    self.pc = self.labels[label] - 1
        
        # JE label (Jump if Equal)
        elif opcode == 'JE':
            if hasattr(self, 'cmp_result') and self.cmp_result == 0:
                label = parts[1]
                if label in self.labels:
                    self.pc = self.labels[label] - 1
        
        # PUSH reg
        elif opcode == 'PUSH':
            value = self.get_value(parts[1])
            self.stack.append(value)
        
        # POP reg
        elif opcode == 'POP':
            if self.stack:
                reg = parts[1]
                self.set_register(reg, self.stack.pop())
        
        # OUT reg/value
        elif opcode == 'OUT':
            value = self.get_value(parts[1])
            print(f"  [OUTPUT] {value}")
            self.output.append(value)
        
        # SENSOR reg, sensor_name
        elif opcode == 'SENSOR':
            reg = parts[1].rstrip(',')
            sensor = parts[2]
            self.update_sensors()
            if sensor in self.sensors:
                self.set_register(reg, self.sensors[sensor])
        
        # ROBOT_MOVE x, y
        elif opcode == 'ROBOT_MOVE':
            x = self.get_value(parts[1].rstrip(','))
            y = self.get_value(parts[2])
            self.robot['x'] = x
            self.robot['y'] = y
            self.robot['at_base'] = (x == 0 and y == 0)
            self.robot['battery'] = max(0, self.robot['battery'] - 1)
            print(f"  [ROBOT] Moved to ({x}, {y}), battery: {self.robot['battery']}%")
        
        # ROBOT_CLEAN intensity
        elif opcode == 'ROBOT_CLEAN':
            intensity = self.get_value(parts[1])
            self.robot['battery'] = max(0, self.robot['battery'] - intensity)
            print(f"  [ROBOT] Cleaned with intensity {intensity}, battery: {self.robot['battery']}%")
        
        # ROBOT_HOME
        elif opcode == 'ROBOT_HOME':
            self.robot['x'] = 0
            self.robot['y'] = 0
            self.robot['at_base'] = True
            print(f"  [ROBOT] Returned to base (0, 0)")
        
        # ROBOT_CHARGE
        elif opcode == 'ROBOT_CHARGE':
            self.robot['battery'] = 100
            print(f"  [ROBOT] Battery charged to 100%")
        
        # HALT
        elif opcode == 'HALT':
            self.running = False

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 roboasm.py <arquivo.asm>")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    try:
        vm = RoboASM()
        vm.parse_file(filename)
        vm.execute()
    except FileNotFoundError:
        print(f"Erro: Arquivo '{filename}' não encontrado")
        sys.exit(1)
    except Exception as e:
        print(f"Erro durante execução: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
