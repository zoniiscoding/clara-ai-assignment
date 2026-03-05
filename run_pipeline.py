import subprocess

print("Step 1: Extracting demo call information...")
subprocess.run(["py", "scripts/extract_demo.py"])

print("Step 2: Generating agent configurations...")
subprocess.run(["py", "scripts/generate_agent.py"])

print("Step 3: Creating review tasks...")
subprocess.run(["py", "scripts/create_tasks.py"])

print("Step 4: Processing onboarding updates...")
subprocess.run(["py", "scripts/update_agent.py"])

print("Step 5: Generating diff reports...")
subprocess.run(["py", "scripts/diff_viewer.py"])

print("Step 6: Generating summary metrics...")
subprocess.run(["py", "scripts/metrics.py"])

print("Pipeline completed successfully.")