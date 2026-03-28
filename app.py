import streamlit as st
import pandas as pd

from analyzer.parser import parse_code
from analyzer.metrics import analyze_metrics
from analyzer.rules import analyze_rules
from analyzer.scoring import calculate_score, get_grade

st.set_page_config(page_title="AI Code Review Tool", layout="wide")

st.title("🔥 AI Code Review Tool")
st.markdown("Upload multiple Python files to analyze full project quality.")

uploaded_files = st.file_uploader(
    "Upload Python Files",
    type=["py"],
    accept_multiple_files=True
)

if uploaded_files:

    project_scores = []
    chart_data = []
    file_results = []

    for uploaded_file in uploaded_files:

        file_name = uploaded_file.name
        code = uploaded_file.read().decode("utf-8")
        tree = parse_code(code)

        if tree is None:
            st.error(f"Syntax Error in {file_name}")
            continue

        metrics_data = analyze_metrics(tree, code)
        rules_data = analyze_rules(tree)
        score = calculate_score(metrics_data, rules_data)
        grade = get_grade(score)

        project_scores.append(score)

        chart_data.append({
            "File": file_name,
            "Score": score
        })

        file_results.append({
            "file_name": file_name,
            "code": code,
            "score": score,
            "grade": grade,
            "metrics": metrics_data,
            "rules": rules_data
        })

    if project_scores:

        overall_score = sum(project_scores) // len(project_scores)
        overall_grade = get_grade(overall_score)

        st.subheader("📊 Project Overview")

        col1, col2 = st.columns(2)
        col1.metric("Overall Score", overall_score)
        col2.metric("Overall Grade", overall_grade)

        st.progress(overall_score)

        st.divider()

        st.subheader("📈 Score Comparison")
        df = pd.DataFrame(chart_data)
        st.bar_chart(df.set_index("File"))

        st.divider()

        st.subheader("📁 Detailed File Analysis")

        for result in file_results:

            with st.expander(f"📄 {result['file_name']} (Grade: {result['grade']})"):

                col1, col2, col3, col4 = st.columns(4)
                col1.metric("Score", result["score"])
                col2.metric("Lines", result["metrics"]["total_lines"])
                col3.metric("Functions", result["metrics"]["functions"])
                col4.metric("Complexity", result["metrics"]["complexity"])

                st.markdown("### 🔎 Issues")

                if result["rules"]["unused_imports"]:
                    st.warning(f"Unused Imports: {result['rules']['unused_imports']}")
                else:
                    st.success("No unused imports")

                if result["rules"]["long_functions"]:
                    st.warning(f"Long Functions: {result['rules']['long_functions']}")
                else:
                    st.success("No long functions")

                if result["rules"]["security_issues"]:
                    for issue in result["rules"]["security_issues"]:
                        st.error(issue)
                else:
                    st.success("No major security issues")

                st.markdown("### 📝 Code Preview")
                st.code(result["code"], language="python")
                