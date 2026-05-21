"""
Database seeder — populates the database with sample books and resources.
Run: python -m app.seed
"""

from .database import SessionLocal, engine, Base
from .models.user import User
from .models.book import Book, BookCondition, BookCategory
from .models.resource import Resource, ResourceType
from .services.auth_service import hash_password

# Ensure tables exist
Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()

    # Create dummy files on disk so they are downloadable (ensure they exist even if DB already has records)
    import os
    os.makedirs("uploads", exist_ok=True)
    sample_files = {
        "uploads/sample_dsa.pdf": ("DSA Complete Notes - Semester 3", "Handwritten notes covering arrays, linked lists, trees, graphs, sorting, and dynamic programming."),
        "uploads/sample_os.pdf": ("Operating Systems PYQ 2020-2024", "Previous Year Questions with solutions for OS course."),
        "uploads/sample_dbms.pdf": ("DBMS Lab Assignment Solutions", "All lab assignments with SQL queries and ER diagrams."),
        "uploads/sample_anatomy.pdf": ("Anatomy Diagrams - Upper Limb", "Detailed diagrams with labels for upper limb anatomy."),
        "uploads/sample_physio.pdf": ("Physiology MCQs with Answers", "500+ MCQs for physiology exam preparation."),
        "uploads/sample_python.pdf": ("Python Programming Cheat Sheet", "Quick reference for Python syntax, data structures, and common patterns."),
        "uploads/sample_accounts.pdf": ("Accounting Standards Summary", "Summary of all important accounting standards for B.Com."),
        "uploads/sample_cat.pdf": ("CAT 2024 Mock Test Paper", "Full-length CAT mock test with answer key.")
    }
    for file_path, (title, desc) in sample_files.items():
        if not os.path.exists(file_path):
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(f"This is a sample study resource file for BookBridge.\n\nTitle: {title}\nDescription: {desc}\n")
                print(f"  Generated dummy file: {file_path}")
            except Exception as e:
                print(f"  Could not create dummy file {file_path}: {e}")

    # Check if already seeded
    if db.query(User).count() > 0:
        print("Database already has data. Skipping seed.")
        db.close()
        return

    print("Seeding database...")

    # ─── Create Demo Users ────────────────────────────────────────
    users = [
        User(
            name="Rahul Sharma",
            email="rahul@bookbridge.com",
            password=hash_password("demo123"),
            college="IIT Delhi",
            year="3rd Year",
            bio="CSE student selling engineering books",
        ),
        User(
            name="Priya Patel",
            email="priya@bookbridge.com",
            password=hash_password("demo123"),
            college="AIIMS Delhi",
            year="2nd Year",
            bio="Medical student sharing resources",
        ),
        User(
            name="Amit Kumar",
            email="amit@bookbridge.com",
            password=hash_password("demo123"),
            college="Delhi University",
            year="Final Year",
            bio="Commerce student, book collector",
        ),
    ]
    db.add_all(users)
    db.commit()
    for u in users:
        db.refresh(u)

    print(f"  Created {len(users)} demo users")

    # ─── Create Sample Books ──────────────────────────────────────
    books = [
        # Engineering
        Book(title="Introduction to Algorithms (CLRS)", author="Cormen, Leiserson, Rivest, Stein", description="The classic CLRS textbook. Covers all major algorithms. 3rd edition, minor highlighting.", price=450, condition=BookCondition.GOOD, category=BookCategory.ENGINEERING, subject="Data Structures & Algorithms", semester="3rd", owner_id=users[0].id),
        Book(title="Engineering Mathematics - I", author="B.S. Grewal", description="Higher Engineering Mathematics. Good condition, all pages intact.", price=280, condition=BookCondition.LIKE_NEW, category=BookCategory.ENGINEERING, subject="Mathematics", semester="1st", owner_id=users[0].id),
        Book(title="Computer Networks", author="Andrew Tanenbaum", description="5th Edition. Great for understanding networking fundamentals.", price=350, condition=BookCondition.GOOD, category=BookCategory.ENGINEERING, subject="Computer Networks", semester="5th", owner_id=users[0].id),
        Book(title="Operating System Concepts", author="Silberschatz, Galvin, Gagne", description="Dinosaur book! 10th edition. Like new condition.", price=520, condition=BookCondition.LIKE_NEW, category=BookCategory.ENGINEERING, subject="Operating Systems", semester="4th", owner_id=users[0].id),
        Book(title="Digital Logic Design", author="Morris Mano", description="4th edition. Minor wear on cover.", price=200, condition=BookCondition.FAIR, category=BookCategory.ENGINEERING, subject="Digital Electronics", semester="2nd", owner_id=users[0].id),

        # Medical
        Book(title="Gray's Anatomy for Students", author="Richard Drake", description="Latest edition. Heavy textbook, must buy for MBBS.", price=1200, condition=BookCondition.LIKE_NEW, category=BookCategory.MEDICAL, subject="Anatomy", semester="1st", owner_id=users[1].id),
        Book(title="Guyton & Hall Textbook of Medical Physiology", author="John E. Hall", description="14th edition. Clean, no markings.", price=950, condition=BookCondition.NEW, category=BookCategory.MEDICAL, subject="Physiology", semester="2nd", owner_id=users[1].id),
        Book(title="Robbins Basic Pathology", author="Kumar, Abbas, Aster", description="10th edition. Some highlighting in early chapters.", price=800, condition=BookCondition.GOOD, category=BookCategory.MEDICAL, subject="Pathology", semester="3rd", owner_id=users[1].id),
        Book(title="Harrison's Principles of Internal Medicine", author="Kasper, Fauci", description="2-volume set. 21st edition. Essential reference.", price=2500, condition=BookCondition.NEW, category=BookCategory.MEDICAL, subject="Medicine", semester="5th", owner_id=users[1].id),

        # Competitive
        Book(title="Quantitative Aptitude for CAT", author="Arun Sharma", description="Latest edition. Practice problems with solutions.", price=320, condition=BookCondition.GOOD, category=BookCategory.COMPETITIVE, subject="Quantitative Aptitude", owner_id=users[2].id),
        Book(title="Word Power Made Easy", author="Norman Lewis", description="Vocabulary building classic. Paperback.", price=150, condition=BookCondition.FAIR, category=BookCategory.COMPETITIVE, subject="English", owner_id=users[2].id),
        Book(title="Indian Polity by M. Laxmikanth", author="M. Laxmikanth", description="6th edition for UPSC. Highlighted important Articles.", price=400, condition=BookCondition.GOOD, category=BookCategory.COMPETITIVE, subject="Political Science", owner_id=users[2].id),

        # Commerce
        Book(title="Financial Accounting", author="T.S. Grewal", description="For B.Com students. Clean copy.", price=250, condition=BookCondition.GOOD, category=BookCategory.COMMERCE, subject="Accounting", semester="1st", owner_id=users[2].id),
        Book(title="Business Statistics", author="S.P. Gupta", description="Statistics textbook with solved examples.", price=300, condition=BookCondition.LIKE_NEW, category=BookCategory.COMMERCE, subject="Statistics", semester="2nd", owner_id=users[2].id),

        # Science
        Book(title="Concepts of Physics - HC Verma (Vol 1 & 2)", author="H.C. Verma", description="Both volumes. Must-have for JEE/NEET prep.", price=380, condition=BookCondition.GOOD, category=BookCategory.SCIENCE, subject="Physics", owner_id=users[0].id),
    ]
    db.add_all(books)
    db.commit()

    print(f"  Created {len(books)} sample books")

    # ─── Create Sample Resources ──────────────────────────────────
    resources = [
        Resource(title="DSA Complete Notes - Semester 3", description="Handwritten notes covering arrays, linked lists, trees, graphs, sorting, and dynamic programming.", file_name="dsa_notes_sem3.pdf", file_path="uploads/sample_dsa.pdf", file_type=ResourceType.NOTES, category="Engineering", subject="Data Structures & Algorithms", semester="3rd", tags="dsa,algorithms,trees,graphs,sorting", download_count=42, uploader_id=users[0].id),
        Resource(title="Operating Systems PYQ 2020-2024", description="Previous Year Questions with solutions for OS course.", file_name="os_pyq.pdf", file_path="uploads/sample_os.pdf", file_type=ResourceType.QUESTION_PAPER, category="Engineering", subject="Operating Systems", semester="4th", tags="os,pyq,exam,scheduling", download_count=67, uploader_id=users[0].id),
        Resource(title="DBMS Lab Assignment Solutions", description="All lab assignments with SQL queries and ER diagrams.", file_name="dbms_lab.pdf", file_path="uploads/sample_dbms.pdf", file_type=ResourceType.ASSIGNMENT, category="Engineering", subject="Database Management", semester="4th", tags="dbms,sql,er-diagram,lab", download_count=31, uploader_id=users[0].id),
        Resource(title="Anatomy Diagrams - Upper Limb", description="Detailed diagrams with labels for upper limb anatomy.", file_name="anatomy_upper_limb.pdf", file_path="uploads/sample_anatomy.pdf", file_type=ResourceType.NOTES, category="Medical", subject="Anatomy", semester="1st", tags="anatomy,diagrams,upper-limb,mbbs", download_count=89, uploader_id=users[1].id),
        Resource(title="Physiology MCQs with Answers", description="500+ MCQs for physiology exam preparation.", file_name="physiology_mcq.pdf", file_path="uploads/sample_physio.pdf", file_type=ResourceType.SOLUTION, category="Medical", subject="Physiology", semester="2nd", tags="physiology,mcq,exam-prep", download_count=55, uploader_id=users[1].id),
        Resource(title="Python Programming Cheat Sheet", description="Quick reference for Python syntax, data structures, and common patterns.", file_name="python_cheatsheet.pdf", file_path="uploads/sample_python.pdf", file_type=ResourceType.PDF, category="Engineering", subject="Programming", tags="python,programming,cheatsheet,coding", download_count=120, uploader_id=users[0].id),
        Resource(title="Accounting Standards Summary", description="Summary of all important accounting standards for B.Com.", file_name="accounting_standards.pdf", file_path="uploads/sample_accounts.pdf", file_type=ResourceType.NOTES, category="Commerce", subject="Accounting", semester="3rd", tags="accounting,standards,bcom", download_count=28, uploader_id=users[2].id),
        Resource(title="CAT 2024 Mock Test Paper", description="Full-length CAT mock test with answer key.", file_name="cat_mock.pdf", file_path="uploads/sample_cat.pdf", file_type=ResourceType.QUESTION_PAPER, category="Competitive", subject="CAT Prep", tags="cat,mock,aptitude,reasoning", download_count=95, uploader_id=users[2].id),
    ]
    db.add_all(resources)
    db.commit()

    # Create dummy files on disk so they are downloadable
    import os
    os.makedirs("uploads", exist_ok=True)
    for r in resources:
        try:
            with open(r.file_path, "w", encoding="utf-8") as f:
                f.write(f"This is a sample study resource file for BookBridge.\n\nTitle: {r.title}\nDescription: {r.description}\nType: {r.file_type}\nCategory: {r.category}\nSubject: {r.subject}\n")
        except Exception as e:
            print(f"  Could not create dummy file {r.file_path}: {e}")

    print(f"  Created {len(resources)} sample resources")
    print("\nDatabase seeded successfully!")
    print("\nDemo login credentials:")
    print("   rahul@bookbridge.com / demo123  (Engineering)")
    print("   priya@bookbridge.com / demo123  (Medical)")
    print("   amit@bookbridge.com  / demo123  (Commerce)")

    db.close()


if __name__ == "__main__":
    seed()
