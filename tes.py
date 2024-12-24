import sys
import os

# 現在のスクリプトディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# Toolfunction ディレクトリを検索パスに追加
toolfunction_dir = os.path.join(current_dir, "Toolfunction")
sys.path.append(toolfunction_dir)