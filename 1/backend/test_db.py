import pymysql

# Test database connection
passwords = ['', '123456', 'root', 'admin', 'password', '123', '1234', '12345', '12345678', 'mysql']

for password in passwords:
    try:
        print(f"Trying password '{password}'...")
        conn = pymysql.connect(
            host='localhost',
            user='root',
            password=password,
            port=3306
        )
        print("Connection successful!")
        
        # Create database
        with conn.cursor() as cursor:
            cursor.execute("CREATE DATABASE IF NOT EXISTS navdb;")
            print("Database created successfully!")
        
        conn.close()
        break
    except Exception as e:
        print(f"Connection failed: {str(e)}")

