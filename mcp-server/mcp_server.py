import json
from mcp.server.fastmcp import FastMCP
from sqlalchemy import func
from models import get_session, Dog, Breed

mcp = FastMCP("Dog Shelter", host="0.0.0.0", port=8000)


@mcp.tool()
def list_dogs() -> str:
    """List all dogs in the shelter with their id, name, and breed."""
    session = get_session()
    try:
        results = (
            session.query(Dog.id, Dog.name, Breed.name.label('breed'))
            .join(Breed, Dog.breed_id == Breed.id)
            .all()
        )
        dogs = [{'id': r.id, 'name': r.name, 'breed': r.breed} for r in results]
        return json.dumps(dogs)
    finally:
        session.close()


@mcp.tool()
def get_dog(dog_id: int) -> str:
    """Get detailed information about a specific dog by its ID.

    Args:
        dog_id: The unique identifier of the dog.
    """
    session = get_session()
    try:
        result = (
            session.query(
                Dog.id,
                Dog.name,
                Breed.name.label('breed'),
                Dog.age,
                Dog.description,
                Dog.gender,
                Dog.status,
            )
            .join(Breed, Dog.breed_id == Breed.id)
            .filter(Dog.id == dog_id)
            .first()
        )

        if not result:
            return json.dumps({"error": "Dog not found"})

        dog = {
            'id': result.id,
            'name': result.name,
            'breed': result.breed,
            'age': result.age,
            'description': result.description,
            'gender': result.gender,
            'status': result.status.name,
        }
        return json.dumps(dog)
    finally:
        session.close()


@mcp.tool()
def search_dogs(query: str) -> str:
    """Search for dogs by name or description (case-insensitive).

    Args:
        query: The search term to match against dog names and descriptions.
    """
    session = get_session()
    try:
        pattern = f"%{query}%"
        results = (
            session.query(Dog.id, Dog.name, Breed.name.label('breed'))
            .join(Breed, Dog.breed_id == Breed.id)
            .filter((Dog.name.ilike(pattern)) | (Dog.description.ilike(pattern)))
            .all()
        )
        dogs = [{'id': r.id, 'name': r.name, 'breed': r.breed} for r in results]
        return json.dumps(dogs)
    finally:
        session.close()


if __name__ == "__main__":
    mcp.run(transport="sse")
