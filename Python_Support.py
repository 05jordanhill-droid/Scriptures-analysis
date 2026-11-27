
import os
import json
import sys
from prompt_toolkit import prompt
import math
import string

"""
CAPITALIZED text in examples are not literal string, 
but rather "fill-in-here" text
"""

class Python_Support:
    def __init__(self):
        """
        {
          "CLASS_TYPE" : {
            "class_name": CLASS_TYPE,
            "constructors": [
                "VARIABLE_NAME",
                "VARIABLE_NAME1",
            ],
            "attributes": [
                "VARIABLE_NAME2",
                "VARIABLE_NAME3",
            ]
          }
        }
        """
        # Having a map of class registries allows for a class map to be easily 
        # accessible for deserializing any given custom class that provides one
        self.class_registry = {}

    def input(input_message="", viable_inputs:list=None, default_input=None, error_message="Invalid. Try Again.", clear:bool=True, num_of_inputs=None, preset_input=""):
        user_input = None

        if viable_inputs is not None:
            # viable inputs are often made up of 2 viable inputs per option
            # For Example: "1" and "name of choice" would both be viable inputs 
            # that would likely be paired
            if num_of_inputs is None:
                num_of_inputs = len(viable_inputs) // 2

            while user_input not in viable_inputs:
                user_input = prompt(input_message, default=preset_input)

                if user_input.lower() not in viable_inputs:
                    if default_input is not None:
                        return default_input

                    if clear:
                        Python_Support.clear_terminal()

                    print(error_message)

        else:
            return prompt(input_message, default=preset_input)

        return user_input


    def clear_terminal(cursor_elevation:int=None):
        if cursor_elevation is not None:
            sys.stdout.write(f"\033[{cursor_elevation}A")
            sys.stdout.write("\033[J")
            sys.stdout.flush()

        else:
            os.system('cls' if os.name == 'nt' else 'clear')
            pass


    def serialize(data):
        if isinstance(data, list):
            return [Python_Support.serialize(x) for x in data]

        elif isinstance(data, dict):
            """
            {
                "key" : value,   
                "key1" : value1,   
                "key2" : value2  
            }
            """
            # data.items() allows for iteration through dict
            return {
                key: Python_Support.serialize(value) for key, value in data.items()
            }

        # If a value has the attributes of a dict yet 
        # isn't an instance of a dict, then it's a class
        elif hasattr(data, "__dict__"):
            return {
                # sets up deserialize later 
                # to be able to know which class it is
                "_python_class": data.__class__.__name__,
                **Python_Support.serialize(data.__dict__)
            }

        # If a value is none of the previous cases, 
        # it is a base value such as str, int, bool, etc...
        return data

    def deserialize(data, class_registry):
        if isinstance(data, list):
            return [
                Python_Support.deserialize(x, class_registry) for x in data
            ]

        elif isinstance(data, dict):
            if "_python_class" in data:
                schema = class_registry[data["_python_class"]]

                constructor_data = {
                    key: data[key] for key in schema["constructors"]
                }

                obj = schema["class_name"](**constructor_data)

                for attribute in schema["attributes"]:
                    setattr(obj, attribute, data[attribute])

                return obj

            return {
                key: Python_Support.deserialize(value, class_registry)
                for key, value in data.items()
            }

        return data

    
    def remove_duplicates(list:list):
        rlist = []
        for item in list:
            if item not in rlist:
                rlist.append(item)

        return rlist


    def are_similar(word, compare, percentage_match=1):
        measurement = math.floor(len(word) * percentage_match)
        letters_left = len(word) - measurement

        # This iteration essentially moves a window of view across word.
        # The view of that window checks to see if the view fits anywhere within compare.
        # This allows for words that share a root word to be matched.
        # Such as "hate" and "hating".
        # Subsequently, "hate" could be matched with "hat" as well
        for i in range(letters_left + 1):
            if word[i : measurement + i] in compare:
                return True

        return False


    def remove_punctuation(text):
        translator = str.maketrans(string.punctuation, " " * len(string.punctuation))
        return text.translate(translator).lower()


    def adjust_terminal_history_capacity(new_capacity=1000):
        settings_path = os.path.expandvars(
            r"%APPDATA%\Code\User\settings.json"
        )

        with open(settings_path, "r") as file:
            settings = json.load(file)

        settings["terminal.integrated.scrollback"] = new_capacity

        with open(settings_path, "w") as file:
            json.dump(settings, file, indent=4)