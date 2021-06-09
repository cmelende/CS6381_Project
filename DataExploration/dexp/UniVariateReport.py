from DataExploration.dexp import UniVariateAnalysis


class UniVariateReport:
    def __init__(self, uni_variate_analysis: UniVariateAnalysis):
        self.__analysis: UniVariateAnalysis = uni_variate_analysis

    def print_quartiles(self):
        print(f"Q1: {self.__analysis.get_q1()}")
        print(f"Q2: {self.__analysis.get_q2()}")
        print(f"Q3: {self.__analysis.get_q3()}")
        print(f"Q4: {self.__analysis.get_q4()}")
        print(f"Mean: {self.__analysis.get_mean()}")
        print(f"Min: {self.__analysis.get_min()}")
        print(f"Median: {self.__analysis.get_median()}")
        print(f"Max: {self.__analysis.get_max()}")

    def print_whiskers(self):
        print(f"Top whisker: {self.__analysis.get_higher_whisker_value()}")
        print(f"Bottom whisker: {self.__analysis.get_lower_whisker_value()}")

    def print_data_type(self):
        print(f"Data type: {self.__analysis.get_data_type()}")

    def print_value_range(self):
        print(f'Range of values: ({self.__analysis.get_min()}, {self.__analysis.get_max()})')

    def print_std(self):
        print(f"Standard deviation: {self.__analysis.get_std()}")

    def print_report(self):
        self.print_data_type()
        self.print_value_range()
        self.print_std()
        self.print_quartiles()
        self.print_whiskers()
