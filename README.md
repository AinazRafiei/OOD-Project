## راه‌اندازی پروژه Ghasedak - راهنمای کامل

### گام 1: نصب Python

1. Python را از [وبسایت Python](https://www.python.org/) دانلود و نصب کنید.
2. مطمئن شوید که متغیر محیطی `PATH` به درستی تنظیم شده است تا به اجرای Python از هر مکان دسترسی داشته باشید.

### گام 2: نصب و مدیریت محیط مجازی

1. اگر نمی‌خواهید از محیط مجازی استفاده کنید، این گام را نادیده بگیرید.
2. از Command Prompt یا Terminal خود، به مسیر پروژه خود بروید.
3. محیط مجازی را با دستور زیر ایجاد کنید:
   
   در ویندوز:
   ```bash
   python -m venv env_name
   ```

   در مک و لینوکس:
   ```bash
   python3 -m venv env_name
   ```

4. محیط مجازی را با دستور زیر فعال کنید:
   
   در ویندوز:
   ```bash
   env_name\Scripts\activate
   ```

   در مک و لینوکس:
   ```bash
   source env_name/bin/activate
   ```

### گام 3: نصب Django و وابستگی‌ها

1. در محیط مجازی، Django و وابستگی‌های مورد نیاز را با دستور زیر نصب کنید:

   ```bash
   pip install -r requirements.txt
   ```

### گام 4: تنظیمات اولیه پروژه

1. یک پروژه Django جدید ایجاد کنید:

   ```bash
   django-admin startproject project_name
   ```

2. وارد دایرکتوری پروژه شوید:

   ```bash
   cd project_name
   ```

3. migrate ها پایگاه داده اولیه را اجرا کنید:

   ```bash
   python manage.py migrate
   ```

4. اکانت ادمین (مدیریتی) را برای پنل مدیریت Django ایجاد کنید:

   ```bash
   python manage.py createsuperuser
   ```

### گام 5: اجرای سرور توسعه

1. سرور توسعه Django را اجرا کنید:

   ```bash
   python manage.py runserver
   ```

2. سرور توسعه به آدرس http://127.0.0.1:8000/ در حالت پیش‌فرض اجرا می‌شود. می‌توانید این آدرس را در مرورگر خود باز کنید تا به نمای پیش‌فرض Django دسترسی پیدا کنید.


### گام 6: خاتمه کار

1. پس از اتمام کار با پروژه، محیط مجازی را غیرفعال کنید:

   ```bash
   deactivate
   ```
