def data_test():
    from common.utils import get_metadata

    METADATA = get_metadata()

    METADATA = METADATA.head()
    METADATA.index = METADATA['ITEM_ID']
    ITEM_MAPPER = METADATA.to_dict('index')
    print(ITEM_MAPPER)


def photo():
    import base64
    PHOTO_REFERENCE = "ATtYBwI3nlD50Xe9FboWTHqOMTaheRLelkdnNRVlsi4p_j3g8x3uWFWxfednICPfGFv7NzjYrZWRqC8rV_vQIn3jaCU-dv-hMJVe6ZHvQgrR_6I40JOr62KC-e0Im7QKzl7GJrzM_ggbKII5xH6szpCDYN3A9bzdVznoiSoeyxrVlvP1NDk"
    decoded = base64.b64decode(PHOTO_REFERENCE)
    print(decoded.decode('ascii'))


if __name__ == '__main__':
    # data_test()
    photo()
