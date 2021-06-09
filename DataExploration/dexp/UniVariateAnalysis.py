import pandas as pd


class UniVariateAnalysis:

    def __init__(self, series: pd.Series):
        self.Series = series

    def get_count(self):
        return self.Series.shape[0]

    def get_q1(self):
        return self.Series.quantile(.25)

    def get_q2(self):
        return self.Series.quantile(.5)

    def get_q3(self):
        return self.Series.quantile(.75)

    def get_q4(self):
        return self.Series.quantile(1)

    def get_iqr(self):
        return self.get_q3() - self.get_q1()

    def get_min(self):
        return self.Series.min()

    def get_median(self):
        return self.Series.median()

    def get_max(self):
        return self.Series.max()

    def get_data_type(self):
        return self.Series.dtypes

    def get_mode(self):
        return self.Series.mode()

    # def get_lower_outlier_rows(self):
    #     return self.DataFrame.loc[(self.DataFrame[self.ColumnName] < self.get_lower_whisker_value())]

    def get_lower_whisker_value(self):
        return self.get_q1() - ((3 / 2) * self.get_iqr())

    # def get_higher_outlier_rows(self):
    #     return self.DataFrame.loc[(self.DataFrame[self.ColumnName] > self.get_higher_whisker_value())]

    def get_higher_whisker_value(self):
        return self.get_q3() + ((3 / 2) * self.get_iqr())

    def get_std(self):
        return self.Series.std()

    def get_mean(self):
        return self.Series.mean()
