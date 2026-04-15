from pathlib import Path

import pandas as pd
from DrissionPage import Chromium


BASE_URL = 'https://biosig.lab.uq.edu.au/pkcsm/prediction'
XLSX_PATH = Path(__file__).with_name('PubChem_compound_kras_inhibitors.xlsx')
OUTPUT_TXT_PATH = Path(__file__).with_name('pk_5299_redirect_urls.txt')

INPUT_XPATH = 'xpath:/html/body/div[3]/div[2]/div[2]/form/div[1]/div[3]/div/input'
SUBMIT_XPATH = 'xpath:/html/body/div[3]/div[2]/div[2]/form/div[3]/div/div/div/div[2]/button'


def load_smiles_from_excel(file_path: Path):
    if not file_path.exists():
        raise FileNotFoundError(f'Excel 文件不存在: {file_path}')

    df = pd.read_excel(file_path)
    if df.empty:
        raise ValueError('Excel 文件为空，未读取到任何数据。')

    # Prefer any column that contains "smiles" in its name.
    smiles_col = None
    for col in df.columns:
        if 'smiles' in str(col).strip().lower():
            smiles_col = col
            break

    if smiles_col is None:
        smiles_col = df.columns[0]

    smiles_series = df[smiles_col].dropna().astype(str).str.strip()
    smiles_list = [s for s in smiles_series.tolist() if s]
    if not smiles_list:
        raise ValueError('未从 Excel 中提取到有效 SMILES。')

    return smiles_list, str(smiles_col)


def submit_and_get_redirect_url(tab, smiles: str, wait_seconds: int = 60):
    tab.get(BASE_URL)
    tab.wait(1)

    text_box = tab.ele(INPUT_XPATH, timeout=10)
    if not text_box:
        raise RuntimeError('未找到输入框，页面结构可能已变化。')

    text_box.input(smiles, clear=True)

    send_button = tab.ele(SUBMIT_XPATH, timeout=10)
    if not send_button:
        raise RuntimeError('未找到提交按钮，页面结构可能已变化。')

    before_submit_url = tab.url
    send_button.click()

    for _ in range(wait_seconds * 2):
        if tab.url != before_submit_url:
            return tab.url
        tab.wait(0.5)

    return tab.url


def main():
    smiles_list, smiles_col = load_smiles_from_excel(XLSX_PATH)
    print(f'已读取 SMILES 列: {smiles_col}，共 {len(smiles_list)} 条。')

    browser = Chromium()
    tab = browser.new_tab(BASE_URL)

    results = []
    total = len(smiles_list)

    for i, smiles in enumerate(smiles_list, 1):
        try:
            redirect_url = submit_and_get_redirect_url(tab, smiles)
            print(f'[{i}/{total}] 跳转网址: {redirect_url}')
            results.append(f'{i}\t{smiles}\t{redirect_url}')
        except Exception as e:
            err = f'ERROR: {type(e).__name__}: {e}'
            print(f'[{i}/{total}] 处理失败: {err}')
            results.append(f'{i}\t{smiles}\t{err}')

    OUTPUT_TXT_PATH.write_text('\n'.join(results), encoding='utf-8')
    print(f'完成，已写入: {OUTPUT_TXT_PATH}')


if __name__ == '__main__':
    main()
