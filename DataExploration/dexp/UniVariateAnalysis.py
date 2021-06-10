import pandas as pd

from DataExploration.dexp.StatisticsBase import StatisticsBase


class UniVariateAnalysis(StatisticsBase):

    def __init__(self, series: pd.Series):
        super().__init__(series)
