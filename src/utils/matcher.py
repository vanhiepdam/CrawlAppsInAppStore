class MatcherUtil:
    @staticmethod
    def is_company_name_match_developer_name(company_name: str, developer_name: str) -> bool:
        developer = developer_name.lower()
        company = company_name.lower()
        developer_parts = developer.split(" ")
        stripped_developer_parts = [
            part.strip(",./<>?;':\"[]\{}|`~!@#$%^&*()_+-= ") for part in developer_parts
        ]
        return company in stripped_developer_parts
