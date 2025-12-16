#!/usr/bin/env python3
"""
Script to add many articles with different authors
"""
import sys
import os
import random
from datetime import datetime, timedelta

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import db
from app.models.article import Article
from app.repositories.user_repository import UserRepository
from app.repositories.category_repository import CategoryRepository
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def slugify(text):
    """Convert text to URL-friendly slug"""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def create_authors():
    """Create multiple author accounts"""
    user_repo = UserRepository()
    
    authors = [
        {'username': 'sarah_johnson', 'email': 'sarah.johnson@news.com', 'first_name': 'Sarah', 'last_name': 'Johnson'},
        {'username': 'michael_chen', 'email': 'michael.chen@news.com', 'first_name': 'Michael', 'last_name': 'Chen'},
        {'username': 'emma_williams', 'email': 'emma.williams@news.com', 'first_name': 'Emma', 'last_name': 'Williams'},
        {'username': 'david_brown', 'email': 'david.brown@news.com', 'first_name': 'David', 'last_name': 'Brown'},
        {'username': 'lisa_anderson', 'email': 'lisa.anderson@news.com', 'first_name': 'Lisa', 'last_name': 'Anderson'},
        {'username': 'james_taylor', 'email': 'james.taylor@news.com', 'first_name': 'James', 'last_name': 'Taylor'},
        {'username': 'olivia_martinez', 'email': 'olivia.martinez@news.com', 'first_name': 'Olivia', 'last_name': 'Martinez'},
        {'username': 'robert_wilson', 'email': 'robert.wilson@news.com', 'first_name': 'Robert', 'last_name': 'Wilson'},
        {'username': 'sophia_thomas', 'email': 'sophia.thomas@news.com', 'first_name': 'Sophia', 'last_name': 'Thomas'},
        {'username': 'william_davis', 'email': 'william.davis@news.com', 'first_name': 'William', 'last_name': 'Davis'},
        {'username': 'jennifer_lee', 'email': 'jennifer.lee@news.com', 'first_name': 'Jennifer', 'last_name': 'Lee'},
        {'username': 'christopher_garcia', 'email': 'christopher.garcia@news.com', 'first_name': 'Christopher', 'last_name': 'Garcia'},
    ]
    
    created_authors = []
    for author_data in authors:
        try:
            # Check if exists
            existing = user_repo.find_by_email(author_data['email'])
            if existing:
                logger.info(f"Author {author_data['username']} already exists")
                created_authors.append(existing)
            else:
                from app.models.user import User
                user = User(
                    username=author_data['username'],
                    email=author_data['email'],
                    password_hash=User.hash_password('password123'),  # Default password
                    first_name=author_data['first_name'],
                    last_name=author_data['last_name'],
                    role='editor'
                )
                user = user_repo.create(user)
                logger.info(f"Created author: {user.username}")
                created_authors.append(user)
        except Exception as e:
            logger.error(f"Error creating author {author_data['username']}: {e}")
    
    return created_authors


def get_article_templates():
    """Return article templates with diverse content"""
    return [
        # Politics
        {'title': 'Presidential Election Results: Key Takeaways', 'category': 'politics', 'content': 'The latest presidential election has concluded with significant implications for national policy. Voters turned out in record numbers, reflecting the high stakes of this election cycle.'},
        {'title': 'Senate Approves Major Infrastructure Bill', 'category': 'politics', 'content': 'In a historic bipartisan vote, the Senate has approved a comprehensive infrastructure bill that allocates billions for transportation, broadband, and clean energy projects.'},
        {'title': 'International Climate Summit Reaches Agreement', 'category': 'politics', 'content': 'World leaders have reached a landmark agreement on climate action, committing to more ambitious emissions reduction targets.'},
        
        # Economy
        {'title': 'Global Markets Reach Record Highs', 'category': 'economy', 'content': 'Stock markets around the world have surged to unprecedented levels, driven by strong corporate earnings and optimistic economic forecasts.'},
        {'title': 'Inflation Rates Stabilize After Months of Increases', 'category': 'economy', 'content': 'Inflation data shows signs of stabilization after months of steady increases, suggesting that monetary policies are taking effect.'},
        {'title': 'Tech Industry Drives Economic Growth', 'category': 'economy', 'content': 'The technology sector continues to be a major driver of economic growth, creating jobs and innovation across multiple industries.'},
        
        # Technology
        {'title': 'Revolutionary AI Model Breaks Language Barriers', 'category': 'technology', 'content': 'A groundbreaking artificial intelligence system has achieved near-instantaneous translation across 100 languages with unprecedented accuracy.'},
        {'title': 'Quantum Computing Breakthrough Achieved', 'category': 'technology', 'content': 'Scientists have successfully demonstrated quantum error correction at a scale that brings practical quantum computing significantly closer to reality.'},
        {'title': 'New Smartphone Features Revolutionize Mobile Experience', 'category': 'technology', 'content': 'Latest smartphone models introduce innovative features that transform how users interact with their devices and access information.'},
        
        # Science
        {'title': 'Mars Mission Returns First Samples to Earth', 'category': 'science', 'content': 'A historic space mission has successfully returned the first samples of Martian rock and soil to Earth, opening new possibilities for understanding the Red Planet.'},
        {'title': 'Breakthrough in Renewable Energy Storage', 'category': 'science', 'content': 'Scientists develop new battery technology that could revolutionize renewable energy storage and make clean energy more reliable.'},
        {'title': 'Ocean Discovery Reveals New Species', 'category': 'science', 'content': 'Deep sea exploration mission uncovers previously unknown marine species in the depths of the ocean, expanding our understanding of biodiversity.'},
        
        # Health
        {'title': 'New Cancer Treatment Shows Promising Results', 'category': 'health', 'content': 'Clinical trials of a novel cancer immunotherapy have shown remarkable results, with over 70% of patients showing significant tumor reduction.'},
        {'title': 'Mental Health Awareness Campaign Launched', 'category': 'health', 'content': 'National campaign aims to reduce stigma around mental health and increase access to treatment and support services.'},
        {'title': 'Breakthrough in Alzheimer\'s Research', 'category': 'health', 'content': 'Researchers identify potential new treatment pathways for Alzheimer\'s disease, offering hope for millions of patients worldwide.'},
        
        # Sports
        {'title': 'Championship Game Breaks Viewership Records', 'category': 'sports', 'content': 'The championship final attracted the largest television audience in the sport\'s history, with millions tuning in worldwide.'},
        {'title': 'Athlete Breaks World Record', 'category': 'sports', 'content': 'In an incredible display of athleticism, the world record has been shattered in dramatic fashion at the international competition.'},
        {'title': 'Team Announces New Coaching Staff', 'category': 'sports', 'content': 'Major team reveals new coaching lineup, bringing decades of combined experience and a fresh perspective to the organization.'},
        
        # Culture
        {'title': 'Major Film Festival Announces Award Winners', 'category': 'culture', 'content': 'The prestigious international film festival concluded with the announcement of its award winners, celebrating cinematic excellence.'},
        {'title': 'New Art Exhibition Opens to Critical Acclaim', 'category': 'culture', 'content': 'Renowned artist\'s latest exhibition opens at the gallery, drawing praise from critics and art enthusiasts alike.'},
        {'title': 'Music Festival Draws Record Crowds', 'category': 'culture', 'content': 'Annual music festival breaks attendance records with performances from top artists and emerging talents.'},
        
        # World
        {'title': 'Global Summit Addresses International Issues', 'category': 'world', 'content': 'World leaders gather to discuss pressing international challenges and coordinate responses to global crises.'},
        {'title': 'Humanitarian Aid Reaches Conflict Zone', 'category': 'world', 'content': 'International aid organizations successfully deliver essential supplies to affected populations in crisis-stricken regions.'},
        {'title': 'Cultural Exchange Program Strengthens Ties', 'category': 'world', 'content': 'International cultural exchange program fosters understanding and collaboration between nations through shared experiences.'},
    ]


def add_many_articles():
    """Add many articles with different authors"""
    try:
        # Create authors
        logger.info("Creating authors...")
        authors = create_authors()
        if not authors:
            logger.error("Failed to create/get authors")
            return False
        
        logger.info(f"Working with {len(authors)} authors")
        
        # Get categories
        category_repo = CategoryRepository()
        categories = category_repo.find_all()
        category_map = {cat.slug: cat.id for cat in categories}
        logger.info(f"Found {len(categories)} categories")
        
        # Get article templates
        templates = get_article_templates()
        
        # Create many articles (50+ articles)
        from app.repositories.article_repository import ArticleRepository
        article_repo = ArticleRepository()
        
        article_count = 0
        
        # Use templates multiple times with variations
        for i in range(60):
            template = templates[i % len(templates)]
            author = random.choice(authors)
            category_slug = template['category']
            category_id = category_map.get(category_slug)
            
            if not category_id:
                logger.warning(f"Category {category_slug} not found, skipping")
                continue
            
            # Create unique title and slug
            title = template['title']
            if i >= len(templates):
                title = f"{template['title']} - Part {i // len(templates) + 1}"
            
            slug = slugify(title)
            if i >= len(templates) or i > 0:
                slug = f"{slug}-{i}-{random.randint(1000, 9999)}"
            
            # Check if article already exists
            try:
                existing = article_repo.find_by_slug(slug)
                if existing:
                    slug = f"{slug}-{random.randint(10000, 99999)}"
            except:
                pass
            
            # Create article
            content = template['content'] + ' ' + template['content'] + ' ' + template['content']  # Make content longer
            excerpt = template['content'][:150] + '...'
            
            article = Article(
                title=title,
                slug=slug,
                content=content,
                excerpt=excerpt,
                author_id=author.id,
                category_id=category_id,
                is_breaking=random.random() > 0.85,  # 15% breaking
                is_premium=random.random() > 0.75,  # 25% premium
                status='published',
                views_count=random.randint(50, 400),
                likes_count=random.randint(5, 60),
                published_at=datetime.now() - timedelta(days=random.randint(0, 30))
            )
            
            try:
                article = article_repo.create(article)
                article_count += 1
                if article_count % 10 == 0:
                    logger.info(f"Created {article_count} articles...")
            except Exception as e:
                logger.error(f"Error creating article {slug}: {e}")
                continue
        
        logger.info(f"Successfully created {article_count} articles!")
        return True
        
    except Exception as e:
        logger.error(f"Error adding articles: {e}", exc_info=True)
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("Adding Many Articles with Different Authors")
    print("=" * 60)
    print()
    
    success = add_many_articles()
    
    if success:
        print()
        print("=" * 60)
        print("SUCCESS!")
        print("=" * 60)
        print("Articles and authors created successfully!")
        print()
    else:
        print()
        print("=" * 60)
        print("ERROR!")
        print("=" * 60)
        print("Failed to create articles. Check the logs above.")
        sys.exit(1)

