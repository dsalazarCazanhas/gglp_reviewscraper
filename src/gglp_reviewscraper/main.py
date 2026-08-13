from datetime import datetime
import logging
import sys

import pandas as pd
import requests
from google_play_scraper import Sort, reviews

# Configuration
APPS = {
    "banco_bienestar": "gob.bancodelbienestar.bcobienapp",
    "imss_publico": "st.android.imsspublico",
}
# id=gob.bancodelbienestar.bcobienapp
# id=st.android.imsspublico
CONFIG = {
    "APP_ID": APPS["banco_bienestar"],
    "TARGET_RATINGS": [1, 2, 3],
    "SCRAPE_COUNT": 200,
    "SCRAPE_LANG": "es",
    "SCRAPE_COUNTRY": "mx",
    "IP_CHECK_URL": "https://ipinfo.io/json",
    "CUT_OFF_DATE": datetime(2026, 4, 30),  # Only reviews after this date will be considered
    "IP_CHECK_TIMEOUT": 5,
    "REQUESTS_TIMEOUT": 10,
}

log = logging.getLogger(__name__)


def setup_logging() -> None:
    """Configure logging for the application."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        force=True,  # Override existing logging config
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    # Flush immediately to avoid buffering delays
    for handler in logging.root.handlers:
        handler.flush()


def check_connection_origin() -> None:
    """
    Check the public IP's origin country and warn the user about it.

    There is no reliable way to detect whether the connection is routed
    through a VPN, so this only informs the user of the detected country
    and recommends using a VPN plus following Google's scraping etiquette.
    This check is informational only and never blocks execution.
    """
    log.info("Checking public IP origin...")

    try:
        response = requests.get(
            CONFIG["IP_CHECK_URL"],
            timeout=CONFIG["IP_CHECK_TIMEOUT"],
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        log.warning("IP check timed out. Skipping origin check.")
        return
    except requests.exceptions.RequestException as e:
        log.warning(f"Failed to check IP origin: {e}")
        return

    try:
        ip_data = response.json()
        country = ip_data.get("country", "UNKNOWN")
    except ValueError:
        log.warning("Invalid JSON response from IP check service. Skipping origin check.")
        return

    log.warning(f"Connection origin country: [{country}]")
    log.warning(
        "Cannot verify whether this connection is routed through a VPN. "
        "Consider using one, and follow Google's scraping etiquette "
        "(reasonable request rates, respect CUT_OFF_DATE, avoid excessive retries)."
    )


def fetch_reviews(app_id: str, score: int):
    """
    Fetch reviews from Google Play Store.

    Args:
        app_id: Google Play Store app package ID.
        score: The rating score to filter reviews.

    Returns:
        DataFrame with fetched reviews, or None if fetch failed.
    """
    log.info(f"Fetching reviews for app: {app_id} with score={score}...")

    collected = []
    continuation_token = None

    while True:
        page, continuation_token = reviews(
            app_id,
            lang=CONFIG["SCRAPE_LANG"],
            country=CONFIG["SCRAPE_COUNTRY"],
            sort=Sort.NEWEST,
            count=CONFIG["SCRAPE_COUNT"],
            filter_score_with=score,
            continuation_token=continuation_token,
        )

        if not page:
            break

        stop_early = False
        for review in page:
            if review["at"] < CONFIG["CUT_OFF_DATE"]:
                stop_early = True
                break
            collected.append(review)

        if stop_early:
            break

        if continuation_token is None or continuation_token.token is None:
            break

    if not collected:
        log.warning("No reviews returned from scraper for score %s", score)
        return pd.DataFrame(
            columns=["reviewId", "userName", "content", "score", "at"]
        )

    try:
        df = pd.DataFrame(
            collected,
            columns=["reviewId", "userName", "content", "score", "at"],
        )
        log.info(f"Successfully fetched {len(df)} reviews for score={score}")
        return df
    except Exception as e:
        log.error(f"Failed to create DataFrame: {e}")
        return None


def filter_low_ratings(df: pd.DataFrame, ratings: list) -> pd.DataFrame:
    """
    Filter DataFrame to keep only reviews with specified ratings.

    Args:
        df: DataFrame with review data.
        ratings: List of rating values to keep (e.g., [1, 2, 3]).

    Returns:
        Filtered DataFrame.
    """
    filtered_df = df[df["score"].isin(ratings)]
    log.info(f"Filtered to {len(filtered_df)} reviews with ratings {ratings}")
    return filtered_df


def build_output_filename(app_id: str) -> str:
    """Build the output CSV filename for a given app id, timestamped to the hour."""
    return f"reviews_{app_id}_{datetime.now().strftime('%Y-%m-%d_%H')}.csv"


def save_reviews(df: pd.DataFrame, output_file: str) -> bool:
    """
    Save reviews DataFrame to CSV file.

    Args:
        df: DataFrame to save.
        output_file: Path to output CSV file.

    Returns:
        True if successful, False otherwise.
    """
    if df.empty:
        log.warning("DataFrame is empty. Skipping save.")
        return False

    try:
        df.to_csv(output_file, index=False, encoding="utf-8-sig")
        log.info(f"Successfully saved {len(df)} reviews to '{output_file}'")
        return True
    except Exception as e:
        log.error(f"Failed to save reviews to '{output_file}': {e}")
        return False


def main() -> int:
    """Main application entry point."""
    setup_logging()

    log.info("=== Google Play Store Reviews Scraper ===")

    # Step 1: Warn about connection origin (informational only, does not block)
    check_connection_origin()

    # Step 2: Fetch reviews
    dfs = []
    for score in CONFIG["TARGET_RATINGS"]:
        df_score = fetch_reviews(CONFIG["APP_ID"], score)
        if df_score is None:
            return 1
        if not df_score.empty:
            dfs.append(df_score)

    if not dfs:
        log.warning("No reviews were fetched for target ratings")
        return 0

    df_reviews = pd.concat(dfs, ignore_index=True)

    # Step 3: Filter to low ratings (sanity check)
    df_low = filter_low_ratings(df_reviews, CONFIG["TARGET_RATINGS"])

    if df_low.empty:
        log.warning("No reviews found with target ratings")
        return 0

    # Step 4: Save to file
    output_file = build_output_filename(CONFIG["APP_ID"])
    if save_reviews(df_low, output_file):
        log.info("✓ Process completed successfully")
        return 0
    else:
        log.error("✗ Failed to save reviews")
        return 1


if __name__ == "__main__":
    sys.exit(main())
