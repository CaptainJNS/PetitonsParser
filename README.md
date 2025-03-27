This is a parser for Ukrainian goverment site **[petition.president.gov.ua](https://petition.president.gov.ua)** that exports all of signers of your petition and can be easily managed later (searching, sorting, etc.).

How to use:

1. Install Python and all necessary dependencies
2. Find your petition and copy its ID from the URL (https://petition.president.gov.ua/petition/**PETITION_ID**)
3. Run `python Petition.py` or `python Petition.py PETITION_ID`

Data will be saved to `.xls` file by default. You can uncomment `save_scv` in the `main()` function to save a `.csv` file.
