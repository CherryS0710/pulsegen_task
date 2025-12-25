from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
from typing import List
import os
import asyncio
from pathlib import Path
from dotenv import load_dotenv

from services.crawler import DocumentationCrawler
from services.extractor import ModuleExtractor

# Load .env from project root (parent directory)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

app = FastAPI(title="Module Extraction API", version="1.0.0")

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ExtractRequest(BaseModel):
    urls: List[str]


class ExtractResponse(BaseModel):
    modules: List[dict]


@app.get("/")
async def root():
    return {"message": "Module Extraction API", "status": "running"}


@app.post("/extract", response_model=ExtractResponse)
async def extract_modules(request: ExtractRequest):
    """
    Extract product modules from documentation URLs.
    
    Accepts a list of documentation URLs, crawls the content,
    and returns structured module information.
    """
    if not request.urls:
        raise HTTPException(status_code=400, detail="At least one URL is required")
    
    try:
        # Initialize services
        crawler = DocumentationCrawler()
        try:
            extractor = ModuleExtractor()
        except ValueError as e:
            if "OPENAI_API_KEY" in str(e):
                raise HTTPException(
                    status_code=500,
                    detail="OpenAI API key not configured. Please set OPENAI_API_KEY in your .env file. See README.md for setup instructions."
                )
            raise
        
        # Crawl and collect content from all URLs with timeout
        all_content = []
        processed_urls = []
        failed_urls = []
        
        for url in request.urls:
            try:
                print(f"Processing URL: {url}")
                # Add timeout for each URL crawl
                content = await asyncio.wait_for(
                    crawler.crawl_documentation(url),
                    timeout=90  # 90 seconds per URL
                )
                if content:  # Only add if we got content
                    all_content.append({
                        "url": url,
                        "content": content
                    })
                    processed_urls.append(url)
                    print(f"Successfully processed {url} ({len(content)} chars)")
                else:
                    print(f"Warning: No content extracted from {url}")
                    failed_urls.append(url)
            except asyncio.TimeoutError:
                print(f"Timeout crawling {url} (exceeded 90s)")
                failed_urls.append(url)
                # Try to continue with other URLs
                continue
            except Exception as e:
                # Log error but continue with other URLs
                print(f"Error crawling {url}: {str(e)}")
                failed_urls.append(url)
                continue
        
        print(f"Processed {len(processed_urls)} URL(s) successfully, {len(failed_urls)} failed")
        
        if not all_content:
            raise HTTPException(
                status_code=500,
                detail="Failed to crawl any of the provided URLs. They may be inaccessible, require authentication, or timed out."
            )
        
        # Extract modules per URL (separate extraction for each URL)
        all_modules_by_url = []
        
        print(f"\n=== Processing URLs Separately ===")
        print(f"Total URLs processed: {len(processed_urls)}")
        
        for item in all_content:
            url = item['url']
            content = item['content']
            
            print(f"\nExtracting modules from: {url}")
            print(f"Content length: {len(content)} characters")
            
            # Extract modules for this specific URL
            try:
                modules_for_url = await extractor.extract_modules([item])
                
                if modules_for_url:
                    print(f"  ✓ Extracted {len(modules_for_url)} module(s) from {url}")
                    all_modules_by_url.append({
                        "url": url,
                        "modules": modules_for_url
                    })
                else:
                    print(f"  ⚠ No modules extracted from {url}")
                    all_modules_by_url.append({
                        "url": url,
                        "modules": []
                    })
            except Exception as e:
                print(f"  ✗ Error extracting from {url}: {str(e)}")
                all_modules_by_url.append({
                    "url": url,
                    "modules": []
                })
        
        print(f"\n=== Summary ===")
        total_modules = sum(len(item['modules']) for item in all_modules_by_url)
        print(f"Total modules across all URLs: {total_modules}")
        for item in all_modules_by_url:
            print(f"  - {item['url']}: {len(item['modules'])} modules")
        print(f"================\n")
        
        # Return modules with URL information
        # Format: [{"url": "...", "modules": [...]}, ...]
        return ExtractResponse(modules=all_modules_by_url)
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during extraction: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

