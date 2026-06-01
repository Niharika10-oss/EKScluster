import os
import sys
from google import genai
from google.genai import types

def analyze_logs(log_file_path):
    # 1. Initialize the Gemini Client
    # It automatically looks for the GEMINI_API_KEY environment variable
    client = genai.Client()
    
    if not os.path.exists(log_file_path):
        print(f"Error: Log file {log_file_path} not found.")
        return

    # 2. Read the failed deployment or Terraform logs
    with open(log_file_path, "r", encoding="utf-8") as f:
        log_content = f.read()

    # Keep only the last 100 lines to save tokens and focus on the actual crash
    log_tail = "\n".join(log_content.splitlines()[-100:])

    prompt = f"""
    You are an expert AWS DevOps and Platform Engineer. 
    The following cloud infrastructure pipeline execution failed. 
    Analyze the tail end of these logs and provide:
    1. A clear, 1-sentence summary of the root cause.
    2. The exact commands or file updates needed to fix it.

    Failed Pipeline Logs:
    \"\"\"
    {log_tail}
    \"\"\"
    """

    print("\n🚀 [AI Engine] Analyzing cloud deployment failure logs via Gemini...")
    
    try:
        # 3. Call the model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        
        print("\n💡 [AI Diagnosis & Remediation Plan]:")
        print("="*60)
        print(response.text)
        print("="*60)

    except Exception as e:
        print(f"Failed to communicate with Gemini API: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python cloud_diagnoser.py <path_to_log_file>")
    else:
        analyze_logs(sys.argv[1])
