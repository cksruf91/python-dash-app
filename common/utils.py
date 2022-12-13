import os
from typing import Tuple, List, Any

import pandas as pd


def get_metadata() -> pd.DataFrame:
    """ 메타 데이터 로드 함수
    Returns: 메타 데이터 데이터프레임
    """
    data = pd.read_csv(os.path.join('files', 'cntnt_meta.csv'), index_col=0)
    data = data[['ITEM_ID', 'CNTNT_ID', 'CNTNT_CATG_NM', 'CNTNT_NM', 'INTC_CONT']]
    data = data[data.ITEM_ID != -1].copy()
    return data


def get_table_source(dataset: pd.DataFrame) -> Tuple[List[dict], List[dict]]:
    """ DataTable 생성을 위한 포멧변환

    Args:
        dataset: 메타 데이터

    Returns: 데이터, 컬럼명
    """
    columns = [{"name": i, "id": i} for i in dataset.columns]
    source = []
    for row in dataset.to_dict('records'):
        row['id'] = row['ITEM_ID']
        source.append(row)
    return source, columns