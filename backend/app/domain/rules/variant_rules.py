from typing import List

from app.domain.entities.idea_variant import IdeaVariant


class VariantRules:
    """
    Reglas de negocio para la gestión de variantes dentro de una versión.

    ¿Qué problema resuelven estas rules?
    Una IdeaVersion puede tener múltiples variantes, pero solo una puede ser
    seleccionada para avanzar al siguiente ciclo. Esta clase centraliza
    las reglas que gobiernan esa selección y la integridad del conjunto de variantes.

    Quién usa estas rules: version_service.py o idea_service.py, antes de
    ejecutar operaciones sobre variantes (seleccionar, validar, limpiar).
    """

    # Número máximo de variantes permitidas por versión.
    # Si la IA genera más de este límite, el mapper debe truncar o el servicio rechazar.
    # Ajustar este valor si el producto decide ofrecer más opciones al usuario.
    MAX_VARIANTS_PER_VERSION = 5

    # Número mínimo de variantes para que una versión sea procesable.
    # Si hay menos, puede indicar que la IA falló parcialmente.
    MIN_VARIANTS_PER_VERSION = 1

    @staticmethod
    def can_select_variant(variant: IdeaVariant, all_variants: List[IdeaVariant]) -> bool:
        """
        Determina si una variante específica puede ser seleccionada.

        Reglas:
          1. La variante debe pertenecer al conjunto de variantes de la versión.
          2. No debe haber ya otra variante seleccionada en el mismo conjunto.

        Si retorna False porque ya hay una seleccionada, el servicio debe
        primero deseleccionar la anterior antes de seleccionar la nueva.
        Esto evita tener dos variantes seleccionadas simultáneamente.
        """
        variant_ids = {v.id for v in all_variants}
        if variant.id not in variant_ids:
            return False

        already_selected = any(v.is_selected for v in all_variants if v.id != variant.id)
        return not already_selected

    @staticmethod
    def get_selected_variant(variants: List[IdeaVariant]) -> IdeaVariant | None:
        """
        Retorna la variante seleccionada de la lista, o None si ninguna lo está.

        Usar este método en los servicios en lugar de buscar manualmente con un loop.
        Si retorna None cuando se esperaba una variante seleccionada,
        revisar si version_service.py está llamando variant.select() correctamente.
        """
        selected = [v for v in variants if v.is_selected]
        if len(selected) > 1:
            # Estado inválido: nunca debería ocurrir si las rules se aplican correctamente.
            # Si llega aquí, hay una race condition o una selección duplicada en el servicio.
            raise ValueError(
                f"Se encontraron {len(selected)} variantes seleccionadas simultáneamente. "
                "Solo puede haber una. Revisar version_service.py o idea_service.py."
            )
        return selected[0] if selected else None

    @staticmethod
    def validate_variant_count(variants: List[IdeaVariant]) -> None:
        """
        Valida que el número de variantes esté dentro de los límites permitidos.

        Llamar este método después de que la IA retorna el conjunto de variantes,
        antes de persistirlas. Si falla, el problema está en cómo el provider de IA
        genera variantes (mock_provider.py u ollama_provider.py).
        """
        count = len(variants)
        if count < VariantRules.MIN_VARIANTS_PER_VERSION:
            raise ValueError(
                f"Se esperaba al menos {VariantRules.MIN_VARIANTS_PER_VERSION} variante(s), "
                f"pero se recibieron {count}. Revisar el provider de IA activo."
            )
        if count > VariantRules.MAX_VARIANTS_PER_VERSION:
            raise ValueError(
                f"Se recibieron {count} variantes, pero el máximo permitido es "
                f"{VariantRules.MAX_VARIANTS_PER_VERSION}. "
                "Revisar variant_mapper.py para truncar correctamente."
            )

    @staticmethod
    def assert_has_selected_variant(variants: List[IdeaVariant]) -> IdeaVariant:
        """
        Versión imperativa de get_selected_variant: lanza excepción si no hay seleccionada.

        Usar en synthesis_service.py o version_service.py cuando el flujo
        requiere obligatoriamente una variante seleccionada para continuar.

        Ejemplo de uso:
            selected = VariantRules.assert_has_selected_variant(variants)
            # Solo llega aquí si hay exactamente una variante seleccionada.
        """
        selected = VariantRules.get_selected_variant(variants)
        if selected is None:
            raise ValueError(
                "No hay ninguna variante seleccionada en esta versión. "
                "El usuario debe seleccionar una variante antes de avanzar al siguiente ciclo."
            )
        return selected