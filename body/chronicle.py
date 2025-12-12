import os
import datetime

class Chronicle:
    LOG_FILE = "chronicle.log"

    @staticmethod
    def log(action: str, thinking: str, risk: str, execution: str):
        """
        Logs a decision to the chronicle.log in the YuHun standard format.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        entry = (
            f"[{timestamp}] [{action}]\n"
            f"Thinking: {thinking}\n"
            f"Risk: {risk}\n"
            f"Execution: {execution}\n"
            f"{'-'*40}\n"
        )
        
        # Append to file
        # Used by both Agent (manual edits) and System (SpineEngine)
        try:
            with open(Chronicle.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(entry)
        except Exception as e:
            print(f"⚠️ Failed to write to Chronicle: {e}")
