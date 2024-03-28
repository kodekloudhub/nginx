import pytest
import httpx
import json

# test our initial set of records:
def test_read_all_records():
    expected_result = [{"id": "0", "name": "Jeff", "email": "jeff@jeff.com"}, {"id": "1", "name": "Jeremy", "email": "jeremy@jeremy.com"}]

    with httpx.Client() as client:
        response = client.get("http://127.0.0.1:5000/api")
        assert response.status_code == 200
        assert response.json() == expected_result
       
# test adding a new record:
def test_add_record():
    new_record = {"name": "Gordon", "email": "gordon@gordon.com"} 

    with httpx.Client() as client:
        response = client.post("http://127.0.0.1:5000/api", json=new_record)
        assert response.status_code == 200
        assert response.json() == {"id": "2", "name": "Gordon", "email": "gordon@gordon.com"}

def test_if_record_exists():
    expected_result = [{"id": "0", "name": "Jeff", "email": "jeff@jeff.com"}, {"id": "1", "name": "Jeremy", "email": "jeremy@jeremy.com"}, {"id": "2", "name": "Gordon", "email": "gordon@gordon.com"}]
    
    with httpx.Client() as client:
        response2 = client.get("http://127.0.0.1:5000/api")
        assert response2.status_code == 200
        assert response2.json() == expected_result

def test_update_function():
    updated_record = {"id": "2", "name": "test", "email": "test@test.com"} 

    with httpx.Client() as client:
        response = client.patch("http://127.0.0.1:5000/api", json=updated_record)
        assert response.status_code == 200
        assert response.json() == updated_record
        
def test_single_record():
    expected_result = {"id": "2", "name": "test", "email": "test@test.com"} 

    with httpx.Client() as client:
        response = client.get("http://127.0.0.1:5000/api/2")
        assert response.status_code == 200
        assert response.json() == expected_result
    
def test_delete_function():
    with httpx.Client() as client:
        response = client.delete("http://127.0.0.1:5000/api/2")
        assert response.status_code == 200
        # call test all records again
        test_read_all_records()