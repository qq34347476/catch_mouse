进入虚拟环境 Windows

```bash
venv\Scripts\activate
```

macOS/Linux
```bash
source venv/bin/activate
```

安装依赖
```bash
pip install -r requirements.txt
```

更新依赖
```bash
pip freeze > requirements.txt
```

打包
```bash
pyinstaller --onefile --noconsole main.py
```