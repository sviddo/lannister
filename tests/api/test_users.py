import json
import requests
import pytest
from services import (
    url,
    return_users_to_add, 
    return_workers,
)


def test_get_users():
    entire_url = url + "/api/users"
    users = requests.get(url=entire_url)
    
    assert users.status_code == 200 or \
        users.status_code == 404 and users.json() == ["No users!"]
        

class TestAddSingleUser:
    specific_url = url + "/api/add_user"
    
    @pytest.mark.parametrize("test",
                             [{
                                 "service_id": "",
                                 "roles": ["cw"]
                             },
                              {
                                 "service_id": "sjvjsvjksvksdjkvnjdkvndjjsnvj",
                                 "roles": ["cw"]
                             },
                              {
                                 "roles": ["cw"]
                             },
                              {
                                 "service_id": "abc"
                             },
                              {
                                 "service_id": "abc",
                                 "roles": ""
                             },
                              {
                                 "service_id": "abc",
                                 "roles": []
                             },
                              {
                                 "service_id": "abc",
                                 "roles": [""]
                             },
                              {
                                 "service_id": "abc",
                                 "roles": ["b"]
                             },])
    def test_invalid_data(self, test):
        invalid_user = requests.post(url=self.specific_url, json=test)
        
        assert invalid_user.status_code == 400
        
    
    # @pytest.mark.order(before="test_requests.py::TestCreateRequests::test_invalid_data")
    @pytest.mark.dependency(name="TestAddSingleUser::test_valid_data")
    @pytest.mark.parametrize("test",
                             return_users_to_add())
    def test_valid_data(self, test):
        user_to_add = requests.post(url=self.specific_url, json=test)
        
        assert user_to_add.status_code == 200 or \
            user_to_add.status_code == 400 and {"service_id": ["This field must be unique."]} == user_to_add.json()
            
            
    @pytest.mark.dependency(depends=["TestAddSingleUser::test_valid_data"])
    @pytest.mark.parametrize("test",
                             return_users_to_add())
    def test_same_valid_data(self, test):
        user_to_add = requests.post(url=self.specific_url, json=test)
        
        assert user_to_add.status_code == 400 and {"service_id": ["This field must be unique."]} == user_to_add.json()
        
        
    
class TestGetSingleUser:
    
    @pytest.mark.parametrize("test",
                             ["abjdsbcjdcjdcjdjjdkj",
                              "1234567891234",
                              "add-user-4"])
    def test_invalid_data(self, test):
        entire_url = url + f"/api/user/{test}"
        single_user = requests.get(url=entire_url)
        
        assert single_user.status_code == 404
        
        
    @pytest.mark.dependency(depends=["TestAddSingleUser::test_valid_data"])
    @pytest.mark.parametrize("test", 
                             return_users_to_add())
    def test_valid_data(self, test):
        entire_url = url + f"/api/user/{test['service_id']}"
        single_user = requests.get(url=entire_url)
        
        assert single_user.status_code == 200
        
        
        
class TestDeleteSingleUser:
    
    @pytest.mark.parametrize("test",
                             ["abjdsbcjdcjdcjdjjdkj",
                              "1234567891234",
                              "add-user-4"])
    def test_invalid_data(self, test):
        entire_url = url + f"/api/user/{test}"
        single_user = requests.delete(url=entire_url)
        
        assert single_user.status_code == 400
        
        
    @pytest.mark.dependency(depends=["TestAddSingleUser::test_valid_data"])
    @pytest.mark.parametrize("test", 
                             return_users_to_add())
    def test_valid_data(self, test):
        entire_url = url + f"/api/user/{test['service_id']}"
        single_user = requests.delete(url=entire_url)
        
        assert single_user.status_code == 200
        
        
        
class TestHandleReviewerRole:
    
    @pytest.mark.parametrize("test",
                             ["abjdsbcjdcjdcjdjjdkj",
                              "1234567891234",
                              "add-user-4"])
    def test_add_invalid_data(self, test):
        entire_url = url + f"/api/reviewer_role/{test}"
        single_user = requests.patch(url=entire_url)
        
        assert single_user.status_code == 400
        
        
    @pytest.mark.dependency(name="TestHandleReviewerRole::test_add_valid_data", depends=["TestAddSingleUser::test_valid_data"])
    @pytest.mark.parametrize("test", 
                             return_workers())
    def test_add_valid_data(self, test):
        requests.post(url=url + "/api/add_user", json=test)  # add worker in database to make him reviewer
        entire_url = url + f"/api/reviewer_role/{test['service_id']}"
        single_user = requests.patch(url=entire_url)
        
        assert single_user.status_code == 200 or \
            single_user.status_code == 400 and single_user.json() == ["User is already reviewer!"]
        
        
    @pytest.mark.dependency(depends=["TestHandleReviewerRole::test_add_valid_data"])
    @pytest.mark.parametrize("test", 
                             return_workers())
    def test_add_same_valid_data(self, test):
        entire_url = url + f"/api/reviewer_role/{test['service_id']}"
        single_user = requests.patch(url=entire_url)
        
        assert single_user.status_code == 400 and single_user.json() == ["User is already reviewer!"]
        
        
    @pytest.mark.parametrize("test",
                             ["abjdsbcjdcjdcjdjjdkj",
                              "1234567891234",
                              "add-user-4"])
    def test_delete_invalid_data(self, test):
        entire_url = url + f"/api/reviewer_role/{test}"
        single_user = requests.delete(url=entire_url)
        
        assert single_user.status_code == 400
        
        
    @pytest.mark.dependency(name="TestHandleReviewerRole::test_delete_valid_data", 
                            depends=["TestHandleReviewerRole::test_add_valid_data"])
    @pytest.mark.parametrize("test", 
                             return_workers())
    def test_delete_valid_data(self, test):
        entire_url = url + f"/api/reviewer_role/{test['service_id']}"
        single_user = requests.delete(url=entire_url)
        
        assert single_user.status_code == 200
        
        
    @pytest.mark.dependency(depends=["TestHandleReviewerRole::test_delete_valid_data"])
    @pytest.mark.parametrize("test", 
                             return_workers())
    def test_delete_same_valid_data(self, test):
        entire_url = url + f"/api/reviewer_role/{test['service_id']}"
        single_user = requests.delete(url=entire_url)
        
        assert single_user.status_code == 400 and single_user.json() == ["User is not reviewer!"]
