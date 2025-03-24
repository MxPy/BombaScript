import argparse
import sys
import os
from src.frontend.myParser import Parser
from src.runtime.myInterpreter import evaluate
from src.runtime.myEnvironment import Environment

# Definiujemy wersję w jednym miejscu dla łatwej aktualizacji
VERSION = "0.0.2"


def run_file(file_path, verbose=False):
    try:
        with open(file_path, 'r') as file:
            data = file.read()
            # Utwórz instancję parsera
            parser = Parser
            # Wywołaj metodę produceAST na instancji (bez przekazywania samej instancji jako argumentu)
            program = parser.produceAST(parser, data)
            
            if verbose:
                print(f"Program AST: {program}")
            
            env = Environment()
            result = evaluate(program, env)
            
            if verbose:
                print(f"Result: {result}")
            
        return True
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return False
    except Exception as e:
        print(f"Error executing file: {e}")
        return False

def run_repl():
    # Utwórz instancję parsera
    parser = Parser()
    env = Environment()
    
    print(f"BombaScript REPL v{VERSION}")
    print("Type 'wóda' or 'kurwix' to exit the REPL")
    
    while True:
        try:
            code = input(">> ")
            
            if code.lower() in ["wóda", "kurwix"]:
                break
            
            # Wywołaj metodę na instancji
            program = parser.produceAST(code)
            result = evaluate(program, env)
            
            if result is not None:
                print(result)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Error: {e}")

def display_version():
    print(f"BombaScript v{VERSION}")

def main():
    parser = argparse.ArgumentParser(description="BombaScript Interpreter")
    parser.add_argument(
        "file", 
        nargs="?", 
        help="Script file to execute"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Enable verbose output (show AST and results)"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Display BombaScript version"
    )
    
    args = parser.parse_args()
    
    # Jeśli podano flagę --version, wyświetl wersję i zakończ program
    if args.version:
        display_version()
        return
  
    
    if args.file:
        run_file(args.file, args.verbose)
    else:
        run_repl()

if __name__ == "__main__":
    main()