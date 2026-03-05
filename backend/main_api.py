import uvicorn
import os, json
import time as time_module
import logging
from fastapi import Depends, FastAPI, HTTPException, Request, status, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic_classes import *
from sql_alchemy import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

############################################
#
#   Initialize the database
#
############################################

def init_db():
    SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./data/Class_Diagram.db")
    # Ensure local SQLite directory exists (safe no-op for other DBs)
    os.makedirs("data", exist_ok=True)
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        pool_size=10,
        max_overflow=20,
        pool_pre_ping=True,
        echo=False
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    return SessionLocal

app = FastAPI(
    title="Class_Diagram API",
    description="Auto-generated REST API with full CRUD operations, relationship management, and advanced features",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=[
        {"name": "System", "description": "System health and statistics"},
        {"name": "Institution", "description": "Operations for Institution entities"},
        {"name": "Institution Relationships", "description": "Manage Institution relationships"},
        {"name": "Author", "description": "Operations for Author entities"},
        {"name": "Author Relationships", "description": "Manage Author relationships"},
        {"name": "Publication", "description": "Operations for Publication entities"},
        {"name": "Publication Relationships", "description": "Manage Publication relationships"},
        {"name": "Conference", "description": "Operations for Conference entities"},
        {"name": "Proceedings", "description": "Operations for Proceedings entities"},
        {"name": "Book", "description": "Operations for Book entities"},
        {"name": "Thesis", "description": "Operations for Thesis entities"},
        {"name": "Others", "description": "Operations for Others entities"},
        {"name": "Journal", "description": "Operations for Journal entities"},
    ]
)

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or restrict to ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

############################################
#
#   Middleware
#
############################################

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests and responses."""
    logger.info(f"Incoming request: {request.method} {request.url.path}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to all responses."""
    start_time = time_module.time()
    response = await call_next(request)
    process_time = time_module.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

############################################
#
#   Exception Handlers
#
############################################

# Global exception handlers
@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    """Handle ValueError exceptions."""
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": "Bad Request",
            "message": str(exc),
            "detail": "Invalid input data provided"
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Handle database integrity errors."""
    logger.error(f"Database integrity error: {exc}")

    # Extract more detailed error information
    error_detail = str(exc.orig) if hasattr(exc, 'orig') else str(exc)

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "Conflict",
            "message": "Data conflict occurred",
            "detail": error_detail
        }
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError):
    """Handle general SQLAlchemy errors."""
    logger.error(f"Database error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "message": "Database operation failed",
            "detail": "An internal database error occurred"
        }
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions with consistent format."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail if isinstance(exc.detail, str) else "HTTP Error",
            "message": exc.detail,
            "detail": f"HTTP {exc.status_code} error occurred"
        }
    )

# Initialize database session
SessionLocal = init_db()
# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        logger.error("Database session rollback due to exception")
        raise
    finally:
        db.close()

############################################
#
#   Global API endpoints
#
############################################

@app.get("/", tags=["System"])
def root():
    """Root endpoint - API information"""
    return {
        "name": "Class_Diagram API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health", tags=["System"])
def health_check():
    """Health check endpoint for monitoring"""
    from datetime import datetime
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected"
    }


@app.get("/statistics", tags=["System"])
def get_statistics(database: Session = Depends(get_db)):
    """Get database statistics for all entities"""
    stats = {}
    stats["institution_count"] = database.query(Institution).count()
    stats["author_count"] = database.query(Author).count()
    stats["publication_count"] = database.query(Publication).count()
    stats["conference_count"] = database.query(Conference).count()
    stats["proceedings_count"] = database.query(Proceedings).count()
    stats["book_count"] = database.query(Book).count()
    stats["thesis_count"] = database.query(Thesis).count()
    stats["others_count"] = database.query(Others).count()
    stats["journal_count"] = database.query(Journal).count()
    stats["total_entities"] = sum(stats.values())
    return stats


############################################
#
#   BESSER Action Language standard lib
#
############################################


async def BAL_size(sequence:list) -> int:
    return len(sequence)

async def BAL_is_empty(sequence:list) -> bool:
    return len(sequence) == 0

async def BAL_add(sequence:list, elem) -> None:
    sequence.append(elem)

async def BAL_remove(sequence:list, elem) -> None:
    sequence.remove(elem)

async def BAL_contains(sequence:list, elem) -> bool:
    return elem in sequence

async def BAL_filter(sequence:list, predicate) -> list:
    return [elem for elem in sequence if predicate(elem)]

async def BAL_forall(sequence:list, predicate) -> bool:
    for elem in sequence:
        if not predicate(elem):
            return False
    return True

async def BAL_exists(sequence:list, predicate) -> bool:
    for elem in sequence:
        if predicate(elem):
            return True
    return False

async def BAL_one(sequence:list, predicate) -> bool:
    found = False
    for elem in sequence:
        if predicate(elem):
            if found:
                return False
            found = True
    return found

async def BAL_is_unique(sequence:list, mapping) -> bool:
    mapped = [mapping(elem) for elem in sequence]
    return len(set(mapped)) == len(mapped)

async def BAL_map(sequence:list, mapping) -> list:
    return [mapping(elem) for elem in sequence]

async def BAL_reduce(sequence:list, reduce_fn, aggregator) -> any:
    for elem in sequence:
        aggregator = reduce_fn(aggregator, elem)
    return aggregator


############################################
#
#   Institution functions
#
############################################

@app.get("/institution/", response_model=None, tags=["Institution"])
def get_all_institution(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Institution)
        institution_list = query.all()

        # Serialize with relationships included
        result = []
        for institution_item in institution_list:
            item_dict = institution_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            publication_list = database.query(Publication).join(publication_institution, Publication.id == publication_institution.c.publication).filter(publication_institution.c.institution_1 == institution_item.id).all()
            item_dict['publication'] = []
            for publication_obj in publication_list:
                publication_dict = publication_obj.__dict__.copy()
                publication_dict.pop('_sa_instance_state', None)
                item_dict['publication'].append(publication_dict)
            author_list = database.query(Author).join(author_institution, Author.id == author_institution.c.author).filter(author_institution.c.institution == institution_item.id).all()
            item_dict['author'] = []
            for author_obj in author_list:
                author_dict = author_obj.__dict__.copy()
                author_dict.pop('_sa_instance_state', None)
                item_dict['author'].append(author_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Institution).all()


@app.get("/institution/count/", response_model=None, tags=["Institution"])
def get_count_institution(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Institution entities"""
    count = database.query(Institution).count()
    return {"count": count}


@app.get("/institution/paginated/", response_model=None, tags=["Institution"])
def get_paginated_institution(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Institution entities"""
    total = database.query(Institution).count()
    institution_list = database.query(Institution).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": institution_list
        }

    result = []
    for institution_item in institution_list:
        publication_ids = database.query(publication_institution.c.publication).filter(publication_institution.c.institution_1 == institution_item.id).all()
        author_ids = database.query(author_institution.c.author).filter(author_institution.c.institution == institution_item.id).all()
        item_data = {
            "institution": institution_item,
            "publication_ids": [x[0] for x in publication_ids],
            "author_ids": [x[0] for x in author_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/institution/search/", response_model=None, tags=["Institution"])
def search_institution(
    database: Session = Depends(get_db)
) -> list:
    """Search Institution entities by attributes"""
    query = database.query(Institution)


    results = query.all()
    return results


@app.get("/institution/{institution_id}/", response_model=None, tags=["Institution"])
async def get_institution(institution_id: int, database: Session = Depends(get_db)) -> Institution:
    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    publication_ids = database.query(publication_institution.c.publication).filter(publication_institution.c.institution_1 == db_institution.id).all()
    author_ids = database.query(author_institution.c.author).filter(author_institution.c.institution == db_institution.id).all()
    response_data = {
        "institution": db_institution,
        "publication_ids": [x[0] for x in publication_ids],
        "author_ids": [x[0] for x in author_ids],
}
    return response_data



@app.post("/institution/", response_model=None, tags=["Institution"])
async def create_institution(institution_data: InstitutionCreate, database: Session = Depends(get_db)) -> Institution:

    if institution_data.publication:
        for id in institution_data.publication:
            # Entity already validated before creation
            db_publication = database.query(Publication).filter(Publication.id == id).first()
            if not db_publication:
                raise HTTPException(status_code=404, detail=f"Publication with ID {id} not found")
    if institution_data.author:
        for id in institution_data.author:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            if not db_author:
                raise HTTPException(status_code=404, detail=f"Author with ID {id} not found")

    db_institution = Institution(
        city=institution_data.city,        name=institution_data.name,        country=institution_data.country        )

    database.add(db_institution)
    database.commit()
    database.refresh(db_institution)


    if institution_data.publication:
        for id in institution_data.publication:
            # Entity already validated before creation
            db_publication = database.query(Publication).filter(Publication.id == id).first()
            # Create the association
            association = publication_institution.insert().values(institution_1=db_institution.id, publication=db_publication.id)
            database.execute(association)
            database.commit()
    if institution_data.author:
        for id in institution_data.author:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            # Create the association
            association = author_institution.insert().values(institution=db_institution.id, author=db_author.id)
            database.execute(association)
            database.commit()


    publication_ids = database.query(publication_institution.c.publication).filter(publication_institution.c.institution_1 == db_institution.id).all()
    author_ids = database.query(author_institution.c.author).filter(author_institution.c.institution == db_institution.id).all()
    response_data = {
        "institution": db_institution,
        "publication_ids": [x[0] for x in publication_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.post("/institution/bulk/", response_model=None, tags=["Institution"])
async def bulk_create_institution(items: list[InstitutionCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Institution entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_institution = Institution(
                city=item_data.city,                name=item_data.name,                country=item_data.country            )
            database.add(db_institution)
            database.flush()  # Get ID without committing
            created_items.append(db_institution.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Institution entities"
    }


@app.delete("/institution/bulk/", response_model=None, tags=["Institution"])
async def bulk_delete_institution(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Institution entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_institution = database.query(Institution).filter(Institution.id == item_id).first()
        if db_institution:
            database.delete(db_institution)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Institution entities"
    }

@app.put("/institution/{institution_id}/", response_model=None, tags=["Institution"])
async def update_institution(institution_id: int, institution_data: InstitutionCreate, database: Session = Depends(get_db)) -> Institution:
    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    setattr(db_institution, 'city', institution_data.city)
    setattr(db_institution, 'name', institution_data.name)
    setattr(db_institution, 'country', institution_data.country)
    existing_publication_ids = [assoc.publication for assoc in database.execute(
        publication_institution.select().where(publication_institution.c.institution_1 == db_institution.id))]

    publications_to_remove = set(existing_publication_ids) - set(institution_data.publication)
    for publication_id in publications_to_remove:
        association = publication_institution.delete().where(
            (publication_institution.c.institution_1 == db_institution.id) & (publication_institution.c.publication == publication_id))
        database.execute(association)

    new_publication_ids = set(institution_data.publication) - set(existing_publication_ids)
    for publication_id in new_publication_ids:
        db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
        if db_publication is None:
            raise HTTPException(status_code=404, detail=f"Publication with ID {publication_id} not found")
        association = publication_institution.insert().values(publication=db_publication.id, institution_1=db_institution.id)
        database.execute(association)
    existing_author_ids = [assoc.author for assoc in database.execute(
        author_institution.select().where(author_institution.c.institution == db_institution.id))]

    authors_to_remove = set(existing_author_ids) - set(institution_data.author)
    for author_id in authors_to_remove:
        association = author_institution.delete().where(
            (author_institution.c.institution == db_institution.id) & (author_institution.c.author == author_id))
        database.execute(association)

    new_author_ids = set(institution_data.author) - set(existing_author_ids)
    for author_id in new_author_ids:
        db_author = database.query(Author).filter(Author.id == author_id).first()
        if db_author is None:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        association = author_institution.insert().values(author=db_author.id, institution=db_institution.id)
        database.execute(association)
    database.commit()
    database.refresh(db_institution)

    publication_ids = database.query(publication_institution.c.publication).filter(publication_institution.c.institution_1 == db_institution.id).all()
    author_ids = database.query(author_institution.c.author).filter(author_institution.c.institution == db_institution.id).all()
    response_data = {
        "institution": db_institution,
        "publication_ids": [x[0] for x in publication_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.delete("/institution/{institution_id}/", response_model=None, tags=["Institution"])
async def delete_institution(institution_id: int, database: Session = Depends(get_db)):
    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")
    database.delete(db_institution)
    database.commit()
    return db_institution

@app.post("/institution/{institution_id}/publication/{publication_id}/", response_model=None, tags=["Institution Relationships"])
async def add_publication_to_institution(institution_id: int, publication_id: int, database: Session = Depends(get_db)):
    """Add a Publication to this Institution's publication relationship"""
    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    # Check if relationship already exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.institution_1 == institution_id) &
        (publication_institution.c.publication == publication_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = publication_institution.insert().values(institution_1=institution_id, publication=publication_id)
    database.execute(association)
    database.commit()

    return {"message": "Publication added to publication successfully"}


@app.delete("/institution/{institution_id}/publication/{publication_id}/", response_model=None, tags=["Institution Relationships"])
async def remove_publication_from_institution(institution_id: int, publication_id: int, database: Session = Depends(get_db)):
    """Remove a Publication from this Institution's publication relationship"""
    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Check if relationship exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.institution_1 == institution_id) &
        (publication_institution.c.publication == publication_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = publication_institution.delete().where(
        (publication_institution.c.institution_1 == institution_id) &
        (publication_institution.c.publication == publication_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Publication removed from publication successfully"}


@app.get("/institution/{institution_id}/publication/", response_model=None, tags=["Institution Relationships"])
async def get_publication_of_institution(institution_id: int, database: Session = Depends(get_db)):
    """Get all Publication entities related to this Institution through publication"""
    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    publication_ids = database.query(publication_institution.c.publication).filter(publication_institution.c.institution_1 == institution_id).all()
    publication_list = database.query(Publication).filter(Publication.id.in_([id[0] for id in publication_ids])).all()

    return {
        "institution_id": institution_id,
        "publication_count": len(publication_list),
        "publication": publication_list
    }

@app.post("/institution/{institution_id}/author/{author_id}/", response_model=None, tags=["Institution Relationships"])
async def add_author_to_institution(institution_id: int, author_id: int, database: Session = Depends(get_db)):
    """Add a Author to this Institution's author relationship"""
    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship already exists
    existing = database.query(author_institution).filter(
        (author_institution.c.institution == institution_id) &
        (author_institution.c.author == author_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = author_institution.insert().values(institution=institution_id, author=author_id)
    database.execute(association)
    database.commit()

    return {"message": "Author added to author successfully"}


@app.delete("/institution/{institution_id}/author/{author_id}/", response_model=None, tags=["Institution Relationships"])
async def remove_author_from_institution(institution_id: int, author_id: int, database: Session = Depends(get_db)):
    """Remove a Author from this Institution's author relationship"""
    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Check if relationship exists
    existing = database.query(author_institution).filter(
        (author_institution.c.institution == institution_id) &
        (author_institution.c.author == author_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = author_institution.delete().where(
        (author_institution.c.institution == institution_id) &
        (author_institution.c.author == author_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Author removed from author successfully"}


@app.get("/institution/{institution_id}/author/", response_model=None, tags=["Institution Relationships"])
async def get_author_of_institution(institution_id: int, database: Session = Depends(get_db)):
    """Get all Author entities related to this Institution through author"""
    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    author_ids = database.query(author_institution.c.author).filter(author_institution.c.institution == institution_id).all()
    author_list = database.query(Author).filter(Author.id.in_([id[0] for id in author_ids])).all()

    return {
        "institution_id": institution_id,
        "author_count": len(author_list),
        "author": author_list
    }





############################################
#
#   Author functions
#
############################################

@app.get("/author/", response_model=None, tags=["Author"])
def get_all_author(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Author)
        author_list = query.all()

        # Serialize with relationships included
        result = []
        for author_item in author_list:
            item_dict = author_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            institution_list = database.query(Institution).join(author_institution, Institution.id == author_institution.c.institution).filter(author_institution.c.author == author_item.id).all()
            item_dict['institution'] = []
            for institution_obj in institution_list:
                institution_dict = institution_obj.__dict__.copy()
                institution_dict.pop('_sa_instance_state', None)
                item_dict['institution'].append(institution_dict)
            publication_list = database.query(Publication).join(author_publication, Publication.id == author_publication.c.publication_1).filter(author_publication.c.author_1 == author_item.id).all()
            item_dict['publication_1'] = []
            for publication_obj in publication_list:
                publication_dict = publication_obj.__dict__.copy()
                publication_dict.pop('_sa_instance_state', None)
                item_dict['publication_1'].append(publication_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Author).all()


@app.get("/author/count/", response_model=None, tags=["Author"])
def get_count_author(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Author entities"""
    count = database.query(Author).count()
    return {"count": count}


@app.get("/author/paginated/", response_model=None, tags=["Author"])
def get_paginated_author(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Author entities"""
    total = database.query(Author).count()
    author_list = database.query(Author).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": author_list
        }

    result = []
    for author_item in author_list:
        institution_ids = database.query(author_institution.c.institution).filter(author_institution.c.author == author_item.id).all()
        publication_ids = database.query(author_publication.c.publication_1).filter(author_publication.c.author_1 == author_item.id).all()
        item_data = {
            "author": author_item,
            "institution_ids": [x[0] for x in institution_ids],
            "publication_ids": [x[0] for x in publication_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/author/search/", response_model=None, tags=["Author"])
def search_author(
    database: Session = Depends(get_db)
) -> list:
    """Search Author entities by attributes"""
    query = database.query(Author)


    results = query.all()
    return results


@app.get("/author/{author_id}/", response_model=None, tags=["Author"])
async def get_author(author_id: int, database: Session = Depends(get_db)) -> Author:
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    institution_ids = database.query(author_institution.c.institution).filter(author_institution.c.author == db_author.id).all()
    publication_ids = database.query(author_publication.c.publication_1).filter(author_publication.c.author_1 == db_author.id).all()
    response_data = {
        "author": db_author,
        "institution_ids": [x[0] for x in institution_ids],
        "publication_ids": [x[0] for x in publication_ids],
}
    return response_data



@app.post("/author/", response_model=None, tags=["Author"])
async def create_author(author_data: AuthorCreate, database: Session = Depends(get_db)) -> Author:

    if author_data.institution:
        for id in author_data.institution:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            if not db_institution:
                raise HTTPException(status_code=404, detail=f"Institution with ID {id} not found")
    if author_data.publication_1:
        for id in author_data.publication_1:
            # Entity already validated before creation
            db_publication = database.query(Publication).filter(Publication.id == id).first()
            if not db_publication:
                raise HTTPException(status_code=404, detail=f"Publication with ID {id} not found")

    db_author = Author(
        last_name=author_data.last_name,        name=author_data.name        )

    database.add(db_author)
    database.commit()
    database.refresh(db_author)


    if author_data.institution:
        for id in author_data.institution:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            # Create the association
            association = author_institution.insert().values(author=db_author.id, institution=db_institution.id)
            database.execute(association)
            database.commit()
    if author_data.publication_1:
        for id in author_data.publication_1:
            # Entity already validated before creation
            db_publication = database.query(Publication).filter(Publication.id == id).first()
            # Create the association
            association = author_publication.insert().values(author_1=db_author.id, publication_1=db_publication.id)
            database.execute(association)
            database.commit()


    institution_ids = database.query(author_institution.c.institution).filter(author_institution.c.author == db_author.id).all()
    publication_ids = database.query(author_publication.c.publication_1).filter(author_publication.c.author_1 == db_author.id).all()
    response_data = {
        "author": db_author,
        "institution_ids": [x[0] for x in institution_ids],
        "publication_ids": [x[0] for x in publication_ids],
    }
    return response_data


@app.post("/author/bulk/", response_model=None, tags=["Author"])
async def bulk_create_author(items: list[AuthorCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Author entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_author = Author(
                last_name=item_data.last_name,                name=item_data.name            )
            database.add(db_author)
            database.flush()  # Get ID without committing
            created_items.append(db_author.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Author entities"
    }


@app.delete("/author/bulk/", response_model=None, tags=["Author"])
async def bulk_delete_author(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Author entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_author = database.query(Author).filter(Author.id == item_id).first()
        if db_author:
            database.delete(db_author)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Author entities"
    }

@app.put("/author/{author_id}/", response_model=None, tags=["Author"])
async def update_author(author_id: int, author_data: AuthorCreate, database: Session = Depends(get_db)) -> Author:
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    setattr(db_author, 'last_name', author_data.last_name)
    setattr(db_author, 'name', author_data.name)
    existing_institution_ids = [assoc.institution for assoc in database.execute(
        author_institution.select().where(author_institution.c.author == db_author.id))]

    institutions_to_remove = set(existing_institution_ids) - set(author_data.institution)
    for institution_id in institutions_to_remove:
        association = author_institution.delete().where(
            (author_institution.c.author == db_author.id) & (author_institution.c.institution == institution_id))
        database.execute(association)

    new_institution_ids = set(author_data.institution) - set(existing_institution_ids)
    for institution_id in new_institution_ids:
        db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
        if db_institution is None:
            raise HTTPException(status_code=404, detail=f"Institution with ID {institution_id} not found")
        association = author_institution.insert().values(institution=db_institution.id, author=db_author.id)
        database.execute(association)
    existing_publication_ids = [assoc.publication_1 for assoc in database.execute(
        author_publication.select().where(author_publication.c.author_1 == db_author.id))]

    publications_to_remove = set(existing_publication_ids) - set(author_data.publication_1)
    for publication_id in publications_to_remove:
        association = author_publication.delete().where(
            (author_publication.c.author_1 == db_author.id) & (author_publication.c.publication_1 == publication_id))
        database.execute(association)

    new_publication_ids = set(author_data.publication_1) - set(existing_publication_ids)
    for publication_id in new_publication_ids:
        db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
        if db_publication is None:
            raise HTTPException(status_code=404, detail=f"Publication with ID {publication_id} not found")
        association = author_publication.insert().values(publication_1=db_publication.id, author_1=db_author.id)
        database.execute(association)
    database.commit()
    database.refresh(db_author)

    institution_ids = database.query(author_institution.c.institution).filter(author_institution.c.author == db_author.id).all()
    publication_ids = database.query(author_publication.c.publication_1).filter(author_publication.c.author_1 == db_author.id).all()
    response_data = {
        "author": db_author,
        "institution_ids": [x[0] for x in institution_ids],
        "publication_ids": [x[0] for x in publication_ids],
    }
    return response_data


@app.delete("/author/{author_id}/", response_model=None, tags=["Author"])
async def delete_author(author_id: int, database: Session = Depends(get_db)):
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")
    database.delete(db_author)
    database.commit()
    return db_author

@app.post("/author/{author_id}/institution/{institution_id}/", response_model=None, tags=["Author Relationships"])
async def add_institution_to_author(author_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Add a Institution to this Author's institution relationship"""
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Check if relationship already exists
    existing = database.query(author_institution).filter(
        (author_institution.c.author == author_id) &
        (author_institution.c.institution == institution_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = author_institution.insert().values(author=author_id, institution=institution_id)
    database.execute(association)
    database.commit()

    return {"message": "Institution added to institution successfully"}


@app.delete("/author/{author_id}/institution/{institution_id}/", response_model=None, tags=["Author Relationships"])
async def remove_institution_from_author(author_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Remove a Institution from this Author's institution relationship"""
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship exists
    existing = database.query(author_institution).filter(
        (author_institution.c.author == author_id) &
        (author_institution.c.institution == institution_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = author_institution.delete().where(
        (author_institution.c.author == author_id) &
        (author_institution.c.institution == institution_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Institution removed from institution successfully"}


@app.get("/author/{author_id}/institution/", response_model=None, tags=["Author Relationships"])
async def get_institution_of_author(author_id: int, database: Session = Depends(get_db)):
    """Get all Institution entities related to this Author through institution"""
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    institution_ids = database.query(author_institution.c.institution).filter(author_institution.c.author == author_id).all()
    institution_list = database.query(Institution).filter(Institution.id.in_([id[0] for id in institution_ids])).all()

    return {
        "author_id": author_id,
        "institution_count": len(institution_list),
        "institution": institution_list
    }

@app.post("/author/{author_id}/publication_1/{publication_id}/", response_model=None, tags=["Author Relationships"])
async def add_publication_1_to_author(author_id: int, publication_id: int, database: Session = Depends(get_db)):
    """Add a Publication to this Author's publication_1 relationship"""
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    # Check if relationship already exists
    existing = database.query(author_publication).filter(
        (author_publication.c.author_1 == author_id) &
        (author_publication.c.publication_1 == publication_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = author_publication.insert().values(author_1=author_id, publication_1=publication_id)
    database.execute(association)
    database.commit()

    return {"message": "Publication added to publication_1 successfully"}


@app.delete("/author/{author_id}/publication_1/{publication_id}/", response_model=None, tags=["Author Relationships"])
async def remove_publication_1_from_author(author_id: int, publication_id: int, database: Session = Depends(get_db)):
    """Remove a Publication from this Author's publication_1 relationship"""
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship exists
    existing = database.query(author_publication).filter(
        (author_publication.c.author_1 == author_id) &
        (author_publication.c.publication_1 == publication_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = author_publication.delete().where(
        (author_publication.c.author_1 == author_id) &
        (author_publication.c.publication_1 == publication_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Publication removed from publication_1 successfully"}


@app.get("/author/{author_id}/publication_1/", response_model=None, tags=["Author Relationships"])
async def get_publication_1_of_author(author_id: int, database: Session = Depends(get_db)):
    """Get all Publication entities related to this Author through publication_1"""
    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    publication_ids = database.query(author_publication.c.publication_1).filter(author_publication.c.author_1 == author_id).all()
    publication_list = database.query(Publication).filter(Publication.id.in_([id[0] for id in publication_ids])).all()

    return {
        "author_id": author_id,
        "publication_1_count": len(publication_list),
        "publication_1": publication_list
    }





############################################
#
#   Publication functions
#
############################################

@app.get("/publication/", response_model=None, tags=["Publication"])
def get_all_publication(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Publication)
        publication_list = query.all()

        # Serialize with relationships included
        result = []
        for publication_item in publication_list:
            item_dict = publication_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            institution_list = database.query(Institution).join(publication_institution, Institution.id == publication_institution.c.institution_1).filter(publication_institution.c.publication == publication_item.id).all()
            item_dict['institution_1'] = []
            for institution_obj in institution_list:
                institution_dict = institution_obj.__dict__.copy()
                institution_dict.pop('_sa_instance_state', None)
                item_dict['institution_1'].append(institution_dict)
            author_list = database.query(Author).join(author_publication, Author.id == author_publication.c.author_1).filter(author_publication.c.publication_1 == publication_item.id).all()
            item_dict['author_1'] = []
            for author_obj in author_list:
                author_dict = author_obj.__dict__.copy()
                author_dict.pop('_sa_instance_state', None)
                item_dict['author_1'].append(author_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Publication).all()


@app.get("/publication/count/", response_model=None, tags=["Publication"])
def get_count_publication(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Publication entities"""
    count = database.query(Publication).count()
    return {"count": count}


@app.get("/publication/paginated/", response_model=None, tags=["Publication"])
def get_paginated_publication(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Publication entities"""
    total = database.query(Publication).count()
    publication_list = database.query(Publication).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": publication_list
        }

    result = []
    for publication_item in publication_list:
        institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == publication_item.id).all()
        author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == publication_item.id).all()
        item_data = {
            "publication": publication_item,
            "institution_ids": [x[0] for x in institution_ids],
            "author_ids": [x[0] for x in author_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/publication/search/", response_model=None, tags=["Publication"])
def search_publication(
    database: Session = Depends(get_db)
) -> list:
    """Search Publication entities by attributes"""
    query = database.query(Publication)


    results = query.all()
    return results


@app.get("/publication/{publication_id}/", response_model=None, tags=["Publication"])
async def get_publication(publication_id: int, database: Session = Depends(get_db)) -> Publication:
    db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_publication.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_publication.id).all()
    response_data = {
        "publication": db_publication,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
}
    return response_data



@app.post("/publication/", response_model=None, tags=["Publication"])
async def create_publication(publication_data: PublicationCreate, database: Session = Depends(get_db)) -> Publication:

    if not publication_data.institution_1 or len(publication_data.institution_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Institution(s) required")
    if publication_data.institution_1:
        for id in publication_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            if not db_institution:
                raise HTTPException(status_code=404, detail=f"Institution with ID {id} not found")
    if not publication_data.author_1 or len(publication_data.author_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Author(s) required")
    if publication_data.author_1:
        for id in publication_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            if not db_author:
                raise HTTPException(status_code=404, detail=f"Author with ID {id} not found")

    db_publication = Publication(
        title=publication_data.title,        year=publication_data.year        )

    database.add(db_publication)
    database.commit()
    database.refresh(db_publication)


    if publication_data.institution_1:
        for id in publication_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            # Create the association
            association = publication_institution.insert().values(publication=db_publication.id, institution_1=db_institution.id)
            database.execute(association)
            database.commit()
    if publication_data.author_1:
        for id in publication_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            # Create the association
            association = author_publication.insert().values(publication_1=db_publication.id, author_1=db_author.id)
            database.execute(association)
            database.commit()


    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_publication.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_publication.id).all()
    response_data = {
        "publication": db_publication,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.post("/publication/bulk/", response_model=None, tags=["Publication"])
async def bulk_create_publication(items: list[PublicationCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Publication entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_publication = Publication(
                title=item_data.title,                year=item_data.year            )
            database.add(db_publication)
            database.flush()  # Get ID without committing
            created_items.append(db_publication.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Publication entities"
    }


@app.delete("/publication/bulk/", response_model=None, tags=["Publication"])
async def bulk_delete_publication(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Publication entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_publication = database.query(Publication).filter(Publication.id == item_id).first()
        if db_publication:
            database.delete(db_publication)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Publication entities"
    }

@app.put("/publication/{publication_id}/", response_model=None, tags=["Publication"])
async def update_publication(publication_id: int, publication_data: PublicationCreate, database: Session = Depends(get_db)) -> Publication:
    db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    setattr(db_publication, 'title', publication_data.title)
    setattr(db_publication, 'year', publication_data.year)
    existing_institution_ids = [assoc.institution_1 for assoc in database.execute(
        publication_institution.select().where(publication_institution.c.publication == db_publication.id))]

    institutions_to_remove = set(existing_institution_ids) - set(publication_data.institution_1)
    for institution_id in institutions_to_remove:
        association = publication_institution.delete().where(
            (publication_institution.c.publication == db_publication.id) & (publication_institution.c.institution_1 == institution_id))
        database.execute(association)

    new_institution_ids = set(publication_data.institution_1) - set(existing_institution_ids)
    for institution_id in new_institution_ids:
        db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
        if db_institution is None:
            raise HTTPException(status_code=404, detail=f"Institution with ID {institution_id} not found")
        association = publication_institution.insert().values(institution_1=db_institution.id, publication=db_publication.id)
        database.execute(association)
    existing_author_ids = [assoc.author_1 for assoc in database.execute(
        author_publication.select().where(author_publication.c.publication_1 == db_publication.id))]

    authors_to_remove = set(existing_author_ids) - set(publication_data.author_1)
    for author_id in authors_to_remove:
        association = author_publication.delete().where(
            (author_publication.c.publication_1 == db_publication.id) & (author_publication.c.author_1 == author_id))
        database.execute(association)

    new_author_ids = set(publication_data.author_1) - set(existing_author_ids)
    for author_id in new_author_ids:
        db_author = database.query(Author).filter(Author.id == author_id).first()
        if db_author is None:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        association = author_publication.insert().values(author_1=db_author.id, publication_1=db_publication.id)
        database.execute(association)
    database.commit()
    database.refresh(db_publication)

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_publication.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_publication.id).all()
    response_data = {
        "publication": db_publication,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.delete("/publication/{publication_id}/", response_model=None, tags=["Publication"])
async def delete_publication(publication_id: int, database: Session = Depends(get_db)):
    db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")
    database.delete(db_publication)
    database.commit()
    return db_publication

@app.post("/publication/{publication_id}/institution_1/{institution_id}/", response_model=None, tags=["Publication Relationships"])
async def add_institution_1_to_publication(publication_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Add a Institution to this Publication's institution_1 relationship"""
    db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Check if relationship already exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == publication_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = publication_institution.insert().values(publication=publication_id, institution_1=institution_id)
    database.execute(association)
    database.commit()

    return {"message": "Institution added to institution_1 successfully"}


@app.delete("/publication/{publication_id}/institution_1/{institution_id}/", response_model=None, tags=["Publication Relationships"])
async def remove_institution_1_from_publication(publication_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Remove a Institution from this Publication's institution_1 relationship"""
    db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    # Check if relationship exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == publication_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = publication_institution.delete().where(
        (publication_institution.c.publication == publication_id) &
        (publication_institution.c.institution_1 == institution_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Institution removed from institution_1 successfully"}


@app.get("/publication/{publication_id}/institution_1/", response_model=None, tags=["Publication Relationships"])
async def get_institution_1_of_publication(publication_id: int, database: Session = Depends(get_db)):
    """Get all Institution entities related to this Publication through institution_1"""
    db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == publication_id).all()
    institution_list = database.query(Institution).filter(Institution.id.in_([id[0] for id in institution_ids])).all()

    return {
        "publication_id": publication_id,
        "institution_1_count": len(institution_list),
        "institution_1": institution_list
    }

@app.post("/publication/{publication_id}/author_1/{author_id}/", response_model=None, tags=["Publication Relationships"])
async def add_author_1_to_publication(publication_id: int, author_id: int, database: Session = Depends(get_db)):
    """Add a Author to this Publication's author_1 relationship"""
    db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship already exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == publication_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = author_publication.insert().values(publication_1=publication_id, author_1=author_id)
    database.execute(association)
    database.commit()

    return {"message": "Author added to author_1 successfully"}


@app.delete("/publication/{publication_id}/author_1/{author_id}/", response_model=None, tags=["Publication Relationships"])
async def remove_author_1_from_publication(publication_id: int, author_id: int, database: Session = Depends(get_db)):
    """Remove a Author from this Publication's author_1 relationship"""
    db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    # Check if relationship exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == publication_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = author_publication.delete().where(
        (author_publication.c.publication_1 == publication_id) &
        (author_publication.c.author_1 == author_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Author removed from author_1 successfully"}


@app.get("/publication/{publication_id}/author_1/", response_model=None, tags=["Publication Relationships"])
async def get_author_1_of_publication(publication_id: int, database: Session = Depends(get_db)):
    """Get all Author entities related to this Publication through author_1"""
    db_publication = database.query(Publication).filter(Publication.id == publication_id).first()
    if db_publication is None:
        raise HTTPException(status_code=404, detail="Publication not found")

    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == publication_id).all()
    author_list = database.query(Author).filter(Author.id.in_([id[0] for id in author_ids])).all()

    return {
        "publication_id": publication_id,
        "author_1_count": len(author_list),
        "author_1": author_list
    }





############################################
#
#   Conference functions
#
############################################

@app.get("/conference/", response_model=None, tags=["Conference"])
def get_all_conference(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Conference)
        conference_list = query.all()

        # Serialize with relationships included
        result = []
        for conference_item in conference_list:
            item_dict = conference_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            institution_list = database.query(Institution).join(publication_institution, Institution.id == publication_institution.c.institution_1).filter(publication_institution.c.publication == conference_item.id).all()
            item_dict['institution_1'] = []
            for institution_obj in institution_list:
                institution_dict = institution_obj.__dict__.copy()
                institution_dict.pop('_sa_instance_state', None)
                item_dict['institution_1'].append(institution_dict)
            author_list = database.query(Author).join(author_publication, Author.id == author_publication.c.author_1).filter(author_publication.c.publication_1 == conference_item.id).all()
            item_dict['author_1'] = []
            for author_obj in author_list:
                author_dict = author_obj.__dict__.copy()
                author_dict.pop('_sa_instance_state', None)
                item_dict['author_1'].append(author_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Conference).all()


@app.get("/conference/count/", response_model=None, tags=["Conference"])
def get_count_conference(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Conference entities"""
    count = database.query(Conference).count()
    return {"count": count}


@app.get("/conference/paginated/", response_model=None, tags=["Conference"])
def get_paginated_conference(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Conference entities"""
    total = database.query(Conference).count()
    conference_list = database.query(Conference).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": conference_list
        }

    result = []
    for conference_item in conference_list:
        institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == conference_item.id).all()
        author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == conference_item.id).all()
        item_data = {
            "conference": conference_item,
            "institution_ids": [x[0] for x in institution_ids],
            "author_ids": [x[0] for x in author_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/conference/search/", response_model=None, tags=["Conference"])
def search_conference(
    database: Session = Depends(get_db)
) -> list:
    """Search Conference entities by attributes"""
    query = database.query(Conference)


    results = query.all()
    return results


@app.get("/conference/{conference_id}/", response_model=None, tags=["Conference"])
async def get_conference(conference_id: int, database: Session = Depends(get_db)) -> Conference:
    db_conference = database.query(Conference).filter(Conference.id == conference_id).first()
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_conference.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_conference.id).all()
    response_data = {
        "conference": db_conference,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
}
    return response_data



@app.post("/conference/", response_model=None, tags=["Conference"])
async def create_conference(conference_data: ConferenceCreate, database: Session = Depends(get_db)) -> Conference:

    if not conference_data.institution_1 or len(conference_data.institution_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Institution(s) required")
    if conference_data.institution_1:
        for id in conference_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            if not db_institution:
                raise HTTPException(status_code=404, detail=f"Institution with ID {id} not found")
    if not conference_data.author_1 or len(conference_data.author_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Author(s) required")
    if conference_data.author_1:
        for id in conference_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            if not db_author:
                raise HTTPException(status_code=404, detail=f"Author with ID {id} not found")

    db_conference = Conference(
        title=conference_data.title,        year=conference_data.year,        month=conference_data.month,        organization=conference_data.organization,        address=conference_data.address,        publisher=conference_data.publisher,        booktitle=conference_data.booktitle,        number=conference_data.number,        pages=conference_data.pages,        series=conference_data.series,        note=conference_data.note,        editor=conference_data.editor        )

    database.add(db_conference)
    database.commit()
    database.refresh(db_conference)


    if conference_data.institution_1:
        for id in conference_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            # Create the association
            association = publication_institution.insert().values(publication=db_conference.id, institution_1=db_institution.id)
            database.execute(association)
            database.commit()
    if conference_data.author_1:
        for id in conference_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            # Create the association
            association = author_publication.insert().values(publication_1=db_conference.id, author_1=db_author.id)
            database.execute(association)
            database.commit()


    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_conference.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_conference.id).all()
    response_data = {
        "conference": db_conference,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.post("/conference/bulk/", response_model=None, tags=["Conference"])
async def bulk_create_conference(items: list[ConferenceCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Conference entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_conference = Conference(
                title=item_data.title,                year=item_data.year,                month=item_data.month,                organization=item_data.organization,                address=item_data.address,                publisher=item_data.publisher,                booktitle=item_data.booktitle,                number=item_data.number,                pages=item_data.pages,                series=item_data.series,                note=item_data.note,                editor=item_data.editor            )
            database.add(db_conference)
            database.flush()  # Get ID without committing
            created_items.append(db_conference.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Conference entities"
    }


@app.delete("/conference/bulk/", response_model=None, tags=["Conference"])
async def bulk_delete_conference(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Conference entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_conference = database.query(Conference).filter(Conference.id == item_id).first()
        if db_conference:
            database.delete(db_conference)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Conference entities"
    }

@app.put("/conference/{conference_id}/", response_model=None, tags=["Conference"])
async def update_conference(conference_id: int, conference_data: ConferenceCreate, database: Session = Depends(get_db)) -> Conference:
    db_conference = database.query(Conference).filter(Conference.id == conference_id).first()
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")

    setattr(db_conference, 'month', conference_data.month)
    setattr(db_conference, 'organization', conference_data.organization)
    setattr(db_conference, 'address', conference_data.address)
    setattr(db_conference, 'publisher', conference_data.publisher)
    setattr(db_conference, 'booktitle', conference_data.booktitle)
    setattr(db_conference, 'number', conference_data.number)
    setattr(db_conference, 'pages', conference_data.pages)
    setattr(db_conference, 'series', conference_data.series)
    setattr(db_conference, 'note', conference_data.note)
    setattr(db_conference, 'editor', conference_data.editor)
    existing_institution_ids = [assoc.institution_1 for assoc in database.execute(
        publication_institution.select().where(publication_institution.c.publication == db_conference.id))]

    institutions_to_remove = set(existing_institution_ids) - set(conference_data.institution_1)
    for institution_id in institutions_to_remove:
        association = publication_institution.delete().where(
            (publication_institution.c.publication == db_conference.id) & (publication_institution.c.institution_1 == institution_id))
        database.execute(association)

    new_institution_ids = set(conference_data.institution_1) - set(existing_institution_ids)
    for institution_id in new_institution_ids:
        db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
        if db_institution is None:
            raise HTTPException(status_code=404, detail=f"Institution with ID {institution_id} not found")
        association = publication_institution.insert().values(institution_1=db_institution.id, publication=db_conference.id)
        database.execute(association)
    existing_author_ids = [assoc.author_1 for assoc in database.execute(
        author_publication.select().where(author_publication.c.publication_1 == db_conference.id))]

    authors_to_remove = set(existing_author_ids) - set(conference_data.author_1)
    for author_id in authors_to_remove:
        association = author_publication.delete().where(
            (author_publication.c.publication_1 == db_conference.id) & (author_publication.c.author_1 == author_id))
        database.execute(association)

    new_author_ids = set(conference_data.author_1) - set(existing_author_ids)
    for author_id in new_author_ids:
        db_author = database.query(Author).filter(Author.id == author_id).first()
        if db_author is None:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        association = author_publication.insert().values(author_1=db_author.id, publication_1=db_conference.id)
        database.execute(association)
    database.commit()
    database.refresh(db_conference)

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_conference.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_conference.id).all()
    response_data = {
        "conference": db_conference,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.delete("/conference/{conference_id}/", response_model=None, tags=["Conference"])
async def delete_conference(conference_id: int, database: Session = Depends(get_db)):
    db_conference = database.query(Conference).filter(Conference.id == conference_id).first()
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")
    database.delete(db_conference)
    database.commit()
    return db_conference

@app.post("/conference/{conference_id}/institution_1/{institution_id}/", response_model=None, tags=["Conference Relationships"])
async def add_institution_1_to_conference(conference_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Add a Institution to this Conference's institution_1 relationship"""
    db_conference = database.query(Conference).filter(Conference.id == conference_id).first()
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")

    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Check if relationship already exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == conference_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = publication_institution.insert().values(publication=conference_id, institution_1=institution_id)
    database.execute(association)
    database.commit()

    return {"message": "Institution added to institution_1 successfully"}


@app.delete("/conference/{conference_id}/institution_1/{institution_id}/", response_model=None, tags=["Conference Relationships"])
async def remove_institution_1_from_conference(conference_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Remove a Institution from this Conference's institution_1 relationship"""
    db_conference = database.query(Conference).filter(Conference.id == conference_id).first()
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")

    # Check if relationship exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == conference_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = publication_institution.delete().where(
        (publication_institution.c.publication == conference_id) &
        (publication_institution.c.institution_1 == institution_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Institution removed from institution_1 successfully"}


@app.get("/conference/{conference_id}/institution_1/", response_model=None, tags=["Conference Relationships"])
async def get_institution_1_of_conference(conference_id: int, database: Session = Depends(get_db)):
    """Get all Institution entities related to this Conference through institution_1"""
    db_conference = database.query(Conference).filter(Conference.id == conference_id).first()
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == conference_id).all()
    institution_list = database.query(Institution).filter(Institution.id.in_([id[0] for id in institution_ids])).all()

    return {
        "conference_id": conference_id,
        "institution_1_count": len(institution_list),
        "institution_1": institution_list
    }

@app.post("/conference/{conference_id}/author_1/{author_id}/", response_model=None, tags=["Conference Relationships"])
async def add_author_1_to_conference(conference_id: int, author_id: int, database: Session = Depends(get_db)):
    """Add a Author to this Conference's author_1 relationship"""
    db_conference = database.query(Conference).filter(Conference.id == conference_id).first()
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")

    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship already exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == conference_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = author_publication.insert().values(publication_1=conference_id, author_1=author_id)
    database.execute(association)
    database.commit()

    return {"message": "Author added to author_1 successfully"}


@app.delete("/conference/{conference_id}/author_1/{author_id}/", response_model=None, tags=["Conference Relationships"])
async def remove_author_1_from_conference(conference_id: int, author_id: int, database: Session = Depends(get_db)):
    """Remove a Author from this Conference's author_1 relationship"""
    db_conference = database.query(Conference).filter(Conference.id == conference_id).first()
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")

    # Check if relationship exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == conference_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = author_publication.delete().where(
        (author_publication.c.publication_1 == conference_id) &
        (author_publication.c.author_1 == author_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Author removed from author_1 successfully"}


@app.get("/conference/{conference_id}/author_1/", response_model=None, tags=["Conference Relationships"])
async def get_author_1_of_conference(conference_id: int, database: Session = Depends(get_db)):
    """Get all Author entities related to this Conference through author_1"""
    db_conference = database.query(Conference).filter(Conference.id == conference_id).first()
    if db_conference is None:
        raise HTTPException(status_code=404, detail="Conference not found")

    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == conference_id).all()
    author_list = database.query(Author).filter(Author.id.in_([id[0] for id in author_ids])).all()

    return {
        "conference_id": conference_id,
        "author_1_count": len(author_list),
        "author_1": author_list
    }





############################################
#
#   Proceedings functions
#
############################################

@app.get("/proceedings/", response_model=None, tags=["Proceedings"])
def get_all_proceedings(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Proceedings)
        proceedings_list = query.all()

        # Serialize with relationships included
        result = []
        for proceedings_item in proceedings_list:
            item_dict = proceedings_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            institution_list = database.query(Institution).join(publication_institution, Institution.id == publication_institution.c.institution_1).filter(publication_institution.c.publication == proceedings_item.id).all()
            item_dict['institution_1'] = []
            for institution_obj in institution_list:
                institution_dict = institution_obj.__dict__.copy()
                institution_dict.pop('_sa_instance_state', None)
                item_dict['institution_1'].append(institution_dict)
            author_list = database.query(Author).join(author_publication, Author.id == author_publication.c.author_1).filter(author_publication.c.publication_1 == proceedings_item.id).all()
            item_dict['author_1'] = []
            for author_obj in author_list:
                author_dict = author_obj.__dict__.copy()
                author_dict.pop('_sa_instance_state', None)
                item_dict['author_1'].append(author_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Proceedings).all()


@app.get("/proceedings/count/", response_model=None, tags=["Proceedings"])
def get_count_proceedings(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Proceedings entities"""
    count = database.query(Proceedings).count()
    return {"count": count}


@app.get("/proceedings/paginated/", response_model=None, tags=["Proceedings"])
def get_paginated_proceedings(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Proceedings entities"""
    total = database.query(Proceedings).count()
    proceedings_list = database.query(Proceedings).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": proceedings_list
        }

    result = []
    for proceedings_item in proceedings_list:
        institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == proceedings_item.id).all()
        author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == proceedings_item.id).all()
        item_data = {
            "proceedings": proceedings_item,
            "institution_ids": [x[0] for x in institution_ids],
            "author_ids": [x[0] for x in author_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/proceedings/search/", response_model=None, tags=["Proceedings"])
def search_proceedings(
    database: Session = Depends(get_db)
) -> list:
    """Search Proceedings entities by attributes"""
    query = database.query(Proceedings)


    results = query.all()
    return results


@app.get("/proceedings/{proceedings_id}/", response_model=None, tags=["Proceedings"])
async def get_proceedings(proceedings_id: int, database: Session = Depends(get_db)) -> Proceedings:
    db_proceedings = database.query(Proceedings).filter(Proceedings.id == proceedings_id).first()
    if db_proceedings is None:
        raise HTTPException(status_code=404, detail="Proceedings not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_proceedings.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_proceedings.id).all()
    response_data = {
        "proceedings": db_proceedings,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
}
    return response_data



@app.post("/proceedings/", response_model=None, tags=["Proceedings"])
async def create_proceedings(proceedings_data: ProceedingsCreate, database: Session = Depends(get_db)) -> Proceedings:

    if not proceedings_data.institution_1 or len(proceedings_data.institution_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Institution(s) required")
    if proceedings_data.institution_1:
        for id in proceedings_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            if not db_institution:
                raise HTTPException(status_code=404, detail=f"Institution with ID {id} not found")
    if not proceedings_data.author_1 or len(proceedings_data.author_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Author(s) required")
    if proceedings_data.author_1:
        for id in proceedings_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            if not db_author:
                raise HTTPException(status_code=404, detail=f"Author with ID {id} not found")

    db_proceedings = Proceedings(
        title=proceedings_data.title,        year=proceedings_data.year,        editor=proceedings_data.editor,        volume=proceedings_data.volume,        series=proceedings_data.series,        organization=proceedings_data.organization,        month=proceedings_data.month,        publisher=proceedings_data.publisher,        address=proceedings_data.address,        number=proceedings_data.number,        pages=proceedings_data.pages,        booktitle=proceedings_data.booktitle        )

    database.add(db_proceedings)
    database.commit()
    database.refresh(db_proceedings)


    if proceedings_data.institution_1:
        for id in proceedings_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            # Create the association
            association = publication_institution.insert().values(publication=db_proceedings.id, institution_1=db_institution.id)
            database.execute(association)
            database.commit()
    if proceedings_data.author_1:
        for id in proceedings_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            # Create the association
            association = author_publication.insert().values(publication_1=db_proceedings.id, author_1=db_author.id)
            database.execute(association)
            database.commit()


    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_proceedings.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_proceedings.id).all()
    response_data = {
        "proceedings": db_proceedings,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.post("/proceedings/bulk/", response_model=None, tags=["Proceedings"])
async def bulk_create_proceedings(items: list[ProceedingsCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Proceedings entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_proceedings = Proceedings(
                title=item_data.title,                year=item_data.year,                editor=item_data.editor,                volume=item_data.volume,                series=item_data.series,                organization=item_data.organization,                month=item_data.month,                publisher=item_data.publisher,                address=item_data.address,                number=item_data.number,                pages=item_data.pages,                booktitle=item_data.booktitle            )
            database.add(db_proceedings)
            database.flush()  # Get ID without committing
            created_items.append(db_proceedings.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Proceedings entities"
    }


@app.delete("/proceedings/bulk/", response_model=None, tags=["Proceedings"])
async def bulk_delete_proceedings(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Proceedings entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_proceedings = database.query(Proceedings).filter(Proceedings.id == item_id).first()
        if db_proceedings:
            database.delete(db_proceedings)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Proceedings entities"
    }

@app.put("/proceedings/{proceedings_id}/", response_model=None, tags=["Proceedings"])
async def update_proceedings(proceedings_id: int, proceedings_data: ProceedingsCreate, database: Session = Depends(get_db)) -> Proceedings:
    db_proceedings = database.query(Proceedings).filter(Proceedings.id == proceedings_id).first()
    if db_proceedings is None:
        raise HTTPException(status_code=404, detail="Proceedings not found")

    setattr(db_proceedings, 'editor', proceedings_data.editor)
    setattr(db_proceedings, 'volume', proceedings_data.volume)
    setattr(db_proceedings, 'series', proceedings_data.series)
    setattr(db_proceedings, 'organization', proceedings_data.organization)
    setattr(db_proceedings, 'month', proceedings_data.month)
    setattr(db_proceedings, 'publisher', proceedings_data.publisher)
    setattr(db_proceedings, 'address', proceedings_data.address)
    setattr(db_proceedings, 'number', proceedings_data.number)
    setattr(db_proceedings, 'pages', proceedings_data.pages)
    setattr(db_proceedings, 'booktitle', proceedings_data.booktitle)
    existing_institution_ids = [assoc.institution_1 for assoc in database.execute(
        publication_institution.select().where(publication_institution.c.publication == db_proceedings.id))]

    institutions_to_remove = set(existing_institution_ids) - set(proceedings_data.institution_1)
    for institution_id in institutions_to_remove:
        association = publication_institution.delete().where(
            (publication_institution.c.publication == db_proceedings.id) & (publication_institution.c.institution_1 == institution_id))
        database.execute(association)

    new_institution_ids = set(proceedings_data.institution_1) - set(existing_institution_ids)
    for institution_id in new_institution_ids:
        db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
        if db_institution is None:
            raise HTTPException(status_code=404, detail=f"Institution with ID {institution_id} not found")
        association = publication_institution.insert().values(institution_1=db_institution.id, publication=db_proceedings.id)
        database.execute(association)
    existing_author_ids = [assoc.author_1 for assoc in database.execute(
        author_publication.select().where(author_publication.c.publication_1 == db_proceedings.id))]

    authors_to_remove = set(existing_author_ids) - set(proceedings_data.author_1)
    for author_id in authors_to_remove:
        association = author_publication.delete().where(
            (author_publication.c.publication_1 == db_proceedings.id) & (author_publication.c.author_1 == author_id))
        database.execute(association)

    new_author_ids = set(proceedings_data.author_1) - set(existing_author_ids)
    for author_id in new_author_ids:
        db_author = database.query(Author).filter(Author.id == author_id).first()
        if db_author is None:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        association = author_publication.insert().values(author_1=db_author.id, publication_1=db_proceedings.id)
        database.execute(association)
    database.commit()
    database.refresh(db_proceedings)

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_proceedings.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_proceedings.id).all()
    response_data = {
        "proceedings": db_proceedings,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.delete("/proceedings/{proceedings_id}/", response_model=None, tags=["Proceedings"])
async def delete_proceedings(proceedings_id: int, database: Session = Depends(get_db)):
    db_proceedings = database.query(Proceedings).filter(Proceedings.id == proceedings_id).first()
    if db_proceedings is None:
        raise HTTPException(status_code=404, detail="Proceedings not found")
    database.delete(db_proceedings)
    database.commit()
    return db_proceedings

@app.post("/proceedings/{proceedings_id}/institution_1/{institution_id}/", response_model=None, tags=["Proceedings Relationships"])
async def add_institution_1_to_proceedings(proceedings_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Add a Institution to this Proceedings's institution_1 relationship"""
    db_proceedings = database.query(Proceedings).filter(Proceedings.id == proceedings_id).first()
    if db_proceedings is None:
        raise HTTPException(status_code=404, detail="Proceedings not found")

    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Check if relationship already exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == proceedings_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = publication_institution.insert().values(publication=proceedings_id, institution_1=institution_id)
    database.execute(association)
    database.commit()

    return {"message": "Institution added to institution_1 successfully"}


@app.delete("/proceedings/{proceedings_id}/institution_1/{institution_id}/", response_model=None, tags=["Proceedings Relationships"])
async def remove_institution_1_from_proceedings(proceedings_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Remove a Institution from this Proceedings's institution_1 relationship"""
    db_proceedings = database.query(Proceedings).filter(Proceedings.id == proceedings_id).first()
    if db_proceedings is None:
        raise HTTPException(status_code=404, detail="Proceedings not found")

    # Check if relationship exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == proceedings_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = publication_institution.delete().where(
        (publication_institution.c.publication == proceedings_id) &
        (publication_institution.c.institution_1 == institution_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Institution removed from institution_1 successfully"}


@app.get("/proceedings/{proceedings_id}/institution_1/", response_model=None, tags=["Proceedings Relationships"])
async def get_institution_1_of_proceedings(proceedings_id: int, database: Session = Depends(get_db)):
    """Get all Institution entities related to this Proceedings through institution_1"""
    db_proceedings = database.query(Proceedings).filter(Proceedings.id == proceedings_id).first()
    if db_proceedings is None:
        raise HTTPException(status_code=404, detail="Proceedings not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == proceedings_id).all()
    institution_list = database.query(Institution).filter(Institution.id.in_([id[0] for id in institution_ids])).all()

    return {
        "proceedings_id": proceedings_id,
        "institution_1_count": len(institution_list),
        "institution_1": institution_list
    }

@app.post("/proceedings/{proceedings_id}/author_1/{author_id}/", response_model=None, tags=["Proceedings Relationships"])
async def add_author_1_to_proceedings(proceedings_id: int, author_id: int, database: Session = Depends(get_db)):
    """Add a Author to this Proceedings's author_1 relationship"""
    db_proceedings = database.query(Proceedings).filter(Proceedings.id == proceedings_id).first()
    if db_proceedings is None:
        raise HTTPException(status_code=404, detail="Proceedings not found")

    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship already exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == proceedings_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = author_publication.insert().values(publication_1=proceedings_id, author_1=author_id)
    database.execute(association)
    database.commit()

    return {"message": "Author added to author_1 successfully"}


@app.delete("/proceedings/{proceedings_id}/author_1/{author_id}/", response_model=None, tags=["Proceedings Relationships"])
async def remove_author_1_from_proceedings(proceedings_id: int, author_id: int, database: Session = Depends(get_db)):
    """Remove a Author from this Proceedings's author_1 relationship"""
    db_proceedings = database.query(Proceedings).filter(Proceedings.id == proceedings_id).first()
    if db_proceedings is None:
        raise HTTPException(status_code=404, detail="Proceedings not found")

    # Check if relationship exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == proceedings_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = author_publication.delete().where(
        (author_publication.c.publication_1 == proceedings_id) &
        (author_publication.c.author_1 == author_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Author removed from author_1 successfully"}


@app.get("/proceedings/{proceedings_id}/author_1/", response_model=None, tags=["Proceedings Relationships"])
async def get_author_1_of_proceedings(proceedings_id: int, database: Session = Depends(get_db)):
    """Get all Author entities related to this Proceedings through author_1"""
    db_proceedings = database.query(Proceedings).filter(Proceedings.id == proceedings_id).first()
    if db_proceedings is None:
        raise HTTPException(status_code=404, detail="Proceedings not found")

    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == proceedings_id).all()
    author_list = database.query(Author).filter(Author.id.in_([id[0] for id in author_ids])).all()

    return {
        "proceedings_id": proceedings_id,
        "author_1_count": len(author_list),
        "author_1": author_list
    }





############################################
#
#   Book functions
#
############################################

@app.get("/book/", response_model=None, tags=["Book"])
def get_all_book(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Book)
        book_list = query.all()

        # Serialize with relationships included
        result = []
        for book_item in book_list:
            item_dict = book_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            institution_list = database.query(Institution).join(publication_institution, Institution.id == publication_institution.c.institution_1).filter(publication_institution.c.publication == book_item.id).all()
            item_dict['institution_1'] = []
            for institution_obj in institution_list:
                institution_dict = institution_obj.__dict__.copy()
                institution_dict.pop('_sa_instance_state', None)
                item_dict['institution_1'].append(institution_dict)
            author_list = database.query(Author).join(author_publication, Author.id == author_publication.c.author_1).filter(author_publication.c.publication_1 == book_item.id).all()
            item_dict['author_1'] = []
            for author_obj in author_list:
                author_dict = author_obj.__dict__.copy()
                author_dict.pop('_sa_instance_state', None)
                item_dict['author_1'].append(author_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Book).all()


@app.get("/book/count/", response_model=None, tags=["Book"])
def get_count_book(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Book entities"""
    count = database.query(Book).count()
    return {"count": count}


@app.get("/book/paginated/", response_model=None, tags=["Book"])
def get_paginated_book(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Book entities"""
    total = database.query(Book).count()
    book_list = database.query(Book).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": book_list
        }

    result = []
    for book_item in book_list:
        institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == book_item.id).all()
        author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == book_item.id).all()
        item_data = {
            "book": book_item,
            "institution_ids": [x[0] for x in institution_ids],
            "author_ids": [x[0] for x in author_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/book/search/", response_model=None, tags=["Book"])
def search_book(
    database: Session = Depends(get_db)
) -> list:
    """Search Book entities by attributes"""
    query = database.query(Book)


    results = query.all()
    return results


@app.get("/book/{book_id}/", response_model=None, tags=["Book"])
async def get_book(book_id: int, database: Session = Depends(get_db)) -> Book:
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_book.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_book.id).all()
    response_data = {
        "book": db_book,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
}
    return response_data



@app.post("/book/", response_model=None, tags=["Book"])
async def create_book(book_data: BookCreate, database: Session = Depends(get_db)) -> Book:

    if not book_data.institution_1 or len(book_data.institution_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Institution(s) required")
    if book_data.institution_1:
        for id in book_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            if not db_institution:
                raise HTTPException(status_code=404, detail=f"Institution with ID {id} not found")
    if not book_data.author_1 or len(book_data.author_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Author(s) required")
    if book_data.author_1:
        for id in book_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            if not db_author:
                raise HTTPException(status_code=404, detail=f"Author with ID {id} not found")

    db_book = Book(
        title=book_data.title,        year=book_data.year,        address=book_data.address,        publisher=book_data.publisher        )

    database.add(db_book)
    database.commit()
    database.refresh(db_book)


    if book_data.institution_1:
        for id in book_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            # Create the association
            association = publication_institution.insert().values(publication=db_book.id, institution_1=db_institution.id)
            database.execute(association)
            database.commit()
    if book_data.author_1:
        for id in book_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            # Create the association
            association = author_publication.insert().values(publication_1=db_book.id, author_1=db_author.id)
            database.execute(association)
            database.commit()


    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_book.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_book.id).all()
    response_data = {
        "book": db_book,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.post("/book/bulk/", response_model=None, tags=["Book"])
async def bulk_create_book(items: list[BookCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Book entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_book = Book(
                title=item_data.title,                year=item_data.year,                address=item_data.address,                publisher=item_data.publisher            )
            database.add(db_book)
            database.flush()  # Get ID without committing
            created_items.append(db_book.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Book entities"
    }


@app.delete("/book/bulk/", response_model=None, tags=["Book"])
async def bulk_delete_book(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Book entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_book = database.query(Book).filter(Book.id == item_id).first()
        if db_book:
            database.delete(db_book)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Book entities"
    }

@app.put("/book/{book_id}/", response_model=None, tags=["Book"])
async def update_book(book_id: int, book_data: BookCreate, database: Session = Depends(get_db)) -> Book:
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    setattr(db_book, 'address', book_data.address)
    setattr(db_book, 'publisher', book_data.publisher)
    existing_institution_ids = [assoc.institution_1 for assoc in database.execute(
        publication_institution.select().where(publication_institution.c.publication == db_book.id))]

    institutions_to_remove = set(existing_institution_ids) - set(book_data.institution_1)
    for institution_id in institutions_to_remove:
        association = publication_institution.delete().where(
            (publication_institution.c.publication == db_book.id) & (publication_institution.c.institution_1 == institution_id))
        database.execute(association)

    new_institution_ids = set(book_data.institution_1) - set(existing_institution_ids)
    for institution_id in new_institution_ids:
        db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
        if db_institution is None:
            raise HTTPException(status_code=404, detail=f"Institution with ID {institution_id} not found")
        association = publication_institution.insert().values(institution_1=db_institution.id, publication=db_book.id)
        database.execute(association)
    existing_author_ids = [assoc.author_1 for assoc in database.execute(
        author_publication.select().where(author_publication.c.publication_1 == db_book.id))]

    authors_to_remove = set(existing_author_ids) - set(book_data.author_1)
    for author_id in authors_to_remove:
        association = author_publication.delete().where(
            (author_publication.c.publication_1 == db_book.id) & (author_publication.c.author_1 == author_id))
        database.execute(association)

    new_author_ids = set(book_data.author_1) - set(existing_author_ids)
    for author_id in new_author_ids:
        db_author = database.query(Author).filter(Author.id == author_id).first()
        if db_author is None:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        association = author_publication.insert().values(author_1=db_author.id, publication_1=db_book.id)
        database.execute(association)
    database.commit()
    database.refresh(db_book)

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_book.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_book.id).all()
    response_data = {
        "book": db_book,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.delete("/book/{book_id}/", response_model=None, tags=["Book"])
async def delete_book(book_id: int, database: Session = Depends(get_db)):
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    database.delete(db_book)
    database.commit()
    return db_book

@app.post("/book/{book_id}/institution_1/{institution_id}/", response_model=None, tags=["Book Relationships"])
async def add_institution_1_to_book(book_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Add a Institution to this Book's institution_1 relationship"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Check if relationship already exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == book_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = publication_institution.insert().values(publication=book_id, institution_1=institution_id)
    database.execute(association)
    database.commit()

    return {"message": "Institution added to institution_1 successfully"}


@app.delete("/book/{book_id}/institution_1/{institution_id}/", response_model=None, tags=["Book Relationships"])
async def remove_institution_1_from_book(book_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Remove a Institution from this Book's institution_1 relationship"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if relationship exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == book_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = publication_institution.delete().where(
        (publication_institution.c.publication == book_id) &
        (publication_institution.c.institution_1 == institution_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Institution removed from institution_1 successfully"}


@app.get("/book/{book_id}/institution_1/", response_model=None, tags=["Book Relationships"])
async def get_institution_1_of_book(book_id: int, database: Session = Depends(get_db)):
    """Get all Institution entities related to this Book through institution_1"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == book_id).all()
    institution_list = database.query(Institution).filter(Institution.id.in_([id[0] for id in institution_ids])).all()

    return {
        "book_id": book_id,
        "institution_1_count": len(institution_list),
        "institution_1": institution_list
    }

@app.post("/book/{book_id}/author_1/{author_id}/", response_model=None, tags=["Book Relationships"])
async def add_author_1_to_book(book_id: int, author_id: int, database: Session = Depends(get_db)):
    """Add a Author to this Book's author_1 relationship"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship already exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == book_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = author_publication.insert().values(publication_1=book_id, author_1=author_id)
    database.execute(association)
    database.commit()

    return {"message": "Author added to author_1 successfully"}


@app.delete("/book/{book_id}/author_1/{author_id}/", response_model=None, tags=["Book Relationships"])
async def remove_author_1_from_book(book_id: int, author_id: int, database: Session = Depends(get_db)):
    """Remove a Author from this Book's author_1 relationship"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    # Check if relationship exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == book_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = author_publication.delete().where(
        (author_publication.c.publication_1 == book_id) &
        (author_publication.c.author_1 == author_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Author removed from author_1 successfully"}


@app.get("/book/{book_id}/author_1/", response_model=None, tags=["Book Relationships"])
async def get_author_1_of_book(book_id: int, database: Session = Depends(get_db)):
    """Get all Author entities related to this Book through author_1"""
    db_book = database.query(Book).filter(Book.id == book_id).first()
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == book_id).all()
    author_list = database.query(Author).filter(Author.id.in_([id[0] for id in author_ids])).all()

    return {
        "book_id": book_id,
        "author_1_count": len(author_list),
        "author_1": author_list
    }





############################################
#
#   Thesis functions
#
############################################

@app.get("/thesis/", response_model=None, tags=["Thesis"])
def get_all_thesis(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Thesis)
        thesis_list = query.all()

        # Serialize with relationships included
        result = []
        for thesis_item in thesis_list:
            item_dict = thesis_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            institution_list = database.query(Institution).join(publication_institution, Institution.id == publication_institution.c.institution_1).filter(publication_institution.c.publication == thesis_item.id).all()
            item_dict['institution_1'] = []
            for institution_obj in institution_list:
                institution_dict = institution_obj.__dict__.copy()
                institution_dict.pop('_sa_instance_state', None)
                item_dict['institution_1'].append(institution_dict)
            author_list = database.query(Author).join(author_publication, Author.id == author_publication.c.author_1).filter(author_publication.c.publication_1 == thesis_item.id).all()
            item_dict['author_1'] = []
            for author_obj in author_list:
                author_dict = author_obj.__dict__.copy()
                author_dict.pop('_sa_instance_state', None)
                item_dict['author_1'].append(author_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Thesis).all()


@app.get("/thesis/count/", response_model=None, tags=["Thesis"])
def get_count_thesis(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Thesis entities"""
    count = database.query(Thesis).count()
    return {"count": count}


@app.get("/thesis/paginated/", response_model=None, tags=["Thesis"])
def get_paginated_thesis(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Thesis entities"""
    total = database.query(Thesis).count()
    thesis_list = database.query(Thesis).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": thesis_list
        }

    result = []
    for thesis_item in thesis_list:
        institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == thesis_item.id).all()
        author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == thesis_item.id).all()
        item_data = {
            "thesis": thesis_item,
            "institution_ids": [x[0] for x in institution_ids],
            "author_ids": [x[0] for x in author_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/thesis/search/", response_model=None, tags=["Thesis"])
def search_thesis(
    database: Session = Depends(get_db)
) -> list:
    """Search Thesis entities by attributes"""
    query = database.query(Thesis)


    results = query.all()
    return results


@app.get("/thesis/{thesis_id}/", response_model=None, tags=["Thesis"])
async def get_thesis(thesis_id: int, database: Session = Depends(get_db)) -> Thesis:
    db_thesis = database.query(Thesis).filter(Thesis.id == thesis_id).first()
    if db_thesis is None:
        raise HTTPException(status_code=404, detail="Thesis not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_thesis.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_thesis.id).all()
    response_data = {
        "thesis": db_thesis,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
}
    return response_data



@app.post("/thesis/", response_model=None, tags=["Thesis"])
async def create_thesis(thesis_data: ThesisCreate, database: Session = Depends(get_db)) -> Thesis:

    if not thesis_data.institution_1 or len(thesis_data.institution_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Institution(s) required")
    if thesis_data.institution_1:
        for id in thesis_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            if not db_institution:
                raise HTTPException(status_code=404, detail=f"Institution with ID {id} not found")
    if not thesis_data.author_1 or len(thesis_data.author_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Author(s) required")
    if thesis_data.author_1:
        for id in thesis_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            if not db_author:
                raise HTTPException(status_code=404, detail=f"Author with ID {id} not found")

    db_thesis = Thesis(
        title=thesis_data.title,        year=thesis_data.year,        month=thesis_data.month,        note=thesis_data.note,        address=thesis_data.address,        type=thesis_data.type        )

    database.add(db_thesis)
    database.commit()
    database.refresh(db_thesis)


    if thesis_data.institution_1:
        for id in thesis_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            # Create the association
            association = publication_institution.insert().values(publication=db_thesis.id, institution_1=db_institution.id)
            database.execute(association)
            database.commit()
    if thesis_data.author_1:
        for id in thesis_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            # Create the association
            association = author_publication.insert().values(publication_1=db_thesis.id, author_1=db_author.id)
            database.execute(association)
            database.commit()


    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_thesis.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_thesis.id).all()
    response_data = {
        "thesis": db_thesis,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.post("/thesis/bulk/", response_model=None, tags=["Thesis"])
async def bulk_create_thesis(items: list[ThesisCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Thesis entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_thesis = Thesis(
                title=item_data.title,                year=item_data.year,                month=item_data.month,                note=item_data.note,                address=item_data.address,                type=item_data.type            )
            database.add(db_thesis)
            database.flush()  # Get ID without committing
            created_items.append(db_thesis.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Thesis entities"
    }


@app.delete("/thesis/bulk/", response_model=None, tags=["Thesis"])
async def bulk_delete_thesis(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Thesis entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_thesis = database.query(Thesis).filter(Thesis.id == item_id).first()
        if db_thesis:
            database.delete(db_thesis)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Thesis entities"
    }

@app.put("/thesis/{thesis_id}/", response_model=None, tags=["Thesis"])
async def update_thesis(thesis_id: int, thesis_data: ThesisCreate, database: Session = Depends(get_db)) -> Thesis:
    db_thesis = database.query(Thesis).filter(Thesis.id == thesis_id).first()
    if db_thesis is None:
        raise HTTPException(status_code=404, detail="Thesis not found")

    setattr(db_thesis, 'month', thesis_data.month)
    setattr(db_thesis, 'note', thesis_data.note)
    setattr(db_thesis, 'address', thesis_data.address)
    setattr(db_thesis, 'type', thesis_data.type)
    existing_institution_ids = [assoc.institution_1 for assoc in database.execute(
        publication_institution.select().where(publication_institution.c.publication == db_thesis.id))]

    institutions_to_remove = set(existing_institution_ids) - set(thesis_data.institution_1)
    for institution_id in institutions_to_remove:
        association = publication_institution.delete().where(
            (publication_institution.c.publication == db_thesis.id) & (publication_institution.c.institution_1 == institution_id))
        database.execute(association)

    new_institution_ids = set(thesis_data.institution_1) - set(existing_institution_ids)
    for institution_id in new_institution_ids:
        db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
        if db_institution is None:
            raise HTTPException(status_code=404, detail=f"Institution with ID {institution_id} not found")
        association = publication_institution.insert().values(institution_1=db_institution.id, publication=db_thesis.id)
        database.execute(association)
    existing_author_ids = [assoc.author_1 for assoc in database.execute(
        author_publication.select().where(author_publication.c.publication_1 == db_thesis.id))]

    authors_to_remove = set(existing_author_ids) - set(thesis_data.author_1)
    for author_id in authors_to_remove:
        association = author_publication.delete().where(
            (author_publication.c.publication_1 == db_thesis.id) & (author_publication.c.author_1 == author_id))
        database.execute(association)

    new_author_ids = set(thesis_data.author_1) - set(existing_author_ids)
    for author_id in new_author_ids:
        db_author = database.query(Author).filter(Author.id == author_id).first()
        if db_author is None:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        association = author_publication.insert().values(author_1=db_author.id, publication_1=db_thesis.id)
        database.execute(association)
    database.commit()
    database.refresh(db_thesis)

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_thesis.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_thesis.id).all()
    response_data = {
        "thesis": db_thesis,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.delete("/thesis/{thesis_id}/", response_model=None, tags=["Thesis"])
async def delete_thesis(thesis_id: int, database: Session = Depends(get_db)):
    db_thesis = database.query(Thesis).filter(Thesis.id == thesis_id).first()
    if db_thesis is None:
        raise HTTPException(status_code=404, detail="Thesis not found")
    database.delete(db_thesis)
    database.commit()
    return db_thesis

@app.post("/thesis/{thesis_id}/institution_1/{institution_id}/", response_model=None, tags=["Thesis Relationships"])
async def add_institution_1_to_thesis(thesis_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Add a Institution to this Thesis's institution_1 relationship"""
    db_thesis = database.query(Thesis).filter(Thesis.id == thesis_id).first()
    if db_thesis is None:
        raise HTTPException(status_code=404, detail="Thesis not found")

    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Check if relationship already exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == thesis_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = publication_institution.insert().values(publication=thesis_id, institution_1=institution_id)
    database.execute(association)
    database.commit()

    return {"message": "Institution added to institution_1 successfully"}


@app.delete("/thesis/{thesis_id}/institution_1/{institution_id}/", response_model=None, tags=["Thesis Relationships"])
async def remove_institution_1_from_thesis(thesis_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Remove a Institution from this Thesis's institution_1 relationship"""
    db_thesis = database.query(Thesis).filter(Thesis.id == thesis_id).first()
    if db_thesis is None:
        raise HTTPException(status_code=404, detail="Thesis not found")

    # Check if relationship exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == thesis_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = publication_institution.delete().where(
        (publication_institution.c.publication == thesis_id) &
        (publication_institution.c.institution_1 == institution_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Institution removed from institution_1 successfully"}


@app.get("/thesis/{thesis_id}/institution_1/", response_model=None, tags=["Thesis Relationships"])
async def get_institution_1_of_thesis(thesis_id: int, database: Session = Depends(get_db)):
    """Get all Institution entities related to this Thesis through institution_1"""
    db_thesis = database.query(Thesis).filter(Thesis.id == thesis_id).first()
    if db_thesis is None:
        raise HTTPException(status_code=404, detail="Thesis not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == thesis_id).all()
    institution_list = database.query(Institution).filter(Institution.id.in_([id[0] for id in institution_ids])).all()

    return {
        "thesis_id": thesis_id,
        "institution_1_count": len(institution_list),
        "institution_1": institution_list
    }

@app.post("/thesis/{thesis_id}/author_1/{author_id}/", response_model=None, tags=["Thesis Relationships"])
async def add_author_1_to_thesis(thesis_id: int, author_id: int, database: Session = Depends(get_db)):
    """Add a Author to this Thesis's author_1 relationship"""
    db_thesis = database.query(Thesis).filter(Thesis.id == thesis_id).first()
    if db_thesis is None:
        raise HTTPException(status_code=404, detail="Thesis not found")

    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship already exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == thesis_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = author_publication.insert().values(publication_1=thesis_id, author_1=author_id)
    database.execute(association)
    database.commit()

    return {"message": "Author added to author_1 successfully"}


@app.delete("/thesis/{thesis_id}/author_1/{author_id}/", response_model=None, tags=["Thesis Relationships"])
async def remove_author_1_from_thesis(thesis_id: int, author_id: int, database: Session = Depends(get_db)):
    """Remove a Author from this Thesis's author_1 relationship"""
    db_thesis = database.query(Thesis).filter(Thesis.id == thesis_id).first()
    if db_thesis is None:
        raise HTTPException(status_code=404, detail="Thesis not found")

    # Check if relationship exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == thesis_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = author_publication.delete().where(
        (author_publication.c.publication_1 == thesis_id) &
        (author_publication.c.author_1 == author_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Author removed from author_1 successfully"}


@app.get("/thesis/{thesis_id}/author_1/", response_model=None, tags=["Thesis Relationships"])
async def get_author_1_of_thesis(thesis_id: int, database: Session = Depends(get_db)):
    """Get all Author entities related to this Thesis through author_1"""
    db_thesis = database.query(Thesis).filter(Thesis.id == thesis_id).first()
    if db_thesis is None:
        raise HTTPException(status_code=404, detail="Thesis not found")

    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == thesis_id).all()
    author_list = database.query(Author).filter(Author.id.in_([id[0] for id in author_ids])).all()

    return {
        "thesis_id": thesis_id,
        "author_1_count": len(author_list),
        "author_1": author_list
    }





############################################
#
#   Others functions
#
############################################

@app.get("/others/", response_model=None, tags=["Others"])
def get_all_others(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Others)
        others_list = query.all()

        # Serialize with relationships included
        result = []
        for others_item in others_list:
            item_dict = others_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            institution_list = database.query(Institution).join(publication_institution, Institution.id == publication_institution.c.institution_1).filter(publication_institution.c.publication == others_item.id).all()
            item_dict['institution_1'] = []
            for institution_obj in institution_list:
                institution_dict = institution_obj.__dict__.copy()
                institution_dict.pop('_sa_instance_state', None)
                item_dict['institution_1'].append(institution_dict)
            author_list = database.query(Author).join(author_publication, Author.id == author_publication.c.author_1).filter(author_publication.c.publication_1 == others_item.id).all()
            item_dict['author_1'] = []
            for author_obj in author_list:
                author_dict = author_obj.__dict__.copy()
                author_dict.pop('_sa_instance_state', None)
                item_dict['author_1'].append(author_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Others).all()


@app.get("/others/count/", response_model=None, tags=["Others"])
def get_count_others(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Others entities"""
    count = database.query(Others).count()
    return {"count": count}


@app.get("/others/paginated/", response_model=None, tags=["Others"])
def get_paginated_others(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Others entities"""
    total = database.query(Others).count()
    others_list = database.query(Others).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": others_list
        }

    result = []
    for others_item in others_list:
        institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == others_item.id).all()
        author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == others_item.id).all()
        item_data = {
            "others": others_item,
            "institution_ids": [x[0] for x in institution_ids],
            "author_ids": [x[0] for x in author_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/others/search/", response_model=None, tags=["Others"])
def search_others(
    database: Session = Depends(get_db)
) -> list:
    """Search Others entities by attributes"""
    query = database.query(Others)


    results = query.all()
    return results


@app.get("/others/{others_id}/", response_model=None, tags=["Others"])
async def get_others(others_id: int, database: Session = Depends(get_db)) -> Others:
    db_others = database.query(Others).filter(Others.id == others_id).first()
    if db_others is None:
        raise HTTPException(status_code=404, detail="Others not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_others.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_others.id).all()
    response_data = {
        "others": db_others,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
}
    return response_data



@app.post("/others/", response_model=None, tags=["Others"])
async def create_others(others_data: OthersCreate, database: Session = Depends(get_db)) -> Others:

    if not others_data.institution_1 or len(others_data.institution_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Institution(s) required")
    if others_data.institution_1:
        for id in others_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            if not db_institution:
                raise HTTPException(status_code=404, detail=f"Institution with ID {id} not found")
    if not others_data.author_1 or len(others_data.author_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Author(s) required")
    if others_data.author_1:
        for id in others_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            if not db_author:
                raise HTTPException(status_code=404, detail=f"Author with ID {id} not found")

    db_others = Others(
        title=others_data.title,        year=others_data.year,        link=others_data.link,        peer_reviewed=others_data.peer_reviewed,        server=others_data.server        )

    database.add(db_others)
    database.commit()
    database.refresh(db_others)


    if others_data.institution_1:
        for id in others_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            # Create the association
            association = publication_institution.insert().values(publication=db_others.id, institution_1=db_institution.id)
            database.execute(association)
            database.commit()
    if others_data.author_1:
        for id in others_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            # Create the association
            association = author_publication.insert().values(publication_1=db_others.id, author_1=db_author.id)
            database.execute(association)
            database.commit()


    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_others.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_others.id).all()
    response_data = {
        "others": db_others,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.post("/others/bulk/", response_model=None, tags=["Others"])
async def bulk_create_others(items: list[OthersCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Others entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_others = Others(
                title=item_data.title,                year=item_data.year,                link=item_data.link,                peer_reviewed=item_data.peer_reviewed,                server=item_data.server            )
            database.add(db_others)
            database.flush()  # Get ID without committing
            created_items.append(db_others.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Others entities"
    }


@app.delete("/others/bulk/", response_model=None, tags=["Others"])
async def bulk_delete_others(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Others entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_others = database.query(Others).filter(Others.id == item_id).first()
        if db_others:
            database.delete(db_others)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Others entities"
    }

@app.put("/others/{others_id}/", response_model=None, tags=["Others"])
async def update_others(others_id: int, others_data: OthersCreate, database: Session = Depends(get_db)) -> Others:
    db_others = database.query(Others).filter(Others.id == others_id).first()
    if db_others is None:
        raise HTTPException(status_code=404, detail="Others not found")

    setattr(db_others, 'link', others_data.link)
    setattr(db_others, 'peer_reviewed', others_data.peer_reviewed)
    setattr(db_others, 'server', others_data.server)
    existing_institution_ids = [assoc.institution_1 for assoc in database.execute(
        publication_institution.select().where(publication_institution.c.publication == db_others.id))]

    institutions_to_remove = set(existing_institution_ids) - set(others_data.institution_1)
    for institution_id in institutions_to_remove:
        association = publication_institution.delete().where(
            (publication_institution.c.publication == db_others.id) & (publication_institution.c.institution_1 == institution_id))
        database.execute(association)

    new_institution_ids = set(others_data.institution_1) - set(existing_institution_ids)
    for institution_id in new_institution_ids:
        db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
        if db_institution is None:
            raise HTTPException(status_code=404, detail=f"Institution with ID {institution_id} not found")
        association = publication_institution.insert().values(institution_1=db_institution.id, publication=db_others.id)
        database.execute(association)
    existing_author_ids = [assoc.author_1 for assoc in database.execute(
        author_publication.select().where(author_publication.c.publication_1 == db_others.id))]

    authors_to_remove = set(existing_author_ids) - set(others_data.author_1)
    for author_id in authors_to_remove:
        association = author_publication.delete().where(
            (author_publication.c.publication_1 == db_others.id) & (author_publication.c.author_1 == author_id))
        database.execute(association)

    new_author_ids = set(others_data.author_1) - set(existing_author_ids)
    for author_id in new_author_ids:
        db_author = database.query(Author).filter(Author.id == author_id).first()
        if db_author is None:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        association = author_publication.insert().values(author_1=db_author.id, publication_1=db_others.id)
        database.execute(association)
    database.commit()
    database.refresh(db_others)

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_others.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_others.id).all()
    response_data = {
        "others": db_others,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.delete("/others/{others_id}/", response_model=None, tags=["Others"])
async def delete_others(others_id: int, database: Session = Depends(get_db)):
    db_others = database.query(Others).filter(Others.id == others_id).first()
    if db_others is None:
        raise HTTPException(status_code=404, detail="Others not found")
    database.delete(db_others)
    database.commit()
    return db_others

@app.post("/others/{others_id}/institution_1/{institution_id}/", response_model=None, tags=["Others Relationships"])
async def add_institution_1_to_others(others_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Add a Institution to this Others's institution_1 relationship"""
    db_others = database.query(Others).filter(Others.id == others_id).first()
    if db_others is None:
        raise HTTPException(status_code=404, detail="Others not found")

    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Check if relationship already exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == others_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = publication_institution.insert().values(publication=others_id, institution_1=institution_id)
    database.execute(association)
    database.commit()

    return {"message": "Institution added to institution_1 successfully"}


@app.delete("/others/{others_id}/institution_1/{institution_id}/", response_model=None, tags=["Others Relationships"])
async def remove_institution_1_from_others(others_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Remove a Institution from this Others's institution_1 relationship"""
    db_others = database.query(Others).filter(Others.id == others_id).first()
    if db_others is None:
        raise HTTPException(status_code=404, detail="Others not found")

    # Check if relationship exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == others_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = publication_institution.delete().where(
        (publication_institution.c.publication == others_id) &
        (publication_institution.c.institution_1 == institution_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Institution removed from institution_1 successfully"}


@app.get("/others/{others_id}/institution_1/", response_model=None, tags=["Others Relationships"])
async def get_institution_1_of_others(others_id: int, database: Session = Depends(get_db)):
    """Get all Institution entities related to this Others through institution_1"""
    db_others = database.query(Others).filter(Others.id == others_id).first()
    if db_others is None:
        raise HTTPException(status_code=404, detail="Others not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == others_id).all()
    institution_list = database.query(Institution).filter(Institution.id.in_([id[0] for id in institution_ids])).all()

    return {
        "others_id": others_id,
        "institution_1_count": len(institution_list),
        "institution_1": institution_list
    }

@app.post("/others/{others_id}/author_1/{author_id}/", response_model=None, tags=["Others Relationships"])
async def add_author_1_to_others(others_id: int, author_id: int, database: Session = Depends(get_db)):
    """Add a Author to this Others's author_1 relationship"""
    db_others = database.query(Others).filter(Others.id == others_id).first()
    if db_others is None:
        raise HTTPException(status_code=404, detail="Others not found")

    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship already exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == others_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = author_publication.insert().values(publication_1=others_id, author_1=author_id)
    database.execute(association)
    database.commit()

    return {"message": "Author added to author_1 successfully"}


@app.delete("/others/{others_id}/author_1/{author_id}/", response_model=None, tags=["Others Relationships"])
async def remove_author_1_from_others(others_id: int, author_id: int, database: Session = Depends(get_db)):
    """Remove a Author from this Others's author_1 relationship"""
    db_others = database.query(Others).filter(Others.id == others_id).first()
    if db_others is None:
        raise HTTPException(status_code=404, detail="Others not found")

    # Check if relationship exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == others_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = author_publication.delete().where(
        (author_publication.c.publication_1 == others_id) &
        (author_publication.c.author_1 == author_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Author removed from author_1 successfully"}


@app.get("/others/{others_id}/author_1/", response_model=None, tags=["Others Relationships"])
async def get_author_1_of_others(others_id: int, database: Session = Depends(get_db)):
    """Get all Author entities related to this Others through author_1"""
    db_others = database.query(Others).filter(Others.id == others_id).first()
    if db_others is None:
        raise HTTPException(status_code=404, detail="Others not found")

    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == others_id).all()
    author_list = database.query(Author).filter(Author.id.in_([id[0] for id in author_ids])).all()

    return {
        "others_id": others_id,
        "author_1_count": len(author_list),
        "author_1": author_list
    }





############################################
#
#   Journal functions
#
############################################

@app.get("/journal/", response_model=None, tags=["Journal"])
def get_all_journal(detailed: bool = False, database: Session = Depends(get_db)) -> list:
    from sqlalchemy.orm import joinedload

    # Use detailed=true to get entities with eagerly loaded relationships (for tables with lookup columns)
    if detailed:
        # Eagerly load all relationships to avoid N+1 queries
        query = database.query(Journal)
        journal_list = query.all()

        # Serialize with relationships included
        result = []
        for journal_item in journal_list:
            item_dict = journal_item.__dict__.copy()
            item_dict.pop('_sa_instance_state', None)

            # Add many-to-one relationships (foreign keys for lookup columns)

            # Add many-to-many and one-to-many relationship objects (full details)
            institution_list = database.query(Institution).join(publication_institution, Institution.id == publication_institution.c.institution_1).filter(publication_institution.c.publication == journal_item.id).all()
            item_dict['institution_1'] = []
            for institution_obj in institution_list:
                institution_dict = institution_obj.__dict__.copy()
                institution_dict.pop('_sa_instance_state', None)
                item_dict['institution_1'].append(institution_dict)
            author_list = database.query(Author).join(author_publication, Author.id == author_publication.c.author_1).filter(author_publication.c.publication_1 == journal_item.id).all()
            item_dict['author_1'] = []
            for author_obj in author_list:
                author_dict = author_obj.__dict__.copy()
                author_dict.pop('_sa_instance_state', None)
                item_dict['author_1'].append(author_dict)

            result.append(item_dict)
        return result
    else:
        # Default: return flat entities (faster for charts/widgets without lookup columns)
        return database.query(Journal).all()


@app.get("/journal/count/", response_model=None, tags=["Journal"])
def get_count_journal(database: Session = Depends(get_db)) -> dict:
    """Get the total count of Journal entities"""
    count = database.query(Journal).count()
    return {"count": count}


@app.get("/journal/paginated/", response_model=None, tags=["Journal"])
def get_paginated_journal(skip: int = 0, limit: int = 100, detailed: bool = False, database: Session = Depends(get_db)) -> dict:
    """Get paginated list of Journal entities"""
    total = database.query(Journal).count()
    journal_list = database.query(Journal).offset(skip).limit(limit).all()
    # By default, return flat entities (for charts/widgets)
    # Use detailed=true to get entities with relationships
    if not detailed:
        return {
            "total": total,
            "skip": skip,
            "limit": limit,
            "data": journal_list
        }

    result = []
    for journal_item in journal_list:
        institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == journal_item.id).all()
        author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == journal_item.id).all()
        item_data = {
            "journal": journal_item,
            "institution_ids": [x[0] for x in institution_ids],
            "author_ids": [x[0] for x in author_ids],
        }
        result.append(item_data)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": result
    }


@app.get("/journal/search/", response_model=None, tags=["Journal"])
def search_journal(
    database: Session = Depends(get_db)
) -> list:
    """Search Journal entities by attributes"""
    query = database.query(Journal)


    results = query.all()
    return results


@app.get("/journal/{journal_id}/", response_model=None, tags=["Journal"])
async def get_journal(journal_id: int, database: Session = Depends(get_db)) -> Journal:
    db_journal = database.query(Journal).filter(Journal.id == journal_id).first()
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_journal.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_journal.id).all()
    response_data = {
        "journal": db_journal,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
}
    return response_data



@app.post("/journal/", response_model=None, tags=["Journal"])
async def create_journal(journal_data: JournalCreate, database: Session = Depends(get_db)) -> Journal:

    if not journal_data.institution_1 or len(journal_data.institution_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Institution(s) required")
    if journal_data.institution_1:
        for id in journal_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            if not db_institution:
                raise HTTPException(status_code=404, detail=f"Institution with ID {id} not found")
    if not journal_data.author_1 or len(journal_data.author_1) < 1:
        raise HTTPException(status_code=400, detail="At least 1 Author(s) required")
    if journal_data.author_1:
        for id in journal_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            if not db_author:
                raise HTTPException(status_code=404, detail=f"Author with ID {id} not found")

    db_journal = Journal(
        title=journal_data.title,        year=journal_data.year,        month=journal_data.month,        volume=journal_data.volume,        note=journal_data.note,        pages=journal_data.pages,        journal=journal_data.journal,        number=journal_data.number        )

    database.add(db_journal)
    database.commit()
    database.refresh(db_journal)


    if journal_data.institution_1:
        for id in journal_data.institution_1:
            # Entity already validated before creation
            db_institution = database.query(Institution).filter(Institution.id == id).first()
            # Create the association
            association = publication_institution.insert().values(publication=db_journal.id, institution_1=db_institution.id)
            database.execute(association)
            database.commit()
    if journal_data.author_1:
        for id in journal_data.author_1:
            # Entity already validated before creation
            db_author = database.query(Author).filter(Author.id == id).first()
            # Create the association
            association = author_publication.insert().values(publication_1=db_journal.id, author_1=db_author.id)
            database.execute(association)
            database.commit()


    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_journal.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_journal.id).all()
    response_data = {
        "journal": db_journal,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.post("/journal/bulk/", response_model=None, tags=["Journal"])
async def bulk_create_journal(items: list[JournalCreate], database: Session = Depends(get_db)) -> dict:
    """Create multiple Journal entities at once"""
    created_items = []
    errors = []

    for idx, item_data in enumerate(items):
        try:
            # Basic validation for each item

            db_journal = Journal(
                title=item_data.title,                year=item_data.year,                month=item_data.month,                volume=item_data.volume,                note=item_data.note,                pages=item_data.pages,                journal=item_data.journal,                number=item_data.number            )
            database.add(db_journal)
            database.flush()  # Get ID without committing
            created_items.append(db_journal.id)
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    if errors:
        database.rollback()
        raise HTTPException(status_code=400, detail={"message": "Bulk creation failed", "errors": errors})

    database.commit()
    return {
        "created_count": len(created_items),
        "created_ids": created_items,
        "message": f"Successfully created {len(created_items)} Journal entities"
    }


@app.delete("/journal/bulk/", response_model=None, tags=["Journal"])
async def bulk_delete_journal(ids: list[int], database: Session = Depends(get_db)) -> dict:
    """Delete multiple Journal entities at once"""
    deleted_count = 0
    not_found = []

    for item_id in ids:
        db_journal = database.query(Journal).filter(Journal.id == item_id).first()
        if db_journal:
            database.delete(db_journal)
            deleted_count += 1
        else:
            not_found.append(item_id)

    database.commit()

    return {
        "deleted_count": deleted_count,
        "not_found": not_found,
        "message": f"Successfully deleted {deleted_count} Journal entities"
    }

@app.put("/journal/{journal_id}/", response_model=None, tags=["Journal"])
async def update_journal(journal_id: int, journal_data: JournalCreate, database: Session = Depends(get_db)) -> Journal:
    db_journal = database.query(Journal).filter(Journal.id == journal_id).first()
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")

    setattr(db_journal, 'month', journal_data.month)
    setattr(db_journal, 'volume', journal_data.volume)
    setattr(db_journal, 'note', journal_data.note)
    setattr(db_journal, 'pages', journal_data.pages)
    setattr(db_journal, 'journal', journal_data.journal)
    setattr(db_journal, 'number', journal_data.number)
    existing_institution_ids = [assoc.institution_1 for assoc in database.execute(
        publication_institution.select().where(publication_institution.c.publication == db_journal.id))]

    institutions_to_remove = set(existing_institution_ids) - set(journal_data.institution_1)
    for institution_id in institutions_to_remove:
        association = publication_institution.delete().where(
            (publication_institution.c.publication == db_journal.id) & (publication_institution.c.institution_1 == institution_id))
        database.execute(association)

    new_institution_ids = set(journal_data.institution_1) - set(existing_institution_ids)
    for institution_id in new_institution_ids:
        db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
        if db_institution is None:
            raise HTTPException(status_code=404, detail=f"Institution with ID {institution_id} not found")
        association = publication_institution.insert().values(institution_1=db_institution.id, publication=db_journal.id)
        database.execute(association)
    existing_author_ids = [assoc.author_1 for assoc in database.execute(
        author_publication.select().where(author_publication.c.publication_1 == db_journal.id))]

    authors_to_remove = set(existing_author_ids) - set(journal_data.author_1)
    for author_id in authors_to_remove:
        association = author_publication.delete().where(
            (author_publication.c.publication_1 == db_journal.id) & (author_publication.c.author_1 == author_id))
        database.execute(association)

    new_author_ids = set(journal_data.author_1) - set(existing_author_ids)
    for author_id in new_author_ids:
        db_author = database.query(Author).filter(Author.id == author_id).first()
        if db_author is None:
            raise HTTPException(status_code=404, detail=f"Author with ID {author_id} not found")
        association = author_publication.insert().values(author_1=db_author.id, publication_1=db_journal.id)
        database.execute(association)
    database.commit()
    database.refresh(db_journal)

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == db_journal.id).all()
    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == db_journal.id).all()
    response_data = {
        "journal": db_journal,
        "institution_ids": [x[0] for x in institution_ids],
        "author_ids": [x[0] for x in author_ids],
    }
    return response_data


@app.delete("/journal/{journal_id}/", response_model=None, tags=["Journal"])
async def delete_journal(journal_id: int, database: Session = Depends(get_db)):
    db_journal = database.query(Journal).filter(Journal.id == journal_id).first()
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")
    database.delete(db_journal)
    database.commit()
    return db_journal

@app.post("/journal/{journal_id}/institution_1/{institution_id}/", response_model=None, tags=["Journal Relationships"])
async def add_institution_1_to_journal(journal_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Add a Institution to this Journal's institution_1 relationship"""
    db_journal = database.query(Journal).filter(Journal.id == journal_id).first()
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")

    db_institution = database.query(Institution).filter(Institution.id == institution_id).first()
    if db_institution is None:
        raise HTTPException(status_code=404, detail="Institution not found")

    # Check if relationship already exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == journal_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = publication_institution.insert().values(publication=journal_id, institution_1=institution_id)
    database.execute(association)
    database.commit()

    return {"message": "Institution added to institution_1 successfully"}


@app.delete("/journal/{journal_id}/institution_1/{institution_id}/", response_model=None, tags=["Journal Relationships"])
async def remove_institution_1_from_journal(journal_id: int, institution_id: int, database: Session = Depends(get_db)):
    """Remove a Institution from this Journal's institution_1 relationship"""
    db_journal = database.query(Journal).filter(Journal.id == journal_id).first()
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")

    # Check if relationship exists
    existing = database.query(publication_institution).filter(
        (publication_institution.c.publication == journal_id) &
        (publication_institution.c.institution_1 == institution_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = publication_institution.delete().where(
        (publication_institution.c.publication == journal_id) &
        (publication_institution.c.institution_1 == institution_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Institution removed from institution_1 successfully"}


@app.get("/journal/{journal_id}/institution_1/", response_model=None, tags=["Journal Relationships"])
async def get_institution_1_of_journal(journal_id: int, database: Session = Depends(get_db)):
    """Get all Institution entities related to this Journal through institution_1"""
    db_journal = database.query(Journal).filter(Journal.id == journal_id).first()
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")

    institution_ids = database.query(publication_institution.c.institution_1).filter(publication_institution.c.publication == journal_id).all()
    institution_list = database.query(Institution).filter(Institution.id.in_([id[0] for id in institution_ids])).all()

    return {
        "journal_id": journal_id,
        "institution_1_count": len(institution_list),
        "institution_1": institution_list
    }

@app.post("/journal/{journal_id}/author_1/{author_id}/", response_model=None, tags=["Journal Relationships"])
async def add_author_1_to_journal(journal_id: int, author_id: int, database: Session = Depends(get_db)):
    """Add a Author to this Journal's author_1 relationship"""
    db_journal = database.query(Journal).filter(Journal.id == journal_id).first()
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")

    db_author = database.query(Author).filter(Author.id == author_id).first()
    if db_author is None:
        raise HTTPException(status_code=404, detail="Author not found")

    # Check if relationship already exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == journal_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")

    # Create the association
    association = author_publication.insert().values(publication_1=journal_id, author_1=author_id)
    database.execute(association)
    database.commit()

    return {"message": "Author added to author_1 successfully"}


@app.delete("/journal/{journal_id}/author_1/{author_id}/", response_model=None, tags=["Journal Relationships"])
async def remove_author_1_from_journal(journal_id: int, author_id: int, database: Session = Depends(get_db)):
    """Remove a Author from this Journal's author_1 relationship"""
    db_journal = database.query(Journal).filter(Journal.id == journal_id).first()
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")

    # Check if relationship exists
    existing = database.query(author_publication).filter(
        (author_publication.c.publication_1 == journal_id) &
        (author_publication.c.author_1 == author_id)
    ).first()

    if not existing:
        raise HTTPException(status_code=404, detail="Relationship not found")

    # Delete the association
    association = author_publication.delete().where(
        (author_publication.c.publication_1 == journal_id) &
        (author_publication.c.author_1 == author_id)
    )
    database.execute(association)
    database.commit()

    return {"message": "Author removed from author_1 successfully"}


@app.get("/journal/{journal_id}/author_1/", response_model=None, tags=["Journal Relationships"])
async def get_author_1_of_journal(journal_id: int, database: Session = Depends(get_db)):
    """Get all Author entities related to this Journal through author_1"""
    db_journal = database.query(Journal).filter(Journal.id == journal_id).first()
    if db_journal is None:
        raise HTTPException(status_code=404, detail="Journal not found")

    author_ids = database.query(author_publication.c.author_1).filter(author_publication.c.publication_1 == journal_id).all()
    author_list = database.query(Author).filter(Author.id.in_([id[0] for id in author_ids])).all()

    return {
        "journal_id": journal_id,
        "author_1_count": len(author_list),
        "author_1": author_list
    }







############################################
# Maintaining the server
############################################
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)



