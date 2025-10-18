"""Widget factory system for creating widgets in a type-safe and extensible manner."""

from typing import Any, Optional

from fabric.utils import logger

from shared.custom_button import CustomButtonWidget


class IndexedWidgetHelper:
    """Helper class to eliminate duplication in indexed widget handling."""

    @staticmethod
    def validate_and_get_index(
        identifier: str, collection: list, collection_name: str
    ) -> Optional[int]:
        """Unified index validation - DRY principle.

        Returns:
            Valid index or None if invalid
        """
        try:
            index = int(identifier)
            if not isinstance(collection, list) or not (0 <= index < len(collection)):
                logger.exception(
                    f"{collection_name} index {index} out of range "
                    f"(0-{len(collection) - 1})"
                )
                return None
            return index
        except (ValueError, TypeError):
            logger.exception(f"Invalid {collection_name} index: {identifier}")
            return None

    @staticmethod
    def get_config_path(config: dict, *path_parts: str) -> list:
        """Navigate config path safely - DRY principle."""
        result = config
        for part in path_parts:
            result = result.get(part, {})
        return result if isinstance(result, list) else []


class WidgetResolver:
    """Universal widget resolver with unified handling for all widget types."""

    def __init__(self, widgets_list: dict[str, type]):
        """Initialize the widget resolver.

        Args:
            widgets_list: Dictionary mapping widget names to widget classes
        """
        self.widgets_list = widgets_list
        self.helper = IndexedWidgetHelper()

    def resolve_widget(
        self, widget_spec: str, context: dict[str, Any]
    ) -> Optional[Any]:
        """Unified method to resolve ALL widget types.

        Args:
            widget_spec: Widget specification (e.g., "battery", "@custom_button:0")
            context: Context containing config and other data needed for resolution

        Returns:
            Widget instance or None if resolution fails
        """
        try:
            # Unified pattern: extract type and identifier
            if widget_spec.startswith("@"):
                widget_type, identifier = self._parse_reference(widget_spec)
                return self._resolve_by_type(widget_type, identifier, context)
            else:
                # Normal widget: treated as special "widget" type
                return self._resolve_by_type("widget", widget_spec, context)

        except Exception:
            logger.exception(f"Failed to resolve widget '{widget_spec}'")
            return None

    def _parse_reference(self, widget_spec: str) -> tuple[str, str]:
        """Parse @type:identifier format."""
        parts = widget_spec[1:].split(":", 1)
        return parts[0], parts[1] if len(parts) > 1 else ""

    def _resolve_by_type(
        self, widget_type: str, identifier: str, context: dict[str, Any]
    ) -> Optional[Any]:
        """Unified resolution by type - all widgets follow the same pattern."""
        resolvers = {
            "widget": lambda: self._create_simple_widget(identifier),
            "custom_button": lambda: self._create_indexed_widget(
                identifier,
                context,
                "custom_button",
                ["widgets", "custom_button_group", "buttons"],
                self._instantiate_custom_button,
            ),
            "group": lambda: self._create_indexed_widget(
                identifier,
                context,
                "widget_group",
                ["widget_groups"],
                self._instantiate_widget_group,
            ),
            "collapsible": lambda: self._create_indexed_widget(
                identifier,
                context,
                "collapsible_group",
                ["collapsible_groups"],
                self._instantiate_collapsible_group,
            ),
        }

        resolver = resolvers.get(widget_type)
        return resolver() if resolver else None

    def _create_simple_widget(self, widget_name: str) -> Optional[Any]:
        """Create normal widget - same pattern as custom button."""
        widget_class = self.widgets_list.get(widget_name)
        return widget_class() if widget_class else None

    def _create_indexed_widget(
        self,
        identifier: str,
        context: dict[str, Any],
        widget_type: str,
        config_path: list,
        instantiator_func,
    ) -> Optional[Any]:
        """Unified indexed widget creation - DRY principle."""
        config = context.get("config", {})
        collection = self.helper.get_config_path(config, *config_path)

        index = self.helper.validate_and_get_index(identifier, collection, widget_type)
        if index is None:
            return None

        return instantiator_func(collection[index], config, index)

    def _instantiate_custom_button(
        self, button_config: dict, config: dict, index: int
    ) -> CustomButtonWidget:
        """Create CustomButtonWidget instance."""
        return CustomButtonWidget(
            widget_name=f"custom_button_{index}", config=button_config
        )

    def _instantiate_widget_group(
        self, group_config: dict, config: dict, index: int
    ) -> Any:
        """Create WidgetGroup instance."""
        from shared.widget_container import WidgetGroup

        return WidgetGroup.from_config(
            group_config,
            self.widgets_list,
            main_config=config,
        )

    def _instantiate_collapsible_group(
        self, group_config: dict, config: dict, index: int
    ) -> Any:
        """Create CollapsibleGroupWidget instance."""
        from shared.collapsible_group import CollapsibleGroupWidget

        collapsible_group = CollapsibleGroupWidget()
        collapsible_group.update_config(group_config)
        collapsible_group.widgets_config = group_config.get("widgets", [])
        collapsible_group.set_context(config, self.widgets_list)
        return collapsible_group

    def batch_resolve(
        self, widget_specs: list[str], context: dict[str, Any]
    ) -> list[Any]:
        """Resolve multiple widgets efficiently.

        Args:
            widget_specs: List of widget specifications to resolve
            context: Context containing config and other data

        Returns:
            List of successfully created widget instances
        """
        return [
            widget
            for spec in widget_specs
            if (widget := self.resolve_widget(spec, context))
        ]
