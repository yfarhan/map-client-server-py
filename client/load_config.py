# load_config.py
import json

def read_json_config(file_path):
	"""
	Reads a JSON configuration file and returns the data as a dictionary.

	Args:
		file_path (str): The path to the JSON file.

	Returns:
		dict: A dictionary containing the data from the JSON file, or None if an error occurs.
	"""
	try:
		with open(file_path, 'r') as file:
			config_data = json.load(file)
			print('config_data', config_data)
			return config_data
	except FileNotFoundError:
		print(f"Error: File not found: {file_path}")
		return None
	except json.JSONDecodeError:
		print(f"Error: Invalid JSON format in: {file_path}")
		return None
	except Exception as e:
		print(f"An unexpected error occurred: {e}")
		return None
