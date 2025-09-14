import pandas as pd
from db.connection import engine


def revenue_by_category() -> pd.DataFrame:
    """
    Returns total revenue per film category.
    """
    query = """
        SELECT c.name AS category,
               SUM(p.amount) AS revenue
        FROM payment p
        JOIN rental r ON p.rental_id = r.rental_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film_category fc ON i.film_id = fc.film_id
        JOIN category c ON fc.category_id = c.category_id
        GROUP BY c.name
        ORDER BY revenue DESC;
    """
    return pd.read_sql(query, engine)


def rentals_per_month() -> pd.DataFrame:
    """
    Returns number of rentals per month.
    """
    query = """
        SELECT DATE_TRUNC('month', r.rental_date) AS month,
               COUNT(*) AS rentals
        FROM rental r
        GROUP BY month
        ORDER BY month;
    """
    return pd.read_sql(query, engine)


def rental_rate_vs_length() -> pd.DataFrame:
    """
    Returns film length vs. rental rate for scatter plot.
    """
    query = """
        SELECT length AS film_length,
               rental_rate
        FROM film;
    """
    return pd.read_sql(query, engine)


def get_film_lengths() -> pd.DataFrame:
    """
    Returns a DataFrame with all film lengths from Pagila.
    """
    query = """
        SELECT length
        FROM film
        WHERE length IS NOT NULL
    """
    return pd.read_sql(query, engine)


def most_rented_films(limit: int = 10) -> pd.DataFrame:
    """
    Returns the most rented films.
    """
    query = f"""
        SELECT f.title AS film,
               COUNT(*) AS rental_count
        FROM rental r
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        GROUP BY f.title
        ORDER BY rental_count DESC
        LIMIT {limit};
    """
    return pd.read_sql(query, engine)
