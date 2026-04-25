import io
import subprocess
import sys
from pathlib import Path

# 設定標準輸出 (stdout) 使用 UTF-8 編碼
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")


def is_merging() -> bool:
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            check=True,
            text=True,
        )
        # 如果 git status 的輸出包含 "UU" 表示有衝突
        return "UU" in result.stdout  # noqa: TRY300
    except subprocess.CalledProcessError as e:
        print(f"ℹ️ Error checking git status: {e}", file=sys.stderr)
        return False


def add_merge_prefix(commit_msg_file: str) -> None:
    # 讀取 commit 訊息檔案的路徑
    commit_msg_path = Path(commit_msg_file)

    try:
        commit_msg = commit_msg_path.read_text(encoding="utf-8")
        print(f"ℹ️ Original commit message: {commit_msg}")
    except FileNotFoundError:
        print(
            f"ℹ️ Error: Commit message file '{commit_msg_file}' not found.",
            file=sys.stderr,
        )
        sys.exit(1)

    # 檢查是否處於合併衝突狀態
    print("ℹ️ Checking for merge conflict...")
    if is_merging():
        print("ℹ️ commit_msg")  # 顯示合併衝突訊息
        print(f"{commit_msg=}")
        # 直接寫入 MERGE_MSG 檔案，修改 commit 訊息在開頭加上 "🔀 "
        # with open(commit_msg_file, "w", encoding="utf-8") as f:
        #     f.write("🔀 Merge conflict\n")
        return

    # 如果 commit 訊息包含 "Merge branch"，且未加上表情符號，則加上 "🔀 "
    if "Merge branch" in commit_msg and not commit_msg.startswith("🔀"):
        new_commit_msg = "🔀 " + commit_msg
        commit_msg_path.write_text(new_commit_msg, encoding="utf-8")
        print("ℹ️ Modified commit message:")
        print(new_commit_msg)  # 顯示修改後的 commit 訊息
    else:
        print("ℹ️ No modifications made to commit message.")


if __name__ == "__main__":
    if len(sys.argv) < 2:  # noqa: PLR2004
        print("ℹ️ Error: No commit message file path provided.", file=sys.stderr)
        sys.exit(1)

    # 接收 commit 訊息檔案的路徑作為參數
    commit_msg_file = sys.argv[1]
    print(f"ℹ️ Commit message file path: {commit_msg_file}")  # 調試訊息

    add_merge_prefix(commit_msg_file)
