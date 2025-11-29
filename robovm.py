#!/usr/bin/env python3
"""
RoboVM - Máquina Virtual para RoboLang
Interpreta e executa programas RoboLang
"""

import sys
import re

class RoboVM:
    def __init__(self):
        # Registradores
        self.registers = {
            'REG_A': 0,
            'REG_B': 0
        }
        
        # Memória (variáveis)
        self.variables = {}
        
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
        self.running = True
        self.output = []
    
    def get_value(self, name):
        """Obtém valor de variável, sensor ou literal"""
        if isinstance(name, int):
            return name
        
        name = str(name).strip()
        
        # Tenta converter para número
        try:
            return int(name)
        except:
            pass
        
        # Verifica sensores
        if name in self.sensors:
            self.update_sensors()
            return self.sensors[name]
        
        # Verifica variáveis
        if name in self.variables:
            return self.variables[name]
        
        # Verifica registradores
        if name in self.registers:
            return self.registers[name]
        
        return 0
    
    def set_value(self, name, value):
        """Define valor de variável ou registrador"""
        if name in self.registers:
            self.registers[name] = value
        else:
            self.variables[name] = value
    
    def update_sensors(self):
        """Atualiza valores dos sensores baseado no estado do robô"""
        self.sensors['bateria'] = self.robot['battery']
        self.sensors['posX'] = self.robot['x']
        self.sensors['posY'] = self.robot['y']
        self.sensors['estaNoBase'] = 1 if self.robot['at_base'] else 0
        
        # Simula obstáculo se muito longe
        if abs(self.robot['x']) > 10 or abs(self.robot['y']) > 10:
            self.sensors['obstaculo'] = 1
        else:
            self.sensors['obstaculo'] = 0
    
    def execute_binary_op(self, op, left, right):
        """Executa operação binária"""
        if op == '+':
            return left + right
        elif op == '-':
            return left - right
        elif op == '*':
            return left * right
        elif op == '/':
            return left // right if right != 0 else 0
        elif op == '==':
            return 1 if left == right else 0
        elif op == '!=':
            return 1 if left != right else 0
        elif op == '<':
            return 1 if left < right else 0
        elif op == '<=':
            return 1 if left <= right else 0
        elif op == '>':
            return 1 if left > right else 0
        elif op == '>=':
            return 1 if left >= right else 0
        return 0
    
    def evaluate_expression(self, expr):
        """Avalia uma expressão"""
        expr = str(expr).strip()
        
        # Número literal
        if expr.isdigit() or (expr.startswith('-') and expr[1:].isdigit()):
            return int(expr)
        
        # Sensor ou variável
        if expr in self.sensors or expr in self.variables:
            return self.get_value(expr)
        
        # Operações binárias simples
        for op in ['==', '!=', '<=', '>=', '<', '>', '+', '-', '*', '/']:
            if op in expr:
                parts = expr.split(op, 1)
                if len(parts) == 2:
                    left = self.evaluate_expression(parts[0].strip())
                    right = self.evaluate_expression(parts[1].strip())
                    return self.execute_binary_op(op, left, right)
        
        return self.get_value(expr)
    
    def execute_assignment(self, var, expr):
        """Executa atribuição"""
        value = self.evaluate_expression(expr)
        self.set_value(var, value)
        print(f"  {var} = {value}")
    
    def execute_print(self, expr):
        """Executa print"""
        value = self.evaluate_expression(expr)
        print(f"  [OUTPUT] {value}")
        self.output.append(value)
    
    def execute_if(self, condition, then_code, else_code=None):
        """Executa if-else"""
        cond_value = self.evaluate_expression(condition)
        print(f"  [IF] condition = {cond_value}")
        
        if cond_value:
            self.execute_block(then_code)
        elif else_code:
            self.execute_block(else_code)
    
    def execute_while(self, condition, body):
        """Executa while loop"""
        iterations = 0
        max_iterations = 1000  # Previne loops infinitos
        
        while iterations < max_iterations:
            cond_value = self.evaluate_expression(condition)
            if not cond_value:
                break
            
            print(f"  [WHILE] iteration {iterations}, condition = {cond_value}")
            self.execute_block(body)
            iterations += 1
        
        if iterations >= max_iterations:
            print(f"  [WARNING] Loop stopped after {max_iterations} iterations")
    
    def execute_robot_action(self, action, args):
        """Executa ação do robô"""
        if action == 'andar':
            dx = self.evaluate_expression(args[0]) if len(args) > 0 else 0
            dy = self.evaluate_expression(args[1]) if len(args) > 1 else 0
            
            self.robot['x'] += dx
            self.robot['y'] += dy
            self.robot['battery'] = max(0, self.robot['battery'] - 1)
            self.robot['at_base'] = (self.robot['x'] == 0 and self.robot['y'] == 0)
            
            print(f"  [ROBOT] Moved to ({self.robot['x']}, {self.robot['y']}), battery: {self.robot['battery']}%")
        
        elif action == 'aspirar':
            intensity = self.evaluate_expression(args[0]) if args else 5
            
            self.robot['battery'] = max(0, self.robot['battery'] - intensity)
            self.sensors['sujeira'] = max(0, self.sensors['sujeira'] - intensity)
            
            print(f"  [ROBOT] Cleaned with intensity {intensity}, battery: {self.robot['battery']}%, dirt: {self.sensors['sujeira']}")
        
        elif action == 'voltarBase':
            self.robot['x'] = 0
            self.robot['y'] = 0
            self.robot['at_base'] = True
            
            print(f"  [ROBOT] Returned to base (0, 0)")
        
        elif action == 'carregar':
            if self.robot['at_base']:
                self.robot['battery'] = 100
                print(f"  [ROBOT] Battery charged to 100%")
            else:
                print(f"  [ROBOT] Cannot charge - not at base!")
        
        elif action == 'esperar':
            delay = self.evaluate_expression(args[0]) if args else 0
            print(f"  [ROBOT] Waiting {delay}ms")
    
    def execute_block(self, code):
        """Executa bloco de código"""
        # Implementação simplificada - processa linha por linha
        lines = code.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or line.startswith('//'):
                continue
            
            self.execute_statement(line)
    
    def execute_statement(self, statement):
        """Executa um statement"""
        statement = statement.strip().rstrip(';')
        
        if not statement:
            return
        
        # Assignment
        if '=' in statement and not any(op in statement for op in ['==', '!=', '<=', '>=']):
            parts = statement.split('=', 1)
            var = parts[0].strip()
            expr = parts[1].strip()
            self.execute_assignment(var, expr)
        
        # Print
        elif statement.startswith('mostrar('):
            expr = statement[8:-1]  # Remove 'mostrar(' e ')'
            self.execute_print(expr)
        
        # Robot actions
        elif statement.startswith('andar('):
            args_str = statement[6:-1]  # Remove 'andar(' e ')'
            args = [a.strip() for a in args_str.split(',') if a.strip()]
            self.execute_robot_action('andar', args)
        
        elif statement.startswith('aspirar('):
            args_str = statement[8:-1]
            args = [args_str] if args_str else []
            self.execute_robot_action('aspirar', args)
        
        elif statement.startswith('voltarBase('):
            self.execute_robot_action('voltarBase', [])
        
        elif statement.startswith('carregar('):
            self.execute_robot_action('carregar', [])
        
        elif statement.startswith('esperar('):
            args_str = statement[8:-1]
            self.execute_robot_action('esperar', [args_str])
    
    def run_program(self, code):
        """Executa programa completo"""
        print("=" * 60)
        print("RoboVM - Executando programa")
        print("=" * 60)
        print(f"Estado inicial: posição=({self.robot['x']}, {self.robot['y']}), bateria={self.robot['battery']}%")
        print()
        
        # Remove comentários
        code = re.sub(r'//.*', '', code)
        
        # Processa linha por linha
        lines = code.split(';')
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detecta estruturas de controle
            if line.startswith('se(') or line.startswith('se ('):
                # Simplificado - não processa blocos aninhados corretamente
                print(f"  [INFO] Condicional detectado (processamento simplificado)")
                continue
            
            elif line.startswith('enquanto(') or line.startswith('enquanto ('):
                print(f"  [INFO] Loop detectado (processamento simplificado)")
                continue
            
            else:
                try:
                    self.execute_statement(line)
                except Exception as e:
                    print(f"  [ERROR] {e}")
        
        print()
        print("=" * 60)
        print(f"Estado final: posição=({self.robot['x']}, {self.robot['y']}), bateria={self.robot['battery']}%")
        print(f"Outputs gerados: {len(self.output)}")
        print("=" * 60)

def main():
    if len(sys.argv) < 2:
        print("Uso: python3 robovm.py <arquivo.robo>")
        return
    
    input_file = sys.argv[1]
    
    try:
        with open(input_file, 'r') as f:
            code = f.read()
        
        vm = RoboVM()
        vm.run_program(code)
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{input_file}' não encontrado")
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    main()
