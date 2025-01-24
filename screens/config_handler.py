import os
import sys

def load_print_coordinates():
    try:
        if getattr(sys, 'frozen', False):
            application_path = os.path.dirname(sys.executable)
        else:
            application_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            
        config_path = os.path.join(application_path, 'config.txt')
        
        with open(config_path, 'r') as f:
            coordinates = {}
            for line in f:
                key, value = line.strip().split('=')
                coordinates[key.strip()] = int(value.strip())
                
        return coordinates.get('x', 108), coordinates.get('y', 152)  # Default values if not found
        
    except Exception as e:
        print(f"Config file error: {str(e)}")
        return 108, 152  # Default values on error