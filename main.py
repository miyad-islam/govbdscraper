from webscrap import WebScraper
import extract_information


if __name__ == "__main__":
    # Input the base URL
    base_url = input("Enter URL: ")

    # Initialize the WebScraper
    scraper = WebScraper(base_url)

    # Start crawling
    scraper.start_crawling()
    # Ask the user what to extract (class or id)
    extract_type = input("Do you want to extract by 'class' or 'id'? ").strip().lower()

    if extract_type not in ["class", "id"]:
        print("Invalid input. Please enter 'class' or 'id'.")
    else:
        # Ask the user for the class or id name
        target_name = input(f"Enter the {extract_type} name: ").strip()

        # Call the extract_data function from the webscraper module
        extract_information.extract_data(extract_type, target_name,base_url)