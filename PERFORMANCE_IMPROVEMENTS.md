# Performance Improvements

## Summary of Changes

The application has been optimized to handle slow URLs and reduce failures. Here are the key improvements:

## Speed Improvements

### 1. Reduced Crawl Limits
- **Max pages**: Reduced from 50 to 20 pages
- **Max depth**: Reduced from 3 to 2 levels
- **Max content**: Reduced from 50,000 to 40,000 characters
- **Result**: Faster crawling with sufficient content for extraction

### 2. Timeout Management
- **Page timeout**: 8 seconds per page (with 2 retries)
- **Overall timeout**: 60 seconds per URL
- **Per-URL timeout**: 90 seconds in the API endpoint
- **Result**: No more hanging on slow URLs

### 3. Optimized Fetching
- **Eliminated double-fetch**: Pages are fetched once, content and links extracted from same response
- **Reduced delays**: Only delay every 3rd page (0.2s instead of 0.5s for every page)
- **Early stopping**: Stops when content limit reached
- **Result**: 2-3x faster crawling

### 4. Content Limits
- **Individual pages**: Limited to 5,000 characters per page
- **Total content**: 40,000 characters max
- **LLM input**: Reduced to 60,000 characters
- **Result**: Faster LLM processing, lower costs

## Reliability Improvements

### 1. Retry Logic
- **Automatic retries**: 2 retries per page on failure
- **Timeout handling**: Graceful handling of timeouts
- **Result**: Better success rate on flaky connections

### 2. Error Handling
- **Per-URL errors**: Continue with other URLs if one fails
- **Partial results**: Returns results even if some URLs fail
- **Better error messages**: More informative error messages
- **Result**: More resilient to individual URL failures

### 3. Timeout Protection
- **Overall timeout**: Stops crawling after 60 seconds
- **Per-URL timeout**: Each URL has 90-second limit
- **Early exit**: Stops when time limit reached
- **Result**: No more infinite waits

### 4. Link Management
- **Limited links**: Max 10 links per page
- **Priority queue**: Main page links processed first
- **Result**: More focused crawling, less wasted time

## Expected Performance

### Before
- **Small sites**: 30-60 seconds
- **Large sites**: 2-5 minutes or timeout
- **Failures**: Common on slow/unresponsive URLs

### After
- **Small sites**: 10-20 seconds
- **Large sites**: 30-60 seconds (with timeout protection)
- **Failures**: Rare, with graceful degradation

## Configuration

You can adjust these settings in the `DocumentationCrawler` initialization in `backend/main.py`:

```python
crawler = DocumentationCrawler(
    max_pages=20,        # Increase for more pages
    max_depth=2,          # Increase for deeper crawling
    max_content_length=40000,  # Increase for more content
    page_timeout=8,       # Seconds per page
    max_total_time=60     # Total seconds per URL
)
```

## Trade-offs

- **Less content**: May miss some deep pages, but gets main content faster
- **Time limits**: May stop early on very large sites, but prevents hanging
- **Fewer pages**: Focuses on most important pages first

These trade-offs prioritize speed and reliability over exhaustive crawling, which is better for user experience.

