"""Repository aggregator module."""
from . import Aggregator
from ..analyser import AnalyserType
from ..report import Report


class Repository(Aggregator):
    """Repository aggregator class."""

    @classmethod
    def get_type(cls) -> AnalyserType:
        """Returns analyser type of the aggregator."""
        return AnalyserType.REPOSITORY


    @classmethod
    def get_name(cls) -> str:
        """Returns aggregator name."""
        return "Packaging Aggregator"


    @classmethod
    def aggregate(cls, report: Report, results: dict):
        """Aggregates available analysis results.

        Args:
            report (Report): Analysis report.
            results (dict): Analyser results.
        """
        raise NotImplementedError
