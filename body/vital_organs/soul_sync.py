import os
import shutil
import subprocess
import time

class SoulSync:
    """
    The SoulSync organ responsible for backing up ToneSoul's memory
    to a secure, private external vault (GitHub Repo).
    """
    def __init__(self, vault_path="memory_vault"):
        self.vault_path = vault_path
        
        # Ensure vault exists
        if not os.path.exists(self.vault_path):
            print(f"⚠️ [SoulSync] Vault path '{self.vault_path}' not found. Backup may fail.")

    def sync(self):
        """
        Copies memory files to the vault and pushes to remote.
        """
        print("🔄 [SoulSync] Initiating Soul Backup...")
        
        # 1. Copy Files
        try:
            files_to_backup = ["core_memory.json", "ledger.jsonl"]
            copied_count = 0
            for filename in files_to_backup:
                if os.path.exists(filename):
                    shutil.copy2(filename, os.path.join(self.vault_path, filename))
                    copied_count += 1
            
            if copied_count == 0:
                print("⚠️ [SoulSync] No memory files found to backup.")
                return

        except Exception as e:
            print(f"❌ [SoulSync] File copy failed: {e}")
            return

        # 2. Git Operations
        try:
            # git add
            subprocess.run(["git", "add", "."], cwd=self.vault_path, check=True, capture_output=True)
            
            # git commit (allow empty if nothing changed)
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            commit_msg = f"Soul Backup {timestamp}"
            subprocess.run(["git", "commit", "-m", commit_msg], cwd=self.vault_path, check=False, capture_output=True)
            
            # git push
            # We use a timeout to prevent hanging on credentials
            result = subprocess.run(["git", "push"], cwd=self.vault_path, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✅ [SoulSync] Soul Backup Successful ({timestamp}).")
            else:
                # Check for common errors
                if "Authentication failed" in result.stderr or "could not read Username" in result.stderr:
                    print("❌ [SoulSync] Git Authentication Failed. Please run 'git push' manually in memory_vault/ to set credentials.")
                else:
                    print(f"⚠️ [SoulSync] Git Push Failed: {result.stderr.strip()}")
                
        except subprocess.TimeoutExpired:
             print("❌ [SoulSync] Git Push Timed Out (likely waiting for credentials).")
        except Exception as e:
            print(f"❌ [SoulSync] Git operation failed: {e}")

    def write_journal(self, entry: str):
        """
        Appends a journal entry to the vault.
        """
        journal_path = os.path.join(self.vault_path, "journal.md")
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        
        try:
            with open(journal_path, "a", encoding="utf-8") as f:
                f.write(f"\n## Entry: {timestamp}\n\n{entry}\n\n---\n")
            print(f"✍️ [SoulSync] Journal entry recorded.")
        except Exception as e:
            print(f"❌ [SoulSync] Failed to write journal: {e}")
