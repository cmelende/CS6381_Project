import pandas as pd

from DataExploration.dexp import UniVariateAnalysis


class DataframeUtils:
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
            counter = counter + 1
        return pd.Series(values)

    @staticmethod
    def create_median_dataframe(dataframes: list[pd.DataFrame], type_str: str, mode_str: str) -> pd.DataFrame:
        mean_or_mode_list = []
        sub_count_list = []
        type_list = []
        for df in dataframes:
            flattened_series: pd.Series = DataframeUtils.flatten_df(df)
            analysis = UniVariateAnalysis(flattened_series)
            if mode_str == 'median':
                median_or_mode = analysis.get_median()
            else:
                median_or_mode = analysis.get_mean()
            series_count = flattened_series.shape[0]
            sub_count_list.append(series_count/1000)
            type_list.append(type_str)
            mean_or_mode_list.append(median_or_mode)
        if mode_str == 'median':
            t = {
                'median': pd.Series(mean_or_mode_list),
                'subscriber_count': pd.Series(sub_count_list),
                'type': pd.Series(type_list)
            }
        else:
            t = {
                'mean': pd.Series(mean_or_mode_list),
                'subscriber_count': pd.Series(sub_count_list),
                'type': pd.Series(type_list)
            }
        t_df = pd.DataFrame(t)
        return t_df

    @staticmethod
    def create_median_dataframes(notifier_dfs: list[pd.DataFrame], pub_sub_dfs: list[pd.DataFrame], mode_str: str) \
            -> pd.DataFrame:
        notifier_median_dataframe = DataframeUtils.create_median_dataframe(notifier_dfs, "notifier", mode_str)

        pub_sub_median_dataframe = DataframeUtils.create_median_dataframe(pub_sub_dfs, "pub_sub", mode_str)
        notifier_median_dataframe.index = range(notifier_median_dataframe.shape[0],
                                                notifier_median_dataframe.shape[0] + pub_sub_median_dataframe.shape[0])

        t_df = pd.DataFrame()
        df = t_df.append(notifier_median_dataframe)
        df = df.append(pub_sub_median_dataframe)
        return df
