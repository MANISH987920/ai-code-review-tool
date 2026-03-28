def calculate_score(metrics_data, rules_data):
    score = 100

    score -= len(rules_data["unused_imports"]) * 5
    score -= len(rules_data["security_issues"]) * 20
    score -= len(rules_data["long_functions"]) * 5

    if metrics_data["complexity"] > 10:
        score -= (metrics_data["complexity"] - 10) * 2

    return max(score, 0)


def get_grade(score):
    if score >= 90:
        return "A"
    elif score >= 75:
        return "B"
    elif score >= 60:
        return "C"
    elif score >= 40:
        return "D"
    else:
        return "F"