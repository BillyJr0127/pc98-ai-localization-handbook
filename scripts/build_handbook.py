"""Build the self-contained reading copy from the maintained chapters."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
CHAPTERS = ['AGENTS.md', 'AI-GUIDE.md', 'WORKFLOW.md', 'FAST-PORT.md', 'TEXT-ROUNDTRIP.md', 'AUDIO.md', 'VALIDATION.md', 'LESSONS.md', 'FOLLOW-UP.md', 'RIGHTS.md', 'SOURCES.md', 'CHANGELOG.md']
INCLUDES = ['templates/PROJECT.json', 'templates/AUDIO-PROFILE.json', 'templates/STATUS.md',
            'templates/ISSUE.json', 'templates/RELEASE.json', 'examples/text.json', 'examples/audio.json', 'examples/binary.json',
            'scripts/inspect_inputs.py', 'scripts/check_examples.py', 'scripts/check_binary_examples.py',
            'requirements.txt', 'templates/ENGINE-ADAPTER.md', 'examples/translation-catalog.json',
            'scripts/engine_adapter.py', 'scripts/translation_exchange.py', 'scripts/export_workbook.py',
            'scripts/import_workbook.py', 'scripts/check_translation_workflow.py']


def render():
    content = ['# 給 AI 的 PC-98 中文化與音訊研究手冊：單檔版\n\n'
               '版本 1.2.1 · 2026-09-10。由分章文件產生。所有 AI 先遵守：**禁止重製；'
               '1. 盡速讓 DOS 下執行；2. 做出導出工具；3. 做出導入工具。** 保留原引擎，最少修改。'
               '先讀 AGENTS 與 AI 工作指引，再依使用者目標開始；'
               '不要假設任何 FDI 都能自動轉換。只分析使用者實際提供且可用的資料。'
               '本檔包含全部章節、模板、自製範例、入門腳本與人工 Excel 往返工具。\n\n'
               '使用者請提供：輸入路徑、來源與使用範圍、目標平台、目標語言、希望保留的音源模式。'
               '若工具無法讀本機檔案，先說明限制，不聲稱已執行。\n']
    for name in CHAPTERS:
        content.append('\n---\n\n' + (ROOT/name).read_text(encoding='utf-8'))
    content.append('\n---\n\n# 附錄：模板、自製範例與入門腳本\n\n'
                   '單檔閱讀時不必另外下載檔案。需要執行時，先閱讀程式，再在獨立教材資料夾按下列相對路徑建立；'
                   '不可覆寫使用者的原檔。這些腳本不是遊戲轉換器。\n')
    for name in INCLUDES:
        suffix = Path(name).suffix
        language = {'.json': 'json', '.md': 'markdown', '.py': 'python', '.txt': 'text'}[suffix]
        content.append(f'\n## `{name}`\n\n```{language}\n' + (ROOT/name).read_text(encoding='utf-8').rstrip() + '\n```\n')
    result = '\n'.join(content)
    # The chapters use external citations. Keep the reading copy independent
    # from local Markdown file links should future chapters introduce any.
    result = re.sub(r'\[([^\]]+)\]\((?:\./)?([A-Z][A-Z-]*\.md)\)', r'\1（本檔對應章節）', result)
    return result


if __name__ == '__main__':
    target = ROOT/'AI-HANDBOOK.md'
    target.write_text(render(), encoding='utf-8', newline='\n')
    print(f'Built {target.name}')
