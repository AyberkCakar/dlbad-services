import pandas as pd
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots

with open('result.json', 'r') as file:
    data = json.load(file)


def parse_data(data):
    algorithm_settings = data['algorithm_settings']
    results = []

    for setting in algorithm_settings:
        setting_name = setting['algorithmSettingName']
        algorithms = setting['algorithm_results']

        for algo in algorithms:
            algo_name = algo['algorithm']['algorithmName']
            result = algo['result']

            if result:
                formatted_result = {
                    'Algorithm Setting Name': setting_name,
                    'Algorithm Name': algo_name,
                    'F1 Score': result.get('f1', 'N/A'),
                    'Recall': result.get('recall', 'N/A'),
                    'Accuracy': result.get('accuracy', 'N/A'),
                    'Precision': result.get('precision', 'N/A')
                }
                results.append(formatted_result)

    return results


formatted_results = parse_data(data["data"])
df = pd.DataFrame(formatted_results)


def plot_interactive_graphs(df):
    metrics = ['F1 Score', 'Recall', 'Accuracy', 'Precision']
    algorithm_names = df['Algorithm Name'].unique()

    colors = [
        '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
        '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
        '#1f77b4', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5',
        '#c49c94', '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5'
    ]
    color_map = {algo: colors[i % len(colors)] for i, algo in enumerate(algorithm_names)}

    fig = make_subplots(rows=4, cols=1, subplot_titles=metrics, shared_xaxes=True)
    for i, metric in enumerate(metrics):
        for algo in algorithm_names:
            algo_data = df[df['Algorithm Name'] == algo]
            fig.add_trace(
                go.Scatter(
                    x=algo_data['Algorithm Setting Name'],
                    y=algo_data[metric],
                    mode='lines+markers',
                    name=algo,
                    legendgroup=algo,
                    showlegend=True if i == 0 else False,
                    line=dict(color=color_map[algo])
                ),
                row=i + 1, col=1
            )

    fig.update_layout(height=1200, width=1600, title_text="Algorithm Performance Metrics", showlegend=True)
    fig.show()


plot_interactive_graphs(df)
