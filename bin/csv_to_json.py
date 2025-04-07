#!/usr/bin/env python3

"""Covert CSV to JSON."""

import argparse
import csv
import json
import logging
from pathlib import Path


fields = {
    "awardNumber": 0,
    "latitude": 1,
    "longitude": 2,
    "projectTitle": 4,
    "awardPeriod": 5,
    "organization": 6,
    "orgState": 8,
    "primaryHumanitiesDiscipline": 12,
    "professionalBody": 13,
    "discipline": 14,
    "grantProgram": 15,
    "divisionOrOffice": 16,
    "awardedOutright": 19,
    "description": 21,
    "district": 30,
    "repLastName": 31,
    "repFirstName": 32,
    "repParty": 33,
    "repUrl": 34,
    "repAddress": 35,
    "repPhone": 36,
    "sen1LastName": 37,
    "sen1FirstName": 38,
    "sen1Party": 39,
    "sen1Url": 40,
    "sen1Address": 41,
    "sen1Phone": 42,
    "sen1ContactForm": 43,
    "sen1Twitter": 45,
    "sen1Facebook": 46,
    "sen2LastName": 47,
    "sen2FirstName": 48,
    "sen2Party": 49,
    "sen2Url": 50,
    "sen2Address": 51,
    "sen2Phone": 52,
    "sen2ContactForm": 53,
    "sen2Twitter": 54,
    "sen2Facebook": 55,
}


def parse_csv(input, representatives):
    """Parse CSV."""

    parsed = []

    with open(input, "r") as _fh:
        reader = csv.DictReader(_fh)
        for i, row in enumerate(reader):
            if not any(_ for _ in row.values()):
                logging.warning("Empty row: %s", i)
                continue
            values = list(row.values())
            values += list(representatives[row["AwardNumber"]])
            parsed.append([values[idx] for idx in fields.values()])

    return parsed


def prep_representatives(input):
    """Parse CSV."""

    representatives = {}

    with open(input, "r") as _fh:
        reader = csv.DictReader(_fh)
        for i, row in enumerate(reader):
            if not any(_ for _ in row.values()):
                logging.warning("Empty row: %s", i)
                continue
            representatives[row["Award Number"]] = list(row.values())

    return representatives


def main():
    """Command-line entry-point."""

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    parser = argparse.ArgumentParser(description="Description: {}".format(__doc__))
    parser.add_argument("-i", "--input", action="store", required=True)
    parser.add_argument("-r", "--representatives", action="store", required=True)
    args = parser.parse_args()

    representatives = prep_representatives(args.representatives)
    parsed = parse_csv(args.input, representatives)
    logging.info("%s records parsed", len(parsed))

    json_out = json.dumps(parsed)

    with Path(args.input).with_suffix(".json").open("w") as _fh:
        _fh.write(json_out)


if __name__ == "__main__":
    main()
