#!/usr/bin/env python3

import argparse
import json
from lib.keyword_search import search_command, InvertedIndex 



def handle_build_command():
        inverindex =  InvertedIndex()
    
        inverindex.build()

        docs = inverindex.get_document("merida")
        inverindex.save()
        print(f"First document for token 'merida' = {docs[0]}")



def main() -> None:
    
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    build_parser = subparsers.add_parser("build", help="builds docs")
    build_parser.set_defaults(func=handle_build_command)

    args = parser.parse_args()

    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            results = search_command(args.query)
            for i, res in enumerate(results, 1):
                print(f"{i}. {res['title']}")
        case _:
            parser.print_help()
    handle_build_command()
if __name__ == "__main__":
    main()


