"""A holder for the Jet KVM device."""

from .import_feature import ImportFeature


class JetKVM(ImportFeature):
    """
    A holder feature for a Jet KVM.
    """

    def __init__(self) -> None:
        super().__init__(asset="jetkvm_trimmed.brep", cutout=True)
