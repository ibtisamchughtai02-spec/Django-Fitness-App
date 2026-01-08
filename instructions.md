CPAN 214 Final Project Requirements
Prolog: Think of this project as more than just another assignment — it’s your chance to build something real, something you can actually show off to future employers. By designing and presenting a Python with Django app, you’ll practice the same skills developers use every day: breaking down requirements, modeling data, writing secure code, and creating a user-friendly interface. Humber’s Learning Outcomes emphasize clarity, and adaptability, and this project gives you all these in one package. When you finish, you won’t just understand Python programming and Django web design better — you’ll have a portfolio-ready example that proves you can take an idea, make it secure, and turn it into a working application as a solution in any organization!

Students are expected to adopt and adapt any project of their choice that satisfy all the following criteria. The project must demonstrate mastery of Python and Django as high-level programming tools, enforce secure programming practices, and that aligns with CPAN 214’s learning outcomes.

Project Overview
Students will design and implement a 3-tier Python-Django application that integrates:
    •Presentation Layer (GUI) using Django templates, forms, and CSS.
    •Logic Layer enforcing Django’s Model-View-Template (MVT) paradigm.
    •Data Layer using MySQL with Django ORM for persistence.

The project must demonstrate mastery of:
    •Python programming (functions, OOP, inheritance).
    •Django web development (templates, models, migrations).
    •Secure coding practices (CSRF, XSS, SQL injection prevention).
    •Usability and aesthetics in GUI design.


1. Analysis & Class Diagram (15%)
Deliverables:
    •Project description with UML class, sequence, and Django model diagrams.
    •At least one composition or one-to-many relationship (e.g., User → Transactions, Book → Orders).
    •Explicit mapping of MVT architecture (Models, Views, Templates).

2. Django–MySQL Data Models & Integration (50%)
Students will design and implement a data layer that integrates seamlessly with Django’s MVT architecture. The focus is on programmatic modeling, integrity enforcement, and secure persistence, rather than raw database administration.
Deliverables:

1.Relational Data Models (via Django ORM)
    •Define at least 3 related models (e.g., User, Account, Transaction) with clear relationships (one-to-many, composition).
    •Use Django’s migrations to generate schema automatically, ensuring consistency between code and database.

2.Data Integrity Enforcement
    •Apply domain integrity (field types, validation rules in Django forms/models).
    •Apply entity integrity (primary keys, unique constraints).
    •Apply referential integrity (foreign keys, on_delete behaviors in Django models).
    •Demonstrate validation logic in Python (e.g., custom model validators, form validation).

3.Advanced Features (High-Level Programming Context)
    •Incorporate views (Django ORM queries wrapped in reusable functions).
    •Use indexes where performance optimization is needed (via Django Meta options).
    •Implement stored procedures/triggers equivalents through Django signals (e.g., post_save to enforce business rules).
    •Showcase how these constructs are integrated programmatically rather than manually managed in SQL.

4.Data Files Integration
    •Import/export data from at least 3 file formats (CSV, JSON, text) using Python libraries (csv, json, pandas).
    •Demonstrate how Django models handle persistence and transformation of these data files.


3. Presentation Layer (25%)
Deliverables:
•Django-based GUI using HTML templates, forms, and CSS.
•Navigation must be intuitive (clear menus, consistent layout).
•CRUD operations implemented securely via Django ORM (no raw SQL).

•Security enforcement:
    •CSRF protection via Django middleware.
    •Input validation and escaping to prevent XSS.
    •ORM-based queries to prevent SQL injection.

•Aesthetic requirements:
    •Articulate, professional design.
    •Consistent use of CSS for styling and layout.
    •User-friendly forms with validation feedback.



4. Final Submission & Presentation (10%)
Deliverables:
•5-minute video presentation including:
    •Schema overview (class diagram + database schema).
    •Architecture explanation (MVT layers).
    •Demonstration of CRUD operations in Django
    •Showcase of GUI aesthetics and navigation.