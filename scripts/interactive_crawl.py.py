import asyncio
import yaml
import json
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
from crawl4ai.extraction_strategy import JsonCssExtractionStrategy

async def interactive_crawl(url: str):
    # Load configs
    with open("configs/browser.yml") as f:
        browser_cfg = BrowserConfig(**yaml.safe_load(f))
    crawler_params = yaml.safe_load(open("configs/crawler.yml"))
    schema = json.load(open("configs/css_schema.json"))
    extractor = JsonCssExtractionStrategy(schema)

    session_id = "hn_session"
    os.makedirs("data", exist_ok=True)

    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        # Step 1: Load initial page & wait for 30 items
        cfg1 = CrawlerRunConfig(
            session_id=session_id,
            extraction_strategy=extractor,
            **crawler_params
        )
        res1 = await crawler.arun(url=url, config=cfg1)
        print(f"Initial items: {len(res1.extracted_content)}")

        # Step 2: Scroll + click "More" and wait for >30 items
        js_steps = [
            "window.scrollTo(0, document.body.scrollHeight);",
            "document.querySelector('a.morelink')?.click();"
        ]
        wait_js = "js:() => document.querySelectorAll('.athing').length > 30"
        cfg2 = CrawlerRunConfig(
            session_id=session_id,
            js_code=js_steps,
            wait_for=wait_js,
            js_only=True,
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=extractor
        )
        res2 = await crawler.arun(url=url, config=cfg2)
        print(f"After load-more: {len(res2.extracted_content)}")

    # Dump final JSON
    with open("data/interactive_output.json", "w") as fout:
        json.dump(res2.extracted_content, fout, indent=2)
    print("✅ Interactive data saved to data/interactive_output.json")

if __name__ == "__main__":
    asyncio.run(interactive_crawl("https://news.ycombinator.com"))
