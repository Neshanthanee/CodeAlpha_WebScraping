import requests
from bs4 import BeautifulSoup
import pandas as pd
import time 

book_data_list = []
for page_num in range(1, 51):
    if page_num == 1:
        URL = "http://books.toscrape.com/"
    else:
        URL = f"http://books.toscrape.com/catalogue/page-{page_num}.html"
    
    print(f"\n--- SCRAPING Page {page_num} ({URL}) ---")
    try:
        page = requests.get(URL, timeout=10) 
        page.raise_for_status() 
    except requests.exceptions.RequestException as e:
        print(f"!! Error fetching Page {page_num}: {e}. Skipping this page.")
        time.sleep(2)
        continue 

    soup = BeautifulSoup(page.content, "html.parser")
    book_containers = soup.find_all("article", class_="product_pod")
    for book in book_containers:
        try:
            title_element = book.find('h3').find('a')
            book_title = title_element['title'] 
        except AttributeError:
            book_title = "Title Not Found"
        try:
            price_element = book.find("p", class_="price_color")
            book_price = price_element.text.strip()
        except AttributeError:
            book_price = "Price Not Found"
       
        try:
            rating_element = book.find("p", class_="star-rating")
            star_rating = rating_element.get('class')[1] + " Stars" # Gets the second class name (e.g., 'Three')
        except (AttributeError, IndexError):
            star_rating = "Rating Not Found"
        
     
        try:
            stock_element = book.find("p", class_="instock availability")
            stock_status = stock_element.text.strip() 
        except AttributeError:
            stock_status = "Stock Not Found"

       
        book_data_list.append({
            'Title': book_title,
            'Price': book_price,
            'Rating': star_rating,
            'Stock Status': stock_status
        })
        
    time.sleep(1) 

if book_data_list:
    df = pd.DataFrame(book_data_list)
    df.to_csv("All_Books_Scraped_Dataset.csv", index=False) 

    print("\n\n####################################")
    print("ALL PAGES SCRAPED SUCCESSFULLY!")
    print(f"Total books extracted: {len(book_data_list)}") # Ithu 1000-kku pakkathula irukkanum
    print("Dataset saved as 'All_Books_Scraped_Dataset.csv'")
    print("####################################")
else:
    print("\n--- Warning ---")
    print("No book data was extracted. Please check your setup and network.")
if book_data_list:
    df = pd.DataFrame(book_data_list)
    
    print("\nStarting Data Cleaning...")
    try:
        df['Price (GBP)'] = df['Price'].str.replace('£', '').astype(float)
        df.drop('Price', axis=1, inplace=True) # Old 'Price' column-a delete pannidalam
    except Exception:
        print("Warning: Price cleaning failed.")
    rating_map = {'One Stars': 1, 'Two Stars': 2, 'Three Stars': 3, 'Four Stars': 4, 'Five Stars': 5}
    try:
        df['Star Rating'] = df['Rating'].replace(rating_map).astype(int)
        df.drop('Rating', axis=1, inplace=True)
    except Exception:
        print("Warning: Rating cleaning failed.")
    df.to_csv("Cleaned_Scraped_Book_Data.csv", index=False) 

    print("\n\n####################################")
    print("TASK 1 COMPLETED AND CLEANED!")
    print(f"Final Cleaned Dataset saved as: Data.csv")
    print("####################################")
