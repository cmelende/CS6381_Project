import numpy as np
import pandas as pd

from DataExploration.dexp import DataframeUtils, UniVariateAnalysis


class MergedResultFactory:
    def __init__(self, notifier_dfs: list[pd.DataFrame], pub_sub_dfs: list[pd.DataFrame]):
        if len(notifier_dfs) != len(pub_sub_dfs):
            raise Exception("You must have the same amount of dataframes")
        self.__pub_sub_dfs = pub_sub_dfs
        self.__notifier_dfs = notifier_dfs

    @staticmethod
    def __flatten_df(dataframe: pd.DataFrame) -> pd.Series:
        return DataframeUtils.flatten_df(dataframe)

    @staticmethod
    def __create_value_sub_count_type_df(index: int, flattened_df_series: pd.Series, type: str):
        number_of_tests = 1000
        # starting_index = index * number_of_tests
        flattened_df_series_count = flattened_df_series.shape[0]
        flattened_df_series_sub_count = int(flattened_df_series_count / number_of_tests)
        count_column: list[int] = [flattened_df_series_sub_count] * flattened_df_series_count
        type_column: list[str] = [type] * flattened_df_series_count
        t = {
            'latency': flattened_df_series,
            'subscriber_count': pd.Series(count_column),
            'type': pd.Series(type_column)
        }
        t_df = pd.DataFrame(t)
        t_df.index = np.arange(index, len(t_df) + index)
        return t_df

    def combine_dfs(self) -> pd.DataFrame:
        flattened_notifier_df_series_list = self.__get_flattened_df_series_list(self.__notifier_dfs)
        flattened_pub_sub_df_series_list = self.__get_flattened_df_series_list(self.__pub_sub_dfs)

        notifier_val_sub_count_type_df = self.__create_value_sub_count_type_dfs(flattened_notifier_df_series_list,
                                                                                "notifier")
        pub_sub_val_sub_count_type_df = self.__create_value_sub_count_type_dfs(flattened_pub_sub_df_series_list,
                                                                               "pub_sub")

        df_list: list[pd.DataFrame] = list[pd.DataFrame]()
        df_list.extend(notifier_val_sub_count_type_df)
        df_list.extend(pub_sub_val_sub_count_type_df)

        return pd.concat(df_list)

    def __create_value_sub_count_type_dfs(self, flattened_df_series_list: list[pd.Series], type_str: str) -> list[
        pd.DataFrame]:
        df_list: list[pd.DataFrame] = list[pd.DataFrame]()
        starting_df_index = 0
        for index, flattened_df_series in enumerate(flattened_df_series_list):
            t_df = self.__create_value_sub_count_type_df(starting_df_index, flattened_df_series, type_str)
            starting_df_index = starting_df_index + flattened_df_series.size
            df_list.append(t_df)
        return df_list

    def __get_flattened_df_series_list(self, dfs: list[pd.DataFrame]) -> list[pd.Series]:
        flattened_df_series_list: list[pd.Series] = list[pd.Series]()
        for df in dfs:
            flat_df = self.__flatten_df(df)
            flattened_df_series_list.append(flat_df)
        return flattened_df_series_list
