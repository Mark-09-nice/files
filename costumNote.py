import os
import sys

# Add paths
sys.path.append('/home/pi/pedellus')
sys.path.append('/home/pi/pedellus/uploadfile')

def set_grade_interactive():
    print("🎓 Pedellus Grade Setter")
    print("=" * 40)
    
    # Get user inputs
    username = input("Enter username: ").strip()
    if not username:
        print("❌ Username cannot be empty!")
        return
    
    homework = input("Enter homework number: ").strip()
    if not homework.isdigit():
        print("❌ Homework must be a number!")
        return
    homework = int(homework)
    
    grade = input("Enter grade: ").strip()
    if not grade.isdigit():
        print("❌ Grade must be a number!")
        return
    grade = int(grade)
    
    note = input("Enter note: ").strip()
    if not note:
        note = "No note provided"
    
    print(f"\n📋 Summary:")
    print(f"   Username: {username}")
    print(f"   Homework: {homework}")
    print(f"   Grade: {grade}")
    print(f"   Note: {note}")
    
    confirm = input("\n✅ Confirm? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled!")
        return
    
    # Try to use the actual db_functions
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pedellus.settings')
        import django
        django.setup()
        
        import db_functions
        db_functions.savehomework(username, homework, grade, note)
        print("🎉 Success using db_functions!")
        
    except Exception as e:
        print(f"❌ db_functions failed: {e}")
        print("Falling back to manual method...")
        
        # Manual fallback method
        try:
            import MySQLdb
            
            # Update these with your actual database credentials
            db = MySQLdb.connect(
                host="localhost", 
                user="your_db_user",      # Change this
                passwd="your_db_password", # Change this  
                db="pedellus"
            )
            cursor = db.cursor()
            
            # Get user info
            cursor.execute("SELECT user_id, class_id FROM users WHERE username = %s", [username])
            user_row = cursor.fetchone()
            if not user_row:
                print(f"❌ User {username} not found!")
                return
                
            user_id, class_id = user_row
            
            # Get homework ID
            cursor.execute("SELECT hw_id FROM homework WHERE class_id = %s AND homework_number = %s", 
                          (class_id, homework))
            hw_row = cursor.fetchone()
            if not hw_row:
                print(f"❌ Homework {homework} not found for user's class!")
                return
                
            hw_id = hw_row[0]
            
            # Insert/update grade
            sql = """INSERT INTO grades (user_id, hw_id, grade, note) 
                     VALUES (%s, %s, %s, %s) 
                     ON DUPLICATE KEY UPDATE grade = %s, note = %s"""
            
            cursor.execute(sql, (user_id, hw_id, grade, note, grade, note))
            db.commit()
            db.close()
            
            print("🎉 Success using manual method!")
            
        except Exception as e2:
            print(f"❌ Manual method also failed: {e2}")

# Run the interactive version
if __name__ == "__main__":
    set_grade_interactive()
