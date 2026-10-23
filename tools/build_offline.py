"""把 src/memo-drafter.src.html 組成可離線使用的 index.html（內嵌 JSZip、補上完整 HTML 外框）。
用法：在專案根目錄執行  npm install  後  python3 tools/build_offline.py"""
import re, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = open(os.path.join(ROOT, 'src/memo-drafter.src.html'), encoding='utf8').read()
jszip = open(os.path.join(ROOT, 'node_modules/jszip/dist/jszip.min.js'), encoding='utf8').read()
s = re.sub(r'<script src="https://cdnjs[^>]*></script>', lambda m: '<script>' + jszip + '</script>', s)
s = s.replace('<link rel="preconnect" href="https://fonts.googleapis.com">\n', '')
s = re.sub(r'<link rel="stylesheet" href="https://fonts.googleapis.com[^>]*>\n', '', s)
s = s.replace('<meta name="claude:viewport-fit-sides" content="cover">\n', '')
title = re.search(r'<title>.*?</title>', s).group(0); s = s.replace(title, '', 1)
head = ('<!doctype html>\n<html lang="zh-Hant">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width,initial-scale=1">\n' + title + '\n</head>\n<body>\n')
open(os.path.join(ROOT, 'index.html'), 'w', encoding='utf8').write(head + s + '\n</body>\n</html>\n')
print('index.html 已更新')
