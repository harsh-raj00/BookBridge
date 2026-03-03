"""Tests for book marketplace endpoints."""


class TestCreateBook:
    """Tests for POST /books/"""

    def test_create_book_success(self, client, auth_headers):
        response = client.post("/books/", json={
            "title": "Data Structures & Algorithms",
            "author": "Cormen",
            "description": "Classic CLRS textbook",
            "price": 350.0,
            "condition": "good",
            "category": "engineering",
            "subject": "Computer Science",
            "semester": "3rd",
        }, headers=auth_headers)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Data Structures & Algorithms"
        assert data["price"] == 350.0
        assert data["condition"] == "good"
        assert data["category"] == "engineering"
        assert data["is_available"] is True

    def test_create_book_unauthorized(self, client):
        response = client.post("/books/", json={
            "title": "Test Book",
            "author": "Test",
            "price": 100.0,
        })
        assert response.status_code == 401


class TestBrowseBooks:
    """Tests for GET /books/"""

    def test_browse_empty(self, client):
        response = client.get("/books/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["books"] == []

    def test_browse_with_books(self, client, auth_headers):
        # Create two books
        for title in ["Physics Vol 1", "Chemistry Basics"]:
            client.post("/books/", json={
                "title": title,
                "author": "Author",
                "price": 200.0,
                "category": "engineering",
            }, headers=auth_headers)

        response = client.get("/books/")
        data = response.json()
        assert data["total"] == 2
        assert len(data["books"]) == 2
        assert data["page"] == 1

    def test_search_books(self, client, auth_headers):
        client.post("/books/", json={
            "title": "Organic Chemistry",
            "author": "Morrison",
            "price": 500.0,
            "category": "medical",
        }, headers=auth_headers)

        client.post("/books/", json={
            "title": "Physics HC Verma",
            "author": "HC Verma",
            "price": 300.0,
            "category": "engineering",
        }, headers=auth_headers)

        # Search by title
        response = client.get("/books/?search=Chemistry")
        assert response.json()["total"] == 1

        # Filter by category
        response = client.get("/books/?category=medical")
        assert response.json()["total"] == 1

    def test_price_filter(self, client, auth_headers):
        client.post("/books/", json={
            "title": "Cheap Book",
            "author": "A",
            "price": 50.0,
        }, headers=auth_headers)

        client.post("/books/", json={
            "title": "Expensive Book",
            "author": "B",
            "price": 1000.0,
        }, headers=auth_headers)

        response = client.get("/books/?max_price=200")
        assert response.json()["total"] == 1
        assert response.json()["books"][0]["title"] == "Cheap Book"


class TestBookCRUD:
    """Tests for update and delete operations."""

    def _create_book(self, client, auth_headers):
        response = client.post("/books/", json={
            "title": "Test Book",
            "author": "Test Author",
            "price": 100.0,
        }, headers=auth_headers)
        return response.json()

    def test_update_book(self, client, auth_headers):
        book = self._create_book(client, auth_headers)
        response = client.put(f"/books/{book['id']}", json={
            "price": 150.0,
            "condition": "like_new",
        }, headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["price"] == 150.0
        assert response.json()["condition"] == "like_new"

    def test_delete_book(self, client, auth_headers):
        book = self._create_book(client, auth_headers)
        response = client.delete(f"/books/{book['id']}", headers=auth_headers)
        assert response.status_code == 200

        # Verify it's gone
        response = client.get(f"/books/{book['id']}")
        assert response.status_code == 404

    def test_get_my_listings(self, client, auth_headers):
        self._create_book(client, auth_headers)
        response = client.get("/books/my-listings", headers=auth_headers)
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_get_categories(self, client):
        response = client.get("/books/categories")
        assert response.status_code == 200
        assert "categories" in response.json()
        assert "conditions" in response.json()
