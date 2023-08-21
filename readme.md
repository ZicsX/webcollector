## **Web Collector**

Web Collector is a Django-based web application that integrates with Scrapy for web crawling. The application allows users to input a domain, triggers a crawl to extract textual content from the web pages within that domain, and then compresses the results into a zip file available for download.

### **Features:**

- **Domain-based crawling:** Enter a domain and crawl its textual content.
- **Progress Status:** Real-time feedback on the status of the web crawl.
- **Data Integrity:** Ensures idempotency by hashing each domain request to avoid unnecessary recrawls.
- **Asynchronous crawling:** Uses Celery and RabbitMQ to manage crawl tasks in the background.

### **Technologies Used:**

- **Backend:** Django
- **Web Crawling:** Scrapy and Trafilatura
- **Asynchronous Tasks:** Celery with RabbitMQ as the broker
- **Frontend:** Basic HTML with jQuery for AJAX

### **Getting Started:**

#### **1. Prerequisites:**

Ensure you have the following installed:

- Python
- RabbitMQ

#### **2. Installation:**

Clone the repository:

```bash
git clone https://github.com/ZicsX/webcollector.git
cd webcollector
```

Set up a virtual environment:

```bash
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`
```

Install the required packages:

```bash
pip install -r requirements.txt
```

#### **3. Configuration:**

Make sure RabbitMQ is running. If you need to configure its URL or other settings, update the `CELERY_BROKER_URL` in the Django settings.

Run Django migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

#### **4. Running the Application:**

Start the Django server:

```bash
python manage.py runserver
```

In a separate terminal, navigate to the project directory and activate the virtual environment. Start the Celery worker:

```bash
celery -A webcollector worker --loglevel=info
```

Now, visit `http://127.0.0.1:8000/` in your browser to access the Web Collector interface.

#### **5. Using the Web Collector:**

1. Enter a domain into the input field.
2. Click "Start Crawling".
3. Monitor the status. Once completed, a download link for a zip file containing the extracted data will appear.

---
Of course! Let's add a section on how to directly run the Scrapy spider without the Django interface:

---

### **Directly Running the Scrapy Spider:**

If you'd like to bypass the Django application and run the Scrapy spider directly, you can use the following command:

```bash
scrapy crawl async_spider -a url=YOUR_DOMAIN_HERE
```

Replace `YOUR_DOMAIN_HERE` with the domain you want to crawl. The extracted textual content will be saved in a folder named after the domain inside 'collect_data', and links will be saved in a `links.csv` file within the same folder.

---
