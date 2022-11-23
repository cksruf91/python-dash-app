import warnings
from io import BytesIO

import pandas as pd
import numpy as np
import requests
from PIL import Image
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid import GridUpdateMode, DataReturnMode


def get_image(url):
    response = requests.get(url)
    assert response.status_code == 200
    image_array = np.array(Image.open(BytesIO(response.content)))
    return image_array


def aggrid_interactive_table(df: pd.DataFrame, multiple=True, height=400):
    mode = 'multiple' if multiple else 'single'
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", FutureWarning)
        options = GridOptionsBuilder.from_dataframe(
            df, enableRowGroup=True, enableValue=False, enablePivot=True
        )
        options.configure_side_bar(columns_panel=True)
        options.configure_selection(selection_mode=mode, use_checkbox=True)
        selection = AgGrid(
            df,
            enable_enterprise_modules=True,
            gridOptions=options.build(),
            height=height,
            # theme="light",
            update_mode=GridUpdateMode.MODEL_CHANGED,
            data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
            allow_unsafe_jscode=True,
        )

    return selection
