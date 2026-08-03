import sys

for fp in ['index_render.html', 'static/index.html']:
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    # We need to inject setupAddEmployeeCascadingDropdowns(); into openAddEmployeeModal()
    # Let's find openAddEmployeeModal and replace it if not already injected
    target = "function openAddEmployeeModal() {"
    
    # Check if we already injected it right after
    injection = "setupAddEmployeeCascadingDropdowns();"
    
    # Split content by the target
    parts = content.split(target)
    
    if len(parts) > 1:
        # Check if the next part starts with our injection
        if injection not in parts[1][:200]:
            # Inject it
            new_content = parts[0] + target + "\n              " + injection + parts[1]
            with open(fp, 'w', encoding='utf-8') as f:
                f.write(new_content)
                print(f"Injected into {fp}")
        else:
            print(f"Already injected into {fp}")
    else:
        print(f"Could not find openAddEmployeeModal in {fp}")
