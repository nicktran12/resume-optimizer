import httpx
from bs4 import BeautifulSoup

REQUEST_TIMEOUT_SECONDS = 10.0
MAX_HTML_BYTES = 5_000_000

NOISE_TAGS = ["script", "style", "nav", "footer", "header", "noscript", "svg", "iframe"]

class JobFetchError(Exception):
    pass

def fetch_job_description(url: str) -> str:
    try:
        response = httpx.get(
            url,
            timeout=REQUEST_TIMEOUT_SECONDS,
            follow_redirects=True,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
                )
            },
        )
    except httpx.TimeoutException:
        raise JobFetchError("The job posting page took too long to respond.")
    except httpx.RequestError as e:
        raise JobFetchError(f"Could not reach that URL: {e}")

    if  response.status_code == 403 or response.status_code == 401:
        raise JobFetchError("That page blocked automated access. Please paste the job description instead.")
    if response.status_code >= 400:
        raise JobFetchError(f"That page returned an error (HTTP {response.status_code}).")

    if len(response.content) > MAX_HTML_BYTES:
        raise JobFetchError("That page is unusually large and was not processed.")

    content_type = response.headers.get("content-type", "")
    if "text/html" not in content_type:
        raise JobFetchError("That URL did not return a webpage.")

    soup = BeautifulSoup(response.text, "html.parser")

    for tag in soup(NOISE_TAGS):
        tag.decompose()

    text = soup.get_text(separator="\n")
    lines = [line.strip() for line in text.split("\n")]
    lines = [line for line in lines if line]
    cleaned = "\n".join(lines)

    if len(cleaned) < 100:
        raise JobFetchError("Could not extract meaningful content from that page. Please paste the job description instead.")

    return cleaned