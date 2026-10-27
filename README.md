# Customer Data Analysis Using Python

## Project Overview

This project retrieves customer records from the JSONPlaceholder API and analyses them using Python data structures, Requests, pandas, and Matplotlib.

API endpoint: https://jsonplaceholder.typicode.com/users

## 1. Retrieving Customer Data

The `get_customers(url)` function uses Requests to retrieve the customer records. It uses a 10-second timeout, checks the HTTP status code, and parses the JSON response. Network and HTTP errors are handled with clear messages.

## 2. Exploring Nested Data

The `explore(record, indent)` function goes through nested dictionaries and lists, printing each key and its Python data type.

The customer records contain these nested attributes:

| Attribute | Access path |
|---|---|
| Address | `customer["address"]` |
| City | `customer["address"]["city"]` |
| ZIP code | `customer["address"]["zipcode"]` |
| Geographic coordinates | `customer["address"]["geo"]` |
| Latitude | `customer["address"]["geo"]["lat"]` |
| Longitude | `customer["address"]["geo"]["lng"]` |
| Company | `customer["company"]` |
| Company name | `customer["company"]["name"]` |

The deepest attributes are latitude and longitude, reached through the `address` and `geo` dictionaries. The coordinates are converted from strings to floats during extraction.

## 3. Extracting Customer Attributes

The `extract_attributes(customers)` function creates one flat dictionary per customer.

The resulting table contains 12 columns:

- customer_id
- name
- username
- email
- email_domain
- phone
- city
- zipcode
- latitude
- longitude
- company
- website

The `customer_id` column is populated from the API's `id` field. The `email_domain` column contains the final email suffix, such as `biz` or `tv`.

## 4. Unique Cities and Marketing Interpretation

The `unique_cities(customers)` function uses a set to find all the distinct cities where the customers live. In this case we find that every customer lives in a different city, thus there really isn't a geographic trend to identify. Marketing should collect a larger dataset before making geographic targeting decisions.

## 5. Counting Customers

The `city_counts(customers)` function uses a dictionary and a loop to count customers by city without using pandas.

The `email_domain_counts(customers)` function uses a dictionary comprehension to count customers by email suffix.

Both results are displayed from most to least common, with alphabetical ordering used to break ties.

## 6. DataFrame and Verification

The `to_dataframe(rows)` function converts the extracted records into a pandas DataFrame.

The program prints the DataFrame shape and column data types. It also compares the manually calculated city and email-domain counts against pandas `value_counts()` results.

We confirm that both counts match.

## 7. CSV Exports

The program creates the following files:

- `output/customers.csv`: flattened customer records with 12 columns.
- `output/city_counts.csv`: city names and customer counts, sorted by descending count and then alphabetically.

Both CSV files are exported with `index=False` to avoid an extra pandas index column.

## 8. Visualisation

The program generates two bar charts:

- `output/customer_distribution.png`: customer counts by city.
- `output/email_domain_distribution.png`: customer counts by email suffix.

The email-domain chart is more useful for comparing category frequencies because all the cities possess the same count.

## Conclusion

This project demonstrates API requests, exception handling, going through nested data levels, dictionaries, sets, list comprehensions, pandas DataFrames, CSV exports, and data visualisation.


## How to Run

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the analysis:

```bash
python starter.py
```
