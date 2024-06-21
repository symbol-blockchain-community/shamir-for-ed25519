from Crypto.Protocol.SecretSharing import Shamir


def split_private_key_for_shamir(key: str) -> list[bytes]:
    """
    秘密鍵をシャミア向けに分割する(ライブラリの仕様上 16bytes 迄しか扱えないため)
    """
    if len(key) != 64:
        raise ValueError("The key must be a 64-character hex string.")

    key_bytes1 = bytes.fromhex(key[:32])
    key_bytes2 = bytes.fromhex(key[32:])
    return [key_bytes1, key_bytes2]


def generate_shamir_keys(key: str) -> list[tuple[int, int, str]]:
    """
    シャミアの秘密分散法を使って秘密鍵を分割する
    """

    # 秘密鍵を分割
    splited_key = split_private_key_for_shamir(key)
    # シャミアの秘密分散法を使って秘密鍵を分割
    shamirs = [Shamir.split(3, 5, k, None) for k in splited_key]

    # splited_key の index と シャミアの index + 分割された秘密鍵
    r: list[tuple[int, int, str]] = []

    # 保管用の配列を作成
    for i, shamir in enumerate(shamirs):
        [r.append((i, idx, s.hex())) for idx, s in shamir]

    return r


def recover_shamir_keys(shares: list[tuple[int, int, str]]) -> str:
    """
    シェアから復元する
    """

    s1 = []
    s2 = []

    for i, idx, s in shares:
        if i == 0:
            s1.append((idx, bytes.fromhex(s)))
            continue

        if i == 1:
            s2.append((idx, bytes.fromhex(s)))
            continue

        raise Exception(f"Invalid index: {i}")

    k1 = Shamir.combine(s1, None)
    k2 = Shamir.combine(s2, None)

    return f"{k1.hex().upper()}{k2.hex().upper()}"
