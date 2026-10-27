"""
Day 1 - API Data Analysis Using Python Structures
Squad Python Specialization - Data Science, AI & Analytics
"""
import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import requests

API_URL = "https://jsonplaceholder.typicode.com/users"
OUTPUT_DIR = Path('output')


def get_customers(url: str = API_URL) -> list[dict]:
    """Fetch the customer list. Report failures clearly instead of crashing."""
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.Timeout:
        print(f'Error: the request to {url} timed out after 10 seconds')
        return []
    except requests.exceptions.RequestException as exc:
        print(f'Error: request to {url} failed: {exc}')
        return []
    if response.status_code != 200:
        print(f'Error: {url} returned HTTP status {response.status_code}')
        return []
    try:
        data = response.json()
    except ValueError:
        print(f'Error: {url} did not return valid JSON.')
        return []

    if not isinstance(data, list):
        print('Error: expected a list of customers but received something else.')
        return []

    return data


def explore(record: dict, indent: int = 0) -> None:
    """Print every key in a (possibly nested) record with its type, indented by depth."""
    pad = ' ' * indent

    for key, value in record.items():
        print(f'{pad}{key}: {type(value).__name__}')

        if isinstance(value, dict):
            explore(value, indent + 2)

        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    print(f'{pad} [{i}]: dict')
                    explore(item, indent + 4)


def extract_attributes(customers: list[dict]) -> list[dict]:
    """Return one flat dict per customer with the attributes listed in the task."""
    rows = []

    for customer in customers:
        email = customer.get('email', '')
        email_domain = (
            email.rsplit('@',1)[-1].rsplit('.',1)[-1].lower()
            if '@' in email and '.' in email.rsplit('@', 1)[-1]
            else ''
        )

        address = customer.get('address', {})
        geo = address.get('geo', {})
        company = customer.get('company', {})

        row = {
            'customer_id': customer.get('id'),
            'name': customer.get('name', ''),
            'username': customer.get('username', ''),
            'email' : email,
            'email_domain': email_domain,
            'phone': customer.get('phone', ''),
            'city': address.get('city', ''),
            'zipcode': address.get('zipcode', ''),
            'latitude': float(geo['lat']),
            'longitude': float(geo['lng']),
            'company' : company.get('name', ''),
            'website': customer.get('website', '')
        }

        rows.append(row)

    return rows


def unique_cities(customers: list[dict]) -> set[str]:
    """Return the set of distinct cities."""
    return {
        customer['address']['city']
        for customer in customers
    }


def city_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per city using a loop and/or a dict comprehension (no Counter, no pandas)."""
    counts = {}

    for customer in customers:
        city = customer['address']['city']
        counts[city] = counts.get(city,0) + 1

    return counts


def email_domain_counts(customers: list[dict]) -> dict[str, int]:
    """Count customers per email top-level domain (e.g. 'biz', 'tv')."""
    rows = extract_attributes(customers)

    return {
        domain: sum(
            row['email_domain'] == domain
            for row in rows
        )
        for domain in {row['email_domain'] for row in rows}
        if domain
    }

def sort_counts(counts: dict[str, int]) -> list[tuple[str, int]]:
    ''' Sort counts from highest to lowest and alphabetically incase of ties.'''
    return sorted(
        counts.items(),
        key=lambda item: (-item[1], item[0])
    )


def to_dataframe(rows: list[dict]) -> pd.DataFrame:
    '''Converting the flattened records into a DataFrame'''
    return pd.DataFrame(rows)


def plot_distribution(counts: dict[str, int], path: Path) -> None:
    """Save a labelled chart of the distribution to path."""
    path.parent.mkdir(parents=True, exist_ok=True)

    ordered = sorted(
        counts.items(),
        key=lambda item:(-item[1], item[0])
    )

    labels = [item[0] for item in ordered]
    values = [item[1] for item in ordered]

    fig,ax = plt.subplots(figsize=(10, 6))
    ax.bar(labels,values)

    ax.set_title('Customer Distribution')
    ax.set_xlabel('Category')
    ax.set_ylabel('Number of Customers')
    ax.tick_params(axis='x', labelrotation=45)

    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)


if __name__ == "__main__":
    # Retriving the data
    customers = get_customers()
    if not customers:
        print('No customer data available.')
        raise SystemExit(1)
    print(f'Customers retrieved : {len(customers)}')


    # Exploring one record
    print('Customer record structure:')
    explore(customers[0])


    #Finding unique cities
    cities = unique_cities(customers)
    print(f'Unique cities: {len(cities)}')


    # Counting cities
    cities_counted = city_counts(customers)
    sorted_cities = sort_counts(cities_counted)

    most_common_city, most_common_count = sorted_cities[0]
    print(f'Most common city: {most_common_city} ({most_common_count})')

    # Counting emails
    domains_counted = email_domain_counts(customers)
    sorted_domains = sort_counts(domains_counted)

    print(f'Email domains: {dict(sorted_domains)}')

    # Flattening records
    rows = extract_attributes(customers)

    # Converting to DataFrame
    df = to_dataframe(rows)

    print(f'\nDataFrame shape: {df.shape}')
    print(f'\nDataFrame data types:')
    print(df.dtypes)


    # Verifying counts
    pandas_city_counts = df['city'].value_counts().to_dict()
    pandas_domain_counts = (df.loc[df['email_domain'] != '','email_domain'].value_counts().to_dict())

    print('\nCity counts same as pandas count:',
          cities_counted == pandas_city_counts)
    print('Email domain counts same as pandas count:',
          domains_counted == pandas_domain_counts)

    

    # Exporting the CSV files
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_DIR / 'customers.csv', index=False)

    city_df = pd.DataFrame(
        sorted_cities,
        columns=['city', 'customer_count']
    )
    city_df.to_csv(OUTPUT_DIR / 'city_counts.csv', index=False)

    print('Saved:', OUTPUT_DIR / 'customers.csv')
    print('Saved:', OUTPUT_DIR / 'city_counts.csv')


    # Generating charts
    plot_distribution(
        cities_counted,
        OUTPUT_DIR / 'customer_distribution.png'
    )

    plot_distribution(
        domains_counted,
        OUTPUT_DIR / 'email_domain_distribution.png'
    )

    print('Chart saved to : output/customer_distribution.png')
    print('Chart saved to : output/email_domain_distribution.png')



   