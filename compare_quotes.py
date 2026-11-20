"""Compare USD bookkeeping quotes recorded in quote-comparison.csv."""

import argparse
import csv
import re
from decimal import Decimal
from pathlib import Path


MONTHLY = ("monthly_base_usd", "required_monthly_add_ons_usd")
UPFRONT = ("setup_fee_usd", "catch_up_fee_usd")
SERVICES = ("record_missing_entries", "correct_entries", "reconcile_accounts", "deliver_reports")
STATUSES = {"included", "extra", "excluded", "unknown"}
MONEY = re.compile(r"[0-9]{1,12}(?:\.[0-9]{1,2})?")


def read_quotes(path):
    quotes = []
    seen = set()
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        missing = {"provider", *MONTHLY, *UPFRONT, *SERVICES} - set(reader.fieldnames or ())
        if missing:
            raise ValueError(f"Missing columns: {', '.join(sorted(missing))}")

        for line, row in enumerate(reader, start=2):
            if None in row or None in row.values():
                raise ValueError(f"Row {line}: the number of values must match the header.")
            if not any(value.strip() for value in row.values()):
                continue
            provider = row["provider"].strip()
            if not provider or provider.casefold() in seen:
                raise ValueError(f"Row {line}: enter a unique provider name.")
            seen.add(provider.casefold())

            amounts = {}
            for field in (*MONTHLY, *UPFRONT):
                value = row[field].strip()
                if value and not MONEY.fullmatch(value):
                    raise ValueError(f"Row {line}: {field} must be blank or a non-negative USD amount with up to two decimal places.")
                amounts[field] = Decimal(value) if value else None

            scope = {field: row[field].strip().casefold() or "unknown" for field in SERVICES}
            for field, status in scope.items():
                if status not in STATUSES:
                    allowed = ", ".join(sorted(STATUSES))
                    raise ValueError(f"Row {line}: {field} must be one of {allowed}.")
            quotes.append((provider, amounts, scope))

    if not quotes:
        raise ValueError("Enter at least one provider quote.")
    return quotes


def subtotal(amounts, fields):
    values = [amounts[field] for field in fields]
    return sum(values, Decimal("0")) if None not in values else None


def usd(value):
    return "unknown" if value is None else f"${value:,.2f}"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("quotes", type=Path, help="Path to a copy of quote-comparison.csv")
    args = parser.parse_args()
    try:
        quotes = read_quotes(args.quotes)
    except (OSError, UnicodeError, ValueError, csv.Error) as error:
        parser.error(str(error))

    for provider, amounts, _ in quotes:
        monthly = subtotal(amounts, MONTHLY)
        upfront = subtotal(amounts, UPFRONT)
        first_year = monthly * 12 + upfront if monthly is not None and upfront is not None else None
        print(f"{provider}: Monthly {usd(monthly)} | Upfront {usd(upfront)} | First year {usd(first_year)}")

    for field in SERVICES:
        statuses = [scope[field] for _, _, scope in quotes]
        if len(set(statuses)) > 1 or "unknown" in statuses or "extra" in statuses:
            details = ", ".join(f"{quote[0]}={status}" for quote, status in zip(quotes, statuses))
            print(f"Check {field.replace('_', ' ')}: {details}")


if __name__ == "__main__":
    main()
