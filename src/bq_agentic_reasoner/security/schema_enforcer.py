from typing import Dict, Any


class SchemaEnforcer:
    """
    Enforces strict schema on untrusted outputs.
    """

    def enforce(
        self,
        data: Dict[str, Any],
        allowed_fields: set[str],
    ) -> Dict[str, Any]:
        """
        Drops any unexpected fields.
        """

        return {
            k: v
            for k, v in data.items()
            if k in allowed_fields
        }
