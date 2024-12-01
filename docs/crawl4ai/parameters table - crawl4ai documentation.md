# Parameter Reference Table

| File Name | Parameter Name | Code Usage | Strategy/Class | Description |
| --- | --- | --- | --- | --- |
| async\_crawler\_strategy.py | user\_agent | `kwargs.get("user_agent")` | AsyncPlaywrightCrawlerStrategy | User agent string for browser identification |
| async\_crawler\_strategy.py | proxy | `kwargs.get("proxy")` | AsyncPlaywrightCrawlerStrategy | Proxy server configuration for network requests |
| async\_crawler\_strategy.py | proxy\_config | `kwargs.get("proxy_config")` | AsyncPlaywrightCrawlerStrategy | Detailed proxy configuration including auth |
| async\_crawler\_strategy.py | headless | `kwargs.get("headless", True)` | AsyncPlaywrightCrawlerStrategy | Whether to run browser in headless mode |
| async\_crawler\_strategy.py | browser\_type | `kwargs.get("browser_type", "chromium")` | AsyncPlaywrightCrawlerStrategy | Type of browser to use (chromium/firefox/webkit) |
| async\_crawler\_strategy.py | headers | `kwargs.get("headers", {})` | AsyncPlaywrightCrawlerStrategy | Custom HTTP headers for requests |
| async\_crawler\_strategy.py | verbose | `kwargs.get("verbose", False)` | AsyncPlaywrightCrawlerStrategy | Enable detailed logging output |
| async\_crawler\_strategy.py | sleep\_on\_close | `kwargs.get("sleep_on_close", False)` | AsyncPlaywrightCrawlerStrategy | Add delay before closing browser |
| async\_crawler\_strategy.py | use\_managed\_browser | `kwargs.get("use_managed_browser", False)` | AsyncPlaywrightCrawlerStrategy | Use managed browser instance |
| async\_crawler\_strategy.py | user\_data\_dir | `kwargs.get("user_data_dir", None)` | AsyncPlaywrightCrawlerStrategy | Custom directory for browser profile data |
| async\_crawler\_strategy.py | session\_id | `kwargs.get("session_id")` | AsyncPlaywrightCrawlerStrategy | Unique identifier for browser session |
| async\_crawler\_strategy.py | override\_navigator | `kwargs.get("override_navigator", False)` | AsyncPlaywrightCrawlerStrategy | Override browser navigator properties |
| async\_crawler\_strategy.py | simulate\_user | `kwargs.get("simulate_user", False)` | AsyncPlaywrightCrawlerStrategy | Simulate human-like behavior |
| async\_crawler\_strategy.py | magic | `kwargs.get("magic", False)` | AsyncPlaywrightCrawlerStrategy | Enable advanced anti-detection features |
| async\_crawler\_strategy.py | log\_console | `kwargs.get("log_console", False)` | AsyncPlaywrightCrawlerStrategy | Log browser console messages |
| async\_crawler\_strategy.py | js\_only | `kwargs.get("js_only", False)` | AsyncPlaywrightCrawlerStrategy | Only execute JavaScript without page load |
| async\_crawler\_strategy.py | page\_timeout | `kwargs.get("page_timeout", 60000)` | AsyncPlaywrightCrawlerStrategy | Timeout for page load in milliseconds |
| async\_crawler\_strategy.py | ignore\_body\_visibility | `kwargs.get("ignore_body_visibility", True)` | AsyncPlaywrightCrawlerStrategy | Process page even if body is hidden |
| async\_crawler\_strategy.py | js\_code | `kwargs.get("js_code", kwargs.get("js", self.js_code))` | AsyncPlaywrightCrawlerStrategy | Custom JavaScript code to execute |
| async\_crawler\_strategy.py | wait\_for | `kwargs.get("wait_for")` | AsyncPlaywrightCrawlerStrategy | Wait for specific element/condition |
| async\_crawler\_strategy.py | process\_iframes | `kwargs.get("process_iframes", False)` | AsyncPlaywrightCrawlerStrategy | Extract content from iframes |
| async\_crawler\_strategy.py | delay\_before\_return\_html | `kwargs.get("delay_before_return_html")` | AsyncPlaywrightCrawlerStrategy | Additional delay before returning HTML |
| async\_crawler\_strategy.py | remove\_overlay\_elements | `kwargs.get("remove_overlay_elements", False)` | AsyncPlaywrightCrawlerStrategy | Remove pop-ups and overlay elements |
| async\_crawler\_strategy.py | screenshot | `kwargs.get("screenshot")` | AsyncPlaywrightCrawlerStrategy | Take page screenshot |
| async\_crawler\_strategy.py | screenshot\_wait\_for | `kwargs.get("screenshot_wait_for")` | AsyncPlaywrightCrawlerStrategy | Wait before taking screenshot |
| async\_crawler\_strategy.py | semaphore\_count | `kwargs.get("semaphore_count", 5)` | AsyncPlaywrightCrawlerStrategy | Concurrent request limit |
| async\_webcrawler.py | verbose | `kwargs.get("verbose", False)` | AsyncWebCrawler | Enable detailed logging |
| async\_webcrawler.py | warmup | `kwargs.get("warmup", True)` | AsyncWebCrawler | Initialize crawler with warmup request |
| async\_webcrawler.py | session\_id | `kwargs.get("session_id", None)` | AsyncWebCrawler | Session identifier for browser reuse |
| async\_webcrawler.py | only\_text | `kwargs.get("only_text", False)` | AsyncWebCrawler | Extract only text content |
| async\_webcrawler.py | bypass\_cache | `kwargs.get("bypass_cache", False)` | AsyncWebCrawler | Skip cache and force fresh crawl |

* * *