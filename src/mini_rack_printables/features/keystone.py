from mini_rack_printables.features.import_feature import ImportFeature


class Keystone(ImportFeature):
    """
    A keystone cutout part.
    """

    def __init__(self) -> None:
        super().__init__(asset="keystone.brep", cutout=True)
