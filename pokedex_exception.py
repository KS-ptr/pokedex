class Pokedex_Exception(Exception):
    """
    スーパークラス
    """
    pass

class SizeNotFound(Pokedex_Exception):
    """
    高さ、重さの数値を取得できなかったときに起こる例外
    """
    pass

class PropertyLength_Exception(Pokedex_Exception):
    """
    特性、タマゴグループ、タイプなどのプロパティが適切な数でない場合に起こる例外
    """
    pass

class AbilityID_NotFound(Pokedex_Exception):
    """
    特性のjsonファイル内に、取得した特性が見つからなかったときに起こる例外
    """
    pass

class MoveID_NotFound(Pokedex_Exception):
    """
    技のjsonファイル内に、取得した技IDが見つからなかったときに起こる例外
    """
    pass