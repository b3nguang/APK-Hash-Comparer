![APK-Hash-Comparer](https://socialify.git.ci/b3nguang/APK-Hash-Comparer/image?description=1&descriptionEditable=%E5%BF%AB%E9%80%9F%E6%AF%94%E5%AF%B9%E4%BA%BA%E4%B8%BA%E7%AF%A1%E6%94%B9%E5%90%8E%E7%9A%84%20APK%20%E6%96%87%E4%BB%B6%EF%BC%8C%E5%8F%B8%E6%B3%95%E9%89%B4%E5%AE%9A%E5%BF%AB%E4%BA%BA%E4%B8%80%E6%AD%A5&forks=1&issues=1&language=1&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F121670274%3Fs%3D400%26u%3D686132087f2e2324958b610f905a1b388478295b%26v%3D4&name=1&owner=1&pulls=1&stargazers=1&theme=Light)

## ✈️ 一、工具特性

- **APK 解压**：将两个 APK 文件解压到指定目录。
- **字节码文件比较**：比较解压目录中的字节码文件（.class 或.dex），通过 SHA-256 哈希值检测文件是否有差异。
- **字节码反编译**：使用 JADX 工具对差异字节码文件进行反编译，以便深入查看代码差异。
- **差异显示**：在控制台中详细显示两个文件之间的代码差异。

## 🚨 二、配置

- Python 3.7 及以上版本
- 必须安装以下 Python 库：
  - `rich`（用于美化控制台输出）
- [JADX](https://github.com/skylot/jadx) 工具（用于反编译字节码）

## 🐉 三、使用

1. **克隆仓库**

   ```bash
   git clone https://github.com/b3nguang/APK-Hash-Comparer.git
   cd APK-Hash-Comparer
   ```

2. **运行脚本**

   在运行脚本时，需要提供原始 APK、修改后 APK 的路径以及 JADX 的路径。可以直接运行以下命令：

   ```bash
   python main.py
   ```

3. **输入路径**

   按照提示输入以下内容：
   - 原始 APK 的路径
   - 修改后 APK 的路径
   - jadx.bat 的路径（JADX 工具的执行文件）

4. **查看结果**

   - 解压 APK 文件后，工具将比较两个 APK 的字节码文件，并列出有差异的文件。
   - 对有差异的文件进行反编译，并在控制台显示反编译后的代码差异。

## 📸 四、示例输出

![image-20240830173238584](assets/image-20240830173238584.png)

## ⚠ 五、注意事项

- 确保提供的 APK 文件和 JADX 路径正确，否则脚本将无法正确运行。
- 该工具仅对比字节码文件（.class 和.dex），不比较资源文件。

## 🤝 六、贡献

欢迎贡献代码！如果有任何改进建议或发现问题，欢迎提交 issue 或 pull request。
