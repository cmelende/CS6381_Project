from DataExploration.dexp import UniVariateAnalysis


class LatencyMeasurement:
    def __init__(self, analysis: UniVariateAnalysis):
        self.__analysis = analysis
        self.Mode = self.__analysis.get_mode()
        self.SubCount = self.__analysis.get_count()/1000
        self.Q1 = self.__analysis.get_q1()
        self.Q2 = self.__analysis.get_q2()
        self.Q3 = self.__analysis.get_q3()
        self.Q4 = self.__analysis.get_q4()
        self.Median = self.__analysis.get_median()

    def print(self):
        print(f'mode: {self.Mode}')
        print(f'count(subs): {self.SubCount}')
        print(f'Q1: {self.Q1}')
        print(f'Median: {self.Median}')
        print(f'Q3: {self.Q3}')
