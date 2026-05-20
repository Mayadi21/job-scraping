import os
import csv
import time
import random
import requests

API_URL = "https://glints.com/api/v2-alc/graphql?op=searchJobsV3"

HEADERS = {
    "Content-Type": "application/json",
    "Accept": "*/*",
    "Origin": "https://glints.com",
    "Referer": "https://glints.com/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36",
    "Cookie": 'device_id=14d3a36f-630d-4e15-80a7-b59bfdc5cb4f; _gcl_au=1.1.1993335785.1777521879; sessionFirstTouchPath=/id/en/companies/nbs-nusantara-beta-studio/134754bf-02a8-48c6-84e0-ab0c3f2e8246; _ga=GA1.1.1545325466.1777521879; airbridge_migration_metadata__taplokerbyglints=%7B%22version%22%3A%221.11.7%22%7D; ab180ClientId=86c14530-c3f8-4e36-90a9-422dfdcfb4e8; country=ID; language=en; builderSessionId=f024cac873c94fdb824e2a874df432ad; glints_tracking_id=fba6f2f4-ccb0-49a9-9f3a-6362408487e7; sessionLastTouchPath=/id/en; sessionIsLastTouch=false; g_state={"i_l":0,"i_ll":1777740411147,"i_e":{"enable_itp_optimization":0},"i_et":1777521880714,"i_b":"rb8hTa3u1aE4VEKH2Zbf8W9l4I6cwtR/c1a4KYLCRIw"}; session=Fe26.2**a6a8da93382d70775923c7fe8b3a643ba255a6b8f5c4260d681994d897104dd0*nuYrYdgrupnHKZIGkKQXTw*ptzsNYCp3afC80Czxl0JVg07cOAFpzskIOZo1cYAJBXqhqpUbBrXONHLoHPbgOlN**99d453cb64c614c7066923e746d4d6ed8ff2650951f4b3b0c3e1f0b12bd7a19e*aPhxGY6XX3MSKSxYZgEnGvJP3rtMoe9Y-bStVkDskdM; airbridge_user__taplokerbyglints=%7B%22externalUserID%22%3A%220faef191-d2e5-41a2-85a3-532a3cb746a6%22%2C%22externalUserEmail%22%3A%22putraalamsyah2108@gmail.com%22%2C%22externalUserPhone%22%3Anull%2C%22alias%22%3A%7B%7D%2C%22attributes%22%3A%7B%22country_code%22%3A%22ID%22%2C%22role%22%3A%22CANDIDATE%22%2C%22has_whatsapp_number%22%3Atrue%2C%22user_email%22%3A%22putraalamsyah2108@gmail.com%22%2C%22days_from_signup%22%3A1%2C%22has_resume%22%3Atrue%2C%22has_mobile_number%22%3Atrue%2C%22age_in_years%22%3Anull%2C%22gender%22%3A%22%22%2C%22number_of_skills_listed%22%3A0%7D%7D; currentJobID=7acabc01-d58c-4ecb-a42c-b75102c8eb7f; traceInfo=%7B%22expInfo%22%3A%22%22%2C%22requestId%22%3A%2244a23dc4ad26e0c8ec4c55d0e9c7dea9%22%7D; _ga_FQ75P4PXDH=GS2.1.s1777738767$o9$g1$t1777740529$j58$l0$h0; airbridge_touchpoint__taplokerbyglints=%7B%22channel%22%3A%22www.google.com%22%2C%22parameter%22%3A%7B%7D%2C%22generationType%22%3A1224%2C%22url%22%3A%22https%3A//glints.com/id/en/opportunities/jobs/recommended%22%2C%22timestamp%22%3A1777740529949%7D; airbridge_session__taplokerbyglints=%7B%22id%22%3A%22338af107-b7a2-4cf7-8740-526e8cdf4fdf%22%2C%22timeout%22%3A1800000%2C%22start%22%3A1777738768063%2C%22end%22%3A1777740529956%7D',
}

GRAPHQL_QUERY = """
query searchJobsV3($data: JobSearchConditionInput!) {
  searchJobsV3(data: $data) {
    jobsInPage {
      id
      title
      workArrangementOption
      minYearsOfExperience
      educationLevel
      type
      company { industry { name } }
      hierarchicalJobCategory {
        name
        level
        parents { name level }
      }
      salaries { salaryMode minAmount maxAmount }
      skills { skill { name } }
    }
    hasMore
  }
}
"""

def scrape_latest_jobs():
    print("=== MEMULAI SCRAPING POSTINGAN TERBARU ===")
    
    csv_file = 'postingan_terbaru.csv'
    max_pages = 25
    file_exists = os.path.isfile(csv_file)
    
    existing_links = set()
    if file_exists:
        try:
            with open(csv_file, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader, None)
                for row in reader:
                    if row:
                        existing_links.add(row[0])
            print(f"[*] Memuat {len(existing_links)} tautan lama dari CSV.")
        except Exception as e:
            print(f"[!] Gagal membaca file lama: {e}")

    with open(csv_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        
        if not file_exists:
            writer.writerow(["Job_Link", "Title", "Industry", "Job_Category_parent", "Job_Category", "Salary_Mode", "Min_Salary", "Max_Salary", "Skills", "Job_Type", "Work Arrangement", "Education", "Experience"])

        for page in range(1, max_pages + 1):
            print(f"Mengambil halaman {page}...")
            payload = {
                "operationName": "searchJobsV3",
                "query": GRAPHQL_QUERY,
                "variables": {
                    "data": {
                        "CountryCode": "ID",
                        "sortBy": "LATEST",                  
                        "lastUpdatedAtRange": "ANY_TIME",    
                        "includeExternalJobs": True,
                        "pageSize": 30,
                        "page": page
                    }
                }
            }
            
            try:
                response = requests.post(API_URL, json=payload, headers=HEADERS, timeout=15)
                if response.status_code != 200:
                    print(f"Status {response.status_code}, berhenti.")
                    break
                    
                search_results = response.json().get('data', {}).get('searchJobsV3', {})
                jobs = search_results.get('jobsInPage', [])
                
                if not jobs:
                    break
                    
                added_count = 0
                for job in jobs:
                    job_id = job.get('id', '')
                    job_link = f"https://glints.com/id/opportunities/jobs/{job_id}"
                    
                    if job_link in existing_links:
                        continue
                    
                    title = job.get('title', 'N/A')
                    company_data = job.get('company') or {}
                    industry_name = (company_data.get('industry') or {}).get('name', 'N/A')
                    category_data = job.get('hierarchicalJobCategory') or {}
                    category_now = category_data.get('name', 'N/A')
                    parents = category_data.get('parents') or []
                    category_parent = parents[0].get('name', 'N/A') if parents else 'N/A'
                    
                    salaries = job.get('salaries') or []
                    if salaries:
                        salary_mode = salaries[0].get('salaryMode', 'N/A')
                        min_salary = salaries[0].get('minAmount', 0)
                        max_salary = salaries[0].get('maxAmount', 0)
                    else:
                        salary_mode, min_salary, max_salary = 'N/A', 0, 0
                        
                    skills_list = job.get('skills') or []
                    skills_str = ", ".join([s.get('skill', {}).get('name', '') for s in skills_list if isinstance(s, dict) and s.get('skill')])
                    
                    writer.writerow([
                        job_link, title, industry_name, category_parent, category_now,
                        salary_mode, min_salary, max_salary, skills_str,
                        job.get('type', 'N/A'), job.get('workArrangementOption', 'N/A'),
                        job.get('educationLevel', 'N/A'), job.get('minYearsOfExperience', 0)
                    ])
                    existing_links.add(job_link)
                    added_count += 1

                print(f"Halaman {page}: Menambahkan {added_count} data baru.")
                if not search_results.get('hasMore', False):
                    break
                    
                time.sleep(random.uniform(2.0, 4.0))
            except Exception as e:
                print(f"Koneksi error: {e}")
                break

if __name__ == "__main__":
    scrape_latest_jobs()
