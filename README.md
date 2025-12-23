# Pet Store API Test Automation

> End-to-end automated API testing framework for the [Pet Store demo API](https://petstore.swagger.io)
## 🛠 Tech Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-000000?style=for-the-badge&logo=python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Allure](https://img.shields.io/badge/Allure-FF4A36?style=for-the-badge&logo=allure&logoColor=white)
![Jenkins](https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=Jenkins&logoColor=white)


---

## 📋 Project Overview

**Professional API testing framework with enterprise integrations:**

- **Pydantic schemas** - Type-safe request/response validation  
- **Allure reporting** - Detailed API call logging and visualization
- **Endpoint architecture** - Clean test design without hardcoded URLs
- **Telegram notifications** with test completion summaries
- **TestOps integration** - Test management and analytics platform
- **Jira workflow** - Issues tracking and sprint integration
- **Jenkins pipeline** integration for automated test execution and reporting

---

## 🚀 Quick Start

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Elias373/api_diploma
cd api_diploma

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# macOS / Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt
```
### ⚙️ Configuration

### **Environment Variables**
Create a `.env` file in the project root directory:

```env
# API Configuration
BASE_URL=https://petstore.swagger.io/v2
```

### Run Tests
```bash
# Run all tests with Allure reporting
pytest --alluredir=allure-results

# Run specific test class
pytest tests/test_pet_resource.py -v
pytest tests/test_store_resource.py -v

# View Allure report
allure serve allure-results
```
---

## ✅ Test Coverage

### Overall Statistics
| Metric | Value             |
|--------|-------------------|
| **Total Tests** | 5                 |
| **Pass Rate** | 100%              |
| **HTTP Methods Covered** | GET, POST, DELETE |
| **Endpoints Tested** | 4                 |

### Detailed Test Breakdown

#### **Pet Resource Tests** (3 tests)
| Test Case | Method | Status | Key Validations |
|-----------|--------|--------|-----------------|
| **Create Pet** | POST | ✅ PASS | ID present, name match, Pydantic schema |
| **Get Pet by ID** | GET | ✅ PASS | ID match, data consistency, schema |
| **Delete Pet** | DELETE | ✅ PASS | Response structure, 404 verification |

#### **Store Resource Tests** (2 tests)  
| Test Case | Method | Status | Key Validations |
|-----------|--------|--------|-----------------|
| **Create Order** | POST | ✅ PASS | Order ID, petId match, schema |
| **Get Order by ID** | GET | ✅ PASS | Order ID match, status validation, schema |
---

### [Jenkins](https://jenkins.autotests.cloud/job/api_diploma/) Build

![Jenkins Build](readme_media/jb.png)
---

### 📊 Report Examples

#### Allure Overview  
![Allure Report](readme_media/ao.png)

#### Test Details with logs
![Test Details](readme_media/atd.png)

#### [TestOps](https://allure.autotests.cloud/project/5047/dashboards) Runs

![TestOps Runs](readme_media/to.png)

#### TestOps Test Cases
![TestOps Test Cases](readme_media/tod.png)

#### [Jira](https://jira.autotests.cloud/browse/HOMEWORK-1560) Integration
![Jira Integration](readme_media/jira.png)


#### Telegram Notification
![Telegram](readme_media/tg.png)

## 👤 Author

**Illia Karcheuski**

[LinkedIn](https://pl.linkedin.com/in/ilyakorchevsky/ru)
