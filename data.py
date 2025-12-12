from base.models import Subject, Material, Goal
import logging

logger = logging.getLogger(__name__)

def populate_modular_data():
    """
    Creates and populates Subject, Material, and Goal objects, with 
    Web Development broken down into sequential HTML, CSS, and JS components.
    """
    logger.info("Starting data population with modular components...")

    # --- 1. Web Development Data (Componentized) ---
    logger.info("Adding Web Development (Modular) data...")
    web_dev, created = Subject.objects.get_or_create(
        name="Web Development (Modular)",
        defaults={
            "description": "A structured path starting with foundational HTML, moving to CSS styling, and concluding with JavaScript interactivity."
        }
    )

    ### HTML Step-by-Step Learning
    Material.objects.get_or_create(
        subject=web_dev, 
        title="HTML Full Course for Beginners - Step-by-Step Video", 
        content_type="video", 
        link="https://www.youtube.com/watch?v=k_K9TMJ-Y6w" # FreeCodeCamp's comprehensive HTML course
    )
    Material.objects.get_or_create(
        subject=web_dev, 
        title="MDN HTML Reference & Documentation", 
        content_type="article", 
        link="https://developer.mozilla.org/en-US/docs/Web/HTML"
    )
    Goal.objects.get_or_create(subject=web_dev, description="Build a multi-page website structure using semantic HTML5 tags (e.g., <header>, <main>, <article>, <footer>)", points=10)


    ### CSS Step-by-Step Learning
    Material.objects.get_or_create(
        subject=web_dev, 
        title="CSS Step-by-Step Tutorial & Complete Guide (Playlist)", 
        content_type="video", 
        link="https://www.youtube.com/playlist?list=PL4-IK0AVrVjNCgM_S0f146W4Xv-F82N0b" # The Net Ninja's structured CSS course
    )
    Material.objects.get_or_create(
        subject=web_dev, 
        title="CSS Flexbox/Grid Documentation (A Visual Guide)", 
        content_type="article", 
        link="https://css-tricks.com/snippets/css/a-guide-to-flexbox/"
    )
    Goal.objects.get_or_create(subject=web_dev, description="Style a layout using either CSS Flexbox or CSS Grid for full responsiveness", points=15)


    ### JavaScript Step-by-Step Learning
    Material.objects.get_or_create(
        subject=web_dev, 
        title="JavaScript Fundamental Concepts - Full Step-by-Step Playlist", 
        content_type="video", 
        link="https://www.youtube.com/playlist?list=PLsyeobzWxl7qtP8Lo9TLiFJGqPNxW6wVf" # Programiz's structured JS fundamentals
    )
    Material.objects.get_or_create(
        subject=web_dev, 
        title="The Modern JavaScript Tutorial (Comprehensive Docs)", 
        content_type="article", 
        link="https://javascript.info/"
    )
    Goal.objects.get_or_create(subject=web_dev, description="Manipulate the DOM by adding, removing, and modifying elements based on user interaction (e.g., a simple To-Do list app)", points=25)

    
    # --- 2. Data Science Data (Remaining the same) ---
    logger.info("Adding Data Science data...")
    data_sci, created = Subject.objects.get_or_create(
        name="Data Science (Python & ML)",
        defaults={
            "description": "A comprehensive journey through Python, Pandas, Data Analysis, and Machine Learning fundamentals."
        }
    )
    Material.objects.get_or_create(
        subject=data_sci, 
        title="Python for Beginners - Full Step-by-Step Playlist", 
        content_type="video", 
        link="https://learn.microsoft.com/en-us/shows/intro-to-python-development/"
    )
    Material.objects.get_or_create(
        subject=data_sci, 
        title="Data Science Full Course For Beginners (Codebasics Playlist)", 
        content_type="video", 
        link="https://www.youtube.com/playlist?list=PLeo1K3SDF_yTwfWh4PD7VqFjOqK0hG-VP"
    )
    Goal.objects.get_or_create(subject=data_sci, description="Complete the Python basics module and write an object-oriented class", points=10)
    Goal.objects.get_or_create(subject=data_sci, description="Clean and pre-process a raw dataset using the Pandas library", points=25)
    Goal.objects.get_or_create(subject=data_sci, description="Implement and evaluate a simple Linear Regression model on a dataset", points=45)


    # --- 3. Graphic Design Data (Remaining the same) ---
    logger.info("Adding Graphic Design data...")
    design, created = Subject.objects.get_or_create(
        name="Graphic Design (Theory & Practice)",
        defaults={
            "description": "Mastering the core principles of visual communication, typography, and composition before diving into tool usage."
        }
    )
    Material.objects.get_or_create(
        subject=design, 
        title="Fundamentals of Graphic Design - Course Modules (Coursera/CalArts)", 
        content_type="article", 
        link="https://www.coursera.org/learn/fundamentals-of-graphic-design"
    )
    Material.objects.get_or_create(
        subject=design, 
        title="Figma for UI/UX Design - Full Course (Video)", 
        content_type="video", 
        link="https://www.youtube.com/watch?v=Guo9402l2E0"
    )
    Goal.objects.get_or_create(subject=design, description="Explain and apply the principles of Color Theory (e.g., complementary, analogous)", points=15)
    Goal.objects.get_or_create(subject=design, description="Design a mobile screen prototype in Figma using a 4-column grid system", points=30)
    Goal.objects.get_or_create(subject=design, description="Create a cohesive brand identity (logo, color palette, typography) for a fictional business", points=50)
    
    
    # --- 4. Wildcard Course: Critical Thinking (Remaining the same) ---
    logger.info("Adding Wildcard: Critical Thinking data...")
    wildcard, created = Subject.objects.get_or_create(
        name="Wildcard: Critical Thinking & Logic",
        defaults={
            "description": "General knowledge focused on developing analytical, logical, and effective decision-making skills applicable to all fields."
        }
    )
    Material.objects.get_or_create(
        subject=wildcard, 
        title="Critical Thinking: The Basics (Playlist)", 
        content_type="video", 
        link="https://www.youtube.com/playlist?list=PL_J4hVndP-d_b5z550sT64qQk9r81T0V6"
    )
    Material.objects.get_or_create(
        subject=wildcard, 
        title="Introduction to Logic and Arguments (Article)", 
        content_type="article", 
        link="https://plato.stanford.edu/entries/logic-classical/"
    )
    Goal.objects.get_or_create(subject=wildcard, description="Identify the key components (premise and conclusion) of a complex argument", points=10)
    Goal.objects.get_or_create(subject=wildcard, description="Write a short essay analyzing a common logical fallacy (e.g., Ad Hominem, Straw Man)", points=25)
    Goal.objects.get_or_create(subject=wildcard, description="Apply a decision matrix to evaluate a complex personal or professional choice", points=35)

    logger.info("✅ SUCCESS: Modular and step-by-step dummy data population is complete!")

# Example of how to run this function in a Django shell or management command:
# populate_modular_data()