"""
Deprecated.
A menos que haya una razón para mantener esta clase, es más sencillo usar
title y content como strings directamente en las clases que lo ocupen,
para no tener que mapear los valores entre python y la base de datos
cada vez que se cree o actualice una idea, versión o variante.
"""
class IdeaContent:
    ...
