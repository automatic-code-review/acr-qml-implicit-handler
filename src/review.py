import os
import re

import automatic_code_review_commons as commons


def __is_qml(path):
    return path.endswith(".qml") or path.endswith(".qml.ui")


def review(config):
    path_source = config['path_source']

    merge = config['merge']
    changes = merge['changes']

    comments = []
    # Regex genérico para capturar "onAlgo:"
    regex = re.compile(r"\bon[A-Z]\w*\s*:")

    objs = []

    for change in changes:
        if change['deleted_file']:
            continue

        new_path = change['new_path']

        if not __is_qml(new_path):
            continue

        path = os.path.join(path_source, new_path)

        with open(path, 'r', encoding='utf-8') as f:
            for line_number, line in enumerate(f, start=1):
                if regex.search(line):
                    after_colon = line.split(":", 1)[1].strip()
                    # ignora funções anônimas tradicionais
                    if after_colon.startswith("function"):
                        continue
                    # ignora funções compactas tipo () { ... } ou (param) { ... }
                    if re.match(r'^\([^\)]*\)\s*{', after_colon):
                        continue
                    # ignora arrow functions tipo () => { ... } ou (param) => { ... }
                    if re.match(r'^\([^\)]*\)\s*=>\s*{', after_colon):
                        continue

                    objs.append({
                        "path": new_path,
                        "line_number": line_number,
                        "line_text": line.strip()
                    })

    if len(objs) > 0:
        occurrences = []

        for obj in objs:
            occurrences.append(f"""Arquivo: {obj['path']}<br>
Linha: {obj['line_number']}
```qml
{obj['line_text']}
```
""")

        comment_description = config["data"]["message"]
        comment_description = comment_description.replace("${OCCURRENCES}", "".join(occurrences))

        comments.append(commons.comment_create(
            comment_id=commons.comment_generate_id(comment_description),
            comment_path=None,
            comment_description=comment_description,
            comment_snipset=False,
        ))

    return comments
