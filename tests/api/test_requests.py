import pytest
import requests
import datetime
from services import (
    url, 
    return_users_to_add, 
    create_invalid_requests,
    create_valid_requests,
)


def test_get_requests():
    entire_url = url + "/api/requests"
    all_requests = requests.get(url=entire_url)
    
    assert all_requests.status_code == 200 or \
        all_requests.status_code == 400 and all_requests.json() == ["No requests created!"]
        
        
class TestRequests:
    pytest.my_list = []
    
    @pytest.mark.parametrize("test",
                             create_valid_requests())
    def test_valid_data_add(self, test):
        valid_request = requests.post(url + "/api/create_request", json=test)
        assert valid_request.status_code in (200, 201)
        pytest.my_list.append(valid_request.json())
    
    
    @pytest.mark.parametrize("test",
                             create_invalid_requests())   
    def test_invalid_data_add(self, test):
        invalid_request = requests.post(url + "/api/create_request", json=test)
        
        assert invalid_request.status_code == 400
        
    
    @pytest.mark.parametrize("test", ["a", "b", "c"])
    def test_invalid_data_ids(self, test):
        invalid_request = requests.patch(url + f"/api/request/{test}", json={"bonus_type": "jbcj"})

        assert invalid_request.status_code == 400
        
        
    def test_invalid_data_update(self):
        created_requests_copy =  pytest.my_list.copy()
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[0]['id']}", json={"creation_time": "2022-07-28T07:03:22.941528Z"})
        assert invalid_request.status_code == 400
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[1]['id']}", json={"creator": "abc"})
        assert invalid_request.status_code == 400
        
        tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[1]['id']}", json={"paymant_day": tomorrow})
        assert invalid_request.status_code == 400
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[1]['id']}", json={"paymant_day": tomorrow, "status": "r"})
        assert invalid_request.status_code == 400
        
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[1]['id']}", json={"paymant_day": tomorrow, "status": "p"})
        assert invalid_request.status_code == 400
                
        invalid_request = requests.patch(url + f"/api/request/{created_requests_copy[1]['id']}")
        assert invalid_request.status_code == 400
        
        
        
    def test_valid_data_update(self):
        valid_request = requests.patch(url + f"/api/request/{pytest.my_list[0]['id']}", json={"status": "r"})
        assert valid_request.status_code == 201
        
        valid_request = requests.patch(url + f"/api/request/{pytest.my_list[1]['id']}", json={"status": "p"})
        assert valid_request.status_code == 201
        
        tomorrow = str(datetime.date.today() + datetime.timedelta(days=1))
        
        valid_request = requests.patch(url + f"/api/request/{pytest.my_list[2]['id']}", json={"paymant_day": tomorrow,
                                                                                                  "status": "a"})
        assert valid_request.status_code == 201
        
        valid_request = requests.patch(url + f"/api/request/{pytest.my_list[3]['id']}", json={"bonus_type": "random_data"})
        assert valid_request.status_code == 201
        
        valid_request = requests.patch(url + f"/api/request/{pytest.my_list[3]['id']}", json={"description": "random_data"})
        assert valid_request.status_code == 201
        
        
    @pytest.mark.parametrize("test", ["random_data_1",
                                      "jashscjbcjnsckasnc"])
    def test_invalid_data_user(self, test):
        invalid_requests = requests.get(url + f"/api/requests/{test}")
        assert invalid_requests.status_code == 400
        
        
    @pytest.mark.parametrize("test", return_users_to_add())
    def test_valid_data_user(self, test):
        valid_requests = requests.get(url + f"/api/requests/{test['service_id']}")
        assert valid_requests.status_code == 200
        
        
    @pytest.mark.parametrize("test", ["add-user-1",
                                      "random_data_1"])
    def test_invalid_data_reviewer(self, test):
        invalid_requests = requests.get(url + f"/api/reviewer_requests/{test}")
        assert invalid_requests.status_code == 400
        
        
    @pytest.mark.parametrize("test", [user for user in return_users_to_add() if "r" in user["roles"]])
    def test_valid_data_reviewer(self, test):
        valid_requests = requests.get(url + f"/api/reviewer_requests/{test['service_id']}")
        assert valid_requests.status_code == 200 or \
            valid_requests.status_code == 400 and valid_requests.json() == ['Reviewer has no assigned requests!']
        
        
    @pytest.mark.parametrize("test", 
                             ["abc",
                              "def",
                              "jhcjhdh"])
    def test_invalid_data_ids(self, test):
        invalid_request = requests.get(url + f"/api/requests/{test}")

        assert invalid_request.status_code == 400
        
        
    def test_requests_history(self):
        response = requests.get(url + "/api/requests_history")
        
        assert response.status_code == 200
        
        
    @pytest.mark.parametrize("test",
                             ["abc",
                              "def",
                              999999999999])
    def test_invalid_data(self, test):
        response = requests.delete(url + f"/api/request/{test}")
        assert response.status_code == 400
        
        
    def test_valid_data_delete(self):
        for request in pytest.my_list:
            response = requests.delete(url + f"/api/request/{request['id']}")
            assert response.status_code == 200
    