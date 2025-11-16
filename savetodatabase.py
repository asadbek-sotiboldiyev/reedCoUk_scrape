

def savetodb(job_data, conn):
    
    try:
        cursor = conn.cursor()

        create_table_query = """
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'JobListings')
        BEGIN
            CREATE TABLE JobListings (
                JobID INT,
                Posted_date NVARCHAR(100),
                Job_Title_from_List NVARCHAR(255),
                Job_Title NVARCHAR(255),
                Company NVARCHAR(255),
                Company_Logo_URL NVARCHAR(MAX),
                Country NVARCHAR(50),
                Location NVARCHAR(255),
                Skills NVARCHAR(MAX),
                Salary_Info NVARCHAR(255),
                Source NVARCHAR(255)
            )
        END
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Insert data into the table
        insert_query = """
        INSERT INTO JobListings (JobID, Posted_date, Job_Title_from_List, Job_Title, Company, Company_Logo_URL, Country, Location, Skills, Salary_Info, Source)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        for idx, job in job_data.iterrows():
            try:
                print("savetodb: inserting row:", job['Job Title'], '|', job['Company'])
                cursor.execute(insert_query, 
                               idx,
                               job['Posted_date'], 
                               job['Job Title from List'], 
                               job['Job Title'], 
                               job['Company'], 
                               job['Company Logo URL'], 
                               job['Country'], 
                               job['Location'], 
                               job['Skills'], 
                               job['Salary Info'], 
                               job['Source'])
            except Exception as row_error:
                print(f"Failed to insert row {idx}: {row_error}")

        conn.commit()
        print("Data saved to SQL Server")

    except Exception as e:
        print(f"Failed to save data to SQL Server: {e}")


def failed_jobs_log(job_data, conn):
    '''
    scrape qilishda muammo bo'lgan rowlarni alohida tablega yozish 
    '''
    try:
        cursor = conn.cursor()

        create_table_query = """
        IF NOT EXISTS (SELECT * FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'failed_reedco_jobs_log')
        BEGIN
            create table failed_reedco_jobs_log (
                id int IDENTITY,
                jobId int,
                job_title_from_list nvarchar(255),
                job_title NVARCHAR(255),
                fail_cause nvarchar(max),
                
                created_at DATETIME default GETDATE(),
            )
        END
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Insert data into the table
        insert_query = """
        INSERT INTO failed_reedco_jobs_log (jobid, job_title_from_list, job_title, fail_cause)
        VALUES (?, ?, ?, ?)
        """

        for idx, job in job_data.iterrows():
            try:
                print("failed jobs savetodb: inserting row")
                print(job)
                parameters = (
                    job['jobid'], 
                    job['job_title_from_list'], 
                    job['job_title'], 
                    job['fail_cause']
                )
                cursor.execute(insert_query,  parameters)
            except Exception as row_error:
                print(f"Failed to insert row {idx}: {row_error}")

        conn.commit()
        print("Log saved to SQL Server")

    except Exception as e:
        print(f"Failed to save LOG to SQL Server: {e}")

    finally:
        cursor.close()
        conn.close()
