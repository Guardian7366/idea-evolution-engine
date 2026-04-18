from dataclasses import dataclass
import json


@dataclass(frozen=True)
class IdeaContent:
    """
    Value Object que representa el contenido textual de una idea.
    Es inmutable: si el contenido cambia, se crea una nueva instancia.
    """
    title: str
    description: str

    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("El título de la idea no puede estar vacío.")
        if len(self.title.strip()) > 200:
            raise ValueError("El título no puede superar los 200 caracteres.")
        if not self.description or not self.description.strip():
            raise ValueError("La descripción de la idea no puede estar vacía.")

    def with_title(self, new_title: str) -> "IdeaContent":
        """Retorna un nuevo IdeaContent con el título actualizado."""
        return IdeaContent(title=new_title, description=self.description)

    def with_description(self, new_description: str) -> "IdeaContent":
        """Retorna un nuevo IdeaContent con la descripción actualizada."""
        return IdeaContent(title=self.title, description=new_description)
    
    def __str__(self) -> str:
        """Representación del contenido en JSON"""
        return json.dumps({
            "title": self.title,
            "description": self.description
        }, ensure_ascii=False)
