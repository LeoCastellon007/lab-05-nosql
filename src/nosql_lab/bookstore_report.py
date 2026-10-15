#!/usr/bin/env python3
"""Print a report of each author's books from the bookstore database on MongoDB Atlas."""

import logging
import os

import pymongo

# Read Atlas connection settings from the environment (never hardcode credentials)
MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

# Authors to include: author_002 and author_003 come from authors.json,
# author_004 (Stephen Baxter) was added in bookstore.js step 7
AUTHOR_IDS = ["author_002", "author_003", "author_004"]

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def main():
    """Connect to Atlas, join authors to their books, and print the report."""
    client = None
    try:
        # Connect to MongoDB Atlas with the credentials from the environment
        client = pymongo.MongoClient(
            MONGODB_ATLAS_URL,
            username=MONGODB_ATLAS_USER,
            password=MONGODB_ATLAS_PWD,
        )
        # Ping the server so a bad connection fails here, not mid-report
        client.admin.command("ping")
        logger.info("Connected to MongoDB Atlas")

        # Select the database and collections from Case Study 1
        db = client["bookstore"]
        authors = db["authors"]
        books = db["books"]

        # Count the authors in our list that exist in the collection
        author_filter = {"_id": {"$in": AUTHOR_IDS}}
        print(f"Authors: {authors.count_documents(author_filter)}")

        # For each author, look up every book whose author_ids contains the author's _id
        for author in authors.find(author_filter).sort("_id"):
            print()
            print(author["name"])
            for book in books.find({"author_ids": author["_id"]}).sort("published_year"):
                print(f"  {book['title']} ({book['published_year']})")
    except Exception as e:
        logger.error(f"MongoDB error: {e}")
    finally:
        # Always close the client, even if something failed
        if client is not None:
            client.close()
            logger.info("Connection closed")


if __name__ == "__main__":
    main()
