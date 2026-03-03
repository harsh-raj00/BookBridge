"""Tests for StudyVault resource endpoints."""

import io


class TestResourceUpload:
    """Tests for POST /resources/upload"""

    def test_upload_resource(self, client, auth_headers):
        # Create a fake PDF file
        file_content = b"fake pdf content for testing"
        files = {"file": ("test_notes.pdf", io.BytesIO(file_content), "application/pdf")}
        data = {
            "title": "DSA Notes Semester 3",
            "description": "Complete data structures notes",
            "file_type": "notes",
            "category": "engineering",
            "subject": "Data Structures",
            "semester": "3rd",
            "tags": "dsa,algorithms,trees",
        }

        response = client.post(
            "/resources/upload",
            files=files,
            data=data,
            headers=auth_headers,
        )
        assert response.status_code == 201
        result = response.json()
        assert result["title"] == "DSA Notes Semester 3"
        assert result["subject"] == "Data Structures"
        assert result["download_count"] == 0

    def test_upload_unauthorized(self, client):
        files = {"file": ("test.pdf", io.BytesIO(b"content"), "application/pdf")}
        response = client.post(
            "/resources/upload",
            files=files,
            data={"title": "Test"},
        )
        assert response.status_code == 401


class TestBrowseResources:
    """Tests for GET /resources/"""

    def _upload_resource(self, client, auth_headers, title, subject="CS"):
        files = {"file": ("test.pdf", io.BytesIO(b"content"), "application/pdf")}
        return client.post(
            "/resources/upload",
            files=files,
            data={"title": title, "subject": subject, "file_type": "notes"},
            headers=auth_headers,
        )

    def test_browse_empty(self, client):
        response = client.get("/resources/")
        assert response.status_code == 200
        assert response.json()["total"] == 0

    def test_browse_with_resources(self, client, auth_headers):
        self._upload_resource(client, auth_headers, "Notes 1")
        self._upload_resource(client, auth_headers, "Notes 2")

        response = client.get("/resources/")
        assert response.json()["total"] == 2

    def test_search_resources(self, client, auth_headers):
        self._upload_resource(client, auth_headers, "Organic Chemistry Notes", "Chemistry")
        self._upload_resource(client, auth_headers, "Python Programming", "CS")

        response = client.get("/resources/?search=Chemistry")
        assert response.json()["total"] == 1

    def test_filter_by_subject(self, client, auth_headers):
        self._upload_resource(client, auth_headers, "Math Notes", "Mathematics")
        self._upload_resource(client, auth_headers, "CS Notes", "Computer Science")

        response = client.get("/resources/?subject=Math")
        assert response.json()["total"] == 1
