import re

def main():
    file_path = "static/index.html"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    # Find the saveEvaluation function block
    pattern = r'(async function saveEvaluation\(\) \{.*?if \(\!emp\.learning_topics\) emp\.learning_topics = new Array\(competencies\.length\)\.fill\(\'\'\);)(.*?)(            // Update evaluation status)'
    
    match = re.search(pattern, content, flags=re.DOTALL)
    if not match:
        print("Could not find the target block in saveEvaluation.")
        return

    new_loop = """
            if (!emp.self_evals) emp.self_evals = [];
            if (!emp.actuals) emp.actuals = [];
            if (!emp.before_evals) emp.before_evals = [];
            if (!emp.supervisor_feedback) emp.supervisor_feedback = [];
            if (!emp.evidences) emp.evidences = [];

            for (let i = 0; i < competencies.length; i++) {
                // Self Eval
                const elSelf = document.getElementById(`eval-self-${id}-${i}`);
                if (elSelf) {
                    let v = parseInt(elSelf.value, 10);
                    emp.self_evals[i] = isNaN(v) ? null : v;
                } else if (emp.self_evals[i] === undefined) {
                    emp.self_evals[i] = null;
                }

                // Actual Eval
                const elActual = document.getElementById(`eval-actual-${id}-${i}`);
                if (elActual) {
                    let v = parseInt(elActual.value, 10);
                    emp.actuals[i] = isNaN(v) ? null : v;
                } else if (emp.actuals[i] === undefined) {
                    emp.actuals[i] = null;
                }

                // Before Eval
                const elBefore = document.getElementById(`eval-before-${id}-${i}`);
                if (elBefore) {
                    let v = parseInt(elBefore.value, 10);
                    emp.before_evals[i] = isNaN(v) ? null : v;
                } else if (emp.before_evals[i] === undefined) {
                    emp.before_evals[i] = null;
                }

                // Feedback
                const elFeedback = document.getElementById(`eval-feedback-${id}-${i}`);
                if (elFeedback) {
                    emp.supervisor_feedback[i] = elFeedback.value;
                } else if (emp.supervisor_feedback[i] === undefined) {
                    emp.supervisor_feedback[i] = "";
                }

                // Evidence, Additional Expectations, Learning Topics
                const elEvi = document.getElementById(`eval-evi-${i}`);
                const elAddExp = document.getElementById(`eval-add-exp-${i}`);
                const elLrnTop = document.getElementById(`eval-lrn-top-${i}`);

                if (elEvi) emp.evidences[i] = elEvi.value;
                else if (emp.evidences[i] === undefined) emp.evidences[i] = "";

                if (elAddExp) emp.additional_expectations[i] = elAddExp.value;
                else if (emp.additional_expectations[i] === undefined) emp.additional_expectations[i] = "";

                if (elLrnTop) emp.learning_topics[i] = elLrnTop.value;
                else if (emp.learning_topics[i] === undefined) emp.learning_topics[i] = "";
            }

"""

    new_content = content[:match.start(2)] + new_loop + content[match.end(2):]
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    
    print("Successfully patched static/index.html")
    
    # Also attempt to patch build_frontend.py if it contains the old string
    build_path = "build_frontend.py"
    try:
        with open(build_path, "r", encoding="utf-8") as f:
            bcontent = f.read()
        
        bpattern = r'(if \(\!emp\.learning_topics\) emp\.learning_topics = new Array\(competencies\.length\)\.fill\(\'\'\);\\n)(.*?)(\\n            // Update evaluation status)'
        bmatch = re.search(bpattern, bcontent, flags=re.DOTALL)
        if bmatch:
            escaped_new_loop = new_loop.replace('`', '\\`').replace('$', '\\$')
            bnew_content = bcontent[:bmatch.start(2)] + escaped_new_loop + bcontent[bmatch.end(2):]
            with open(build_path, "w", encoding="utf-8") as f:
                f.write(bnew_content)
            print("Successfully patched build_frontend.py")
    except Exception as e:
        print(f"Failed to patch build_frontend.py: {e}")

if __name__ == "__main__":
    main()
