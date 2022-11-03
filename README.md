# Enhancing our Django Shopping with Behave
Using behave for testing in the shopping with Django example

A shopping site done in Django to show the basics of an ecommerce site. This repository builds on the general shopping site found at https://github.com/scharlau/shopping_with_django. Go do that one first, if you haven't done it already to gain insight into what is working/missing from this site.

This one focuses on adding Behave for behavioural driven design to enhance testing using the given, when, then approach that it shares with Cucumber.

After you clone or download the repository use these commands to set things up:

    pyenv local 3.10.7 # this sets the local version of python to 3.10.7
    python3 -m venv .venv # this creates the virtual environment for you
    source .venv/bin/activate # this activates the virtual environment
    pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.
    pip install django
    pip install faker
    python3 manage.py migrate

This app uses Faker to generate customer and product details in the 'shop/management/commands/populate_tables.py' file. Go to https://faker.readthedocs.io/en/stable/providers.html and look through the options for Standard Providers to see if you want to change any details in values used.

You should now be able to populate the tables with the command:

        python3 manage.py populate_tables

Then you can start the server to see it running. 

You will need to create a superuser as well if you want to work with the admin features. You can do that with the command:

        python3 manage.py createsuperuser

Otherwise each customer created is also a user with a default password set in the management/commands/populate_tables.py file. 

You can launch django with the usual command:

        python3 manage.py runserver

With the server running, you can navigate around both parts of the application:
1. Go around the genearl website and notice what's working, what's bare-bones, and other issues. This is not finished, but a work in progress to illustrate how you might build a shopping application. 
2. Go to localhost:8000/admin and login with your superuser credentials. There you'll see the Django admin interface. From here you can also add products, and customers. The models listed here are specified in the shop/admin.py file.

### Testing 
There are basic Django focused tests to confirm the site works for Products, but more should be added to confirm all models, and that the basket and purchase work correctly. We want to build on these to fill in the gaps they leave.

The current unit and integration tests run fast, and confirm that the individual parts work. We want to add Behave to test the integration of the whole system.


## Behave added for BDD
This adds driver directory, and features, with steps directory.
We can now add the testing library Behave, along with Selenium for and the appropriate web drivers for your system, which you can find at https://selenium-python.readthedocs.io/installation.html#drivers Then put the binary at driver/chromedriver, gecko, or other driver in your app, as you see in the repo. Add it to the 'driver' folder mentione further below.

You might want to look at the documentation for Behave https://behave.readthedocs.io/en/latest/ for more about how to use it.
You should look at Selenium documentation for [navigating web pages] (https://www.selenium.dev/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#module-selenium.webdriver.remote.webdriver)

## Install and Configure Behave
We can add behave with pip:

        pip install behave

As this is for learning purposes, you can ignore the deprecation warning that might appear during the install. The current behavious of the install will work around the issue, and do what is required. We can now start to configure our application to work with Behave.


### Behave integration details
If you're using Behave with Django, then you need to edit the following folders and files. These need to be added in the root folder of your application. They should sit at the same level as 'shopping' and 'shop':

1. Create the 'features' directory to hold your <model>.feature files. To start with add a blank product.feature file.
2. Create a 'steps' directory inside of the 'features' folder, which hold the <model>.py files to implement each item in the feature. To start with add a blank product.py file to hold the steps.
3. Create a 'driver' folder to hold the browser driver files, which you intend to use such as Chrome.
4. Inside 'features' should also be an environment.py file. We'll add to this shortly.

We now have the basics for using behave, and can start filling in the details. We'll start with the product.feature file. Add this code, which you'll see uses the given, when, then syntax:

        Feature: checking products

        Scenario: add a product
            Given we want to add a product
            When we fill in the form
            Then it succeeds
        
        Scenario: adding products
            Given we have specific products to add
            | name          | price  |
            | this one      | 23.45  |
            | another thing | 34.56  |
            When we visit the listing page
            Then we will find 'another thing'

We can now have behave generate the skeleton code to inmplemnt this by running the command:

        behave
    
This will run your tests, which of course fail, as we've not implemented any steps yet. You'll see a mix of coloured output for your tests. The yellow ones, as it says, are placeholder code to implement each step. Copy the yellow code to your feature/steps/product.py file.

We can now back up and configure the features/environment.py file. This sets out the way the tests are run and other important details. Add this code to the file:

        from behave import fixture, use_fixture
        import os, urllib
        import django
        from django.shortcuts import resolve_url
        from django.test import selenium
        from django.test.testcases import TestCase
        from django.test.runner import DiscoverRunner
        from django.test.testcases import LiveServerTestCase
        # from django.contrib.staticfiles.testing import StaticLiveServerTestCase
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        os.environ["DJANGO_SETTINGS_MODULE"] = "shopping.settings"
        django.setup()

        # Use the chrome driver specific to your version of Chrome browser and put it in ./driver directory
        # CHROME_DRIVER = os.path.join(os.path.join(os.path.dirname(__file__), 'driver'), 'chromedriver')
        CHROME_DRIVER = os.path.join('driver/chromedriver')
        chrome_options = Options()
        # comment out the line below if you want to see the browser launch for tests
        # possibly add time.sleep() if required
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-proxy-server')
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")

        def before_all(context):
            use_fixture(django_test_runner, context)
            context.browser = webdriver.Chrome(options=chrome_options, executable_path=CHROME_DRIVER)
            context.browser.set_page_load_timeout(time_to_wait=200)

        def before_scenario(context, scenario):
            context.test = TestCase()
            context.test.setUpClass()
            use_fixture(django_test_case, context)

        def after_scenario(context, scenario):
            context.test.tearDownClass()
            del context.test

        def after_all(context):
            context.browser.quit()

        @fixture
        def django_test_runner(context):
            context.test_runner = DiscoverRunner()
            context.test_runner.setup_test_environment()
            context.old_db_config = context.test_runner.setup_databases()
            yield
            context.test_runner.teardown_databases(context.old_db_config)
            context.test_runner.teardown_test_environment()

        @fixture
        def django_test_case(context):
            context.test_case = LiveServerTestCase
            context.test_case.setUpClass()
            yield
            context.test_case.tearDownClass()
            del context.test_case


that sets out the relevant options you're using for browser driver such as Chrome, and the before_all(), before_scenario() and such testsuite details. Here we are making use of Django's built in testing framework. This should also hold relevant @fixture methods to load the test database, and set up the testing web server for you too. This runs at a different port from the normal server. 
Your <model>.py step files will need to point to your test server. You can grab the base_url with some lines like this:

        import urllib
        from urllib.parse import urljoin
        from behave import given, when, then

        @given( "we want to add a product")
        def user_on_product_newpage(context):
           base_url = urllib.request.url2pathname(context.test_case.live_server_url)
           print(base_url)
           open_url = urljoin(base_url,'/product_new/')
           context.browser.get(open_url)

As you can see we're pushing the limits of chaining methods, but this works without you having to hard code any paths. We print the base_url only to confirm that it's what we expect it to be for debugging, and can be commented out when running smoothly.

The other useful step is to create a fixture table in the feature file, which we access in the step file. For example, we can use this in the product.feature file:

    Scenario: adding products
        Given we have specific products to add
        | name          | price  |
        | this one      | 23.45  |
        | another thing | 34.56  |
        When we visit the listing page
        Then we will find 'another thing'

And then iterate through the items to load them into a form in the step file like this:

    open_url = urljoin(base_url,'/product_new/')
    for row in context.table:
        context.browser.get(open_url)
        name_textfield = context.browser.find_element_by_name('name')
        name_textfield.send_keys(row['name'])
        price_textfield = context.browser.find_element_by_name('price')
        price_textfield.send_keys(row['price'])
        context.browser.find_element_by_name('submit').click()
        assert row['name'] in context.browser.page_source

This will iteratively load and submit each item in the feature file.
A nice and easy way to test integration, and load data into the database for testing in a scenario.

#### Codio options for Behave
If doing this on Codio, then you can add the chromedriver as follows from the command line before downloading the driver:
Open a terminal and install the chromium browser with the command:

        sudo apt-get install -y chromium-browser

This will install the browser plus its required libraries. If that still shows missing libraries, then use this command for the rest. Hopefully, they were installed with the browser, but they might not have been.

        sudo apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1

This should now give you chrome. You now can look over the install log in the terminal to see which version number of the chromedriver that you need to install in the driver folder. However, be warned, this might not work fully in Codio, as it requires more memory and a few other components, which are not available by default in Codio.

#### Mac OS options for Behave
If you're on a Mac, then you will need to remove the chrome driver from quarantine with the command

        xattr -d com.apple.quarantine <name-of-executable>

as found and detailed at https://stackoverflow.com/questions/60362018/macos-catalinav-10-15-3-error-chromedriver-cannot-be-opened-because-the-de 

#### Using Behave
You can run behave with the command 

        behave

Which will launch the tests in the features folder. Configure behave in the environment.py file, and put your given, when, then statement scenarios into feature files. Each of those will map to a file in the 'steps' directory, where you put the implementation details for the test.



### There is still more to do with this
This still needs more work. There is currently no way to set up admin users, other than using the admin system to change users to 'staff', who could then see a dashboard of orders, and customers. The current dashboard is a placeholder, which only 'is_staff' can see. You can look at this other repo for ideas of how to add visuals to it https://github.com/scharlau/polar_bears_django_visuals based on what you find interesting.

A better version would only allow staff to remove and edit the products too. Ideally, there should be more tests too. It would've made developing these extra parts easier if tests showed where the pages 'broke' as parts were added.
Oh, and the stuff from faker sometimes adds extra characters. Those need to be cleaned up.

##  Doing the Work
Work through the three rounds with a partner, or on your own, depending upon your circumstances. Each round should be twelve minutes, followed by a discussion of where you are and what has been working, as well as, what you're working on next.

You may want to refer to the shop/models.py file to understand the database schema before you get started. Some of you might even want to diagram the schema. 

You might also want to spend a few minutes at the start of each round planning what you might want to do.

You'll see that this version works with the objects in the shop/models.py file to manipulate the data we display on the page. This means we've mostly abstracted away the SQL, and are working with objects for our queries and the dislay of results.

There are some forms here for the products. These add the basic CRUD methods (create, read, update and delete). You could add similar ones for other objects.



## The Exercises

1. Round one should be fixing the order_detail.html page to show names of items and customers, who placed the order. If you have time, then you can also fix the customer_details.html page to show the customer's orders, and let them click through to the order_details.html page, which also needs more details added so customers/staff can see items.
2. Round two should be implementing the 'dashboard' page to show the total value of orders placed by customers.
3. Round three is adding it so that customers can see their own orders.

