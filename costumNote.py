import os
import sys

# Add paths
sys.path.append('/home/pi/pedellus')
sys.path.append('/home/pi/pedellus/uploadfile')

def set_grade_interactive():
    print("Pedellus Grade Setter")
    print("=" * 40)
    
    # Get user inputs
    username = input("Enter username: ").strip()
    if not username:
        print("Username cannot be empty!")
        return
    
    homework = input("Enter homework number: ").strip()
    if not homework.isdigit():
        print("Homework must be a number!")
        return
    homework = int(homework)
    
    grade = input("Enter grade: ").strip()
    if not grade.isdigit():
        print("Grade must be a number!")
        return
    grade = int(grade)
    
    note = input("Enter note: ").strip()
    if not note:
        note = "No note provided"
    
    print(f"\nSummary:")
    print(f"   Username: {username}")
    print(f"   Homework: {homework}")
    print(f"   Grade: {grade}")
    print(f"   Note: {note}")
    
    confirm = input("\nConfirm? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Cancelled!")
        return
    
    # Try to use the actual db_functions with encoding fix
    try:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pedellus.settings')
        import django
        django.setup()
        
        import db_functions
        
        # Fix encoding issue by encoding the note
        note_encoded = note.encode('utf-8', 'ignore').decode('utf-8')
        
        db_functions.savehomework(username, homework, grade, note_encoded)
        print("Success using db_functions!")
        
    except Exception as e:
        print(f"db_functions failed: {e}")
        print("Note: Manual method requires database credentials")

# Run the interactive version
if __name__ == "__main__":
    set_grade_interactive()
