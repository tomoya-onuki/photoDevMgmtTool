# 現像サポートツール
## 写真選択ツール
- photoSelectTool.py
### Usage
```
. venv/bin/activate
python3 photoSelectTool.py [ディレクトリ名]
```

[ディレクトリ名]/selectedディレクトリ/下に選択済み画像ファイルがコピーされる

## DaVinci Resolveで写真を現像したのちにExifをコピーするツール
- cpExifTool.py
### 前提条件
- .[任意ディレクトリ]/dev/に現像済み画像ファイルを保存する
- .[任意ディレクトリ]/dev/の現像済み画像ファイルと.[任意ディレクトリ]/selected/の現像前画像ファイルの順序は一致している

### Usage
```
. venv/bin/activate
python3 photoSelectTool.py [任意ディレクトリ名]
```