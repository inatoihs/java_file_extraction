import os
import re

# Javaファイルのパス
java_file_path = "/Users/username/your/source/your_folder/your_file.java"

# プロジェクトのソースディレクトリ
source_directory = "/Users/username/your/source"

# ソースディレクトリからJavaファイルへの相対パスを取得
relative_path = os.path.relpath(java_file_path, source_directory)

# Import文を見つける正規表現
import_pattern = re.compile(r"^import\s+([\w\.]+);", re.M)


def find_file(root_folder, file_name):
    for root, dirs, files in os.walk(root_folder):
        if file_name in files:
            return os.path.join(root, file_name)
    return None


def rec_finder(java_file_path):
    not_found = set()
    with open(java_file_path, "r") as file:
        java_content = file.read()

    # Import文を探す
    imports = import_pattern.findall(java_content)
    unique_imports = set(imports)  # 重複を排除

    for import_line in unique_imports:
        # パッケージ構造をファイルパスに変換
        relative_path = import_line.replace(".", "/") + ".java"
        file_path = find_file(source_directory, relative_path.split("/")[-1])
        if file_path:
            # 依存ファイルをフォルダ"dependencies"にコピー
            with open(file_path, "r") as file:
                content = file.read()
            try:
                with open(f"dependencies/{relative_path}", "x") as file:
                    file.write(content)
            # パスに含まれるフォルダが存在しない場合は作成
            except FileNotFoundError as e:
                os.makedirs(os.path.dirname(f"dependencies/{relative_path}"))
                with open(f"dependencies/{relative_path}", "x") as file:
                    file.write(content)
            except FileExistsError as e:
                pass

            not_found.update(rec_finder(file_path))
        else:
            not_found.add(import_line)
    return not_found


def main():
    with open(java_file_path, "r") as file:
        content = file.read()
    try:
        with open(
            f"dependencies/{relative_path}",
            "x",
        ) as file:
            file.write(content)
    # パスに含まれるフォルダが存在しない場合は作成
    except FileNotFoundError as e:
        os.makedirs(os.path.dirname(f"dependencies/{relative_path}"))
        with open(
            f"dependencies/{relative_path}",
            "x",
        ) as file:
            file.write(content)
    except FileExistsError as e:
        pass
    not_found = rec_finder(java_file_path)
    with open("not_found.txt", "w") as file:
        for line in not_found:
            file.write(line + "\n")


if __name__ == "__main__":
    main()
