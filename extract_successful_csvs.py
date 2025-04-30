import json
from create_results_html import format_markdown
from evaluator import Reason
from main import load_saved_runs


def main():
    # models = ["openrouter/meta-llama/llama-3.3-70b-instruct"]
    models = [
        "openrouter/anthropic/claude-3.7-sonnet",
        "openrouter/meta-llama/llama-3.1-8b-instruct",
    ]
    data = {}
    for model in models:
        kvs = load_saved_runs(
            "/home/cadegord/projects/yet-another-applied-llm-benchmark/results/45070ee7e6a3998bc3796c0b03462104a7e05737",
            model.replace("/", "-"),
        )
        data[model] = {}
        for k, v in kvs.items():
            data[model][k] = v

    # stealing from create_results_html.py
    reasons = {key: {k1: v1[1] for k1,v1 in value.items()} for key, value in data.items()}
    data = {key: {k1: v1[0] for k1,v1 in value.items()} for key, value in data.items()}

    for k in reasons:
        for k1 in reasons[k]:
            for i in range(len(reasons[k][k1])):
                if isinstance(reasons[k][k1][i], Reason):
                    fmt = format_markdown(reasons[k][k1][i])
                    while '\n\n' in fmt:
                        fmt = fmt.replace('\n\n', '\n')
                    fmt = fmt.replace("\n#", "\n\n#")
                    # model, test, iteration -> reason
                    reasons[k][k1][i] = fmt

    successful_csvs = {}
    for model in data:
        successful_csvs[model] = {}
        for test in data[model]:
            successful_csvs[model][test] = []
            for iteration in data[model][test]:
                if data[model][test][iteration]:
                    reason = reasons[model][test][iteration]
                    search_str = "And got the output:\n```"
                    start = reason.find(search_str)
                    reason = reason[start+len(search_str):]
                    end = reason.find("```")
                    reason = reason[:end]
                    successful_csvs[model][test].append(reason)

    with open("successful_csvs.json", "w") as f:
        json.dump(successful_csvs, f)

if __name__ == "__main__":
    main()
