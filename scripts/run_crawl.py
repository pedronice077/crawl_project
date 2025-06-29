import subprocess
import os

def run_crawl(target_url: str):
    configs = {
        "browser": "configs/browser.yml",
        "crawler": "configs/crawler.yml",
        "extractor": "configs/extract_css.yml",
        "schema": "configs/css_schema.json",
        "output": "data/output.json"
    }

    os.makedirs(os.path.dirname(configs["output"]), exist_ok=True)
    cmd = [
        "crwl", target_url,
        "-B", configs["browser"],
        "-C", configs["crawler"],
        "-e", configs["extractor"],
        "-s", configs["schema"],
        "-o", configs["output"],
        "-v"
    ]

    print("🚀 Running static crawl...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Saved to", configs["output"])
    else:
        print("❌ Error during crawl:")
        print(result.stderr)

if __name__ == "__main__":
    # Example target; swap in your URL
    run_crawl("https://news.ycombinator.com")
