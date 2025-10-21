import pkgutil
import importlib
import inspect
from enum import Enum
from functools import lru_cache
from typing import Dict, List, Optional

__all__ = ["get_all_enums", "get_enum", "get_enum_names"]

@lru_cache(maxsize=1)
def _load_enums() -> Dict[str, List[str]]:
    enums: Dict[str, List[str]] = {}
    # Recorre recursivamente todos los módulos dentro de este paquete
    for finder, module_name, ispkg in pkgutil.walk_packages(__path__, prefix=__name__ + "."):
        try:
            module = importlib.import_module(module_name)
        except Exception:
            # Ignorar módulos que fallan al importar (evita romper la carga global)
            continue
        for _, obj in inspect.getmembers(module, inspect.isclass):
            try:
                if issubclass(obj, Enum) and obj is not Enum:
                    # Extraer los valores de la enumeración (convertir a str para estabilidad)
                    enums[obj.__name__] = [member.value for member in obj]
            except Exception:
                # Ignorar cualquier clase que no pueda procesarse
                continue
    return enums

def get_all_enums() -> Dict[str, List[str]]:
    """
    Devuelve un diccionario { EnumClassName: [value, ...] } con todas las enums
    encontradas en el paquete acb_orm.enums.
    """
    return dict(_load_enums())

def get_enum(name: str) -> Optional[List[str]]:
    """
    Devuelve la lista de valores de la enum cuyo nombre de clase es `name`.
    Retorna None si no existe.
    """
    return _load_enums().get(name)

def get_enum_names() -> List[str]:
    """
    Devuelve la lista ordenada de nombres de clases Enum disponibles en acb_orm.enums.
    Estos son los nombres que puedes pasar a get_enum(name).
    """
    return sorted(_load_enums().keys())
