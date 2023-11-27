from app.repositories.test_repository import TestRepository
from nordic_realm.decorators.controller import Service

@Service()
class TestService:
    test_repo : TestRepository
    
    def get(self):
        return self.test_repo.get_all()