import decimal

import pandas as pd

from DataExploration.dexp import UniVariateAnalysis


class StatisticsReport:
    def __init__(self, dataframes: list[pd.DataFrame]):
        self.__dataframes = dataframes

    @staticmethod
    def flatten_df(dataframe: pd.DataFrame) -> pd.Series:
        values = []
        dataframe_columns = list(dataframe)
        counter = 0
        number_of_rows = dataframe.shape[0]
        while counter < number_of_rows:
            for col in dataframe_columns:
                values.append(dataframe[col][counter])
                # print(df[col][counter])
            counter = counter + 1
        return pd.Series(values)

    def create_dataframe(self) -> pd.DataFrame:
        # q1
        q1_list: list[decimal] = list[decimal]()
        q2_list: list[decimal] = list[decimal]()
        q3_list: list[decimal] = list[decimal]()
        q4_list: list[decimal] = list[decimal]()
        median_list: list[decimal] = list[decimal]()
        std_dev_list: list[decimal] = list[decimal]()
        mode_list = []
        for df in self.__dataframes:
            series = StatisticsReport.flatten_df(df)
            analysis = UniVariateAnalysis(series)
            q1_list.append(analysis.get_q1())
            q2_list.append(analysis.get_q2())
            q3_list.append(analysis.get_q3())
            q4_list.append(analysis.get_q4())
            std_dev_list.append(analysis.get_std())
            median_list.append(analysis.get_median())
            modes = analysis.get_mode()
            mode_strings: list[str] = list[str]()
            for m in modes:
                mode_strings.append(str(m))

            mode_string = ",".join(mode_strings)
            mode_list.append(mode_string)

        q1_series = pd.Series(q1_list)
        q2_series = pd.Series(q2_list)
        q3_series = pd.Series(q3_list)
        q4_series = pd.Series(q4_list)
        std_dev_series = pd.Series(std_dev_list)
        median_series = pd.Series(median_list)
        mode_series = pd.Series(mode_list)
        sub_count: list[int] = list[int]()
        for i in range(0, len(self.__dataframes)):
            sub_count.append(2 ** (i+1))
        sub_count_series = pd.Series(sub_count)

        t = {
            'sub_count': sub_count_series,
            'Q1': q1_series,
            'Q2': q2_series,
            'Q3': q3_series,
            'Q4': q4_series,
            'Standard Deviation': std_dev_series,
            'Median': median_series,
            'Mode': mode_series
        }

        t_df = pd.DataFrame(t)
        return t_df
