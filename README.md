# 🧪 Python Selenium Test Automation Framework

This is a modular and scalable **test automation framework** built using **Python** and **Selenium WebDriver**. It follows industry best practices such as the **Page Object Model (POM)**, **data-driven testing**, and structured **setup/teardown** routines.

---

## 🚀 Features

- ✅ **Setup and Teardown**
  - Initialize and clean up browser sessions automatically.


- 🧪 **Data-Driven Testing**
  - The framework supports parameterized testing using:
    - pytest.mark.parametrize (manual inline data)
    - Excel files as an external data source (e.g., for login credentials, test inputs, etc.)


- 📌 **Assertions**
  - Validates test outcomes with clear and informative assertion messages.


- 📸 **Screenshot on Failure**
  - Capture screenshots automatically when a test fails (useful for debugging UI failures).


- 📄 **Page Object Model (POM)**
  - Encapsulates page-specific actions and locators in dedicated classes for maintainability.
  

- 📊 **Test Reporting**
  - This framework includes HTML test reporting via the pytest-html plugin.
  - An HTML report is automatically generated in the `results/` directory by adding the following parameter: `--html="results/result.html"`



- 🌐 Browser Support
  - This framework supports running tests on multiple browsers, including Chrome and Firefox, through the command-line option `--driver`.
  - Use the --driver flag when running tests: `pytest test_suites/ --driver=firefox -v --html="results/result.html"`


- ⚙️ Configuration with YAML
  - This framework supports externalizing environment-specific variables using a YAML configuration file
  - Supports running headless mode through `webdriver_visible: False` configuration
---

## ⚙️ Pre-requisites
Before running tests, ensure the following are set up:
* Install google chrome
* Python 3.13.3
* Dependencies installed `pip install -r requirements.txt`
* Chrome web driver added to path environment variable. 
* Firefox web driver added to path environment variable. 
* Verify that the webdriver on the path support your current Chrome/Firefox version

---

## 🧪 How to run the test

##### ✅ Run the entire test suite
<pre>pytest test_suites/ -v"</pre>

##### 📊 Run the entire test suite with HTML results
<pre>pytest test_suites/ -v --html="results/result.html"</pre>

##### 🔍 Run specific test cases with markers
<pre>pytest test_suites/ -v --html="results/result.html" -m 'login_test' </pre>

---

## 📋 Sample Tests Included in This Repo

- **Test Invalid Login**
  - Validates that login fails with invalid credentials.

- **Test Item Add, Update, Delete**
  - Verifies correct behavior for adding, updating, and deleting items.

- **Test Form Submission**
  - Interacts with various input types and validates form submission results.
    
## References
https://github.com/atlassian/dc-app-performance-toolkit/blob/master/app/selenium_ui/base_page.py
