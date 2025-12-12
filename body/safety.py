import os
import shutil
from .chronicle import Chronicle


class SafetyError(Exception):
    pass


class ActionPlan:
    """
    Governs destructive file operations to ensure they are logged and safe.
    Adheres to the YuHun Protocols:
    1. No obscure deletion of user data.
    2. Mandatory logging to Chronicle.
    """

    SAFE_EXTENSIONS = [".tmp", ".log", ".bak", ".cache"]
    SAFE_DIRS = [
        "temp", "tmp", "cache", "build", "dist",
        "__pycache_", "node_modules", ".pytest_cache"
    ]

    @staticmethod
    def _is_safe_path(path: str) -> bool:
        """Determines if a path is considered 'safe' to delete (temporary or build artifacts)."""
        path = path.lower().replace("\\", "/")
        parts = path.split("/")
        basename = parts[-1]

        # Check directories (exact match in path)
        for part in parts:
            if part in ActionPlan.SAFE_DIRS:
                return True

        # Check safe prefixes for the directory/file itself
        if basename.startswith("temp_") or basename.startswith("tmp_") or basename.startswith("test_"):
            return True

        # Check extensions
        for ext in ActionPlan.SAFE_EXTENSIONS:
            if path.endswith(ext):
                return True

        return False

    @staticmethod
    def delete_file(
        path: str,
        reason: str,
        force: bool = False,
    ) -> None:
        """Safely deletes a file."""
        path = os.path.abspath(path)
        if not os.path.exists(path):
            return

        is_safe = ActionPlan._is_safe_path(path)

        if not is_safe and not force:
            thinking = f"Prevented deletion of sensitive file: {path}"
            Chronicle.log("BLOCK_DELETION", thinking, "Data Loss Risk", "Raised SafetyError")
            raise SafetyError(
                f"SAFETY BLOCK: Cannot delete sensitive file '{path}' without force=True. Reason: {reason}"
            )

        # Execution
        action_type = "DELETE_FILE" if is_safe else "DELETE_SENSITIVE_FILE"
        risk = "Low (Temp)" if is_safe else "High (Permanent Data Loss)"
        Chronicle.log(
            action=action_type,
            thinking=f"Deleting {path}. Reason: {reason}. Safe={is_safe}, Force={force}",
            risk=risk,
            execution="os.remove()",
        )

        try:
            os.remove(path)
        except Exception as e:
            Chronicle.log("DELETE_ERROR", f"Failed to delete {path}", str(e), "None")
            raise e

    @staticmethod
    def delete_directory(path: str, reason: str, force: bool = False) -> None:
        # Existing method unchanged
        """
        Safely deletes a directory.
        """
        path = os.path.abspath(path)
        if not os.path.exists(path):
            return

        is_safe = ActionPlan._is_safe_path(path)

        if not is_safe and not force:
            thinking = f"Prevented deletion of sensitive directory: {path}"
            Chronicle.log("BLOCK_DELETION_DIR", thinking, "Mass Data Loss Risk", "Raised SafetyError")
            raise SafetyError(f"SAFETY BLOCK: Cannot delete sensitive directory '{path}' without force=True. Reason: {reason}")

        action_type = "DELETE_DIR" if is_safe else "DELETE_SENSITIVE_DIR"
        risk = "Low (Temp)" if is_safe else "High (Mass Data Loss)"

        Chronicle.log(
            action=action_type,
            thinking=f"Deleting recursive {path}. Reason: {reason}. Safe={is_safe}, Force={force}",
            risk=risk,
            execution="shutil.rmtree()"
        )

        try:
            shutil.rmtree(path)
        except Exception as e:
            Chronicle.log("DELETE_DIR_ERROR", f"Failed to delete {path}", str(e), "None")
            raise e
