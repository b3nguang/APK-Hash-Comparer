import zipfile
import hashlib
import os
import subprocess
from rich.progress import Progress
import difflib
from rich.console import Console
from rich.syntax import Syntax
from rich.text import Text

console = Console()

def calculate_hash(file_path):
    """计算文件的SHA-256哈希值"""
    sha256 = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            sha256.update(chunk)
    return sha256.hexdigest()

def extract_apk(apk_path, extract_to):
    """解压APK文件到指定目录"""
    with zipfile.ZipFile(apk_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

def is_bytecode_file(file_path):
    """判断文件是否为字节码文件（.class 或 .dex）"""
    return file_path.endswith('.class') or file_path.endswith('.dex')

def compare_files(original_dir, modified_dir):
    """比较两个目录中的字节码文件，并找出有差异的文件"""
    differences = []
    for root, _, files in os.walk(original_dir):
        for file in files:
            if is_bytecode_file(file):
                original_file_path = os.path.join(root, file)
                modified_file_path = original_file_path.replace(original_dir, modified_dir)
                
                if os.path.exists(modified_file_path):
                    original_hash = calculate_hash(original_file_path)
                    modified_hash = calculate_hash(modified_file_path)
                    
                    if original_hash != modified_hash:
                        differences.append((original_file_path, modified_file_path))
    
    return differences

def run_jadx(file_path, output_dir, jadx_path):
    """运行jadx将文件反编译"""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    cmd = f"{jadx_path} -d {output_dir} {file_path}"
    subprocess.run(cmd, shell=True, check=True)

def get_file_lines(file_path):
    """读取文件并返回其内容"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.readlines()
    except Exception as e:
        console.print(f"[red]读取文件 {file_path} 时出错: {e}[/red]")
        return []

def print_diff(file1, file2):
    """打印两个文件的差异"""
    lines1 = get_file_lines(file1)
    lines2 = get_file_lines(file2)

    if not lines1 or not lines2:
        return

    diff = difflib.unified_diff(
        lines1, lines2,
        fromfile=os.path.relpath(file1),
        tofile=os.path.relpath(file2),
        lineterm=''
    )

    diff_lines = list(diff)
    if diff_lines:
        for line in diff_lines:
            if line.startswith('-'):
                console.print(Text(line, style="bold red"))
            elif line.startswith('+'):
                console.print(Text(line, style="bold green"))
            elif line.startswith('@@'):
                console.print(Text(line, style="bold yellow"))
            else:
                console.print(line, style="default")

        console.print("\n" + "=" * 40 + "\n")

def compare_files_in_directory(root_directory):
    """比较目录中同名文件的差异"""
    files_dict = {}

    # 遍历所有目录和子目录
    for dirpath, _, filenames in os.walk(root_directory):
        for file in filenames:
            full_path = os.path.join(dirpath, file)
            if file not in files_dict:
                files_dict[file] = []
            files_dict[file].append(full_path)

    # 比较同名文件
    for file, paths in files_dict.items():
        if len(paths) > 1:
            for i in range(len(paths)):
                for j in range(i + 1, len(paths)):
                    console.print(f"Comparing {paths[i]} and {paths[j]}:\n", style="bold cyan")
                    print_diff(paths[i], paths[j])

if __name__ == "__main__":
    original_apk = input("请输入原始APK的路径: ")
    modified_apk = input("请输入修改后APK的路径: ")
    jadx_path = input("请输入jadx.bat的路径: ")

    original_output_dir = "original_apk_files"
    modified_output_dir = "modified_apk_files"
    decompiled_output_dir = "decompiled_files"

    # 解压APK文件
    with Progress() as progress:
        task = progress.add_task("解压APK文件", total=2)
        
        extract_apk(original_apk, original_output_dir)
        progress.advance(task)
        
        extract_apk(modified_apk, modified_output_dir)
        progress.advance(task)

    # 比较字节码文件的哈希值并反编译不同的字节码文件
    console.print("正在比较字节码文件...")
    differences = compare_files(original_output_dir, modified_output_dir)
    
    if differences:
        console.print("以下字节码文件存在差异:")
        for original_file, modified_file in differences:
            console.print(f"原始文件: {original_file}")
            console.print(f"修改后的文件: {modified_file}")
            

            # 反编译原始和修改后的文件
            original_decompiled_dir = os.path.join(decompiled_output_dir, 'original')
            modified_decompiled_dir = os.path.join(decompiled_output_dir, 'modified')
            
            run_jadx(original_file, original_decompiled_dir, jadx_path)
            run_jadx(modified_file, modified_decompiled_dir, jadx_path)
    else:
        console.print("字节码文件中未发现差异。")

    compare_files_in_directory(decompiled_output_dir)
