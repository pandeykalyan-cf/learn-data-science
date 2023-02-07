import ast

from typing import Dict

def change_string_to_dict(cor: str) -> Dict:
  return ast.literal_eval(cor)