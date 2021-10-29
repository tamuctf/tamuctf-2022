# Taxes

## Description

Thank you for completing your 2021 taxes with Another Data Harvester!

We've sent you your 2021 tax return. For your safety and privacy, we've delivered the document as encrypted with your Social Security Number, with no dashes.

We hope you have a pleasant 2022. Make sure to file with us next year so we can ~~harvest your data further~~ help you with your taxes again!

## Solution

1. pdf2john and adjust for hashcat (remove filename from file)
2. `hashcat -m 10500 ./pdf.hash -a3 "?d?d?d?d?d?d?d?d?d"`
3. wait
4. `694705124` & `gigem{hope_you_did_your_taxes_already}`
