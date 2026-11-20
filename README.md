# Bookkeeping Scope Toolkit

English-language templates and a local quote calculator for small businesses preparing a catch-up bookkeeping project.

| File | Use it to |
| --- | --- |
| [Catch-up handoff checklist](catch-up-checklist.md) | Agree on the months, accounts, corrections, exceptions, and deliverables before approving a quote. |
| [Month and account inventory](scope-inventory.csv) | Capture one row per account and month, including missing statements and transaction counts. |
| [Quote comparison template](quote-comparison.csv) | Capture recurring charges, setup fees, catch-up fees, and what each provider includes. |
| [Quote calculator](compare_quotes.py) | Calculate each quote's upfront and first-year costs and flag scope differences from the CSV. |

## Start with the scope

Copy `scope-inventory.csv`, remove its illustrative rows, and enter one row per account and month. Use the same non-identifying account alias across months. Leave unknown transaction counts blank and mark missing statements as `missing`. Use the checklist to agree on which rows and corrections the provider quoted.

## Compare written quotes

Copy `quote-comparison.csv` and replace its illustrative rows with USD amounts from written quotes. Enter `0` only for a charge the provider has confirmed is zero. A blank charge means the total is unknown. For scope columns use `included`, `extra`, `excluded`, or `unknown`. Add prices for any required extras to the relevant charge fields once confirmed.

Run with Python 3.10 or later. No third-party packages or network access are needed.

```sh
python compare_quotes.py quote-comparison.csv
```

The first-year total is twelve times the monthly base plus required monthly add-ons, plus the setup and catch-up fees. The sample values are fictional and demonstrate the worksheet. Totals are comparable only when the quotes cover the same work and use equivalent service periods. The tool flags differing or unknown scope statuses and preserves unknown totals.

For an interactive month-by-month scope builder and a guide to handing it off, see [Bookkeeping Scope](https://bookkeepingscope.com/).

Released under the [MIT License](LICENSE).
