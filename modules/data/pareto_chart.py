import pandas as pd
from matplotlib import pyplot as plt

class ParetoChart():
    def __init__(self, df: pd.DataFrame):
        self.df = df

        self.failures = ['High'
                         , 'High-Right'
                         , 'Right'
                         , 'Low-Right'
                         , 'Low'
                         , 'Low-Left'
                         , 'Left'
                         , 'High-Left'
                         , 'Chain Out'
                         , 'Foot Fault']
        self.total_failures = {}
        self.percent_failures = []
        self.total_misses = 0
        self.cumulative_percent = []

        self.execute()

    def execute(self):
        self.create_failures()
        self.create_total_misses()
        self.create_cumulative_percent()

    def create_failures(self):
        total_failures = {x: int(self.df[x].sum()) for x in self.failures}
        total_failures.sort(reverse=True)
        self.total_failures = total_failures

    def create_total_misses(self):
        for x in self.total_failures:
            self.total_misses += x

    def create_cumulative_percent(self):
        self.percent_failures = [(x / self.total_misses) * 100 for x in self.total_failures]
        for x, i in enumerate(self.percent_failures):
            if x == 0:
                self.cumulative_percent.append(i)
            else:
                self.cumulative_percent.append(i + self.cumulative_percent[x-1])

    def create_pareto_chart(self):
        fig = plt.figure(figsize=(10,5))
        plot_points = [x for x in range(len(self.failures))]
        plt.bar(plot_points, self.percent_failures)
        plt.plot(plot_points, self.cumulative_percent, color='red', marker='o')
        for x in plot_points:
            plt.annotate(str(round(self.percent_failures[x], 1)), (x, self.percent_failures[x]))
            plt.annotate(str(round(self.cumulative_percent[x], 1)), (x, self.cumulative_percent[x]))
        plt.xticks(plot_points, labels=self.failures)
        return fig