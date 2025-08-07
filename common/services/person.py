from common.repositories.factory import RepositoryFactory, RepoType
from common.models.person import Person


class PersonService:

    def __init__(self, config):
        self.config = config

        from common.services import EmailService
        self.email_service = EmailService(config)

        self.repository_factory = RepositoryFactory(config)
        self.person_repo = self.repository_factory.get_repository(RepoType.PERSON)

    def save_person(self, person: Person):
        person = self.person_repo.save(person)
        return person

    def get_person_by_email_address(self, email_address: str):
        email_obj = self.email_service.get_email_by_email_address(email_address)
        if not email_obj:
            return
        
        person = self.person_repo.get_one({"entity_id": email_obj.person_id})
        return person

    def get_person_by_id(self, entity_id: str):
        person = self.person_repo.get_one({"entity_id": entity_id})
        return person

    def update_person(self, entity_id: str, first_name=None, last_name=None):
        """Update person's first_name and/or last_name"""
        person = self.get_person_by_id(entity_id)
        if not person:
            return None
        
        if first_name is not None:
            person.first_name = first_name
        if last_name is not None:
            person.last_name = last_name
        
        updated_person = self.person_repo.save(person)
        return updated_person
    